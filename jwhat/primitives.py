def is_primitive(data):
    return data is None or \
           isinstance(data, int) or \
           isinstance(data, float) or \
           isinstance(data, str) 
