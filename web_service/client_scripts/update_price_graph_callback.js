function(data, figure) {
	console.log("The update graph callback with data:")
	console.log(data);

	figure.data[0].x = data.times.map((t, _) =>  datetimeToPlotlyNative(t))
	figure.data[0].y = data.values;

	timeline_start = datetimeToPlotlyNative(data.times[0]);
	timeline_end = datetimeToPlotlyNative(data.times[data.times.length - 1]);
	figure.layout.xaxis.range = [timeline_start, timeline_end]

	new_figure = {'data': figure.data, 'layout': figure.layout}

	console.log("New figure object:")
	console.log(new_figure);		

	return new_figure;
}
