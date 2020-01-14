window.onload = function() {
    let source = new EventSource('http://localhost:5001/event/' + "1@1.com", {"Access-Control-Allow-Origin": true});
    source.onmessage = function (event) {
			console.log(event.data)
    }
}