import asyncio
import json
import random
import discord
from urllib.request import urlopen

def generate_help(commands, config):
    e_title = config['help']['title']
    e_colour = discord.Colour (0x123654)
    e_url = config['help']['url']
    e_desc = config['help']['description']
    for com in commands:
        if 'usage' in commands[com]:
            h = f"**{com}** \n\t{commands[com]['description']}\
                    \n\t`@xkcd {commands[com]['usage']}`"

            if 'alias' in commands[com]:
                h += f"\n\tAliases: `{'`, `'.join(commands[com]['alias'])}`"

            e_desc += f"\n\n{h}"

    h_embed = discord.Embed (
            title = e_title,
            colour = e_colour,
            url = e_url,
            description = f"{e_desc}\n\n")
    h_embed.set_footer (
            text = config['help']['footer'],
            icon_url = config['help']['icon_url'])
    
    return h_embed

def is_someone(msg):
    return True

# Delete all messages in channel
async def purge(msg, wame):
    deleted = await wame.purge_from \
           (msg.channel, limit = 1000, check = is_someone)
    await wame.send_message \
           (msg.channel, 'Deleted {} message(s)'.format(len(deleted)))

# Load the content of a json file
# The return value isn't necessary a dictionary
# f is the file name(same dir or absolute path)
def loadJson(f):
    a = dict()
    with open(f) as infile:
        a = json.load(infile)
    return a

# Notify a successful connection in the terminal
def greet(wame, channel = None):
    a = ""
    for i in wame.servers:
        a += "\n\t        : @" + i.name
    print("Logged in as: " + \
            "\n\tName\t: " + wame.user.name +\
            "\n\tServers : " + str(len(wame.servers)) +\
            a +\
            "\n\tID  \t: " + wame.user.id +\
            "\n\tBug \t: " + channel.name + "@" + channel.server.name +\
            "\n")
    wame.change_presence(game = 'with Nerds')

# Ask the user to type a tring a number of times
# Felicitate when it's done
async def challenge(msg, wame):
    chal = "Wame is awesome"
    it = 4
    await wame.send_message(msg.channel, 'Type {} {} times.'.format(chal, it))
    for i in range(4):
        msg = await wame.wait_for_message(author = msg.author, content = chal)
        fmt = '{} left to go...'
        await wame.send_message(msg.channel, fmt.format(it - i -1))

    await wame.send_message(msg.channel, \
            'Not so dumb, heh?\nI mean great job wumpus!')

# Stop sending messages for a given time
async def pause(msg, wame):
    t = 5
    await asyncio.sleep(10)
    await wame.send_message(msg.channel, 'Came back, has the Jedi!')

# Count the number of messages a user has in a channel
async def count(msg, wame):
    counter = 0
    tmp = await wame.send_message(msg.channel, 'Calculating messages...')
    logs = wame.logs_from(msg.channel, limit = 10000)
    async for log in logs:
        if log.author == msg.author:
            counter += 1

    await wame.edit_message(tmp, 'You have {} messages.'.format(counter))

# Delete roles
async def clean(msg, wame):
    to_del = 'new role'
    rol = msg.server.roles
    count = len(rol)
    nr = [x for x in rol if x.name == to_del]
    to_del_count = len(nr)
    await wame.send_message \
           (msg.channel, 'Role count: {}\nTo delete: {}'.format \
           (count, to_del_count))
    for r in nr:
        await wame.delete_role(msg.server, r)
    await wame.send_message \
           (msg.channel, 'New role count: {}'.format(len(msg.server.roles)))

# Parse a string to extract the command and the arguments
# msg = "<prefix>command arg1 arg2 arg3 ..."
# return = [command, arg1, arg2, arg3, ...]
# NOTE: A prefix of length to is assumed
async def parse_args(msg, prefix):
    args = msg.split(' ')
    args = args[1:]
    args = [a for a in args if a] # Take a wild guess: you missed. Try harder.
    return args

