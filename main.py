import sys
import asyncio

from kolkarasbot import KolkarasBot

TOKEN = sys.argv[1]  # get token from command-line

bot = KolkarasBot(TOKEN)
loop = asyncio.get_event_loop()

loop.create_task(bot.message_loop())
print('Listening ...')

loop.run_forever()
