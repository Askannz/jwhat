from .CollapsedData import CollapsedPrimitive, CollapsedEmptyArray, CollapsedArray
from .primitives import is_primitive


def try_collapse_array(array):

    assert isinstance(array, list)

    if len(array) == 0:
        return True, CollapsedEmptyArray()

    for i, item in enumerate(array):

        success, collapsed_item = _collapse_item(item)

        if not success:
            return False, None

        if i == 0:
            reference_collapsed_item = collapsed_item
            continue

        if collapsed_item != reference_collapsed_item:
            return False, None

    collapsed_array = _collect_items(reference_collapsed_item, len(array))

    return True, collapsed_array


def _collapse_item(item):

    if isinstance(item, list):
        success, collapsed_item = try_collapse_array(item)
    else:
        if is_primitive(item):
            collapsed_item = CollapsedPrimitive(item)
            success = True
        else:
            collapsed_item = None
            success = False

    return success, collapsed_item

def _collect_items(reference_collapsed_item, nb_items):

    if isinstance(reference_collapsed_item, CollapsedEmptyArray):
        collapsed_array = reference_collapsed_item.add_dimension(nb_items)

    elif isinstance(reference_collapsed_item, CollapsedPrimitive):
        collapsed_array = CollapsedArray(reference_collapsed_item.type, shape=[nb_items])

    else:
        collapsed_array = reference_collapsed_item.add_dimension(nb_items)

    return collapsed_array
