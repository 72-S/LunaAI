function ledControl(action) {
  var xhr = new XMLHttpRequest();
  var url = "https://10.0.1.12:6969/control_led";
  xhr.open("POST", url, true);
  xhr.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
  xhr.send("action=" + action);
}

function playPause(action) {
  var xhr = new XMLHttpRequest();
  var url = "https://10.0.1.12:6969/music";
  xhr.open("POST", url, true);
  xhr.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
  xhr.send("action=" + action);
}