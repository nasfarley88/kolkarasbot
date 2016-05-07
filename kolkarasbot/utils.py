import random
import re
import dice

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

async def roll_the_dice(string):
    dice_roll = dice.roll(string)
    try:
        return "*{}* = [{}]".format(
            sum(dice_roll), dice_roll)
    except TypeError:
        # Something went wrong, just send the output
        return str(dice_roll)

async def odin_transmission(string):
    """Formats a string as an ODIN transmission. """
    return """~~~ ODIN TRANSMISSION ~~~

{}

~~~ END ODIN TRANSMISSION ~~~
""".format(string)


help_message = """~~~ ODIN TRANSMISSION ~~~

/roll AdS - e.g. 4d12
/roll - Rolls 3d6

~~~ END ODIN TRANSMISSION ~~~
"""
