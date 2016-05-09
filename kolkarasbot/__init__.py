import os
import sys
import asyncio
import telepot
import telepot.async
from fuzzywuzzy import process
import re

from . import utils

from fuzzywuzzy.fuzz import WRatio, ratio

def custom_match(s1, s2):
    """A custom matching function which weights strings which match ratio.

    Check the code."""

    main_match = 100*WRatio(s1, s2)
    ratio_match = ratio(s1, s2)

    return main_match + ratio_match


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
                await utils.odin_transmission(utils.help_message))

        if "/latest" == parsed_text[0]:
            await self.sendMessage(
                chat_id,
                await odin_transmission(
                    "WARNING: CURRENT NEWS FEEDS ARE NOT OPERATIONAL."))

        if "/roll" == parsed_text[0]:
            await self.sendMessage(
                chat_id,
                await utils.roll_the_dice(
                    ''.join(parsed_text[1] if parsed_text[1] else "3d6"
                    )),
                parse_mode="Markdown")

        if "/lore" == parsed_text[0]:
            await self.search_lore(msg)

        if "/wiki" == parsed_text[0]:
            await self.where_is_wiki(msg)

    async def create_listener(self, chat_id, **kwargs):
        """Create listener and wait for response. """
        listener = super(KolkarasBot, self).create_listener()
        listener.capture(chat__id=chat_id, **kwargs)
        return listener

    async def where_is_wiki(self, msg):
        content_type, chat_type, chat_id = telepot.glance(msg)
        await self.sendMessage(
            chat_id,
            await utils.get_wiki_address()
        )

    async def search_lore(self, msg):
        """Search lore."""
        content_type, chat_type, chat_id = telepot.glance(msg)
        listener = await self.create_listener(chat_id)

        await self.sendMessage(chat_id, "Which entry would you like?")
        entry_name = (await listener.wait())['text']

        choices = os.listdir("wiki/lore")
        with open(
                "wiki/lore/{}".format(
                    process.extractOne(
                        entry_name,
                        choices,
                        scorer=custom_match)[0])) as data_file:
            data = re.sub(r" ?\* ", r"- ", data_file.read())
            data = re.sub(r"\[(.*?)\]\(.*?\)", r"*\1*", data)
            data = re.sub(r"\[\[(.*?)\]\]", r"\1", data)
            import pdb; pdb.set_trace()
            await self.sendMessage(
                chat_id,
                await utils.odin_transmission(
                    "Entry matching: {}\n\n{}\n\nFull Entry: {}".format(
                        data_file.name.split('/')[-1].replace('.md', ''),
                        data,
                        await utils.construct_url_from_path(data_file.name)
                    )),
                parse_mode="Markdown")
