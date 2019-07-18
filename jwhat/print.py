from termcolor import cprint, colored
from .primitives import is_primitive
from .CollapsedData import CollapsedItem

CHAR_HORIZ = "─"
CHAR_VERT = "│"
CHAR_BRANCH_BOTTOM = "┬"
CHAR_BRANCH_LEFT = "├"
CHAR_ANGLE = "└"

def print_data(collapsed_data, current_depth=0, current_delta=0, parents_deltas=[], max_depth=-1, no_color=False, color_picker=None):

    if color_picker is None:
        color_picker = ColorPicker()

    if isinstance(collapsed_data, CollapsedItem):
        print(": " + str(collapsed_data))
        return

    if max_depth != -1 and current_depth == max_depth:
        text = colored_wrapper(": <max depth reached>", "white", no_color)
        print(text)
        return

    if isinstance(collapsed_data, dict):

        color = color_picker.get_color()
        nb_items = len(collapsed_data)
        max_key_len = max(map(len, collapsed_data.keys()))

        for i, (key, item) in enumerate(collapsed_data.items()):
            _print_data_with_key(key, item, current_depth, current_delta, color, i, nb_items, max_key_len, parents_deltas, max_depth, no_color, color_picker)

    elif isinstance(collapsed_data, list):

        color = color_picker.get_color()
        nb_items = len(collapsed_data)

        keys_list = ["{%d}" % i for i in range(nb_items)]
        max_key_len = max(map(len, keys_list))

        for i, (key, item) in enumerate(zip(keys_list, collapsed_data)):
            _print_data_with_key(key, item, current_depth, current_delta, color, i, nb_items, max_key_len, parents_deltas, max_depth, no_color, color_picker)

    else:
        assert False

def _print_data_with_key(key, item, current_depth, current_delta, color, i, nb_items, max_key_len, parents_deltas, max_depth, no_color, color_picker):

    formatted_key_txt = _get_formatted_key(key, current_delta, color, i, nb_items, max_key_len, parents_deltas, no_color)
    print(formatted_key_txt, end="")

    new_delta = max_key_len
    new_parent_color = "" if i == nb_items - 1 else color
    new_parents_deltas = parents_deltas + [(current_delta, new_parent_color)]
    new_depth = current_depth + 1

    print_data(item, new_depth, new_delta, new_parents_deltas, max_depth, no_color=no_color, color_picker=color_picker)

def _get_formatted_key(key, current_delta, color, index, nb_items, max_key_len, parents_deltas, no_color):

    if index == 0:

        first_char_branch = CHAR_HORIZ if nb_items == 1 else CHAR_BRANCH_BOTTOM
        padding_branch = (max_key_len - len(key)) * CHAR_HORIZ

        txt = colored_wrapper(first_char_branch + padding_branch + key, color, no_color)

    else:

        parent_bars_txt = ""
        for padding, parent_color in parents_deltas:
            if parent_color == "":
                parent_bars_txt += " " * (padding + 1)
            else:
                parent_bars_txt += " " * padding + colored_wrapper(CHAR_VERT, parent_color, no_color)

        space_padding = " " * current_delta

        first_char_branch = CHAR_ANGLE if index == nb_items - 1 else CHAR_BRANCH_LEFT
        padding_branch = (max_key_len - len(key)) * CHAR_HORIZ

        txt = parent_bars_txt + colored_wrapper(space_padding + first_char_branch + padding_branch + key, color, no_color)

    return txt

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
