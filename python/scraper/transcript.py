#!/usr/bin/python

#==============================================================================#
# DEPENDENCIES LOADING                                                         #
#==============================================================================#
import sys
sys.path.insert (0, '/home/nhatz/Code/GitHub/randi/python/lib')
PROMPT = "[xkcd Parser]"
PREPATH = '/home/nhatz/Code/GitHub/randi/'

REFS = PREPATH + 'json/xkcd.references.json'

try:
    print (PROMPT + " Loading dependencies.")
    from splinter import Browser
    import json
    import xkcd_helpers
    print (PROMPT + " Dependencies loaded.")
except ModuleNotFoundError:
    print (PROMPT + " Missing or broke dependencies.\n \
            \tMake sure:\n \
                    \t\txkcd_helper.py exists in ./\n \
                    \t\tsplinter is installed")
    exit (1)

#==============================================================================#
# FILE LOADING                                                                 #
#==============================================================================#

XKCD = dict ()
try:
    print (PROMPT + " Loading references")
    with open (REFS) as infile:
        XKCD = json.load (infile)
    print (PROMPT + " References loaded")
except FileNotFoundError:
    xkcd_helpers.fileNotFound (PROMPT, REFS)

#==============================================================================#
# ARGUMENT CHECK                                                               #
#==============================================================================#

args = xkcd_helpers.getArgs (sys.argv [1:])
if (args [0] == 0): # Success
    print (PROMPT + \
            " Requested fetch: " + str (args [1])  + " to " + str (args [2]))
elif (args [0] == -1): #  
    print (PROMPT + \
            " Insufficient arguments. Provide one or two numbers.")
    exit (2)
elif (args [0] == -2):
    print (PROMPT + \
            " Invalid arguments. Provide numbers.")
    exit (3)
else:
    print (PROMPT + \
            " Unexpected return code from args retrieving. Stoping script.")
    exit (6)

#==============================================================================#
# FETCHING                                                                     #
#==============================================================================#

print (PROMPT + " Starting fetch...")
# last + 1 because we need to access the last element
for i in range(args [1], args [2] + 1):
        print ('{} Retrieving {}'.format(PROMPT, i))
        temp_xkcd = xkcd_helpers.get_xkcd(i)
        XKCD[i] = {\
                'comic': temp_xkcd['comic'], \
                'stat_com': {\
                'status': temp_xkcd['status'], 'error': temp_xkcd['error']}, \
                'stat_tr': {'status': 0, 'error': '', 'complete': 0}}
        
        if temp_xkcd['status'] != 0: 
            XKCD[i]['stat_tr'] = \
                    {'status': -3, 'error': 'xkcd', 'complete': -3}
        elif not temp_xkcd['comic']['transcript']:
            temp_tr = xkcd_helpers.get_transcript(i)
            XKCD[i]['comic']['transcript'] = temp_tr['tr']
            XKCD[i]['stat_tr']['status'] = temp_tr['status']
            XKCD[i]['stat_tr']['error'] = temp_tr['error']
        
        print ('{} Comic {} referenced.'.format(PROMPT, i))


#==============================================================================#
# FILES SAVING                                                                 #
#==============================================================================#

try:
    print (PROMPT + " Saving comic references in " + REFS)
    with open (REFS, 'w') as outfile:
        json.dump (XKCD, outfile, indent = 4)
    print (PROMPT + " Comic references succesfully saved.")
except:
    print (PROMPT + " Something went wrong while saving the comic file. \
            \n\tThat's not to bad.")

#==============================================================================#
print (PROMPT + " Done.")
#==============================================================================#
