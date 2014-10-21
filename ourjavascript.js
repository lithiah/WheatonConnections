$(document).ready(function() {

	$.ajax(
	{      
  		type: 'GET',
		url: 'connections.json',
		data: "{}",
		contentType: "application/json; charset=utf-8",
		dataType: "json",
		async: false,
		success: function (data) {
		alert('got data!');
		},
		error: function(xhr, status) {
		alert("hatada:" + xhr.responseXML);
  		}
	});




  $('.connectiondescriptions').hide();
  
  $('#selectionform').change(function(){
    $('.connectiondescriptions').hide();
  	$('.onesWEWANT').show();
  });
  
});