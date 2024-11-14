import os
import json


# Dictionary of participant IDs to All audio files for that participant
def audiofiles(directory = 'bids_with_sensitive_recordings'):
    files = dict()
    for sub in os.listdir(directory):
        if sub[0:3] == 'sub':
            wavs = []
            i = os.path.join(directory, sub)
            for ses in os.listdir(i):
                if ses[0:3] == 'ses':
                    x = os.path.join(i, ses)
                    for aud in os.listdir(x):
                        if aud == 'audio':
                            y = os.path.join(x, aud)
                            for wav in os.listdir(y):
                                if wav[-3:-1] == 'wa':
                                    t = os.path.join(y, wav)
                                    wavs.append(t)
            files[i] = wavs
    return files

'''
getInfo takes a subject and returns the answer to the prompt if linkID is in participant or Confounder 
survey [more surveys can easily be added]. If it returns None, then prompt wasnt found in either survey
'''
def getInfo(sub, prompt):
    par = getPartSurv(sub)
    a = pullAns(par, prompt)
    if a != None:
        return a
    con = getConSurv(sub)
    b = pullAns(con, prompt)
    if b != None:
        return b
    return None

#returns the value of the json [used as heper func in getInfo]
def pullAns(file, target):
    if file == None:
        return None
    with open(file, 'r') as f:
        data = json.load(f)
    value = None
    for item in data.get('item', []):
        if item.get('linkId') == target:
            answer = item.get('answer', [{}])[0]
            if 'valueBoolean' in answer:
                value = answer['valueBoolean']
            elif 'valueString' in answer:
                value = answer['valueString']
            break

    return value  

#returns the particpant survey of the subject [used as heper func in getInfo]
def getPartSurv(sub):
    for surv in os.listdir(sub):
        if surv[-9:-5] == "pant":
            return os.path.join(sub, surv)

#returns the confounder survey of the subject [used as heper func in getInfo]
def getConSurv(sub):
    for ses in os.listdir(sub):
        if ses[0:3] == 'ses':
            x = os.path.join(sub, ses)
            for beh in os.listdir(x):
                if beh == 'beh':
                    y = os.path.join(x, beh)
                    for f in os.listdir(y):
                        if f[-30:-5] == 'qgenericconfoundersschema':
                            t = os.path.join(y, f)
                            return t
