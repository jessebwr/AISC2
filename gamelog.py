#gamelog.py
#Author: Henry Tay

#Overview: A class that stores event sequence data from a StarCraft II 
#replay files as a sparse matrix of integers.

import numpy as np
from __future__ import division
from math import ceil, floor
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
    
    def __init__(self,classifier,replay=None,start=0,end=None,framesPerRow=16):
        """
        Extracts and stores data about the replay into an instance of gamelog.
        The events of the replay file are stored within a matrix. 
        """
        #Crops the event log using the specified frames. This is necessary to 
        #use the event matrix as a feature vector for classification.
        self.start = start
        
        if end: #Use the provided argument
            self.end = end
        elif not replay: #The log was initialized with no replay. Start = End.
            assert start == 0
            end = 0
        else: #Use the whole replay 
            self.end = replay.frames
            
        #The classifier sorts events into columns of the matrix
        self.classifier = classifier
           
        self.fpr = framesPerRow
        self.initializeMatrix()
        
        if self.replay:
            self.loadReplay(replay)
            
    def initializeMatrix(self):
        """
        Sets the event matrix to a matrix of zeroes.
        """
        self.rows = ceil((self.end - self.start)/self.fpr)
        self.columns = len(self.classifier.labels)
        
        shape = (self.rows, self.columns)
        self.matrix = np.zeros(shape)  
        
        
    def loadReplay(self,replay,start=None,end=None):
        """
        Populates the event matrix with data from the replay's event log.
        The default is to not change the shape of the event matrix. 
        """
        #Use provided arguments to change the shape of the event matrix
        if start:
            self.start = start
        if end:
            self.end = end
            
        #No replay was previously loaded and the end was not specified.
        #Set the end to the last frame of the replay. This assumes that the
        #user will never want to have a gamelog object that has a replay and
        #an empty event matrix. It would be preferable to use enumerations to
        #have a special value to indicate that a gamelog's matrix should be
        #empty even if the log has a replay.
        if self.end == 0:
            self.end = replay.frames
        
        self.initializeMatrix()
        
        for event in replay.events:
            #Ignore events that aren't assigned any index 
            if self.classifier.eventIndex(event):
                row = floor(event.frame/self.fpr)
                col = self.classifier.eventIndex(event)
                self.matrix[row,col] += 1 
                    
    def toVector(self):
        """
        Reshapes the event matrix and returns it as a one dimensional feature
        vector. 
        """
        return np.reshape(self.matrix, self.rows*self.columns)
        
    def getColumn(self,column):
        """
        Returns a column of the event matrix as a one dimnesional vector.
        """
        return self.matrix[:,column]
                
    def __getitem__(self,(row,col)):
        """
        Returns the event count at the specified index. The column corresponds
        to the classification of the event and the row corresponds to the time
        that the event took place. 
        """
        return self.matrix[row,col]
        
    def __repr__(self):
        """
        Prints the event matrix. 
        """
        matrix = self.matrix.tolist()
        result = ""
        for row in matrix:
            result += "    ".join(str(i) for i in row)
            result += '\n'
        return result