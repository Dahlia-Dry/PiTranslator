#Test version of translator Pi software
#goal = design basic control structure sans screen controls/interfacing
#run as just a command-line interface
import xmltodict
import csv

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
        writer.writerow([query,dict[query][0] + ',' + dict[query][1]])

def readjournal():
    with open('journal.csv') as csvfile:
        reader = csv.reader(csvfile)
        journal = dict(reader)

def filterdict(callback):
    newDict = {}
    for (key,value) in dict.items():
        if callback((key,value)):
            newDict[key]= value
    return newDict

def checkconjugated(query, restrict=-1):
    try:
        possibilities = filterdict(lambda x : 'v' in x[1][1][1])[query[:len(query)-1]]
    except KeyError:
        checkconjugated(query, restrict=restrict-1)
    print(possibilities)

def main():
    #dictionaryloop()
    checkconjugated(input())

main()
