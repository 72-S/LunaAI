document.getElementById("showResponce").addEventListener("click", function() {
    // Get the output element
    var outputElement = document.getElementById("responce");

    // Toggle the display of the output element
    if (outputElement.style.display === "none" || outputElement.style.display === "") {
        outputElement.style.display = "block";
        this.classList.add("active"); // Button weiß machen
    } else {
        outputElement.style.display = "none";
        this.classList.remove("active"); // Button zurücksetzen

        // Setze das output-Element auf seine ursprüngliche Position zurück
        document.getElementById('output').style.transform = 'translate(0, 0)';
        offsetX = 0;
        offsetY = 0;
    }
});

let button = document.getElementById('showResponce');

button.addEventListener('mousedown', function() {
    this.style.transform = 'scale(0.95)';
});

button.addEventListener('mouseup', function() {
    this.style.transform = 'scale(1)';
});

button.addEventListener('touchstart', function() {
    this.classList.add('pressed');
});

button.addEventListener('touchend', function() {
    this.classList.remove('pressed');
});

button.addEventListener('animationend', function() {
    this.classList.remove('pressed');
});

let isDragging = false;
let startX = 0;
let startY = 0;
let offsetX = 0;
let offsetY = 0;

// Touch Events
document.getElementById('output').addEventListener('touchstart', function(e) {
    if (document.getElementById('showResponce').classList.contains('active')) {
        isDragging = true;
        let touch = e.touches[0];
        startX = touch.clientX - offsetX;
        startY = touch.clientY - offsetY;
    }
});

document.getElementById('output').addEventListener('touchmove', function(e) {
    if (isDragging) {
        e.preventDefault();
        let touch = e.touches[0];
        offsetX = touch.clientX - startX;
        offsetY = touch.clientY - startY;
        this.style.transform = `translate(${offsetX}px, ${offsetY}px)`;
    }
});

document.getElementById('output').addEventListener('touchend', function() {
    isDragging = false;
});

// Mouse Events
document.getElementById('output').addEventListener('mousedown', function(e) {
    if (document.getElementById('showResponce').classList.contains('active')) {
        isDragging = true;
        startX = e.clientX - offsetX;
        startY = e.clientY - offsetY;
    }
});

document.getElementById('output').addEventListener('mousemove', function(e) {
    if (isDragging) {
        e.preventDefault();
        offsetX = e.clientX - startX;
        offsetY = e.clientY - startY;
        this.style.transform = `translate(${offsetX}px, ${offsetY}px)`;
    }
});

document.getElementById('output').addEventListener('mouseup', function() {
    isDragging = false;
});

// Dieser Event-Listener sorgt dafür, dass das Dragging stoppt, auch wenn die Maus das Element verlässt
document.addEventListener('mouseup', function() {
    isDragging = false;
});
