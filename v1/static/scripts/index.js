document.addEventListener("DOMContentLoaded", function () {
  let recognition = new webkitSpeechRecognition();
  recognition.continuous = true;
  recognition.interimResults = true;
  recognition.lang = "de-DE"; // Deutsch

  let isActivated = false;
  let finalTranscript = "";
  const audio1 = new Audio("../../static/audio/audio1.mp3");
  const audio3 = new Audio("../../static/audio/audio3.mp3");
  let typewriterContainer = document.getElementById("output");
  let circleOuter = document.getElementById("circleOuter");
  let circleOuter1 = document.getElementById("circleOuter1");
  let visible = document.getElementById("responce");
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
      finalTranscript = finalTranscript.replace(/hey Jarvis|Jarvis/gi, "").trim();

      if (finalTranscript) {
        // Only send if there's text after the activation word
        console.log("Input:", finalTranscript);
        audio1.play();
        circleOuter.style.display = "block";
        circleOuter1.style.display = "block";

        // Send the finalTranscript to your API
        fetch("https://127.0.0.1:443/chat", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({ text: finalTranscript }),
        })
          .then((response) => {
            if (!response.ok) {
              throw new Error("Error from server");
            }
            return response.json();
          })
          .then((data) => {
            let output = data.text;
            if (output.startsWith("?")) {
              output = output.replace("?", "");
          }
            
            console.log("Output:", output);
            visible.style.display = "block";
            function addButton() {
              const button = document.getElementById("showResponce");
              button.classList.add("active");
            }
            addButton()
            typewriterContainer.innerText = output;
            let audio = new Audio("data:audio/mp3;base64," + data.audio);
            audio.addEventListener('ended', function(){
              function resetButton() {
                const button = document.getElementById("showResponce");
                button.classList.remove("active");
              }
                visible.style.display = "none";
                resetButton();
            })
            audio.play();
            circleOuter.style.display = "none";
            circleOuter1.style.display = "none";
          })
          .catch((error) => {
            console.error(
              "Error from server: ",
              error.message
            );
          });

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
});
