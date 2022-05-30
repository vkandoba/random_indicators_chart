function(msg, instrument_data, current_data) {
	if (current_data && instrument_data && instrument_data.symbol != current_data.symbol)
	{
		console.log('Was called update the data callback by change the instrument symbol. New instrument data:');
		console.log(instrument_data);
		
		return instrument_data;
	}
				
	if (current_data && msg)
	{
		console.log('Was called the data callback with new prices. Updates data:');
		console.log(price_update);
		
		var price_update = JSON.parse(msg.data);
		var new_price = price_update[current_data.symbol];
		current_data.values.push(new_price);
		return current_data;
	}
	
	console.log('Was called the data callback with no current price data. Price data from server:');
	console.log(instrument_data);
	return instrument_data || {'symbol': "", 'values': []};
}
