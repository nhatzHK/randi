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

wame_config = wame_helpers.loadJson (CONFIG)
xkcd_index = wame_helpers.loadJson (INDEX)
xkcd_refs = wame_helpers.loadJson (REF)

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
    
        if command == 'xkcd':
            tmp = await Wame.send_message (message.channel, 'Searching...')
            comic = await wame_helpers.get_xkcd (args[1:], xkcd_index, xkcd_refs)
            # 0 == comic found
            if comic[0] == 0:
                # pull the comic returned from the references 
                c = xkcd_refs[comic[1]]
                #await Wame.edit_message \
                #        (tmp, \
                #        'Number: {}\nTitle: {}\nAlt: {}\nhttp://{}'\
                #        .format (c['number'], c['title'], c['alt'], c['url']))

                embed_comic = discord.Embed (title = '{}: {}'.format (c['number'], c['title']), \
                        colour = discord.Colour(0x000000), url = 'https://xkcd.com/{}'.format(c['number']))
                embed_comic.set_footer (text = '{}'.format (c['alt']))
                embed_comic.set_image (url = 'https://{}'.format (c['url']))
                embed_comic.set_author (name = 'xkcd', url = 'https://xkcd.com')
                await Wame.edit_message (tmp,' ', embed = embed_comic)

Wame.run (wame_config['token'])
