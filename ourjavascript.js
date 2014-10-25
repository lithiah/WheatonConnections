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
				var Three = String(this["Three"]);
				var Natural = this["Natural"];
				var Social = this["Social"];
				var Humanities = this["Humanities"];

				var end = Description.length - 43;

				currentText = $("#jsonfill").html();

				$("#jsonfill").html(currentText + "<div id='con" + i + "' <br>" + Name + "<br>" + Description.substring(0, end) + "</div>");
								
				var newdiv = "#con" + i

				$(newdiv).addClass("two");

				if (Three == "True") {
					$(newdiv).addClass("three");
				};
				if (Natural == "True") {
					$(newdiv).addClass("natural");
				};
				if (Social == "True") {
					$(newdiv).addClass("social");
				};
				if (Humanities == "True") {
					$(newdiv).addClass("humanities");
				};

				i = i + 1;
			});

		},
		error: function(xhr, status) {
		alert("hatada:" + xhr.responseXML);
  		}
	});
  	
  	$(function(){ 
  		$('.2or3').find(':checkbox').each(function(){

  		console.log(this);
        $(this).attr('checked', true);

    	});
    });   

	$('.uk-form').change(function(){

		// 2 or 3 courses
		if ($('#2course').is(":checked")) {
			$('.two').show();
		}
		else {
			$('.two').hide();
		}
		if ($('#3course').is(":checked")) {
			$('.three').show();
		}
		else {
			$('.three').hide();
		}
		
		// division
		if ($('#natsci').is(":checked")) {
			$('.natural').show();
		}
		else {
			$('.natural').hide();
		}
		if ($('#socsci').is(":checked")) {
			$('.social').show();
		}
		else {
			$('.social').hide();
		}
		if ($('#hum').is(":checked")) {
			$('.humanities').show();
		}
		else {
			$('.humanities').hide();
		}	

    				
  	});
  
});

