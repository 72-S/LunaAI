import * as THREE from 'three';
import { GUI } from 'dat.gui';
import { EffectComposer } from 'three/examples/jsm/postprocessing/EffectComposer';
import { RenderPass } from 'three/examples/jsm/postprocessing/RenderPass';
import { UnrealBloomPass } from 'three/examples/jsm/postprocessing/UnrealBloomPass';
import { OutputPass } from 'three/examples/jsm/postprocessing/OutputPass';

const renderer = new THREE.WebGLRenderer({ antialias: true });
renderer.setSize(window.innerWidth, window.innerHeight);
document.body.appendChild(renderer.domElement);

const scene = new THREE.Scene();
const camera = new THREE.PerspectiveCamera(45, window.innerWidth / window.innerHeight, 0.1, 1000);

const values = {
    radius: 4,
    time_multiplier: 0.2,
    target_time_multiplier: 0.2, // Add target time multiplier
}

const params = {
    red: 0.9,
    green: 0.55,
    blue: 0.99,
    threshold: 0.4,
    strength: 0.6,
    bloom_radius: 0.3,
    detail: 15,
}

let isActivated = false;
let finalTranscript = "";
let recognition = new webkitSpeechRecognition();


renderer.outputColorSpace = THREE.SRGBColorSpace;

const renderScene = new RenderPass(scene, camera);

const bloomPass = new UnrealBloomPass(new THREE.Vector2(window.innerWidth, window.innerHeight));
bloomPass.threshold = params.threshold;
bloomPass.strength = params.strength;
bloomPass.radius = params.bloom_radius;

const bloomComposer = new EffectComposer(renderer);
bloomComposer.addPass(renderScene);
bloomComposer.addPass(bloomPass);

const outputPass = new OutputPass();
bloomComposer.addPass(outputPass);

camera.position.set(0, -2, 14);
camera.lookAt(0, 0, 0);

const uniforms = {
    u_time: { type: 'f', value: 0.0 },
    u_frequency: { type: 'f', value: 0.0 },
    u_red: { type: 'f', value: 1.0 },
    u_green: { type: 'f', value: 1.0 },
    u_blue: { type: 'f', value: 1.0 }
}

const mat = new THREE.ShaderMaterial({
    uniforms,
    vertexShader: document.getElementById('vertexshader').textContent,
    fragmentShader: document.getElementById('fragmentshader').textContent,
    wireframe: true
});

const geo = new THREE.IcosahedronGeometry(values.radius, params.detail);

const mesh = new THREE.Mesh(geo, mat);
scene.add(mesh);

const points = new THREE.Points(geo, mat);
scene.add(points);

const listener = new THREE.AudioListener();
camera.add(listener);

const sound = new THREE.Audio(listener);
const analyser = new THREE.AudioAnalyser(sound, 32);

const gui = new GUI();

const colorsFolder = gui.addFolder('Colors');
colorsFolder.add(params, 'red', 0, 1).onChange(function (value) {
    uniforms.u_red.value = Number(value);
});
colorsFolder.add(params, 'green', 0, 1).onChange(function (value) {
    uniforms.u_green.value = Number(value);
});
colorsFolder.add(params, 'blue', 0, 1).onChange(function (value) {
    uniforms.u_blue.value = Number(value);
});

const bloomFolder = gui.addFolder('Bloom');
bloomFolder.add(params, 'threshold', 0, 1).onChange(function (value) {
    bloomPass.threshold = Number(value);
});
bloomFolder.add(params, 'strength', 0, 3).onChange(function (value) {
    bloomPass.strength = Number(value);
});
bloomFolder.add(params, 'bloom_radius', 0, 1).onChange(function (value) {
    bloomPass.radius = Number(value);
});

gui.add(params, 'detail', 1, 30).step(1).onChange(function (value) {
    scene.remove(mesh);
    scene.remove(points);
    const newGeo = new THREE.IcosahedronGeometry(4, value);
    mesh.geometry = newGeo;
    points.geometry = newGeo;
    scene.add(mesh);
    scene.add(points);
});

let mouseX = 0;
let mouseY = 0;
document.addEventListener('mousemove', function (e) {
    let windowHalfX = window.innerWidth / 2;
    let windowHalfY = window.innerHeight / 2;
    mouseX = (e.clientX - windowHalfX) / 100;
    mouseY = (e.clientY - windowHalfY) / 100;
});

const clock = new THREE.Clock();

async function sendToApi(prompt) {
    const payload = {
        prompt: prompt
    };

    try {
        const response = await fetch('http://127.0.0.1:5000/api/post', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(payload)
        });

        if (!response.ok) {
            throw new Error('Network response was not ok');
        }

        return await response.json();
    } catch (error) {
        console.error('Error sending request to API:', error);
        return { response: 'Error connecting to API.', speech: '' };
    }
}

