import sys
import asyncio
import random
import telepot
import telepot.async
from telepot.namedtuple import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardHide, ForceReply
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton
from telepot.namedtuple import InlineQueryResultArticle, InlineQueryResultPhoto, InputTextMessageContent

import dataset

import dice

import re

message_with_inline_keyboard = None

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


class KolkarasBot(telepot.async.SpeakerBot):
    async def on_chat_message(self, msg):
        content_type, chat_type, chat_id = telepot.glance(msg)
        print('Chat:', content_type, chat_type, chat_id)

        # Shove every message in the microphone
        self.mic.send(msg)

        if content_type != 'text':
            return

        parsed_text = await parse_command(msg['text'])
        if not parsed_text:
            return

        if "/help" == parsed_text[0]:
            await self.sendMessage(chat_id, help_message)

        if "/latest" == parsed_text[0]:
            await self.sendMessage(
                chat_id,
                await odin_transmission("WARNING: CURRENT NEWS FEEDS ARE NOT OPERATIONAL."))

        if "/roll" == parsed_text[0]:
            await self.sendMessage(
                chat_id,
                await roll_the_dice(
                    ''.join(parsed_text[1] if parsed_text[1] else "3d6"
                    )),
                parse_mode="Markdown")

        if "/newlore" == parsed_text[0]:
            await self.enter_lore(msg)

        if "/lore" == parsed_text[0]:
            await self.search_lore(msg)

    async def create_listener(self, chat_id, **kwargs):
        """Create listener and wait for response. """
        listener = super(KolkarasBot, self).create_listener()
        listener.capture(chat__id=chat_id, **kwargs)
        return listener

    async def enter_lore(self, msg):
        """Enters lore into database."""
        content_type, chat_type, chat_id = telepot.glance(msg)
        listener = await self.create_listener(chat_id)
        await self.sendMessage(chat_id, "Enter entry name:")
        entry_name = (await listener.wait())['text']
        await self.sendMessage(chat_id, "Enter entry text:")
        entry_text = (await listener.wait())['text']

        with dataset.connect() as db:
            table = db["lore_arcadia"]
            table.insert(dict(
                name=entry_name,
                text=entry_text,))

        await self.sendMessage(chat_id, "Entry added.")

    async def search_lore(self, msg):
        """Search lore."""
        content_type, chat_type, chat_id = telepot.glance(msg)
        listener = await self.create_listener(chat_id)

        await self.sendMessage(chat_id, "Which entry would you like?")
        entry_name = (await listener.wait())['text']
        with dataset.connect() as db:
            table = db['lore_arcadia']
            entry = table.find_one(
                name=entry_name)

        await self.sendMessage(
            chat_id,
            "{}\n\n{}".format(
                entry['name'],
                entry['text']))



    # if command == 'c':
    #     markup = ReplyKeyboardMarkup(keyboard=[
    #                  ['Plain text', KeyboardButton(text='Text only')],
    #                  [dict(text='Phone', request_contact=True), KeyboardButton(text='Location', request_location=True)],
    #              ])
    #     await bot.sendMessage(chat_id, 'Custom keyboard with various buttons', reply_markup=markup)
    # elif command == 'i':
    #     markup = InlineKeyboardMarkup(inline_keyboard=[
    #                  [dict(text='Telegram URL', url='https://core.telegram.org/')],
    #                  [InlineKeyboardButton(text='Callback - show notification', callback_data='notification')],
    #                  [dict(text='Callback - show alert', callback_data='alert')],
    #                  [InlineKeyboardButton(text='Callback - edit message', callback_data='edit')],
    #                  [dict(text='Switch to using bot inline', switch_inline_query='initial query')],
    #              ])

    #     global message_with_inline_keyboard
    #     message_with_inline_keyboard = await bot.sendMessage(chat_id, 'Inline keyboard with various buttons', reply_markup=markup)
    # elif command == 'h':
    #     markup = ReplyKeyboardHide()
    #     await bot.sendMessage(chat_id, 'Hide custom keyboard', reply_markup=markup)
    # elif command == 'f':
    #     markup = ForceReply()
    #     await bot.sendMessage(chat_id, 'Force reply', reply_markup=markup)

# async def on_callback_query(msg):
#     query_id, from_id, data = telepot.glance(msg, flavor='callback_query')
#     print('Callback query:', query_id, from_id, data)

    # if data == 'notification':
    #     await bot.answerCallbackQuery(query_id, text='Notification at top of screen')
    # elif data == 'alert':
    #     await bot.answerCallbackQuery(query_id, text='Alert!', show_alert=True)
    # elif data == 'edit':
    #     global message_with_inline_keyboard

    #     if message_with_inline_keyboard:
    #         msgid = (from_id, message_with_inline_keyboard['message_id'])
    #         await bot.editMessageText(msgid, 'NEW MESSAGE HERE!!!!!')
    #     else:
            # await bot.answerCallbackQuery(query_id, text='No previous message to edit')

# def on_inline_query(msg):
#     def compute():
#         query_id, from_id, query_string = telepot.glance(msg, flavor='inline_query')
#         print('Computing for: %s' % query_string)

#         articles = [InlineQueryResultArticle(
#                         id='abcde', title='Telegram', input_message_content=InputTextMessageContent(message_text='Telegram is a messaging app')),
#                     dict(type='article',
#                         id='fghij', title='Google', input_message_content=dict(message_text='Google is a search engine'))]

#         photo1_url = 'https://core.telegram.org/file/811140934/1/tbDSLHSaijc/fdcc7b6d5fb3354adf'
#         photo2_url = 'https://www.telegram.org/img/t_logo.png'
#         photos = [InlineQueryResultPhoto(
#                       id='12345', photo_url=photo1_url, thumb_url=photo1_url),
#                   dict(type='photo',
#                       id='67890', photo_url=photo2_url, thumb_url=photo2_url)]

#         result_type = query_string[-1:].lower()

#         if result_type == 'a':
#             return articles
#         elif result_type == 'p':
#             return photos
#         else:
#             results = articles if random.randint(0,1) else photos
#             if result_type == 'b':
#                 return dict(results=results, switch_pm_text='Back to Bot', switch_pm_parameter='Optional start parameter')
#             else:
#                 return dict(results=results)

#     answerer.answer(msg, compute)

# def on_chosen_inline_result(msg):
#     result_id, from_id, query_string = telepot.glance(msg, flavor='chosen_inline_result')
#     print('Chosen Inline Result:', result_id, from_id, query_string)


TOKEN = sys.argv[1]  # get token from command-line

bot = KolkarasBot(TOKEN)
loop = asyncio.get_event_loop()

loop.create_task(bot.message_loop())
print('Listening ...')

loop.run_forever()
# TOKEN = sys.argv[1]  # get token from command-line

# bot = telepot.async.SpeakerBot(TOKEN)
# answerer = telepot.async.helper.Answerer(bot)

# loop = asyncio.get_event_loop()
# loop.create_task(bot.message_loop({'chat': on_chat_message,
#                                    # 'callback_query': on_callback_query,
#                                    # 'inline_query': on_inline_query,
#                                    # 'chosen_inline_result': on_chosen_inline_result,
# }))
# print('Listening ...')

# loop.run_forever()
