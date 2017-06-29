import asyncio

def is_someone (msg):
    return True

# Delete all messages in channel
async def purge (msg, wame):
    deleted = await wame.purge_from \
            (msg.channel, limit = 1000, check = is_someone)
    await wame.send_message \
            (msg.channel, 'Deleted {} message(s)'.format (len (deleted)))

# Load the content of a json file
# The return value isn't necessar a dictionary
# f is the file name (same dir or absolute path)
def loadJson (f):
    import json
    a = dict ()
    with open (f) as infile:
        a = json.load (infile)
    return a

# Notify a successful connection in the terminal
def greet (wame, channel = None):
    a = ""
    for i in wame.servers:
        a += "\n\t        : @" + i.name
    print ("Logged in as: " + \
            "\n\tName\t: " + wame.user.name +\
            "\n\tServers : " + str (len (wame.servers)) +\
            a +\
            "\n\tID  \t: " + wame.user.id +\
            "\n\tBug \t: " + channel.name + "@" + channel.server.name +\
            "\n")
    wame.change_presence (game = 'with Nerds')

# Ask the user to type a tring a number of times
# Felicitate when it's done
async def challenge (msg, wame):
    chal = "Wame is awesome"
    it = 4
    await wame.send_message (msg.channel, 'Type {} {} times.'.format (chal, it))
    for i in range (4):
        msg = await wame.wait_for_message (author = msg.author, content = chal)
        fmt = '{} left to go...'
        await wame.send_message (msg.channel, fmt.format (it - i -1))

    await wame.send_message (msg.channel, \
            'Not so dumb, heh?\nI mean great job wumpus!')

# Stop sending messages for a given time
async def pause (msg, wame):
    t = 5
    await asyncio.sleep (10)
    await wame.send_message (msg.channel, 'Came back, has the Jedi!')

# Count the number of messages a user has in a channel
async def count (msg, wame):
    counter = 0
    tmp = await wame.send_message (msg.channel, 'Calculating messages...')
    logs = wame.logs_from (msg.channel, limit = 10000)
    async for log in logs:
        if log.author == msg.author:
            counter += 1

    await wame.edit_message (tmp, 'You have {} messages.'.format (counter))

# Delete roles
async def clean (msg, wame):
    to_del = 'new role'
    rol = msg.server.roles
    count = len (rol)
    nr = [x for x in rol if x.name == to_del]
    to_del_count = len (nr)
    await wame.send_message \
            (msg.channel, 'Role count: {}\nTo delete: {}'.format \
            (count, to_del_count))
    for r in nr:
        await wame.delete_role (msg.server, r)
    await wame.send_message \
            (msg.channel, 'New role count: {}'.format (len (msg.server.roles)))

# Parse a string to extract the command and the arguments
# msg = "<prefix>command arg1 arg2 arg3 ..."
# return = [command, arg1, arg2, arg3, ...]
# NOTE: A prefix of length to is assumed
async def parse_args (msg, prefix):
    args = msg.split (' ')
    args[0] = args[0][len(prefix):] # 2 because that's the length of my prefix
    args = [a for a in args if a] # Take a wild guess: you missed. Try harder.
    return args

# Search for a comic in the index and return it's number
# Highest: greatest number of words from the query
#       and greatest weight in absolute 'comic': [weight, score]
# We prefer a greater score
# i.e query = "kek lol haha"
# index: "kek": {'1': 1, '2': 1, '4': 3},
#        "lol": {'2': 2, '5': 1, '9': 2},
#       "haha": {'1': 2, '3': 4, '6': 1}
# resulting score:  '1': [3, 2], '2': [3, 2], '3': [4, 1], '4': [3, 1]
#                   '5': [1, 1], '6': [1, 1], '9': [2, 1]
# We first select the comic with the greatest score:
#   '1': [3, 2], '2': [3, 2]
# Then select the ones with greated weight:
#   '1': [3, 2], '2': [3, 2]
# Return one of them (1|2)
async def get_xkcd (phrase, index, refs):
    import random

    if len (phrase) == 1 and phrase [0].isdigit ():
        if int (phrase[0]) <=  len (refs):
            return [0, phrase [0]]

    matched = dict ()
    score = dict ()
    for word in phrase:
        if word in index:
            m = index[word]
            await combine (matched, m)
    
    if len (matched) > 0:
        max_score = matched \
                [max (matched, key = lambda x: matched[x]['score'])]['score']
        a = {x: matched[x] for x in matched if matched[x]['score'] == max_score}

        max_weight = a [max (a, key = lambda x: a[x]['weight'])]['weight']
        b = {x: a[x] for x in a if a[x]['weight'] == max_weight}
        
        return [0, random.choice (list(b.keys()))]
    else:
        return [-1]

# a: dict, b: dict
# for each key in b:
#   if the key is in a:
#       add their value
#   else: 
#       a[key] = b[key], aka create the key in a with the same  value as in b
async def combine (a, b):
    bk = list (b.keys ())
    for k in bk:
        if k in a:
            a[k]['weight'] = a[k]['weight'] + b[k]
        else:
            a[k] = {'weight': b[k], 'score': 0}

    for k in list (set (bk)):
        a[k]['score'] += 1

# Clean up the query then call get_xkcd
async def search (q, index, refs, bl):
    import xkcd_helpers as XKCD
    query = XKCD.removePunk (q)
    qlist = list (set (query.split (' ')))
    qlist = [x for x in qlist if x and not (x in bl or x == ' ')]
    return await get_xkcd (qlist, index, refs)

async def create_embed (comic):
    import discord
    embed_comic = discord.Embed \
            (title = '{}: {}'.format (comic['number'], comic['title']), \
            colour = discord.Colour(0x00ff00), \
            url = 'https://{}'.format (comic['url']))

    embed_comic.set_footer (text = '{}'.format (comic['alt']))
    embed_comic.set_image (url = 'https://{}'.format (comic['url']))
    embed_comic.set_author (name = 'xkcd', url = 'https://xkcd.com')

    return embed_comic

async def random_embed (refs):
    import random
    return await create_embed \
            (refs [random.choice (list (refs.keys()))])
