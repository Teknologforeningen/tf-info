'use strict';

$(document).ready(function(){
	function getLogo(index){
		$.getJSON('/rotatelogos/'+index+'/')
		.success(function(data){

			$("#footer_left").html('<img src="'+data.url+'"></img>');

			setTimeout(getLogo, 20000, data.next);
		})
	}

	getLogo(0);
});