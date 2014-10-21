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
			
			var connections = data["ConnectionDescriptions"];

			var i = 1;

			$.each(connections, function() {

				var D = this["CourseDescription"];
				var N = this["CourseName"];
				var end = D.length - 43;

				currentText = $("#jsonfill").html();

				$("#jsonfill").html(currentText + "<div id='con" + i + "' <br>" + N + "<br>" + D.substring(0, end) + "</div>");
				
				i = i + 1;

			});

			$('.uk-form').change(function(){

    				$('#jsonfill').toggle();
  			});

		},
		error: function(xhr, status) {
		alert("hatada:" + xhr.responseXML);
  		}
	});
  
  
  
});