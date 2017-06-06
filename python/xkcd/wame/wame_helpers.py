import asyncio

# Load and return the content of a json file in a dictionary
def loadJson (f):
    import json
    a = dict ()
    with open (f) as infile:
        a = json.load (infile)
    return a

# Notified that the client is logged in properly, in the terminal
def greet (wame):
    print ("Logged in as: " + \
            "\n\tName\t: " + wame.user.name + \
            "\n\tID  \t: " + wame.user.id +\
            "\n")
    wame.change_presence (game = 'with Nerds')

# Parse the command received and return it in a list
# The first element of the list is the command to execute
# The rest are the arguments
async def parse_args (msg):
    args = msg.split (' ')
    # Remove the prefix
    args[0] = args[0][2:] # 2 because that's the length of my prefix
    args = [a for a in args if a] # Take a wild guess: you missed. Try harder.
    return args

# Search for a comic in the index
# If the query(phrase) is one word and this word is a number:
#     we return this number
# else:
# for each word in the query we retrieve the index ( a dictionary)\
#        And merge it with the already retrieved dictionaries (see comibine ())
# From the resulting dictionary\
#        we return the key (a comic number) with the higher value 
async def get_xkcd (phrase, index, refs):
    # If we have to search only one term and it's a digit
    if len (phrase) == 1 and phrase [0].isdigit ():
        
        # last comic referenced
        l = (list (refs.keys ())) [-1]
        
        # if the request is bigger than that, return -1
        if int (phrase[0]) >  int (l):
            return [-1]
        else:
            # return  [0, number of the comic]
            return [0, phrase[0]]
    else:
        matched = dict () # dict to hold the matching comics
        for word in phrase:
            # if the word is in the index
            if word in index:
                m = index[word]
                await combine (matched, m)
        if len (matched) > 0:
            return [0, max (matched, key = matched.get)]
        else:
            return [-1]

# Combine the two dictionaries
# The value of the keys are assumed to be integers
# First we assume a as the older dict and will merge b in it
# This previous line is important read it again
# If a key in a is already in b:
#    It's value is added to the b key
# Otherwise the key is add to be with it's existing value
# e.g a => {'a': 1, 'b': 2}, b => {'a': 2, 'c' : 4}
# When merged we end up with a => {'a': 3, 'b': 2, 'c': 4}
async def combine (a, b):
    bk = list (b.keys ())
    for k in bk:
        if k in a:
            a[k] = a[k] + b[k]
        else:
            a[k] = b[k]
