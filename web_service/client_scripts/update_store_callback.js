function(msg, instrument_name) {
    console.log("-----------------------------------")
    console.log("The data update callback with new prices. Updates:");
    console.log(msg);
    if (msg)
    {
        var update_data = JSON.parse(msg.data);

        console.log(instrument_name);
        var new_price = update_data['prices'][instrument_name];
        update_time = update_data['timestamp']

        console.log("update time: " + update_time)
        console.log("new price: " + new_price)

        return {'new_price': new_price, 'timestamp': update_time};
    }
    else
    {
        console.warn("The update message is empty")
        return {}
    }
}
