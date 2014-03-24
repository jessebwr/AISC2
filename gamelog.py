#gamelog.py
#Author: Henry Tay

#Overview: A class that stores event sequence data from a StarCraft II 
#replay files as a sparse matrix of integers.

import numpy as np

class gamelog:
    """
    Stores the event sequence data of a StarCraft II replay as a matrix
    of integer values. 
    
    The index of a row represents a frame or a block of frames in the game and 
    the index of a column represents a unique action or a group of actions. The 
    value at an index (i,j) represents the number of times an action from group 
    j was executed during the time frame i.  
    """
    
    def __init__(self, replay, classify=lambda x : x.pid, startFrame = 0, endFrame = None, framesPerRow=16):
        """
        Extracts and stores data about the replay into an instance of gamelog.
        The events of the replay file are stored within a matrix. 
        """
        #Crops the event log using the specified frames.
        #This is necessary to use the event log data as a feature vector for 
        #classification.
        self.start = startFrame
        if endFrame:
            self.end = endFrame
        else:
            self.end = replay.frames
           
        #The dimensions of the event matrix. fpr is how many frames are 
        #represented in each row. 
        self.fpr = framesPerRow
        self.players = len(replay.players)
        self.rows = (self.end - self.start)/self.fpr + 1
        self.columns = self.players
        self.shape = (self.rows, self.columns)
        
        #Populate the matrix with data from the replay's event log. 
        self.matrix = np.zeros(self.shape)  
        for event in replay.events:
            if hasattr(event, "pid") and event.pid < self.players \
            and event.frame < self.end and event.frame >= self.start:
                row = event.frame/self.fpr
                col = classify(event)
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
                
    def __getitem__(self, (row, col)):
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