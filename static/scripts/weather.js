document.addEventListener("DOMContentLoaded", (event) => {
  const weatherWidget = document.querySelector(".weather-widget");
  const wrapper = weatherWidget.querySelector(".wrapper");
  const weatherPart = wrapper.querySelector(".weather-part");
  const wIcon = weatherPart.querySelector("img");

  let api;
  let apiKey = "b190a0605344cc4f3af08d0dd473dd25";

  function requestApi(city) {
    api = `https://api.openweathermap.org/data/2.5/weather?q=${city}&units=metric&appid=${apiKey}`;
    fetchData();
  }

  function fetchData() {
    fetch(api)
      .then((res) => res.json())
      .then((result) => weatherDetails(result))
      .catch(() => {
        alert("Something went wrong");
      });
  }

  function weatherDetails(info) {
    if (info.cod == "404") {
      alert("Invalid city name");
    } else {
      const city = info.name;
      const country = info.sys.country;
      const { description, id } = info.weather[0];
      const { temp, feels_like, humidity } = info.main;
      console.log(id);

      let dayNight = info.weather[0].icon.slice(-1); // Extracts 'd' for day or 'n' for night

      if (id == 800) {
        wIcon.src = `../static/icons/clear-${dayNight == 'd' ? 'day' : 'night'}.svg`;
      } else if (id >= 210 && id <= 212) {
        wIcon.src = "../static/icons/thunderstorms.svg";
      } else if ((id >= 200 && id <= 202) || (id >= 221 && id <= 232)) {
        wIcon.src = "../static/icons/thunderstorms-rain.svg";
      } else if (id >= 300 && id <= 321) {
        wIcon.src = "../static/icons/drizzle.svg";
      } else if (id >= 500 && id <= 531) {
        wIcon.src = "../static/icons/rain.svg";
      } else if (id >= 600 && id <= 622) {
        wIcon.src = "../static/icons/snow.svg";
      } else if (id >= 701 && id <= 710) {
        wIcon.src = "../static/icons/mist.svg";
      } else if (id >= 711 && id <= 720) {
        wIcon.src = "../static/icons/smoke.svg";
      } else if (id >= 721 && id <= 730) {
        wIcon.src = "../static/icons/haze.svg";
      } else if ((id >= 731 && id <= 740) || (id >= 751 && id <= 771)) {
        wIcon.src = "../static/icons/dust.svg";
      } else if (id == 781) {
        wIcon.src = "../static/icons/tornado.svg";
      } else if (id >= 801 && id <= 804) {
        wIcon.src = "../static/icons/cloudy.svg"
      } else if (id >= 741 && id <= 750) {
        wIcon.src = "../static/icons/fog.svg"
      }
      
      
      weatherPart.querySelector(".temp .numb").innerText = Math.floor(temp);
      weatherPart.querySelector(".weather").innerText = description;
      weatherPart.querySelector(".temp .numb-2").innerText =
        Math.floor(feels_like);
      weatherPart.querySelector(".humidity span").innerText = `${humidity}%`;
      wrapper.classList.add("active");
    }
  }

  // Call requestApi with a default city
  requestApi("Waakirchen");

  // Then call requestApi every 7 minutes
  setInterval(function () {
    requestApi("Waakirchen");
  }, 15 * 60 * 1000); // 7 minutes in milliseconds
});
