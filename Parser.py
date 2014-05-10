#ampParser.py
#Author: Henry Tay, Jesse Watts-Russell

#Overview: This is a script to parse the data into .np files. Feature vectors
#are a time series of APM over time. Target values indicate player race.  

import os
import re
import json
from eventParser import eventParser
from gamelog import gamelog
import sc2reader
from sc2reader.exceptions import MPQError
import numpy as np

mainPath = os.path.dirname(os.path.realpath(__file__))
replayPath = os.path.join(mainPath, 'Replays')
testPath = os.path.join(mainPath, 'TestReplays')

#Some global values
framesPerMinute = 960 #The SC2 engine runs at 16 frames per second
fpr = 32 #Each feature represents the number of events within each 16 frame interval
pattern = r"(?<=\().+?(?=\))" #Matches any string inside parentheses
race = {"Protoss":0, "Terran":1, "Zerg":2} #Race classification dictionary
frames = 5*framesPerMinute #Frames in the first five minutes of the game 

def ability_id(event):
    """
    Helper function which returns the pid of an event. Returns -1 if the event
    does not have a pid member.
    """
    if hasattr(event, 'ability_id'):
        return u'%i' % event.ability_id
    else:
        return 0
        
def winner(replay):
    """
    Returns a label for each player in the replay. Returns 1 if the player is
    the winner of the replay and false otherwise. 
    """
    gameWinner = str(replay.winner.players[0])
    isPlayer1Winner = 0
    isPlayer2Winner = 0
    if gameWinner == str(replay.players[0]):
        isPlayer1Winner = 1
    if gameWinner == str(replay.players[1]):
        isPlayer2Winner = 1
    return (isPlayer1Winner, isPlayer2Winner)

#Classify worker and supply build events
with open('workersupply.txt') as infile:
    labels = json.load(infile) 
parser_ws = eventParser(labels, ability_id) 
log_ws = gamelog(parser_ws,2,start=0,end=frames,framesPerRow=fpr)

#Classify micro and macro
with open('micromacro.txt') as infile:
    labels = json.load(infile)
parser_mm = eventParser(labels, ability_id)
log_mm = gamelog(parser_mm,2,start=0,end=frames,framesPerRow=fpr)

#Load and parse the training data
def parseData(path):
    """
    Returns a list of feature vectors and a list of classes for each replay 
    file in the given path. 
    """
    data = []
    targets = []
    for index, filename in enumerate(os.listdir(path)):
        if os.path.splitext(filename)[-1] == '.SC2Replay':
            fullpath = os.path.join(path, filename)
            try:
                replay = sc2reader.load_replay(fullpath)
                print "Loading replay %s" % replay.filename
                log_mm.loadReplay(replay)
                log_ws.loadReplay(replay)
                if len(replay.players) == 2:
                    player1race = re.search(pattern, log_ws.players[0])
                    player2race = re.search(pattern, log_ws.players[1])
                    player1winner, player2winner = winner(replay)
                    if player1race.group(0) in race and player2race.group(0) in race \
                    and not player1winner == None and not player2winner == None:
                        # Micro/macro events
                        events1 = log_mm.actions[0].flatten()
                        events2 = log_mm.actions[1].flatten()
                        events_mm = np.concatenate((events1,events2))
                        # Worker supply events
                        events1 = log_ws.actions[0].flatten()
                        events2 = log_ws.actions[1].flatten()
                        events_ws = np.concatenate((events1,events2))
                        # Races
                        race1,race2 = race[player1race.group(0)],race[player2race.group(0)]
                        races = np.array((race1, race2))
                        features = np.concatenate((events_ws, events_mm, races))
                        data.append(features)
                        targets.append(player1winner)
            except:
                print "Failed to load replay %s" % fullpath 
    return (data, targets)

#Parse and store data 
import time
start_time = time.time()
data, targets = parseData(replayPath)
print "Running time:", time.time() - start_time
print "Saving data. . ."
np.save('X_wl_ws_mm5-32', data)
np.save('y_wl_ws_mm5-32', targets)


