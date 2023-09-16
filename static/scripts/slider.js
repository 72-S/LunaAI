window.onload = () => {
  const sliderContainer = document.querySelector(".slidercontainer");
  const slider = document.querySelector("#slider");

  let isDragging = false;
  let startY;
  let debounceTimeout;

  const socket = io.connect('https://10.0.1.12:6969');

  socket.on('message', function(volume) {
    let bottom =
      volume * (sliderContainer.clientHeight - slider.clientHeight);
    slider.style.transition = "bottom 0.0s ease-out";
    slider.style.bottom = bottom + "px";

    // Update the slider progress
    updateSliderProgress(volume);
  });

  function startDrag(event) {
    isDragging = true;
    startY = event.clientY || event.touches[0].clientY;
  }

  function stopDrag() {
    isDragging = false;
  }

  function performDrag(event) {
    if (isDragging) {
      event.preventDefault();
      let clientY = event.clientY || event.touches[0].clientY;
      let deltaY = startY - clientY;
      let bottom = parseInt(slider.style.bottom) || 0;
      bottom += deltaY;

      if (bottom < 0) bottom = 0;
      if (bottom > sliderContainer.clientHeight - slider.clientHeight) {
        bottom = sliderContainer.clientHeight - slider.clientHeight;
      }

      slider.style.bottom = bottom + "px";
      startY = clientY;

      let volume =
        bottom / (sliderContainer.clientHeight - slider.clientHeight);
      updateVolumeOnServer(volume);

      // Update the slider progress
      updateSliderProgress(volume);
    }
  }

  // Update the slider progress without animation
  function updateSliderProgress(volume) {
    let trackHeight = sliderContainer.offsetHeight;
    let progressHeight = volume * trackHeight;
    let perc = (progressHeight / trackHeight) * 100;

    sliderContainer.style.backgroundImage = `linear-gradient(to top, #fff ${perc}%, #002439 0%)`;
    perc = perc.toFixed();
    var output = document.getElementById('percentage');
    perc = perc < 10 ? "0" + perc : perc;
  }

  slider.addEventListener("mousedown", startDrag);
  slider.addEventListener("touchstart", startDrag, {passive: false});

  document.addEventListener("mouseup", stopDrag);
  document.addEventListener("touchend", stopDrag);

  document.addEventListener("mousemove", performDrag);
  document.addEventListener("touchmove", performDrag, {passive: false});

  async function updateVolumeOnServer(volume) {
    // Clear the previous timeout if it exists
    if (debounceTimeout) {
      clearTimeout(debounceTimeout);
    }

    // Set a new timeout
    debounceTimeout = setTimeout(async function() {
      await fetch("https://10.0.1.12:6969/send_volume", {
        method: "POST",
        headers: {
          "Content-Type": "application/x-www-form-urlencoded",
        },
        body: `volume=${volume}`,
      });
    }, 200);  // Wait 200 milliseconds before sending the request
  }
};
