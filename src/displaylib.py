"""
A library to display things on screen.
"""

from __future__ import print_function

import math
import sys

# define some colors
# ----------------------------------------------------------------------------------------------------------------------
BLACK = '\033[30m'
RED = '\033[31m'
GREEN = '\033[32m'
YELLOW = '\033[33m'
BLUE = '\033[34m'
MAGENTA = '\033[35m'
CYAN = '\033[36m'
WHITE = '\033[37m'
BRIGHT_RED = '\033[91m'
BRIGHT_GREEN = '\033[92m'
BRIGHT_YELLOW = '\033[93m'
BRIGHT_BLUE = '\033[94m'
BRIGHT_MAGENTA = '\033[95m'
BRIGHT_CYAN = '\033[96m'
BRIGHT_WHITE = '\033[97m'
ENDC = '\033[0m'


# ----------------------------------------------------------------------------------------------------------------------
def display_progress(count,
                     total,
                     old_percent,
                     width=50,
                     completed_char="#",
                     empty_char=".",
                     postpend_str=""):
    """
    Draws and updates ASCII progress bar on the stdout.

    :param count: The current count for our progress bar.
    :param total: The count at 100%.
    :param old_percent: The previous percent. Necessary to prevent updates if
           the percentage has not changed since the last call.
    :param width: How wide to draw the progress bar in characters. If given an
           odd number, it will be rounded down to the nearest even value.
    :param completed_char: The character to display for a completed chunk.
    :param empty_char: The character to display for an as-yet uncompleted chunk.
    :param postpend_str: An arbitrary (and optional) string to append to the end of the progress bar.

    :return: The percent value for the current state.
    """

    # only allow even numbered widths
    if width % 2 != 0:
        width -= 1

    # calculate the percent
    percent = round((count * 1.0) / total * 100, 1)

    # only update the display if the percentage has changed
    if percent == old_percent and percent != 0:
        return percent

    # build the completed and uncompleted portions of the progress bar
    done_str = "{0}".format(completed_char * (int(round(percent / (100 / width), 0))))
    empty_str = "{0}".format(empty_char * (width - (int(round(percent / (100 / width))))))

    # build the X out of Y text
    count_str = " (" + BRIGHT_WHITE + str(count) + ENDC + " of " + BRIGHT_WHITE + str(total) + ENDC + ")"

    # build the percent string
    percent_str = "{0}".format(" " * (4 - len(str(int(math.floor(percent)))))) + str(percent) + "%" + " "

    # build the complete string, and insert the percent
    progress_bar_str = "[" + done_str + empty_str + "]"
    progress_left = progress_bar_str[:int((len(progress_bar_str) / 2) - math.floor(len(percent_str) / 2)) + 2]
    progress_right = progress_bar_str[int((len(progress_bar_str) / 2) + math.ceil(len(percent_str) / 2)) + 2:]
    progress_bar_str = progress_left
    progress_bar_str += BRIGHT_YELLOW + percent_str + ENDC
    progress_bar_str += progress_right

    # append the count string
    progress_bar_str += count_str

    # append the postpend string
    progress_bar_str += postpend_str

    # show it
    sys.stdout.write(progress_bar_str)
    sys.stdout.flush()
    sys.stdout.write("\b" * (len(progress_bar_str)))  # return to start of line

    # return the percent (so that we only update the percentage when it changes)
    return percent


# ----------------------------------------------------------------------------------------------------------------------
def display_error(*msgs):
    """
    Given any number of args, converts those args to strings, concatenates them, and prints to stdErr.

    :return: Nothing.
    """

    output = ""
    for msg in msgs:
        output += " " + str(msg)
    print(output.lstrip(" "), file=sys.stderr)


# ----------------------------------------------------------------------------------------------------------------------
def format_string(msg):
    """
    Given a string (msg) this will format it with colors based on the {{COLOR}} tags. (example {{COLOR_RED}}). It will
    also convert literal \n character string into a proper newline.

    :param msg: The string to format.

    :return: The formatted string.
    """

    output = msg.replace(r"\n", "\n")
    output = output.replace("{{", "{")
    output = output.replace("}}", "}")

    try:
        output = output.format(
            BLACK=BLACK,
            RED=RED,
            GREEN=GREEN,
            YELLOW=YELLOW,
            BLUE=BLUE,
            MAGENTA=MAGENTA,
            CYAN=CYAN,
            WHITE=WHITE,
            BRIGHT_RED=BRIGHT_RED,
            BRIGHT_GREEN=BRIGHT_GREEN,
            BRIGHT_YELLOW=BRIGHT_YELLOW,
            BRIGHT_BLUE=BRIGHT_BLUE,
            BRIGHT_MAGENTA=BRIGHT_MAGENTA,
            BRIGHT_CYAN=BRIGHT_CYAN,
            BRIGHT_WHITE=BRIGHT_WHITE,
            COLOR_NONE=ENDC,
        )
    except KeyError:
        pass

    output += ENDC

    return output


# ----------------------------------------------------------------------------------------------------------------------
def display_message(*msgs):
    """
    Given any number of args, converts those args to strings, concatenates them, and prints to stdOut.

    :return: Nothing.
    """

    msg = " ".join([str(item) for item in msgs])
    msg = format_string(msg)
    print(msg)


# ----------------------------------------------------------------------------------------------------------------------
def format_boolean(value,
                   colorize=True):
    """
    Converts a boolean value into a Yes or No. If colorize is True, then Yes will be returned as green, and no will be
    returned as red.

    :param value: A boolean either passed as a boolean or as a string.
    :param colorize: If True, then the returned string will be formatted green for True, or red for False.

    :return: A string containing either "Yes" or "No" depending on the original boolean value.
    """

    assert type(value) is bool or (type(value) is str and value.upper() in ("TRUE", "FALSE"))

    if str(value).upper() == "TRUE":
        color = "BRIGHT_GREEN"
        return_value = "Yes"
    else:
        color = "BRIGHT_RED"
        return_value = "No"

    if colorize:
        return_value = format_string("{{" + color + "}}" + return_value)

    return return_value


# ----------------------------------------------------------------------------------------------------------------------
def display_refreshable_message(*msgs):
    """
    Given any number of args, converts those args to strings, concatenates them, and prints to stdOut. Then resets the
    output to be back at the beginning f the line ready for the next string to overwrite the just printed string. NOTE:
    THIS ONLY WORKS FOR STRINGS THAT STAY THE SAME LENGTH OR GROW IN LENGTH. If the string shrinks in length, part of
    the previous message will be left behind. To counter this (if you have potentially shrinking strings), it may be
    necessary to pad your strings with spaces at the end to a known length.

    :return: Nothing.
    """

    # Print the message, flush buffer, and move back to the beginning of the line.
    message = " ".join([str(item) for item in msgs])
    sys.stdout.write(message)
    sys.stdout.flush()
    sys.stdout.write("\b" * (len(message)))


# ----------------------------------------------------------------------------------------------------------------------
def finish_refreshable_message():
    """
    Called when the refreshable message is no longer needed (prevents the next printed statement from overwriting the
    last version of the refreshed message).

    :return: Nothing.
    """

    print()
