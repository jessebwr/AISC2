#classifier.py 
#Author: Henry Tay

#Overview: A class that classifies events in a StarCraft II replay. 

class eventClassifier:
    """
    Classifies the events in a replay file. Assigns each event to an event 
    index - a non-negative integer value used to sort the event into a column
    in an event matrix. 
    
    Keyword arguments:
        
    classify -- a function that accepts an event and returns an event label.
        This label is not necessarily the event index used to assign an event 
        to some column in an event matrix, but is unique to each class.
        
    labels -- a dictionary of event labels returned by classify. If classify
        returns a label that is not in this dictionary, the label is simply
        added to the dictionary with a value corresponding to the event index.
        The values of each label should provide some descriptive information
        about that event. 
    """
    
    def __init__(self, labels={}, classify=lambda x : x.pid):
        self.labels = labels
        self.classify = classify
        self.indices = {}
        
    def eventIndex(self, event):
        """
        Assigns an index to each event according to some classification scheme.
        """
        label = self.classify(event)
        
        #Label already encountered. Return the index assigned to it. 
        if label in self.indices:
            return self.indices[label]
            
        #Label not recognized. Ignore the event. 
        elif label not in self.labels:
            return None
            
        #Label recognized but not yet encounterd. Give it an index. 
        else:
            index = len(self.indices)
            self.indices[label] = index
        
        return index
        
    def eventLabel(self, event):
        """
        Returns a label for the event. The label should provide some 
        descriptive information about the event.
        """
        label = self.classify(event)
        
        #No event label available. Return the event's repr.
        if label == None:
            return 'No label available for event: %s' % str(event)
        return self.labels[label]