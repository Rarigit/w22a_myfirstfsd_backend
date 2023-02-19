def check_data(data_sent, data_required):
    for data in data_required:
        if data_sent.get(data) == None:
            return f"The field {data} is required!"
    return None