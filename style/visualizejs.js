$(document).ready(function() {
  
  function makeforcegraph() {
  	
  	var margin = {top: 50, right: 50, bottom: 50, left: 50},
				width = 940 - margin.left - margin.right,
				height = 500 - margin.top - margin.bottom

  	svg = d3.select('#svgbody')
  	.append("svg:svg")
				.attr('width', width + margin.left + margin.right)
				.attr('height', height + margin.top + margin.bottom)
	.append("svg:g")
				.attr("transform", "translate(" + margin.left + "," + margin.top + ")");

	svg.append("svg:rect")
				.attr("width", width)
				.attr("height", height)
				.attr("class", "plot");

  };

  makeforcegraph();
  
});

// function makeRWAGraph() {
// 		if ($("#rwagraphdiv").text() == 'True') {
// 			$("#rwagraphdiv").removeClass('hidden');
// 			$("#rwagraphdiv").text('');

// 			// size of the graph variables
// 			var margin = {top: 20, right: 20, bottom: 30, left: 50},
// 				width = 940 - margin.left - margin.right,
// 				height = 500 - margin.top - margin.bottom


// 			// scales your x-axis. input domain is the range of possible input data values (here, d3.extent returns the largest and
// 			// smallest values found within dataArray)
// 			// and the range is the possible output values. basically this makes it so that no matter what size your graph, values
// 			// will be scaled according to the width we've defined above
// 			var x = d3.scale.linear()
// 				.range([0, width])
// 				.domain(d3.extent(dataArray, function(d) { return d[0] }));

// 			// essentially doing the same thing, but slightly lowering/increasing min/max values so that our y-axis is better centered
// 			var yExtent = d3.extent(dataArray, function(d) { return d[1] })
// 			yExtent[0] = yExtent[0] * 0.9;
// 			yExtent[1] = yExtent[1] * 1.1;

// 			var y = d3.scale.linear()
// 				.range([height, 0])
// 				.domain(yExtent);

// 			// specifies the path data using path data generator method, each x,y coordinate is from our dataArray/d, but processed 
// 			// through var x or var y to get the appropriately scaled value
// 			var line = d3.svg.line()
// 				.x(function(d) { return x(d[0]); })
// 				.y(function(d) { return y(d[1]); });

// 			// https://github.com/mbostock/d3/wiki/Zoom-Behavior
// 			// allows user to perform zoom action. .x(x) sets the x scale to be the one you zoom, the extent sets the scale's allowed
// 			// range, and .on("zoom", zoomed) says that on the call zoom, the result of the function zoomed() (selecting all the 
// 			// necessary elements of chart) will be passed to zoom/d3.behavior.zoom() (I think? not positive on this)
// 			var zoom = d3.behavior.zoom()
// 				.x(x)
// 				.scaleExtent([1, Number.POSITIVE_INFINITY])
// 				.on("zoom", redraw);

// 			// creates an svg, and sets it to the #rwagraphdiv from rwanalysis.html, basically assigning what goes into that div
// 			svg = d3.select('#rwagraphdiv')
// 			// our div is an svg, and we are creating an svg image in our svg variable (which is the div #rwagraphdiv) with this width/height
// 			.append("svg:svg")
// 				.attr('width', width + margin.left + margin.right)
// 				.attr('height', height + margin.top + margin.bottom)
// 			// g allows you to group together elements and perform actions that apply to all of them at once
// 			// here, we are grouping the svg as one element, so that our call to zoom will work on the entire graph/svg image as a whole
// 			.append("svg:g")
// 				.attr("transform", "translate(" + margin.left + "," + margin.top + ")")
// 				.call(zoom);

// 			// adds a rectangle to our svg, sets our assigned width and height and sets it's class to "plot"
// 			//plot doesn't come up here, but in css styling
// 			svg.append("svg:rect")
// 				.attr("width", width)
// 				.attr("height", height)
// 				.attr("class", "plot");

// 			// creates a variable x axis, assigns the scale to x and orients it to the bottom, with 5 tick marks
// 			var xAxis = d3.svg.axis()
// 				.scale(x)
// 				.orient("bottom")
// 				.ticks(5);

// 			// adds our xAxis to our svg g (group of elements) and uses transform to put it in the right spot(not sure why height?)
// 			svg.append("svg:g")
// 				.attr("class", "x axis")
// 				.attr("transform", "translate(0, " + height + ")")
// 				.call(xAxis);

// 			// does the same thing with y axis
// 			var yAxis = d3.svg.axis()
// 				.scale(y)
// 				.orient("left")
// 				.ticks(10);
// 			// does the same thing with y axis
// 			svg.append("g")
// 				.attr("class", "y axis")
// 				.call(yAxis);

// 			// creates a variable clip which holds the clipPath. this is a set of restrictions for where our image is visible to the user
// 			// so here, we restrict the visibility of our svg image to a rectangle bound by the four attr coordinates listed below
// 			var clip = svg.append("svg:clipPath")
// 				.attr("id", "clip")
// 			.append("svg:rect")
// 				.attr("x", 0)
// 				.attr("y", 0)
// 				.attr("width", width)
// 				.attr("height", height);

// 			// creates scatterplot overlay for line graph and adds browser automatic tooltip for begining of each window
// 			var dots = svg.selectAll("dot")
//       			.data(dataArray)
//     		    .enter()
//     		    .append("circle")
//       			.attr("class", "dot")
//       			.attr("r", 3)
//       			.attr("cx", function(d) {return x(d[0]);})
//       			.attr("cy", function(d) {return y(d[1]);})
//       			.append("svg:title")
//       			.text(function(d) {
//       				return "beginning word/letter of window: " + d[0]
//       			;});


//       		// adds dots for scatterplot values to svg g
//       		svg.append("g")
//       			.attr("class", "dot")


// 			// we create a variable called ChartBody that holds everything in our svg g (so basically our whole graph) and gives it our
// 			// clipPath attribute 
// 			var chartBody = svg.append("g")
// 				.attr("clip-path", "url(#clip)");

// 			// adds a path to our ChartBody that takes the form of a line (attr "d" assigns the shape of the path) 
// 			// and gets it's data (datum) from the variable dataArray, which was passed in to this js from rwanalysis.html
// 			chartBody.append("svg:path")
// 				.datum(dataArray)
// 				.attr("class", "line")
// 				.attr("d", line)

// 			// zoomed() function called earlier. 
// 			function redraw() {
// 				svg.select(".x.axis").call(xAxis);
// 				svg.select(".y.axis").call(yAxis);
// 				svg.select(".line")
// 					.attr("class", "line")
// 					.attr("d", line);
// 				svg.selectAll(".dot")
//       				.attr("class", "dot")
//       				.attr("r", 3)
//       				.attr("cx", function(d) {return x(d[0]);})
//       				.attr("cy", function(d) {return y(d[1]);})
// 			}


// 		}
// 	}

// 	makeRWAGraph();
// });