import asyncio

# Delete all messages in channel
async def purge (msg, wame):
    deleted = await wame.purge_from \
            (msg.channel, limit = 1000, check = is_not_me)
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
def greet (wame):
    print ("Logged in as: " + \
            "\n\tName\t: " + wame.user.name + \
            "\n\tID  \t: " + wame.user.id +\
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
async def parse_args (msg):
    args = msg.split (' ')
    args[0] = args[0][2:] # 2 because that's the length of my prefix
    args = [a for a in args if a] # Take a wild guess: you missed. Try harder.
    return args

# Search for a comic in the index and return it's number
# Phrase: list
# index: dict {word: {number: weight, number: weight, ...}, word: ..}
#   word: str, number: str (isdigit() = true), weight: int
# create a dictionary (matched) with some numbers as its keys
# matched : {number: weight, number: weight, ..}
# the numbers used for the keys are the one who appear as a value when ding:
#   index[word] <- word is in the index
#       now matched (dict) contain all the values of word (dict) as its keys
# How:
# If phrase contains only one word and it's a sequence of digits:
#   if this digit is not greater than the last key of refs (dict)
#       it is returned
#   else: normal procedure
#
# for eah word in phrase:
#   If the word is in the index:
#       combine the content of index[word] with matched
# 
# if the length of match is not > 0:
#   nothing as been found
# else:
# return the key with the higher value
async def get_xkcd (phrase, index, refs):
    if len (phrase) == 1 and phrase [0].isdigit ():
        if int (phrase[0]) <=  len (refs):
            return [0, phrase [0]]

    matched = dict ()
    for word in phrase:
        if word in index:
            m = index[word]
            await combine (matched, m)
    
    if len (matched) > 0:
        return [0, max (matched, key = matched.get)]
    else:
        return [-1]

# a: dict, b: dict
# for each key in b:
#   if the key is in a:
#       a[key] = a[key] + b[key], aka add their values and put it in a
#   else: 
#       a[key] = b[key], aka create the key in a with the same  value as in b
async def combine (a, b):
    bk = list (b.keys ())
    for k in bk:
        if k in a:
            a[k] = a[k] + b[k]
        else:
            a[k] = b[k]
