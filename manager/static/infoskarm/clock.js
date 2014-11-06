'use strict';
$(document).ready(function(){
	var updateClock = function() {
		var time = new Date();
		$("#time").html(time.toLocaleTimeString('sv'));
		$("#date").html(time.getDate()+'.'+(time.getMonth()+1)+'.'+time.getFullYear());
	};

	setInterval(updateClock, 1000);
});
