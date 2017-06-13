import discord
import logging
import asyncio
import json
import wame_helpers

JSON = "/home/nhatz/Code/Bots/Wame/json/"
CONFIG = JSON + "wame.config.json"
INDEX = JSON + "xkcd.index.json"
REF = JSON + "xkcd.references.json"

def is_me(m):
    return m.author == Wame.user

logging.basicConfig (level = logging.INFO)

Wame = discord.Client ()

wame_config = dict ()
xkcd_index = dict ()
xkcd_refs = dict ()
#commands = list ()

with open (CONFIG) as infile:
    wame_config = json.load (infile)

with open (INDEX) as infile:
    xkcd_index = json.load (infile)

with open (REF) as infile:
    xkcd_refs = json.load (infile)

async def startsWith (test, start):
    return test.startswith (start)

@Wame.event
async def on_ready ():
    wame_helpers.greet (Wame)

@Wame.event
async def on_message (message):
    if not message.content.startswith (wame_config['py_prefix']):
       pass 
    else:
        args = await wame_helpers.parse_args (message.content)
        logging.info ('\nFull mess: {}\nCommand  : {}\nArgs     : {}'\
                .format (message.content, args[0], args[1:]))
        
        command = args [0]
        if command == 'count':
            await wame_helpers.count (message, Wame)
    
        elif command == 'sleep':
            await wame_helpers.pause (message, Wame)

        elif command == 'start':
            await wame_helpers.challenge (message, Wame)
    
        elif command == 'xkcd':
            tmp = await Wame.send_message (message.channel, 'Searching...')
            comic = await wame_helpers.get_xkcd (args[1:], xkcd_index, xkcd_refs)
            if comic[0] == 0:
                c = xkcd_refs[comic[1]]
                await Wame.edit_message \
                        (tmp, \
                        'Number: {}\nTitle: {}\nAlt: {}\nhttp://{}'\
                        .format (c['number'], c['title'], c['alt'], c['url']))

            #tmp = await Wame.send_message (message.channel, 'Searching...') 
            #c = args[1]
            #l = list (xkcd_refs.keys ()) [-1]
            #if c.isdigit () and len (args) == 2:
            #    if int (c) > int (l):
            #        await Wame.edit_message \
            #                (tmp, "This commic is not recorded yet.")
            #    else:
            #        await Wame.edit_message \
            #                (tmp, 'https://{}'.format (xkcd_refs[c]['url']))
            #else:
            #    await Wame.edit_message \
            #            (tmp, 'Provide a number')

        elif command == 'purge':
            #await wame_helpers.purge (message, Wame)
            pass

        elif command == 'clean':
            await wame_helpers.clean (message, Wame)

Wame.run (wame_config['token'])
