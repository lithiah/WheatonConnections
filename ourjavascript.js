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

				var Description = this["CourseDescription"];
				var Name = this["CourseName"];
				var Three = this["Three"];
				var Natural = this["Natural"];
				var Social = this["Social"];
				var Humanities = this["Humanities"];

				var end = Description.length - 43;

				currentText = $("#jsonfill").html();

				$("#jsonfill").html(currentText + "<div id='con" + i + "' <br>" + Name + "<br>" + Description.substring(0, end) + "</div>");
								
				var newdiv = "#con" + i

				console.console.log(Three);
				if (Three == "True") {
					$("newdiv").addClass("three");
				};

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