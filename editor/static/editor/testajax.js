function loadDoc() {
    var xhttp = new XMLHttpRequest();
    xhttp.open("POST", "/static/editor/fixture.json", false);
    xhttp.send();
    document.getElementById("demo").innerHTML = xhttp.responseText;
}
