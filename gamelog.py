#gamelog.py
#Author: Henry Tay

#Overview: A class that stores event sequence data from a StarCraft II 
#replay files as a sparse matrix of integers.

from __future__ import division

import numpy as np
from math import ceil, floor

class gamelog:
    """
    Stores the event sequence data of a StarCraft II replay as a matrix
    of integer values. 
    
    The index of a row represents a frame or a block of frames in the game and 
    the index of a column represents a unique action or a group of actions. The 
    value at an index (i,j) represents the number of times an action from group 
    j was executed during the time frame i.  
    
    A StarCraft II replay contains the following data:
        Initial state
        Input events
        Output events
        
    Input events encode the actions of the players in the game and come in two
    flavors: 
        Game events: these actually affect the state of the game. These events
            are used by the StarCraft II engine to reconstruct a game from a 
            replay file
        Message events: records messages and pings sent to other players. This
            class ignores these events since we won't be using them for
            classification tasks
        
    Output events (tracker events) periodically provide game state information.
    They record important non-player events that happen in game and provide
    snapshots of the game state at regular intervals of time. These are
    unneccesary for reconstructing gamestate but may provide useful features
    for classification. 
    
    This gamelog class should parse the data in the replay file so that the 
    game events are stored separately from the tracker events and the events
    for each player are stored separately. This allows for easy access. 
    """
    
    def __init__(self,classifier,columns,replay=None,start=0,end=None,framesPerRow=16):
        """
        Extracts and stores data about the replay into an instance of gamelog.
        The events of the replay file are stored within a matrix. 
        """
        #Crops the event log at provided start and end frames. 
        #This is necessary to use the event matrix as a feature vector for 
        #classification.
        
        self.start = start
        if end: #Use the provided argument
            self.end = end
        elif not replay == None: #Use the whole replay 
            self.end = replay.frames
        else: #No replay, use start = end = 0
            self.end = 0
            
        self.fpr = framesPerRow
            
        self.rows = ceil((self.end - self.start)/self.fpr)
        self.columns = columns
            
        #The classifier sorts events into columns of the matrix
        self.classifier = classifier
               
        if not replay == None:
            self.loadReplay(replay)
            
    def initializeMatrix(self):
        """
        Returns an event matrix with the correct shape 
        """
        shape = (self.rows, self.columns)
        return np.zeros(shape)  
        
    def loadReplay(self,replay,start=None,end=None):
        """
        Populates the event matrix with data from the replay's event log.
        The default is to not change the shape of the event matrix. 
        """
        #Change where to crop 
        if start:
            self.start = start
        if end:
            self.end = end
        
        self.rows = ceil((self.end - self.start)/self.fpr)
            
        #Find the names of the players and store them in a list
        self.players = [str(player) for player in replay.players]
        
        self.actions = [] #Game events for each player
        self.trackers = [] #Tracker events for each player
        
        #Initialize event matrix for each player and for tracker/action events
        for i in range(len(self.players)):
            self.actions.append(self.initializeMatrix())
            self.trackers.append(self.initializeMatrix())
            
        #For events that don't correspond to any one player
        self.trackers.append(self.initializeMatrix())
        
        self.counted = [] #String repr for each event counted
        self.ignored = [] #String repr for each event ignored
        
        for event in replay.game_events:
            if event.pid < len(self.players):
                events = self.actions[event.pid] # The event matrix for that player
                shape = events.shape #The shape of the matrix
                row = floor(event.frame/self.fpr)
                col = self.classifier.eventIndex(event)
                if not col == None and row < shape[0] and col < shape[1]:
                    events[row,col] += 1
                    self.counted.append(str(event))
                else: self.ignored.append(str(event))
            else:
                self.ignored.append(str(event))
                
        for event in replay.tracker_events:
            #Not yet implemented!
            #Unlike game events tracker events are not always associated with a player. 
            self.ignored.append(str(event))