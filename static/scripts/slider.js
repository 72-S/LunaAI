window.onload = () => {
  const sliderContainer = document.querySelector(".slidercontainer");
  const slider = document.querySelector(".sliderthumb");

  let isDragging = false;
  let startY;

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

      let value =
          bottom / (sliderContainer.clientHeight - slider.clientHeight);

      // Update the slider progress
      updateSliderProgress(value);
    }
  }

  function updateSliderProgress(value) {
    let trackHeight = sliderContainer.offsetHeight;
    let progressHeight = value * trackHeight;
    let perc = (progressHeight / trackHeight) * 100;
    let temp = (progressHeight / trackHeight);
    temp = temp.toFixed(2);
    const ref = db.ref("TEMP");
    ref.set(temp);
    sliderContainer.style.backgroundImage = `linear-gradient(to top, #fff ${perc}%, #002439 0%)`;
  }

  slider.addEventListener("mousedown", startDrag);
  slider.addEventListener("touchstart", startDrag, {passive: false});

  document.addEventListener("mouseup", stopDrag);
  document.addEventListener("touchend", stopDrag);

  document.addEventListener("mousemove", performDrag);
  document.addEventListener("touchmove", performDrag, {passive: false});

}