from termcolor import cprint
from .primitives import is_primitive
from .CollapsedData import CollapsedItem

SEP_FIRST_SINGLE = "─"
SEP_FIRST_MULTI = "┬"
SEP_MIDDLE = "├"
SEP_LAST = "└"

def print_data(collapsed_data, current_tabbing=0, current_depth=0, max_depth=-1, no_color=False, color_picker=None):

    if color_picker is None:
        color_picker = ColorPicker()

    color = color_picker.get_color()

    if isinstance(collapsed_data, CollapsedItem):
        print_wrapper(": " + str(collapsed_data) + "\n", "white", no_color)
        return

    if max_depth != -1 and current_depth == max_depth:
        print_wrapper(": <max depth reached>\n", "white", no_color)
        return

    elif isinstance(collapsed_data, dict):

        max_key_len = _get_max_key_length_dict(collapsed_data)

        for i, (key, item) in enumerate(collapsed_data.items()):

            tabbing_dict_key = 0 if i == 0 else current_tabbing
            sep = _get_separator(i, len(collapsed_data))

            key_padding = _get_key_padding(len(key), max_key_len)
            key_and_separators = _get_tabbed_text(sep + key_padding + key, tabbing_dict_key)

            print_wrapper(key_and_separators, color, no_color=no_color)

            tabbing_dict_value = tabbing_dict_key + len(key_and_separators)
            print_data(item, current_tabbing=tabbing_dict_value, current_depth=current_depth+1,
                       max_depth=max_depth, color_picker=color_picker)

    elif isinstance(collapsed_data, list):

        max_key_len = _get_max_key_length_list(collapsed_data)

        for i, item in enumerate(collapsed_data):

            key = "{%d}" % i

            tabbing_dict_key = 0 if i == 0 else current_tabbing
            sep = _get_separator(i, len(collapsed_data))

            key_padding = _get_key_padding(len(key), max_key_len)
            key_and_separators = _get_tabbed_text(sep + key_padding + key, tabbing_dict_key)

            print_wrapper(key_and_separators, color, no_color=no_color)

            tabbing_dict_value = tabbing_dict_key + len(key_and_separators)
            print_data(item, current_tabbing=tabbing_dict_value, current_depth=current_depth+1,
                       max_depth=max_depth, color_picker=color_picker)

    else:
        assert False

def _get_tabbed_text(text, nb_spaces):
    return " " * nb_spaces + text

def _get_separator(index, nb_items):

    if nb_items == 1:
        return SEP_FIRST_SINGLE
    else:
        if index == 0:
            return SEP_FIRST_MULTI
        elif index == nb_items - 1:
            return SEP_LAST
        else:
            return SEP_MIDDLE

def _get_key_padding(key_len, max_key_len):
    return SEP_FIRST_SINGLE * (max_key_len - key_len)

def _get_max_key_length_dict(data_dict):
    return max(len(k) for k in data_dict.keys())

def _get_max_key_length_list(data_list):
    return max(len(str(i)) for i in range(len(data_list)))

def print_wrapper(text, color, no_color):

    if no_color:
        print(text, end="")
    else:
        cprint(text, color, end="")

class ColorPicker:

    def __init__(self):

        self.COLORS = ["red", "green", "blue", "magenta", "cyan", "yellow", "grey"]
        self.index = 0

    def get_color(self):

        color = self.COLORS[self.index]
        self.index = (self.index + 1) % len(self.COLORS)
        return color
