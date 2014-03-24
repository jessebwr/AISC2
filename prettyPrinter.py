#prettyPrinter.py
#Author: Henry Tay
#Adapted from sc2reader tutorial at 
#   http://sc2reader.readthedocs.org/en/latest/tutorials/prettyprinter.html

#Overview: Playing around to figure out what kind of data is inside an .sc2replay file
#   Lots of useful tricks using formatted strings 

import sc2reader
import sys
import json
import os.path
from os import rename
from sc2reader.factories import SC2Factory
from sc2reader.exceptions import MPQError, CorruptTrackerFileError
from datetime import datetime

mainpath = 'C:\Users\Henry\Documents\HMC Junior\AI\AISC2'
replaypath = 'C:\Users\Henry\Documents\HMC Junior\AI\AISC2\Replays'

def main():
    paths = sys.argv[1:]

    #You can create a factory with a custom configuration
    sc2 = SC2Factory(
            directory=replaypath,
            exclude=['Customs','Pros'],
            followlinks=True
        )
    sc2.configure(depth=1)
        
    #Or configure the default factory: 
    sc2reader.configure(
        directory=mainpath,
        exclude=['Customs','Pros'],
        depth=1, #Max recursion depth
        followlinks=True #Recurse on subdirectories
    )

    replay = sc2reader.load_replay('derp.SC2Replay')
    #replays = sc2reader.load_replays()
    #replays = sc2reader.load_replays(replaypath)
    
    #Print out all event types and and example of their attributes
    #print json.dumps(getEventTypes(replay, "game"), indent = 2)

    #Print out the attributes contained in the sc2reader class
    printFormattedList(getAttributesWithValues(replay, True))

    #Print out the abilities used in the replay
    #print json.dumps(getAbilityIDs(replay), indent = 2)

    #Print out command events in the replay in chronological order
    #print printFormattedList(getCommandEvents(replay))
    
    #Add new ability IDs to the json archive
    #archiveAbilityIDs('abilities.txt')
    
    #Classify ability IDs as micro or macro
    #classifyMicroMacro('abilities.txt', 'micromacro.txt')
    
def classifyMicroMacro(archiveFile, outfile, path=replaypath):
    '''
    Classifies abilities within an archive as "Micro" or "Macro" or neither.
    
    Prompts the user to give a classification to each ability in the archive.
    '''
    
    fullpath = os.path.join(path, archiveFile)
    outpath = os.path.join(path, outfile)
    
    #Read in abilities from json file
    with open(fullpath, 'r') as infile: 
        archive = json.load(infile)
    infile.close()
    
    #Read in existing classifications from outfile if it exists
    try:
        with open(outpath, 'r') as infile:
            classifications = json.load(infile)
        infile.close()
    except IOError:
        classifications = {}
    
    #Prompt the user to classify each ability
    for ID in archive.keys():
        if ID not in classifications:
            classification = ""
            prompt = "Please classify (micro/macro): %s. Type \"stop\" to quit. \n" % archive[ID]
            classification = raw_input(prompt)
            if classification in ["micro", "macro", "none"]:
                classifications[ID] = classification
            elif classification == "stop":
                break
            else:
                print "Invalid input. Skipping to next ability."
      
    #Write the result into the specified outfile  
    with open(outpath, 'w') as outfile:
        print "Writing data to %s" % outfile
        json.dump(classifications, outfile)
        
    return
    
def archiveAbilityIDs(filename, replay=None, path=replaypath):
    '''
    Stores the abilities used in a replay to a json text file.
    
    If no replay is specified, loop through all of the files in the directory. 
    '''
    #Keep track of execution time
    startime = datetime.now()
        
    filepath = os.path.join(path, filename)
    newIDFound = False
    
    #Read in existing IDs from the archive file into a dictionary
    try:
        with open(filename, 'r') as infile:
            archive = json.load(infile)
        infile.close()
    except (ValueError, IOError):
        archive = {}
        open(filename, 'w')
        
    #Update dictionary of IDs with IDs from replay(s)
    if replay != None:
        getAbilityIDs(replay, archive)
    else:
        #Keep track of the files that fail to load
        failed = []
        
        for filename in os.listdir(os.path.join('.',path)):
            #Update the archive with abilities from each replay in the directory
            if os.path.splitext(filename)[-1] == '.SC2Replay':
                fullpath = os.path.join(path, filename)
                try:
                    replay = sc2reader.load_replay(fullpath)
                    print "Loading replay %s" % replay.filename
                    getAbilityIDs(replay, archive)
                except:
                    print "Failed to load replay %s" % fullpath 
                    failed.append(filename)
                
    #Write ability IDs to archive file
    print "Printing new IDs"
    with open(filepath, 'w') as outfile:
        json.dump(archive, outfile)
        outfile.close()
        
    print "Function ran in time : %s" % (datetime.now() - startime)
    printFormattedList(failed)
    

