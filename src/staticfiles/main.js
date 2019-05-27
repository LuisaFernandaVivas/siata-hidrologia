var v02 = document.getElementById("label_v02")
var v04 = document.getElementById("label_v04")
var v08 = document.getElementById("label_v08")
var url = 'http://127.0.0.1:8000/items/nueva_dovela'


$.ajax({
	method:'GET',
	url: url,
	success: function(data){
		console.log("success")
	},
	error: function(error_data){
		console.log("error")
	}
})

function showHint(lamina) {
  var xhttp;
  console.log(lamina.length)
  if (lamina.length == 0) { 
    posicion.innerHTML = "";
    return;
  }
  xhttp = new XMLHttpRequest();
  xhttp.onreadystatechange = function() {
    if (this.readyState == 4 && this.status == 200) {
      v02.innerHTML = 'V02 | y = '+(lamina*0.8).toFixed(2)+' m)'
      v04.innerHTML = 'V04 | y = '+(lamina*0.6).toFixed(2)+' m)'
      v08.innerHTML = 'V08 | y = '+(lamina*0.2).toFixed(2)+' m)'
    }
  };
  xhttp.open("GET", url, true);
  xhttp.send();   
}
