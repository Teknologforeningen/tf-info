'use strict';

$(document).ready(function(){
	function getPage(index){
		$.getJSON('/pages/'+index+'/')
		.success(function(data){

			$.get(data.url).success(function(content){
				$("#content").html(content);
			});

			setTimeout(getPage, data.duration * 1000 ,data.next);
		})
	}

	getPage(0);
});