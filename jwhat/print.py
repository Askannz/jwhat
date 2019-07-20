from copy import deepcopy
from termcolor import colored
from .primitives import is_primitive
from .CollapsedData import CollapsedItem

CHAR_HORIZ = "─"
CHAR_VERT = "│"
CHAR_BRANCH_BOTTOM = "┬"
CHAR_BRANCH_LEFT = "├"
CHAR_ANGLE = "└"

def print_data(config, collapsed_data, context=None):

    if context is None:
        context = _make_initial_context()

    is_collapsed_item = isinstance(collapsed_data, CollapsedItem)
    is_max_depth_leaf = config["max_depth"] != -1 and context["current_depth"] == config["max_depth"]
    is_dict = isinstance(collapsed_data, dict)
    is_list = isinstance(collapsed_data, list)

    # Leaf
    if is_collapsed_item or is_max_depth_leaf:

        parent_bars_txt = _get_parents_bars_txt(context["parents_deltas"], config["no_color"])
        collapsed_end_newline = "\n" + parent_bars_txt if context["last"] or not context["compact"] else ""

        if is_collapsed_item:
            print(": " + str(collapsed_data) + collapsed_end_newline)

        elif is_max_depth_leaf:
            text = colored_wrapper(": <max depth reached>", "white", config["no_color"]) + collapsed_end_newline
            print(text)

    # Node
    elif is_dict or is_list:

        color = context["color_picker"].get_color()
        nb_items = len(collapsed_data)

        if is_dict:
            keys_list = collapsed_data.keys()
            values_list = collapsed_data.values()
        elif is_list:
            keys_list = ["{%d}" % i for i in range(nb_items)]
            values_list = collapsed_data

        max_key_len = max(map(len, keys_list))
        are_all_items_collapsed = all(map(lambda it: isinstance(it, CollapsedItem), values_list))

        for i, (key, item) in enumerate(zip(keys_list, values_list)):

            iterable_context = {
                "key_string": key,
                "color": color,
                "index": i,
                "nb_items": nb_items,
                "max_key_len": max_key_len,
                "are_all_items_collapsed": are_all_items_collapsed
            }

            _print_data_with_key(config, item, iterable_context, context)


def _print_data_with_key(config, item, iterable_context, context):

    formatted_key_txt = _get_formatted_key(config, iterable_context, context)
    print(formatted_key_txt, end="")

    new_context = deepcopy(context)

    new_context["last"] = iterable_context["index"] == iterable_context["nb_items"] - 1
    new_parent_color = "" if new_context["last"] else iterable_context["color"]
    new_context["current_delta"] = iterable_context["max_key_len"]
    new_context["parents_deltas"] = context["parents_deltas"] + [(context["current_delta"], new_parent_color)]
    new_context["current_depth"] = context["current_depth"] + 1
    new_context["compact"] = iterable_context["are_all_items_collapsed"]

    print_data(config, item, new_context)

def _get_formatted_key(config, iterable_context, context):

    index = iterable_context["index"]
    max_key_len = iterable_context["max_key_len"]
    key = iterable_context["key_string"]
    color = iterable_context["color"]
    nb_items = iterable_context["nb_items"]

    if index == 0:

        first_char_branch = CHAR_HORIZ if nb_items == 1 else CHAR_BRANCH_BOTTOM
        padding_branch = (max_key_len - len(key)) * CHAR_HORIZ

        txt = colored_wrapper(first_char_branch + padding_branch + key, color, config["no_color"])

    else:

        parent_bars_txt = _get_parents_bars_txt(context["parents_deltas"], config["no_color"])

        space_padding = " " * context["current_delta"]

        first_char_branch = CHAR_ANGLE if index == nb_items - 1 else CHAR_BRANCH_LEFT
        padding_branch = (max_key_len - len(key)) * CHAR_HORIZ

        txt = parent_bars_txt + colored_wrapper(space_padding + first_char_branch + padding_branch + key, color, config["no_color"])

    return txt

def _get_parents_bars_txt(parents_deltas, no_color):

    parent_bars_txt = ""
    for padding, parent_color in parents_deltas:
        if parent_color == "":
            parent_bars_txt += " " * (padding + 1)
        else:
            parent_bars_txt += " " * padding + colored_wrapper(CHAR_VERT, parent_color, no_color)

    return parent_bars_txt

def _make_initial_context():

    context = {}
    context["color_picker"] = ColorPicker()
    context["current_depth"] = 0
    context["current_delta"] = 0
    context["parents_deltas"] = []
    context["compact"] = False
    context["last"] = False

    return context

def colored_wrapper(text, color, no_color):
    if no_color:
        return text
    else:
        return colored(text, color)

class ColorPicker:

    def __init__(self):

        self.COLORS = ["red", "green", "blue", "magenta", "cyan", "yellow"]
        self.index = 0

    def get_color(self):

        color = self.COLORS[self.index]
        self.index = (self.index + 1) % len(self.COLORS)
        return color
