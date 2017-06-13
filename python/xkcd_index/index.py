import sys
sys.path.insert (0, '/home/nhatz/Code/GitHub/wame/python/lib')
import json
import client_helpers as CLIENT
import xkcd_helpers as XKCD

PREPATH = '/home/nhatz/Code/GitHub/wame/'
REFS = PREPATH + 'json/xkcd.references.json'
INDEX = PREPATH + 'json/xkcd.index.json'
BLACK_LIST = PREPATH + 'json/xkcd.common.json'
OUTDEX = 'new_index.json'

index = dict ()
refs = CLIENT.loadJson (REFS)
black_list = CLIENT.loadJson (BLACK_LIST)

for comic in refs:
    # Retrieve the comic info from the references
    title = XKCD.removePunk (refs[comic]['title'])
    alt = XKCD.removePunk (refs[comic]['alt'])
    transcript = XKCD.removePunk \
            (refs[comic]['transcript'])
    # Remove noise from transcript [that's noise]
    # Record the comic in the index
    XKCD.indexComic ('{} {} {}'.format (title, alt, transcript), \
            refs[comic]['number'], index, black_list)

# save file
with open (OUTDEX, 'w') as outfile:
    json.dump (index, outfile, indent = 4)
