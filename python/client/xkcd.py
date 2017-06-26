import sys
import discord
import logging
import asyncio
import json
import random

PATH = dict ()
with open ('./xkcd.path.json.priv') as path_file:
    PATH = json.load (path_file)


sys.path.insert (0, PATH['lib'])
import client_helpers as CLIENT

JSON = PATH['json']
# Yep you should rename your config.json and append priv to it
# This way you won't add even more private stuff on github
CONFIG = JSON + "xkcd.config.json.priv"
INDEX = JSON + "xkcd.index.json"
REF = JSON + "xkcd.references.json"
BL = JSON + "xkcd.common.json"

logging.basicConfig (level = logging.INFO)

wame_config = dict ()
xkcd_index = dict ()
xkcd_refs = dict ()

wame_config = CLIENT.loadJson (CONFIG)
xkcd_index = CLIENT.loadJson (INDEX)
xkcd_refs = CLIENT.loadJson (REF)
blk_list = CLIENT.loadJson (BL)

wame_help = discord.Embed \
        (title = wame_config['help']['title'], \
        colour = discord.Colour(0x123654), \
        url = wame_config['help']['url'], \
        description = wame_config['help']['description'])
wame_help.set_footer (text = wame_config['help']['footer'], \
        icon_url = wame_config['help']['icon_url'])

Wame = discord.Client ()
wgame = discord.Game (name = wame_config['game'])

@Wame.event
async def on_ready ():
    await Wame.change_presence (game = wgame)
    bug_channel = Wame.get_channel ("320387081446752257")
    CLIENT.greet (Wame, channel = bug_channel)

@Wame.event
async def on_message (message):
    if not message.content.startswith (wame_config['prefix']):
        pass
    else:
        args = await CLIENT.parse_args (message.content)
        logging.info ('\nFull mess: {}\nCommand  : {}\nArgs     : {}'\
                .format (message.content, args[0], args[1:]))

        command = args [0]
        if len (args) == 0:
            pass
        elif command == 'xkcd':
            tmp = await Wame.send_message (message.channel, 'Searching...')

            # 0 == comic found
            comic = await CLIENT.search \
                    (message.content [5:], xkcd_index, xkcd_refs, blk_list)
            if len (args) < 2:
                embed_comic = await CLIENT.random_embed (xkcd_refs)
                await Wame.edit_message (tmp, ' ', embed = embed_comic) 
            elif comic[0] == 0:
                # Create embed
                embed_comic = await CLIENT.create_embed (xkcd_refs [comic [1]])
                await Wame.edit_message (tmp, ' ', embed = embed_comic)
            else:
                # It hasn't been found, too bad
                not_found = discord.Embed (description =
                    "_I found nothing. I'm so sawry and sad :(_. \
                    \nReply with **`random`** for a surprise\n",
                    colour = (0x000000))
                await Wame.edit_message (tmp, " ", embed = not_found)
                msg = await Wame.wait_for_message \
                        (author = message.author, \
                        content = "random", timeout = 20)
                if (msg):
                    embed_comic = await CLIENT.random_embed (xkcd_refs)
                    await Wame.send_message \
                            (message.channel, embed = embed_comic)
                else:
                    await Wame.edit_message (tmp, "Timeout")
        elif command == 'random':
            embed_comic = await CLIENT.random_embed (xkcd_refs)
            await Wame.send_message (message.channel, embed = embed_comic)
        elif command == 'latest':
            embed_comic = await CLIENT.create_embed \
                    (xkcd_refs [list (xkcd_refs.keys ())[-1]])
            # For dumb system like ubuntu, uncomment the following line
            # embed_comic = wame_config['latest']
            await Wame.send_message (message.channel, embed = embed_comic)
        elif command == 'report':
            bug_channel = Wame.get_channel ("320387081446752257")
            embed_report = discord.Embed (title = 'Report: {} -> {}'.format \
                    (message.timestamp, message.author), \
                    description = message.content[8:],\
                    colour = (0xff0000))
            embed_report.set_footer \
                    (text = '{}@{}'.format (message.channel, message.server))
            report = await Wame.send_message (bug_channel, embed = embed_report)
            await Wame.pin_message (report)
        elif command == 'help':
            await Wame.send_message (message.channel, \
                    embed = wame_help)

Wame.run (wame_config['token'])
