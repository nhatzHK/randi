import xkcd_helpers as xkcd

import urllib.error
from urllib.request import urlopen
import json

edited = False

# adding path
with open('../client/xkcd.path.json.priv') as path_file:
    PATH = json.load(path_file)

# opening file to read
with open(PATH['json'] + "xkcd.references.json") as json_data:
    xkcd_data = json.load(json_data)

# checking last comic and current comic
last_comic = max(map(lambda x: int(x), xkcd_data.keys()))
with urllib.request.urlopen('https://xkcd.com/info.0.json') as url:
    current_comic = json.loads(url.read().decode('utf-8'))['num']

comics = {}

def set_transcript_completition(comic, tr):
    transcript = tr['tr']
    status = {'status':tr['status'], 'error':tr['error'], 'complete':tr['complete']}

    # set comic transcript
    comic['comic']['transcript'] = transcript

    # set status
    comic['stat_tr'] = status
    comic['stat_com'] = {'status':comic['status'], 'error':comic['error']}

    # removing the duplicate comic status and error key
    comic.pop('status', None)
    comic.pop('error', None)


def updatePastComics():
    global comics, edited

    ''' Look through the references and check if any of the status are incomplete
        update if they are
    '''

    for key in xkcd_data.keys():
        trans_stat = xkcd_data[key]['stat_tr']['status']
        comp_stat = xkcd_data[key]['stat_com']['status']
        if key != '404':
            if trans_stat != 0 or comp_stat != 0:
                key = int(key)
                c = xkcd.get_xkcd(key)
                transcript = xkcd.get_transcript(key)
                set_transcript_completition(c, transcript)

                comics[key] = c
                edited = True

def addNewComics():
    global last_comic, comics, edited

    # add each comic from the last one in the database to the current
    while last_comic < current_comic:
        last_comic += 1

        c = xkcd.get_xkcd(last_comic)
        transcript = xkcd.get_transcript(last_comic)

        set_transcript_completition(c,transcript)

        comics[str(last_comic)] = c
        edited = True


def update_ref():
    # updating past comics and adding new ones
    updatePastComics()
    addNewComics()

    # if database has been edited, then update the database
    if edited:
        xkcd_data.update(comics)

        with open(PATH['json'] + "xkcd.references.json", "w") as json_data:
            json.dump(xkcd_data, json_data, indent=4)