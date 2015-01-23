'use strict';

$(document).ready(function(){
	function getVoteresults(){
		$.get('/voteresults/')
		.success(function(data){
			$("#footer_center").html(data);
			setTimeout(getVoteresults, 300 * 1000);
		})
	}

	getVoteresults();
});