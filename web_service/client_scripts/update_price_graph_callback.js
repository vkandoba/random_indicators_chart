function(update_data) {
	console.log("The update graph callback with data:")
	console.log(update_data);
    if (update_data && update_data['timestamp'] && update_data['new_price'])
        return {'x': [[update_data['timestamp']]], 'y': [[update_data['new_price']]]}
     else
        return {'x': [], 'y': []}
}
