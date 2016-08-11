/*  jQuery ready function. Specify a function to execute when the DOM is fully loaded.  */
$(document).ready(
  
  /* This is the function that will get executed after the DOM is fully loaded */
  function () {
    $("#status").html("jQuery is loaded and ready.");
  }


);

function updTime() {
  var d = new Date();
  var date_str = d.toUTCString().replace(/GMT/g, "").replace(/[A-Z][a-z]{2},\s/g,"");
  //date_str = date_str.replace(/GMT/, "");
  document.getElementById('universal').innerHTML = date_str;

}
function startClock() {
  setInterval(function () { updTime() }, 1000);
}
startClock();