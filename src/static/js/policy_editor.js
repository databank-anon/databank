function process() {
    var policy = document.getElementById("editor").textContent;
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
	if (this.readyState == 4 && this.status == 200) {
	    document.getElementById("status").innerHTML = this.responseText;
	}
    };
    xhttp.open("POST", "/policy/check", true);
    xhttp.setRequestHeader('Content-type', 'application/x-www-form-urlencoded');
    xhttp.send("policy=" + policy);
    document.getElementById("status").innerHTML = '<div class="spinner-border" role="status"></div>';
}

function save() {
    var f = document.createElement('form');
    f.action = "/policy/save";
    f.method = "POST"
    var i = document.createElement('input');
    i.type = "hidden";
    i.name = "policy";
    i.value = document.getElementById("editor").textContent;
    f.appendChild(i);
    document.body.appendChild(f);
    f.submit();
}