async function playAudioFromApi(prompt) {
    const result = await sendToApi(prompt);
    const audioBase64 = result.speech; // Adjust according to your API response structure

    if (audioBase64) {
        const audioBuffer = await decodeAudioBase64(audioBase64);
        sound.setBuffer(audioBuffer);
        sound.stop();
        sound.play();

        sound.onEnded = function() {
            console.log("Audio has ended");
            values.target_time_multiplier = 0.2; // Change the target value

            let resetTimeout = setTimeout(() => {
                values.time_multiplier = 0.2;
                isActivated = false; // Reset activation state
            }, 6000); // Continue listening for 3 seconds

            // Clear the timeout if new speech is detected during the 3-second window
            recognition.onresult = function (event) {
                clearTimeout(resetTimeout);
                handleSpeechResult(event);
            };
        };
    }
}

async function decodeAudioBase64(base64String) {
    const audioContext = new (window.AudioContext || window.webkitAudioContext)();
    const audioData = atob(base64String);
    const arrayBuffer = new ArrayBuffer(audioData.length);
    const view = new Uint8Array(arrayBuffer);

    for (let i = 0; i < audioData.length; i++) {
        view[i] = audioData.charCodeAt(i);
    }

    return new Promise((resolve, reject) => {
        audioContext.decodeAudioData(arrayBuffer, resolve, reject);
    });
}

document.getElementById('send-prompt').addEventListener('click', function () {
    const prompt = document.getElementById('prompt-input').value;
    playAudioFromApi(prompt);
});

let lastFrequency = 0;
const alpha = 0.3;

function lowPassFilter(currentValue, previousValue, alpha) {
    return alpha * currentValue + (1 - alpha) * previousValue;
}

function lerp(a, b, t) {
    return a + (b - a) * t;
}

function animate() {
    // Camera movement
    camera.position.x += (mouseX - camera.position.x) * 0.05;
    camera.position.y += (-mouseY - camera.position.y) * 0.5;
    camera.lookAt(scene.position);

    // Get the average frequency from the audio analyser
    const averageFrequency = analyser.getAverageFrequency();

    const smoothedFrequency = lowPassFilter(averageFrequency / 256, lastFrequency, alpha);
    lastFrequency = smoothedFrequency;

    // Smoothly transition the time_multiplier towards the target_time_multiplier
    values.time_multiplier = lerp(values.time_multiplier, values.target_time_multiplier, 0.05);

    // Update shader uniforms
    uniforms.u_time.value = clock.getElapsedTime() * values.time_multiplier;
    uniforms.u_frequency.value = smoothedFrequency; // Normalize frequency data
    uniforms.u_blue.value = params.blue + (averageFrequency / 256) / 0.6;
    uniforms.u_red.value = params.red + (averageFrequency / 256) * 0.1;
    uniforms.u_green.value = params.green + (averageFrequency / 256) * 0.1;

    // Render the scene with bloom effect
    bloomComposer.render();

    requestAnimationFrame(animate);
}

animate();

window.addEventListener('resize', function () {
    camera.aspect = window.innerWidth / window.innerHeight;
    camera.updateProjectionMatrix();
    renderer.setSize(window.innerWidth, window.innerHeight);
    bloomComposer.setSize(window.innerWidth, window.innerHeight);
});

function handleSpeechResult(event) {

    let interimTranscript = "";
    for (let i = event.resultIndex; i < event.results.length; ++i) {
        if (event.results[i].isFinal) {
            finalTranscript += event.results[i][0].transcript;
        } else {
            interimTranscript += event.results[i][0].transcript;
        }
    }

    if (
        (interimTranscript.includes("hey Luna") ||
            interimTranscript.includes("Luna")) &&
        !isActivated
    ) {
        console.log("Speak Now!");
        isActivated = true;
        values.target_time_multiplier = 1.2;
        finalTranscript = "";
    }

    if (isActivated && finalTranscript) {
        // Remove the activation word from the final transcript
        finalTranscript = finalTranscript.replace(/hey Luna|Luna/gi, "").trim();

        if (finalTranscript) {
            // Only send if there's text after the activation word
            console.log("Input:", finalTranscript);

            // Send the finalTranscript to your API
            playAudioFromApi(finalTranscript);

            finalTranscript = "";
        }
    }
}

document.addEventListener('DOMContentLoaded', function () {
    recognition.continuous = true;
    recognition.interimResults = true;
    recognition.lang = "de-DE"; // Deutsch

    let isActivated = false;
    let finalTranscript = "";

    recognition.onresult = function (event) {
        handleSpeechResult(event);
    };

    recognition.onerror = function (event) {
        console.error("Error:", event.error);
    };

    recognition.onend = function () {
        recognition.start(); // Restart recognition
    };

    recognition.start();
});
