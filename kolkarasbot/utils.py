import random
import re
import dice
import itertools



async def parse_command(string):
    """Formats command and returns arguments (if any)."""

    # If there is no command, just return None
    command_matches = re.findall(r"(^/\w+)(@\w+ot)?", string)
    if not command_matches:
        return
    else:
        command = command_matches[0][0]

    # If no match for argments, make arguments == None
    arguments = re.sub(r"^/\w+(@\w+ot)? ?", "", string).split(' ')
    if arguments == ['']:
        arguments = None

    # TODO make logging things for this
    return (command, arguments)

def roll_the_dice(string):
    dice_roll = dice.roll(string)
    try:
        return "*{}* = [{}]".format(
            sum(dice_roll), dice_roll)
    except TypeError:
        # Something went wrong, just send the output
        return str(dice_roll)

def average(iterable):
    return float(sum(iterable))/float(len(iterable))

def has_passed(win_up_to, dice):
    if sum(dice) <= win_up_to and sum(dice) < 17:
        return True
    elif sum(dice) <= 4:
        return True
    else:
        return False

ALL_POSSIBLE_ROLLS = list(itertools.product(range(1,7), range(1,7), range(1,7)))
def success_probability(to_beat):
    probability = average(
        [1 if has_passed(to_beat, x) else 0 for x in ALL_POSSIBLE_ROLLS])
    return probability

def odin_transmission(string):
    """Formats a string as an ODIN transmission. """
    return """~~~ ODIN TRANSMISSION ~~~

{}

~~~ END ODIN TRANSMISSION ~~~
""".format(string)


help_message = """/roll AdS - e.g. 4d12
/roll - Rolls 3d6
/wiki - Returns current wiki url
/lore - Searches ODIN's archives (aka wiki) for lore

Source code: https://github.com/nasfarley88/kolkarasbot
"""



