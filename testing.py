#Test version of translator Pi software
#goal = design basic control structure sans screen controls/interfacing
#run as just a command-line interface
import xmltodict
import csv
import pandas as pd
import datetime
from pynput import keyboard

def parse(xml='es-en.xml'):
    #parse xml to dict with format dict['spanish word'] = (english definition, part of speech)
    with open(xml) as fd:
        doc = xmltodict.parse(fd.read())
    raw = doc['dic']['l']
    dict = {}
    for i in range(len(raw)):
        for j in range(len(raw[i]['w'])):
            dict[raw[i]['w'][j]['c']] = (raw[i]['w'][j]['d'],raw[i]['w'][j]['t'])
    return dict

dict = parse()

def dictionaryloop():
    query = input()
    while query != '.':
        try:
            print('def:' + dict[query][0] + '\n' + dict[query][1])
            add = input('Add to Journal?')
            if add == '':
                addtojournal(query)
        except KeyError:
            print(query + ' not found.')
        query = input()

def addtojournal(query):
    with open('journal.csv','a') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([query,dict[query][0] + ',' + dict[query][1], '0',datetime.datetime.now()])

def sortjournal(mode):
    journal = pd.read_csv('journal.csv')
    if mode == 0: #old->new
        journal['created'] = pd.to_datetime(journal['created'])
        journal = journal.sort_values(by='created')
    elif mode == 1: #new->old
        journal['created'] = pd.to_datetime(journal['created'])
        journal = journal.sort_values(by='created',ascending=False)
    elif mode == 2: #low -> high score
        journal = journal.sort_values(by='score')
    elif mode == 3: #random
        journal = journal.sample(frac=1)
    else:
        raise TypeError('Invalid Mode; use 0,1,2, or 3')
    print(journal)

def on_press(key):
    try:
        print('alphanumeric key {0} pressed'.format(
            key.char))
    except AttributeError:
        print('special key {0} pressed'.format(
            key))

def on_release(key):
    if key == keyboard.Key.esc:
        # Stop listener
        return False

def main():
    #dictionaryloop()
    sortjournal(mode=3)
    listener= keyboard.Listener(on_press = on_press,
                                on_release = on_release)
    listener.start()
    while True:
        pass

main()
