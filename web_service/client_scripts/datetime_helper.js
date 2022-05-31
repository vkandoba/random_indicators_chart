function datetimeToPlotlyNative(dt_str){
    // TODO: use Plotly.js functions
    // TODO: shift to client timezone from GMT
	return dt_str.replace('T', ' ').replace(/\.\d+/, '');
}