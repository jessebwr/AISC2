#classifier.py 
#Author: Henry Tay

#Overview: A class that classifies events in a StarCraft II replay. 

class eventClassifier:
    
    def __init__(self, classes, classify=lambda x : x.pid):
        """
        """
        print "Initializing a classifier"
        self.classes = classes
        self.classify = classify
        