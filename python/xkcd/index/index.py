import json
import xkcd_helpers # It's in ../fetch/ go get it yourself
import wame_helpers # It's in ../wame/ ditto

REFS = 'path/to/xkcd_references.json'
INDEX = 'path/to/xkcd_index.json'
B_LIST = 'path/to/common.json'

index = dict ()
refs = wame_helpers.loadJson (REFS)
black_list = list (set ( wame_helpers.loadJson (B_LIST)['common']))

for comic in refs:
    # Retrieve the comic info from the references
    title = xkcd_helpers.removePunk (refs[comic]['title'])
    alt = xkcd_helpers.removePunk (refs[comic]['alt'])
    transcript = xkcd_helpers.removePunk (refs[comic]['transcript'])
    # Record the comic in the index
    xkcd_helpers.indexComic ('{} {} {}'.format (title, alt, transcript), \
            refs[comic]['number'], index, black_list)

# save file
with open (INDEX, 'w') as outfile:
    json.dump (index, outfile, indent = 4)
