import sys
import discord
import logging
import asyncio
import json
import random

PATH = dict ()
try:
    with open (sys.argv [1]) as path_file:
        PATH = json.load (path_file)
except IndexError: #FileNotFoundError
    print ('Usage: python {} path/to/priv.xkcd.path.json'.format (sys.argv [0]))
    exit (1)
except FileNotFoundError:
    print ('Unable to open file: {}'.format (sys.argv[1]))
    exit (2)

sys.path.insert (0, PATH['lib'])
print(sys.path[0])
try:
    import client_helpers as CLIENT
    from command import CommandManager
except ModuleNotFoundError:
    print ('Error: One or more modules were not found in path.')
    exit (2)

JSON = PATH['json']
# Yep you should rename your config.json and append priv to it
# This way you won't add even more private stuff on github
CONFIG = JSON + "priv.xkcd.config.json"
INDEX = JSON + "xkcd.index.json"
REF = JSON + "xkcd.references.json"
BL = JSON + "xkcd.common.json"
COMMANDS = JSON + "xkcd.command.json"

logging.basicConfig (level = logging.INFO)

wame_config = dict ()
xkcd_index = dict ()
xkcd_refs = dict ()

wame_config = CLIENT.loadJson (CONFIG)
xkcd_index = CLIENT.loadJson (INDEX)
xkcd_refs = CLIENT.loadJson (REF)
blk_list = CLIENT.loadJson (BL)
commands = CLIENT.loadJson (COMMANDS)

wame_help = discord.Embed \
        (title = wame_config['help']['title'], \
        colour = discord.Colour(0x123654), \
        url = wame_config['help']['url'], \
        description = wame_config['help']['description'])
wame_help.set_footer (text = wame_config['help']['footer'], \
        icon_url = wame_config['help']['icon_url'])

Wame = discord.Client ()
wgame = discord.Game (name = wame_config['game'])

comanager = CommandManager(
        Wame,
        xkcd_refs,
        xkcd_index,
        blk_list,
        commands,
        wame_config,
        wame_help)

@Wame.event
async def on_ready ():
    await Wame.change_presence (game = wgame)
    bug_channel = Wame.get_channel (wame_config['report_channel'])
    CLIENT.greet (Wame, channel = bug_channel)

@Wame.event
async def on_message (message):
    if message.content.startswith (wame_config['prefix']):
        if message.mention_everyone \
                or len(message.content.split("@here")) > 1 \
                or len(message.mentions) > 1:
                    return

        args = await CLIENT.parse_args (message.content, wame_config['prefix'])
        
        # Empty message handling
        if len(args) > 0:
            command = args[0]
            del args[0]
        else:
            command = False
        
        logging.info ('\nFull mess: {}\nCommand  : {}\nArgs     : {}'\
                .format (message.content, command, args))

        # length 1, messag handling
        # i.e   <prefix> --command <= length = 1
        #       <prefix> --command arg0 arg2 <= length = 3
        if len(args) > 1:
            args = args[1:]

        if command in comanager.com:
            await comanager.run(message, command, args)
        else:
            # put the first arg back in the list
            if command:
                args.insert(0, command)

            await comanager.run(message, '--search', args)

Wame.run (wame_config['token'])
