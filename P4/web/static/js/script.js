window.onload = function() {
    let source = new EventSource("http://localhost:5001/event/" + "1@1.com", {"Access-Control-Allow-Origin": true});
    source.onmessage = function (event) {
            document.getElementById("notification_text").innerHTML = "";
            document.getElementById("notification_text").innerHTML = event.data;
            document.getElementById("notification").style.display = "block";
    }
}