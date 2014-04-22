#testClassifier.py
#Author: Henry Tay, Jesse Watts-Russell

#Overview: A test to see if we can classify a player's race
#(Protoss,Terran,Zerg) from frequencies of events over the course of the game
#using a support vector machine

import os
import re
import sc2reader
from gamelog import *
from classifier import eventClassifier
from sc2reader.exceptions import MPQError
from sklearn.preprocessing import StandardScaler
from sklearn.cross_validation import train_test_split
from sklearn.cross_validation import StratifiedKFold
from sklearn.grid_search import GridSearchCV
from sklearn.svm import SVC

mainPath = 'C:\Users\Henry\Documents\HMC Junior\AI\AISC2' 
relayPath = os.path.join(mainPath, 'Replays')

framesPerMinute = 960 #The SC2 engine runs at 16 frames per second
fpr = 16 #Each feature represents the number of events within each 16 frame interval
pattern = r"(?<=\().+?(?=\))" #Matches any string inside parentheses
race = {"Protoss":0, "Terran":1, "Zerg":2} #Race classification dictionary

def abilityID(event):
    """
    Returns the event's ability ID. This function is passed to gamelog to
    classify events accoring to ability ID.
    """
    if hasattr(event, 'ability_id'):
        return u'%i' % event.ability_id
    else:
        return None 

#The classifier we use to assign events to columns
archive = os.path.join(mainPath, 'abilities.txt')
with open(archive, 'r') as infile:
    abilities = json.load(infile)
abilityidClassifier = eventClassifier(abilities, abilityID)
log = gamelog(abilityidClassifier, end=frames, framesPerRow=frames)

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
                #Get data from the first 5 minutes of the replay
                frames = 5*framesPerMinute
                if replay.frames >= frames and len(replay.players) == 2:
                    player1race = re.search(pattern, str(replay.players[0]))
                    player2race = re.search(pattern, str(replay.players[1]))
                    if player1race.group(0) in race and player2race.group(0) in race:
                        targets.append(race[player1race.group(0)])
                        targets.append(race[player2race.group(0)])
                        data.append(gamelog(replay, endFrame=frames, classify=abilityID, framesPerRow=frames).getColumn(0))
                        data.append(gamelog(replay, endFrame=frames, classify=abilityID, framesPerRow=frames).getColumn(1))
            except MPQError:
                print "Failed to load replay %s" % fullpath 
    return (data, targets)
    
#Parse the data and split into train/test sets. Store data. 
data, targets = parseData(replayPath)
print "Saving data. . ."
np.save('X_abilityid', data)
np.save('y_abilityid', targets)
print "Splitting data. . ."
X_train, X_test, y_train, y_test = \
train_test_split(data, targets, test_size = 0.30, random_state = 42)
                   
#Scale the data
print "Scaling data. . ."
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)
  

#Train a classifier
C_range = 10.0 ** np.arange(-2, 2)
gamma_range = 10.0 ** np.arange(-2, 2)
param_grid = dict(gamma=gamma_range, C=C_range)
print "Creating cross-validation sets. . ."
cv = StratifiedKFold(y=y_train, n_folds=3)
grid = GridSearchCV(SVC(), param_grid=param_grid, cv=cv)
"""
print "Fitting classifier. . ."
grid.fit(X_train, y_train)
print "Scoring classifier. . ."
print grid.score(X_test, y_test)
"""