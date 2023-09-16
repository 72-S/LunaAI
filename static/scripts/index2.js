document.addEventListener("DOMContentLoaded", function (event) {
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    const recognition = new SpeechRecognition();
    const wakeUpWord = "jarvis" || "hey jarvis"; // Set your wake up word
    const apiKey = "aed2ca66-42a2-49b4-8131-7f506e6aeb47"; // Set your API key here
    const typewriterContainer = document.getElementById("output");
    const circleOuter = document.getElementById("circleOuter");
    const circleOuter1 = document.getElementById("circleOuter1");
    const visible = document.getElementById("responce");
    const animationDuration = 1000; // Duration of the typing animation in milliseconds
    const maxLength = 50;
    let audio1 = new Audio("../../static/audio/audio1.mp3");	
    let audio2 = new Audio("../../static/audio/audio2.mp3");
    let audio3 = new Audio("../../static/audio/audio3.mp3");
    let myvad = null;
    
    // Get a reference to the database service
    var database = firebase.database();

    // Listen for changes to the CAMERA value in Firebase
    var cameraRef = firebase.database().ref('CAMERA');
    cameraRef.on('value', (snapshot) => {
        const cameraValue = snapshot.val();
        if (cameraValue === true) {
            // If the CAMERA value is true, start continuous listening
            window.startProcessing();
            audio2.play().catch(error => console.error('Error playing audio:', error));
        } else {
            // If the CAMERA value is false, stop continuous listening
            setTimeout(() => {
                window.stopProcessing();
            }, 5000); // 5000 milliseconds = 5 seconds
        }
    });

    recognition.addEventListener("start", () => {
    });

    recognition.addEventListener("result", ({ results, resultIndex }) => {
        const [{ transcript }] = results[resultIndex];
        if (transcript.toLowerCase().includes(wakeUpWord)) {
            console.log("Wake up word detected");
            audio3.play().catch(error => console.error('Error playing audio:', error));
            recognition.stop();
            if (myvad) myvad.start();
        } else {
            
        }
    });

    async function main() {
        myvad = await vad.MicVAD.new({
            positiveSpeechThreshold: 0.8,
            negativeSpeechThreshold: 0.8 - 0.15,
            minSpeechFrames: 5,
            preSpeechPadFrames: 1,
            redemptionFrames: 3,
            onSpeechStart: () => {
                console.log("Listening...");
                
            },
            onSpeechEnd: (audio) => {
                myvad.pause();
                console.log("Processing...");
                postDataToAPI(audio);
                circleOuter.style.display = "block";
                circleOuter1.style.display = "block";
                audio1.play().catch(error => console.error('Error playing audio:', error));
                
            },
        });
    }

    main().then(() => {
        recognition.onend = () => recognition.start();
        recognition.start();
    });

    function postDataToAPI(audio) {
        const wavBuffer = vad.utils.encodeWAV(audio);
        const base64 = vad.utils.arrayBufferToBase64(wavBuffer);

        fetch("https://api.carterlabs.ai/chat", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                audio: base64,
                key: apiKey,
                user_id : "Consti",
            }),
        })
            .then((response) => response.json())
            .then((data) => {
                if (data.output && data.output.text) {
                    var outputText = data.output.text;
                    console.log("Output text: " + outputText);
                    console.log(data);

                    // Split the output text into multiple lines if it's too long
                    const maxLength = 50;
                    const lines = splitText(outputText, maxLength);
                    addLinesSequentially(lines, animationDuration);

                    //Forced behaviors
                    if (data.forced_behaviours && data.forced_behaviours.length > 0) {
                        data.forced_behaviours.forEach(function(behaviour) {
                          if (behaviour.name === 'ledOn') {
                            ledControl('on');
                          }
                          else if (behaviour.name === 'ledOff') {
                            ledControl('off');
                          }
                          else if (behaviour.name === 'red') {
                            ledControl('red');
                          }
                          else if (behaviour.name === 'green') {
                            ledControl('green');
                          }
                          else if (behaviour.name === 'blue') {
                            ledControl('blue');
                          }
                          else if (behaviour.name === 'yellow') {
                            ledControl('yellow');
                          }
                          else if (behaviour.name === 'purple') {
                            ledControl('purple');
                          }
                          else if (behaviour.name === 'white') {
                            ledControl('white');
                          }
                          else if (behaviour.name === 'play') {
                            playPause(('play'));
                          }
                          else if (behaviour.name === 'pause') {
                            playPause(('pause'));
                          }
                        });
                      }
                          

                    // Make a separate request to the /speak endpoint with the output text
                    fetch("https://api.carterlabs.ai/speak", {
                        mode: "no-cors",
                        method: "POST",
                        headers: { "Content-Type": "application/json" },
                        body: JSON.stringify({
                            text: outputText,
                            key: apiKey
                        }),
                    })
                    .then((response) => response.json())
                    .then((data) => {
                        // Play the audio from the returned audio URL
                        if (data.output.audio_error === null) {
                            speak(data.output.audio);
                        } else {
                            console.error('No audio data returned from API', data);
                        }
                        
                    })
                    .catch((error) => {
                        console.error(error);
                    });
                } else {
                    console.error('Invalid API response', data);
                }
            })
            .catch((error) => {
                console.error(error);
            });
    }

    async function addLinesSequentially(lines, animationDuration) {
        typewriterContainer.innerHTML = "";
        circleOuter.style.display = "block";
        circleOuter1.style.display = "block";
        
        for (const line of lines) {
            typewriterContainer.appendChild(createTypewriterLine(line));
            await sleep(animationDuration);
        }
        circleOuter.style.display = "none";
        circleOuter1.style.display = "none";
    }

    function createTypewriterLine(content) {
        const line = document.createElement("div");
        line.textContent = content;
        return line;
    }

    function splitText(text, maxLength) {
        const words = text.split(" ");
        const lines = [];
        let currentLine = "";

        for (const word of words) {
            if (currentLine.length + word.length <= maxLength) {
                currentLine += word + " ";
            } else {
                lines.push(currentLine.trim());
                currentLine = word + " ";
            }
        }

        if (currentLine.trim()) {
            lines.push(currentLine.trim());
        }

        return lines;
    }

    function speak(url) {
        const audio = new Audio(url);
        audio.play();
    
        // Set the visibility of the element to 'block' when the audio starts playing
        visible.style.display = "block";
    
        audio.addEventListener('ended', function() {
    
            // Set the visibility of the element to 'none' after a delay when the audio ends
            setTimeout(function() {
                visible.style.display = "none";
            }, 2000); // 2000 milliseconds = 2 seconds

            // Check the CAMERA value and restart continuous listening if it's still true
            cameraRef.once('value', (snapshot) => {
                const cameraValue = snapshot.val();
                if (cameraValue === true) {
                    window.startProcessing();
                }
            });
        });
    }
    

    function sleep(ms) {
        return new Promise((resolve) => setTimeout(resolve, ms));
    }

    // Add a global function to start processing
    window.startProcessing = function() {
        recognition.stop();
        if (myvad) myvad.start();
    }

    // Add a global function to stop processing
    window.stopProcessing = function() {
        recognition.stop();
        if (myvad) myvad.pause();
    }
});
