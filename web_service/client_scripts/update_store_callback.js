function(msg, instrument_data, current_data) {
	if (current_data && instrument_data && instrument_data.symbol != current_data.symbol)
	{
		console.log('The data update callback by change the instrument symbol. New instrument data:');
		console.log(instrument_data);

		return instrument_data;
	}
				
	if (current_data && msg)
	{
		console.log('The data update callback with new prices. Updates:');
		console.log(msg);
		
		var update_date = JSON.parse(msg.data);
		
		var new_price = update_date['new_prices'][current_data.symbol];
		update_time = update_date['timestamp']
		
		console.log("update time: " + update_time)
		console.log("new price: " + new_price)
		
		current_data.values.push(new_price);
		current_data.times.push(update_time);

		return {'values': current_data.values.slice(), 'times': current_data.times.slice()};
	}
	
	console.log('The data update callback with no current price data. Price data from server:');
	console.log(instrument_data);

	return instrument_data || {'symbol': "", 'values': [], 'times': []};
}
