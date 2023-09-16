document.addEventListener('DOMContentLoaded', (event) => {
    const video = document.getElementById('video');
    let noFaceTimeout; // Variable zum Speichern des Timeout-Handlers

    if (video) {
        // Laden der Modelle
        Promise.all([
            faceapi.nets.tinyFaceDetector.loadFromUri('/static/models'),
            faceapi.nets.faceLandmark68Net.loadFromUri('/static/models'),
            faceapi.nets.faceRecognitionNet.loadFromUri('/static/models'),
            faceapi.nets.faceExpressionNet.loadFromUri('/static/models')
        ]).then(startVideo);

        function startVideo() {
            navigator.getUserMedia(
                { video: { width: 320, height: 340 } }, // Reduzieren Sie die Videoauflösung
                stream => {
                    if (stream) {
                        video.srcObject = stream;
                    } else {
                        console.error('Stream is null or undefined');
                    }
                },
                err => console.error(err)
            )
        }

        video.addEventListener('play', () => {
            const canvas = faceapi.createCanvasFromMedia(video);
            document.body.append(canvas);
            const displaySize = { width: video.offsetWidth, height: video.offsetHeight };
            faceapi.matchDimensions(canvas, displaySize);
            setInterval(async () => {
                const detections = await faceapi.detectAllFaces(video, new faceapi.TinyFaceDetectorOptions()).withFaceLandmarks().withFaceExpressions();
                const resizedDetections = faceapi.resizeResults(detections, displaySize);
                canvas.getContext('2d').clearRect(0, 0, canvas.width, canvas.height);
                faceapi.draw.drawDetections(canvas, resizedDetections);
                faceapi.draw.drawFaceLandmarks(canvas, resizedDetections);
                faceapi.draw.drawFaceExpressions(canvas, resizedDetections);

                // Check if a face is detected and it's close to the camera
                if (resizedDetections && resizedDetections.length > 0 && resizedDetections[0].detection.box.width > video.offsetWidth / 5) {
                    firebase.database().ref("CAMERA").set(true);

                    // Wenn ein Gesicht erkannt wird, Timeout abbrechen
                    clearTimeout(noFaceTimeout);
                } else {
                    // Wenn kein Gesicht erkannt wird, Timeout setzen
                    noFaceTimeout = setTimeout(() => {
                        firebase.database().ref("CAMERA").set(false);
                    }, 3000); // 3 Sekunden Verzögerung
                }
            }, 1000); // Reduzieren Sie die Bildrate auf 1 Mal pro Sekunde
        });
    } else {
        console.error('Video element is null or undefined');
    }
});
