function(data, figure) {
	console.log("was called the update graph callback with data")
	console.log(data);
	
	figure.data[0].x = Array(data.values.length).fill().map((_, i) => i);
	figure.data[0].y = data.values;
	return figure;
}