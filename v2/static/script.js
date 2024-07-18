document.addEventListener("DOMContentLoaded", function () {
    console.log("Document loaded");

    const video = document.getElementById('video');
    const canvas = document.getElementById('canvas');
    const context = canvas.getContext('2d');
    let localMediaStream = null; // Holds the stream

    const audio1 = new Audio("../../static/audio1.mp3");
    const audio3 = new Audio("../../static/audio3.mp3");
    let typewriterContainer = document.getElementById("output");
    let circleOuter = document.getElementById("circleOuter");
    let circleOuter1 = document.getElementById("circleOuter1");
    let visible = document.getElementById("responce");

    audio1.onerror = function(err) {
        console.error("Error loading audio1:", err);
    };

    audio3.onerror = function(err) {
        console.error("Error loading audio3:", err);
    };

    // Function to start the video
    function startVideo() {
        console.log("Starting video");
        navigator.mediaDevices.getUserMedia({video: true})
            .then(stream => {
                console.log("Video stream obtained");
                video.srcObject = stream;
                localMediaStream = stream; // Save the stream for later access
                video.play(); // Play the video
            })
            .catch(err => {
                console.error("Error obtaining video stream:", err);
            });
    }

    async function apiRequest(prompt, image) {
        document.getElementById('loader').style.display = 'block';
        const response = await fetch('http://127.0.0.1:5000/api/post', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({prompt: prompt, image_base64: image}),
        });
        document.getElementById('loader').style.display = 'none';
        if (response.ok) {
            const data = await response.json();
            console.log(data);
            document.getElementById('responseText').innerText = data.response;
            playAudio(data.speech);
        } else {
            console.error('Fehler bei der Anfrage');
        }
    }

    window.generateResponse = function () {
        const prompt = document.getElementById('promptInput').value;
        let image = '';

        // Check if the stream is running and the checkbox is checked before capturing the frame
        if (document.getElementById('includeVideoCheckbox').checked && localMediaStream) {
            context.drawImage(video, 0, 0, canvas.width, canvas.height);
            image = canvas.toDataURL('image/png');
        }

        // Send API request
        apiRequest(prompt, image);
    };

    function playAudio(base64String) {
        const audioPlayer = document.getElementById('audioPlayer');
        audioPlayer.src = `data:audio/mp3;base64,${base64String}`;
        audioPlayer.play().catch(err => {
            console.error("Error playing audio:", err);
        });
    }

    // Check for Web Speech API support
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    if (!SpeechRecognition) {
        alert("Web Speech API is not supported in this browser. Please use Google Chrome or a compatible browser.");
    } else {
        console.log("Web Speech API supported");
        let recognition = new webkitSpeechRecognition();
        recognition.continuous = true;
        recognition.interimResults = true;
        recognition.lang = "de-DE"; // Deutsch

        let isActivated = false;
        let finalTranscript = "";

        recognition.onresult = function (event) {
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
                audio3.play();
                isActivated = true;
                finalTranscript = "";
                return;
            }

            if (isActivated && finalTranscript) {
                // Remove the activation word from the final transcript
                finalTranscript = finalTranscript.replace(/hey Luna|Luna/gi, "").trim();

                if (finalTranscript) {
                    // Only send if there's text after the activation word
                    console.log("Input:", finalTranscript);
                    audio1.play();
                    circleOuter.style.display = "block";
                    circleOuter1.style.display = "block";

                    apiRequest(finalTranscript, '');

                    isActivated = false;
                    finalTranscript = ""; // Reset the transcript after sending
                }
            }
        };

        recognition.onerror = function (event) {
            console.error("Error:", event.error);
        };

        recognition.onend = function () {
            recognition.start(); // Restart recognition
        };

        recognition.start();
    }

    // Start the video when the page loads if checkbox is checked
    document.getElementById('includeVideoCheckbox').addEventListener('change', function () {
        if (this.checked) {
            video.style.display = 'block';
            startVideo();
        } else {
            video.style.display = 'none';
            if (localMediaStream) {
                const tracks = localMediaStream.getTracks();
                tracks.forEach(track => track.stop());
                localMediaStream = null;
            }
        }
    });
});