from .array_collapse import try_collapse_array
from .CollapsedData import CollapsedPrimitive
from .primitives import is_primitive

def collapse_data(data):

    if is_primitive(data):
        return CollapsedPrimitive(data)
    elif isinstance(data, dict):
        return _process_dict(data)
    elif isinstance(data, list):
        return _process_list(data)
    else:
        assert False


def _process_dict(data):

    assert isinstance(data, dict)

    processed_dict = {}
    for key in data.keys():
        processed_dict[key] = collapse_data(data[key])

    return processed_dict

def _process_list(data):

    assert isinstance(data, list)

    success, collapsed_array = try_collapse_array(data)

    if success:
        return collapsed_array

    else:
        processed_list = []
        for item in data:
            processed_list.append(collapse_data(item))

        return processed_list
