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
fpr = 16 #Each feature represents the number of events within each 16 frame interval
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
        
#Parse the event log
with open('micromacro.txt') as infile:
    labels = json.load(infile) 
#parser = eventParser() #Default uses APM as features
parser = eventParser(labels, ability_id) #Classify micro/macro
log = gamelog(parser,1,start=0,end=frames,framesPerRow=fpr)

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

def race(replay):
    """
    Returns a label for each player in the replay. Returns 0 if the player is
    Protoss, 1 if the player is Terran and 2 if the player is Zerg.
    """
    player1race = re.search(pattern, log.players[0])
    player2race = re.search(pattern, log.players[1])
    if player1race.group(0) in race:
        player1race = race[player1race.group(0)]
    else:
        player1race = None
        
    if player2race.group(0) in race:
        player2race = race[player2race.group(0)]
    else:
        player2race = None
        
    return (player1race, player2race)

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
                log.loadReplay(replay)
                if len(replay.players) == 2:
                    player1class, player2class = winner(replay)
                    #For classifying win/loss
                    if not player1class == None and not player2class == None:
                        targets.append(player1class)
                        events1 = log.actions[0].flatten()
                        events2 = log.actions[1].flatten()
                        data.append(np.concatenate((events1,events2)))
                    """ #Use for classifying race
                    if not player1class == None:
                        targets.append(player1class)
                        data.append(log.actions[0].flatten())
                    if not player2class == None:
                        targets.append(player2class)
                        data.append(log.actions[1].flatten())
                    """
            except:
                print "Failed to load replay %s" % fullpath 
    return (data, targets)

#Parse and store data 
import time
start_time = time.time()
data, targets = parseData(replayPath)
print "Running time:", time.time() - start_time
print "Saving data. . ."
np.save('X_micromacro_wl', data)
np.save('y_micromacro_wl', targets)


