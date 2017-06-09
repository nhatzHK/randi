import asyncio

async def purge (msg, wame):
    deleted = await wame.purge_from \
            (msg.channel, limit = 1000, check = is_not_me)
    await wame.send_message \
            (msg.channel, 'Deleted {} message(s)'.format (len (deleted)))

def is_not_me (msg):
    return True

def loadJson (f):
    import json
    a = dict ()
    with open (f) as infile:
        a = json.load (infile)
    return a

# Done
def greet (wame):
    print ("Logged in as: " + \
            "\n\tName\t: " + wame.user.name + \
            "\n\tID  \t: " + wame.user.id +\
            "\n")
    wame.change_presence (game = 'with Nerds')

# Done
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

# Done
async def pause (msg, wame):
    t = 5
    await asyncio.sleep (10)
    await wame.send_message (msg.channel, 'Came back, has the Jedi!')

# Done
async def count (msg, wame):
    counter = 0
    tmp = await wame.send_message (msg.channel, 'Calculating messages...')
    logs = wame.logs_from (msg.channel, limit = 10000)
    async for log in logs:
        if log.author == msg.author:
            counter += 1

    await wame.edit_message (tmp, 'You have {} messages.'.format (counter))

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

async def parse_args (msg):
    args = msg.split (' ')
    args[0] = args[0][2:] # 2 because that's the length of my prefix
    args = [a for a in args if a] # Take a wild guess: you missed. Try harder.
    return args

async def get_xkcd (phrase, index, refs):
    if len (phrase) == 1 and phrase [0].isdigit ():
        l = list (xkcd_keys ()) [-1]
        if int (phrase) >  l:
            return [-1]
        else:
            return [0, refs [phrase [0]] ['url']]
    else:
        matched = dict ()
        for word in phrase:
            if word in index:
                m = index[word]
                await combine (matched, m)
        if len (matched) > 0:
            return [0, max (matched, key = matched.get)]
        else:
            return [-1]

async def combine (a, b):
    bk = list (b.keys ())
    for k in bk:
        if k in a:
            a[k] = a[k] + b[k]
        else:
            a[k] = b[k]
