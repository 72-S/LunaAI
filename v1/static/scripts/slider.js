import {db, ref, set, get} from "./firebase.js";
window.onload = () => {
  const sliderContainer = document.querySelector(".slidercontainer");
  const slider = document.querySelector(".sliderthumb");
  updateSliderValue();
  let isDragging = false;
  let startY;
  let currentValue = 0;
  let targetValue;
  const increment = 0.05;

  function smoothIncrement() {
    if (currentValue < targetValue) {
      currentValue += increment;
      sliderContainer.style.backgroundImage = `linear-gradient(to top, #fff ${currentValue * 100}%, #002439 0%)`;
      requestAnimationFrame(smoothIncrement);
    }
  }
  async function updateSliderValue() {
    const dbRef = ref(db, "TEMP");

    const snapshot = await get(dbRef);

    if (snapshot.exists()) {
      const value = snapshot.val();
      targetValue = value;
      const thumbPosition = value * (sliderContainer.clientHeight + 0.5 - slider.clientHeight);
      slider.style.bottom = `${thumbPosition}px`;
      smoothIncrement();
    } else {
      console.log("No Data were Found.");
    }
  }
  function startDrag(event) {
    isDragging = true;
    startY = event.clientY || event.touches[0].clientY;
  }

  function saveValue(dataValue) {
    const floatValue = parseFloat(dataValue);
    const dbRef = ref(db, 'TEMP');
    set(dbRef, floatValue);
  }
  function stopDrag() {
    isDragging = false;
    let bottom = parseInt(slider.style.bottom) || 0;
    let value = bottom / (sliderContainer.clientHeight - slider.clientHeight);
    let temp = value.toFixed(2);
    saveValue(temp)
    console.log(temp)

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


      updateSliderProgress(value);
    }
  }

  function updateSliderProgress(value) {
    let trackHeight = sliderContainer.offsetHeight;
    let progressHeight = value * trackHeight;
    let perc = (progressHeight / trackHeight) * 100;
    sliderContainer.style.backgroundImage = `linear-gradient(to top, #fff ${perc}%, #002439 0%)`;
  }

  slider.addEventListener("mousedown", startDrag);
  slider.addEventListener("touchstart", startDrag, {passive: false});

  document.addEventListener("mouseup", stopDrag);
  document.addEventListener("touchend", stopDrag);

  document.addEventListener("mousemove", performDrag);
  document.addEventListener("touchmove", performDrag, {passive: false});



}