"""
Search for a comic in the index and return it's number

Highest: greatest number of words from the query
and greatest weight in absolute 'comic': [weight, score]

We prefer a greater score

i.e query = "kek lol haha"
index: "kek": {'1': 1, '2': 1, '4': 3},
        "lol": {'2': 2, '5': 1, '9': 2},
        "haha": {'1': 2, '3': 4, '6': 1}
resulting score:  '1': [3, 2], '2': [3, 2], '3': [4, 1], '4': [3, 1]
                '5': [1, 1], '6': [1, 1], '9': [2, 1]
We first select the comic with the greatest score:
    '1': [3, 2], '2': [3, 2]
Then select the ones with greated weight:
    '1': [3, 2], '2': [3, 2]
Return one of them(1|2)
"""
async def get_xkcd(phrase, index, refs):
    """
    If the query is one string long and the string is a number
    1. Look if a comic of this number is in the reference
    2. If not in reference check for it online
    If both failed proceed to normal search,
    otherwise return the comic of the said number
    """
    if len(phrase) == 1 and phrase [0].isdigit():
        if int(phrase[0]) <=  len(refs):
            return {'status': 0, 'comic': refs[phrase[0]]}
        else:
            online_check = await get_online_xkcd(number = phrase[0])
            if online_check['status'] is 0:
                # it\s to get shitty, get shitty
                # FIXME: this is really shitty, gawd
                return {'status': 0, 'comic': online_check}

    # Real search starts here
    matched = dict()
    score = dict()
    for word in phrase:
        if word in index:
            await combine(matched, index[word])
    
    if len(matched) > 0:
        max_score = matched \
                [max(matched, key = lambda x: matched[x]['score'])]['score']
        a = {x: matched[x] for x in matched if matched[x]['score'] == max_score}

        max_weight = a [max(a, key = lambda x: a[x]['weight'])]['weight']
        b = {x: a[x] for x in a if a[x]['weight'] == max_weight}
        
        return {'status': 0, 'comic': refs[random.choice(list(b.keys()))]}
    else:
        return {'status': -1}

"""
a: dict, b: dict
for each key in b:
    if the key is in a:
        add their value
    else: 
        a[key] = b[key], aka create the key in a with the same  value as in b
"""
async def combine(a, b):
    bk = list(b.keys())
    for k in bk:
        if k in a:
            a[k]['weight'] = a[k]['weight'] + b[k]
        else:
            a[k] = {'weight': b[k], 'score': 0}

    for k in list(set(bk)):
        a[k]['score'] += 1

# Clean up the query then call get_xkcd
async def search(q, index, refs, bl):
    import xkcd_helpers as XKCD
    query = XKCD.removePunk(q)
    qlist = list(set(query.split(' ')))
    qlist = [x for x in qlist if x and not(x in bl or x == ' ')]
    return await get_xkcd(qlist, index, refs)

async def create_embed(xkcd):
    comic = xkcd['comic']
    
    embed_comic = discord.Embed \
           (title = '{}: {}'.format(comic['num'], comic['title']), \
            colour = discord.Colour(0x00ff00), url = comic['img'])

    embed_comic.set_footer(text = '{}'.format(comic['alt']))
    embed_comic.set_image(url = comic['img'])
    embed_comic.set_author(name = 'xkcd', \
            url = 'https://xkcd.com/{}'.format(comic['num']))

    return embed_comic

async def random_embed(refs):
    return await create_embed \
           (refs [random.choice(list(refs.keys()))])

#FIXME: This is some kind of a special madness, I don't remember having
#coded while drunk
async def report_embed(msg, report):
    t = 'Report -> {}'.format(report['type'])
    c = report['color']

    d = '\n**Context**\nServer -> {}\nChannel -> {}\nUser -> {}\nTime -> {}\
            \n**Client**: \n\tName: -> {}\n\tId -> {}\n' \
            .format(msg.server, msg.channel, msg.author, msg.timestamp, \
            report['client'].user.name, report['client'].user.id)
    d+= '**Message**\n{}\n'.format(msg.content)
    if report['type'] is 'internal':
        d += '\n\n**Internal**{}'.format(report['internal_report'])

    embed_report = discord.Embed(title = t, description = d, colour = c)

    return embed_report

async def get_online_xkcd(number = 0):
    if number is 0:
        url ='https://xkcd.com/info.0.json'
    else:
        url = 'https://xkcd.com/{}/info.0.json'.format(number)

    response = {'status': 0, 'comic': ""}
    
    try:
        online_comic = urlopen(url).read()
        response['comic'] = json.loads(online_comic.decode('utf-8'))
    except:
        response['status'] = -1
    
    return response
