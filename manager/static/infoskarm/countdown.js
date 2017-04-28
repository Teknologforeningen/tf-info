'use strict';
$(document).ready(function(){
	
	function getTimeRemaining(endtime) {
	  var t = Date.parse(endtime) - Date.parse(new Date());
	  var seconds = Math.floor((t / 1000) % 60);
	  var minutes = Math.floor((t / 1000 / 60) % 60);
	  var hours = Math.floor((t / (1000 * 60 * 60)) % 24);
	  var days = Math.floor(t / (1000 * 60 * 60 * 24));
	  return {
	    'total': t,
	    'days': days,
	    'hours': hours,
	    'minutes': minutes,
	    'seconds': seconds
	  };
	};



	function initializeClock(id) {
	  function updateCountdown() {
	    var clock = document.getElementById(id);
	    if(clock){
	    	var data = document.getElementById('clockdata');
	    	var endtime = new Date(data.getAttribute('year'), data.getAttribute('month'), data.getAttribute('day'), data.getAttribute('hour'), 0, 0, 0);
		    var daysSpan = clock.querySelector('.days');
		    var hoursSpan = clock.querySelector('.hours');
		    var minutesSpan = clock.querySelector('.minutes');
		    var secondsSpan = clock.querySelector('.seconds');
		    var t = getTimeRemaining(endtime);
		    daysSpan.innerHTML = t.days;
		    hoursSpan.innerHTML = ('0' + t.hours).slice(-2);
		    minutesSpan.innerHTML = ('0' + t.minutes).slice(-2);
		    secondsSpan.innerHTML = ('0' + t.seconds).slice(-2);

		    if (t.total <= 0) {
		      clearInterval(timeinterval);
		    }
	    }
	  };

	  updateCountdown();
	  var timeinterval = setInterval(updateCountdown, 1000);
	};

	
	initializeClock('clockdiv');
});
