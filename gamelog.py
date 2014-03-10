#gamelog.py
#Author: Henry Tay

#Overview: A class that stores event sequence data from a StarCraft II 
#replay files as a sparse matrix of integers.

import sc2reader
from scipy import sparse
from classifier import *

class gamelog:
    """
    Stores the event sequence data of a StarCraft II replay as a matrix
    of integer values. 
    
    The index of a row represents a frame or a block of frames in the game and 
    the index of a column represents a unique action or a group of actions. The 
    value at an index (i,j) represents the number of times an action from group 
    j was executed during the time frame i.  
    """
    def __init__(self, replay, classify=lambda x : x.pid, framesPerRow=60):
        """
        """
        self.frames = replay.frames
        self.fps = replay.game_fps
        self.fpr = framesPerRow
        self.players = len(replay.players)
                
        self.rows = self.frames/framesPerRow + 1
        #Fix later. There are actions that are taken by a third player w/ pid 2
        self.columns = self.players + 1
        
        #The dok (dictionary of keys) implementation of a sparse matrix
        #allows for O(1) element access
        self.matrix = sparse.dok_matrix((self.rows, self.columns))  
        for event in replay.events:
            if hasattr(event, "pid"):
                row = event.frame/framesPerRow
                col = classify(event)
                self.matrix[row,col] += 1 
                
    def getCount(self, row, col):
        """
        """
        return self.matrix[row,col]
        
    def __repr__(self):
        """
        """
        matrix = self.matrix.toarray().tolist()
        result = ""
        for row in matrix:
            result += "    ".join(str(i) for i in row)
            result += '\n'
        return result