def getAttributes(object, includeUnderscores=False):
    '''Returns a list of the object's attributes and methods.
    By default does not return attributes with leading underscores'''
    if includeUnderscores:
        return dir(object)
    else:
        return filter(lambda x : x[0] != '_', dir(object))

def formatAttribute(attribute, Object, abridged=False):
    '''Helper function which returns a string of the specified attribute and its value'''
    value = unicode(getattr(Object, attribute))
    if abridged and len(value) > 100:
        value = value[:100]
    return attribute + u': ' + value

def getAttributesWithValues(Object, abridged=False, includeUnderscores=False):
    '''Returns a list of the object's attributes and their values
    By default does not return attributes or methods with leading underscores'''
    return map(lambda x : formatAttribute(x, Object, abridged),
                 getAttributes(Object,includeUnderscores))

def printFormattedList(List):
    print u"[\n\t{}\n]".format(',\n\t'.join(unicode(x) for x in List))

def getEventTypes(replay, type=None):
    '''
    Find the event types in the replay and list their attributes.
    There are three main types of events: tracker, message, and game events.
    '''
    eventTypes = {}

    #It would better to use an enumeration, but this version of Python does not support enums
    if type == "tracker":
        events = replay.tracker_events
    elif type == "message":
        events = replay.message_events
    elif type == "game":
        events = replay.game_events
    else:
        events = replay.events

    for event in events:
        if event.name not in eventTypes:
            attributes = filter(lambda x: x[0] != '_', dir(event))
            eventTypes[event.name] = map(lambda x: x + ': ' + str(getattr(event,x)), attributes)
    return eventTypes

def getAbilityIDs(replay, abilities={}):
    '''Returns a dictionary of ability IDs mapped to ability names'''
    for event in replay.events:
        if hasattr(event, 'ability') and event.ability_id not in abilities:
            #Keys are unicode encoded when read from a json file.
            abilities[unicode(event.ability_id)] = event.ability_name
    return abilities

def getCommandEvents(replay):
    '''Returns a list of command events in chronological order'''
    fps = replay.game_fps
    events = []
    for event in replay.game_events:

        '''
        Game events have ability attributes or name attributes.
        Only two game events have both: TargetUnitCommand and TargetPointCommand.
        Since the ability_name of these events is both "CAbil" we prefer to print the 
        name over the ability_name. 
        '''
        eventName = ""
        if hasattr(event, 'ability') and not event.ability_name == 'CAbil':
            eventName = event.ability_name
        else: 
            eventName = event.name

        if not eventName == "":
            eventString = ''
            if event.pid == 0:
                eventString = "{0}-{1}-{2} : {3}".format(event.second/60, event.second % 60, 
                    int(event.frame % fps), eventName)
            elif event.pid == 1:
                #Kind of hacky, but suffices to enhance visualization of command event sequence
                eventString = "{0}-{1}-{2} :\t\t\t\t\t\t\t\t\t\t\t{3}".format(event.second/60, 
                    event.second % 60, int(event.frame % fps), eventName)
            else:
                print "Third player!"

            events.append(eventString)
    return events

def formatReplay(replay):
    return u"""

{filename}
--------------------------------------------
SC2 Version {release_string}
{category} Game, {start_time}
{type} on {map_name}
Length: {game_length}

""".format(**replay.__dict__)

def formatTeams(replay):
    teams = list()
    for team in replay.teams:
        players = list()
        for player in team:
            players.append(u"({0}) {1}".format(player.pick_race[0], player.name))
        formattedPlayers = '\n         '.join(players)
        teams.append(u"Team {0}:  {1}".format(team.number, formattedPlayers))
    return '\n\n'.join(teams)

if __name__ == '__main__':
    main()
