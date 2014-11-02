$(document).ready(function(){
	function update(){
		$.get('/weather/small/', function(data){
			$("#small-screen").html(data);
		});
	}
	update();
	setInterval(update, 1000*60);
});