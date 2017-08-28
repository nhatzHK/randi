#!/usr/bin/python

import sys
import json

with open('../client/xkcd.path.json.priv') as path_file:
    PATH = json.load(path_file)
    sys.path.insert(0, PATH['lib'])

import client_helpers as CLIENT
import xkcd_helpers as XKCD

PREPATH = PATH['json']
REFS = PREPATH + 'xkcd.references.json'
INDEX = PREPATH + 'xkcd.index.json'
BLACK_LIST = PREPATH + 'xkcd.common.json'

index = dict ()
refs = CLIENT.loadJson (REFS)
black_list = CLIENT.loadJson (BLACK_LIST)
edited = False

def update_index(references=REFS):
    global edited, index
    for i in list(refs.keys ()):
        transcript = str ()
        title = str ()
        alt = str ()
        complete_str = str ()

        #FIXME: I really need to fix these magic numbers
        if refs[i]['stat_com']['status'] == 0:
            edited = True
            # Retrieve the comic info from the references
            title = refs[i]['comic']['title']
            alt = refs[i]['comic']['alt']
            if refs[i]['stat_tr']['status'] >= -1:
                transcript = XKCD.removeNoise (refs[i]['comic']['transcript'])

        complete_str = XKCD.removePunk('{} {} {}'.format(title, alt,  transcript)) 

        # Record the comic in the index
        XKCD.indexComic (complete_str, i, index, black_list)

    # save file
    if edited:
        with open (INDEX, 'w') as outfile:
            json.dump (index, outfile, indent = 4)
