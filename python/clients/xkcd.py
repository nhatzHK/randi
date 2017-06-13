import sys
sys.path.insert (0, '/home/nhatz/Code/GitHub/wame/python/lib/')
import discord
import logging
import asyncio
import json
import client_helpers as CLIENT

JSON = "/home/nhatz/Code/GitHub/wame/json/"
# Yep you should rename your json and append priv to it
# This way you won't add even more private stuff on github
CONFIG = JSON + "wame.config.json.priv"
INDEX = JSON + "xkcd.index.json"
REF = JSON + "xkcd.references.json"

def is_me(m):
    return m.author == Wame.user

logging.basicConfig (level = logging.INFO)

Wame = discord.Client ()

wame_config = dict ()
xkcd_index = dict ()
xkcd_refs = dict ()

wame_config = CLIENT.loadJson (CONFIG)
xkcd_index = CLIENT.loadJson (INDEX)
xkcd_refs = CLIENT.loadJson (REF)

@Wame.event
async def on_ready ():
    CLIENT.greet (Wame)

@Wame.event
async def on_message (message):
    if not message.content.startswith (wame_config['py_prefix']):
       pass 
    else:
        args = await CLIENT.parse_args (message.content)
        logging.info ('\nFull mess: {}\nCommand  : {}\nArgs     : {}'\
                .format (message.content, args[0], args[1:]))
        
        command = args [0]
    
        if command == 'xkcd':
            tmp = await Wame.send_message (message.channel, 'Searching...')
            comic = await CLIENT.get_xkcd \
                    (args[1:], xkcd_index, xkcd_refs)
            # 0 == comic found
            if comic[0] == 0:
                # pull the comic returned from the references 
                c = xkcd_refs[comic[1]]
                # Create embed
                embed_comic = discord.Embed \
                        (title = '{}: {}'.format (c['number'], c['title']), \
                        colour = discord.Colour(0x000000), \
                        url = 'https://xkcd.com/{}'.format(c['number']))
                embed_comic.set_footer (text = '{}'.format (c['alt']))
                embed_comic.set_image (url = 'https://{}'.format (c['url']))
                embed_comic.set_author (name = 'xkcd', url = 'https://xkcd.com')
                # send embed, ' ', is to remove the previous text in tmp
                await Wame.edit_message (tmp,' ', embed = embed_comic)
            else:
                # It hasn't been found, too bad
                await Wame.edit_message (tmp, \
                        "I found nothing. I'm so sawry and sad :(. \
                        \nReply with (under 1 minute):\n \
                        **<<random**: if you want me to pull out a random comic\n\
                        **<<new _<query>_**: for a new query\n\
                        **<<stop**: if you're a loser and want to give up")


Wame.run (wame_config['token'])
