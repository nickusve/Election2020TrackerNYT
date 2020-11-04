import requests
# For testing
#import json
from copy import deepcopy
from time import sleep
from datetime import datetime


def getUpdate():
    return requests.get('https://static01.nyt.com/elections-assets/2020/data/api/2020-11-03/votes-remaining-page/national/president.json').json()


def getNytUpdate():
    return parseUpdate(getUpdate())


def parseUpdate(toParse):
    parsed = {}
    for state in toParse["data"]["races"]:
        parsed[state["state_name"]] = {
            "name": state["state_name"],
            "lastUpdate": state["last_updated"],
            "votes": state["votes"],
            "votePercent": state["eevp"],
            "candidates": {}
        }
        for candidate in state["candidates"]:
            parsed[state["state_name"]]["candidates"][candidate["candidate_id"]] = {
                "name": candidate["last_name"],
                "votes": candidate["votes"],
                "percent": candidate["percent"]
            }

    return parsed


bidenId = "biden-1036"
trumpId = "trump-8639"
# For testing
# local = open("president.json")
# oldData = parseUpdate(json.load(local))
# local.close()
oldData = getNytUpdate()


trumpStr = "Trump: {:09,d} -> {:09,d} ({:+09,d}) | {:.2f}% -> {:.2f}% ({:+.2f}%)"
bidenStr = "Biden: {:09,d} -> {:09,d} ({:+09,d}) | {:.2f}% -> {:.2f}% ({:+.2f}%)"
stateStr = "State: {:09,d} -> {:09,d} ({:+09,d}) | {:.2f}% -> {:.2f}% ({:+.2f}%)"
deltaStr = "Biden delta   : Votes -> {:+09,d} Percent -> {:+.2f}%"
bidenDiffStr = "Biden Vs Trump: Votes -> {:+09,d} Percent -> {:+.2f}%\n"

while True:
    newData = getNytUpdate()

    print(datetime.now())

    for state in sorted(newData):
        if oldData[state]["votes"] != newData[state]["votes"]:
            trumpOld = oldData[state]["candidates"][trumpId]["votes"]
            trumpNew = newData[state]["candidates"][trumpId]["votes"]
            trumpDelta = trumpNew - trumpOld
            trumpOldPer = oldData[state]["candidates"][trumpId]["percent"]
            trumpNewPer = newData[state]["candidates"][trumpId]["percent"]
            trumpPerDelta = trumpNewPer - trumpOldPer
            bidenOld = oldData[state]["candidates"][bidenId]["votes"]
            bidenNew = newData[state]["candidates"][bidenId]["votes"]
            bidenDelta = bidenNew - bidenOld
            bidenOldPer = oldData[state]["candidates"][bidenId]["percent"]
            bidenNewPer = newData[state]["candidates"][bidenId]["percent"]
            bidenPerDelta = bidenNewPer - bidenOldPer
            print("{}:".format(state))
            print(trumpStr.format(trumpOld, trumpNew, trumpDelta, trumpOldPer, trumpNewPer, trumpPerDelta))
            print(bidenStr.format(bidenOld, bidenNew, bidenDelta, bidenOldPer, bidenNewPer, bidenPerDelta))
            print(stateStr.format(oldData[state]["votes"], newData[state]["votes"],
                                  newData[state]["votes"] - oldData[state]["votes"],
                                  oldData[state]["votePercent"], newData[state]["votePercent"],
                                  newData[state]["votePercent"] - oldData[state]["votePercent"]))
            print(deltaStr.format(bidenDelta - trumpDelta, bidenPerDelta - trumpPerDelta))
            print(bidenDiffStr.format(bidenNew - trumpNew, bidenNewPer - trumpNewPer))

    oldData = deepcopy(newData)
    sleep(10)
