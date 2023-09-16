function displayDateTime() {
  var now = new Date();

  // Array of full weekday names
  var weekdays = [
    "Sunday",
    "Monday",
    "Tuesday",
    "Wednesday",
    "Thursday",
    "Friday",
    "Saturday",
  ];

  // Get full weekday name
  var weekday = weekdays[now.getDay()];

  // Get day of the month
  var day = now.getDate();

  // Get full year
  var year = now.getFullYear();

  // Display formatted date in 'date' element
  document.getElementById("date").innerHTML = `${weekday} ${day} ${year}`;

  // Display time in 'time' element
  var time = now.toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" });
  document.getElementById("time").innerHTML = time;
}

// Run the function every second to keep the time updated
setInterval(displayDateTime, 1000);
