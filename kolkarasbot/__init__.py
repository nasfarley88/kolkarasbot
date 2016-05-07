import os
import sys
import asyncio
import telepot
import telepot.async

import dataset

from . import utils

class KolkarasBot(telepot.async.SpeakerBot):
    async def on_chat_message(self, msg):
        content_type, chat_type, chat_id = telepot.glance(msg)
        print('Chat:', content_type, chat_type, chat_id)

        # Shove every message in the microphone
        self.mic.send(msg)

        if content_type != 'text':
            return

        parsed_text = await utils.parse_command(msg['text'])
        if not parsed_text:
            return

        if "/help" == parsed_text[0]:
            await self.sendMessage(
                chat_id,
                await utils.odin_transmission((
                    "/roll AdS - e.g. 4d12\n"
                    "/roll - Rolls 3d6")))

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

    # async def enter_lore(self, msg):
    #     """Enters lore into database."""
    #     content_type, chat_type, chat_id = telepot.glance(msg)
    #     listener = await self.create_listener(chat_id)
    #     await self.sendMessage(chat_id, "Enter entry name:")
    #     entry_name = (await listener.wait())['text']
    #     await self.sendMessage(chat_id, "Enter entry text:")
    #     entry_text = (await listener.wait())['text']

    #     with dataset.connect() as db:
    #         table = db["lore_arcadia"]
    #         table.insert(dict(
    #             name=entry_name,
    #             text=entry_text,))

    #     await self.sendMessage(chat_id, "Entry added.")

    async def search_lore(self, msg):
        """Search lore."""
        content_type, chat_type, chat_id = telepot.glance(msg)
        listener = await self.create_listener(chat_id)

        await self.sendMessage(chat_id, "Which entry would you like?")
        entry_name = (await listener.wait())['text']
        path = "wiki/lore/{}.md".format(entry_name.replace(' ', '-'))
        if os.path.exists(path):
            with open(path) as file:
                entry = {"name": entry_name,
                         "text": file.read()}
            # with dataset.connect() as db:
            #     table = db['lore_arcadia']
            #     entry = table.find_one(
            #         name=entry_name)

            await self.sendMessage(
                chat_id,
                "{}\n\n{}".format(
                    entry['name'],
                    entry['text']))
        else:
            await self.sendMessage(
                chat_id,
            "No entry found")
