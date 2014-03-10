#prettyPrinter.py
#Author: Henry Tay
#Adapted from sc2reader tutorial at 
#   http://sc2reader.readthedocs.org/en/latest/tutorials/prettyprinter.html

#Overview: Playing around to figure out what kind of data is inside an .sc2replay file
#   Lots of useful tricks using formatted strings 

import sc2reader
import sys
import json
from sc2reader.factories import SC2Factory



def main():
    paths = sys.argv[1:]

    #You can create a factory with a custom configuration
    sc2 = SC2Factory(
            directory='C:\Users\Henry\Documents\HMC Junior\AI\AISC2',
            exclude=['Customs','Pros'],
            followlinks=True
        )
    sc2.configure(depth=1)
        
    #Or configure the default factory: 
    sc2reader.configure(
        directory='C:\Users\Henry\Documents\HMC Junior\AI\AISC2',
        exclude=['Customs','Pros'],
        depth=1, #Max recursion depth
        followlinks=True #Recurse on subdirectories
    )

    replay = sc2reader.load_replay(paths[0]) 

    #Print out all event types and and example of their attributes
    print json.dumps(getEventTypes(replay, "game"), indent = 2)

    #Print out the attributes contained in the sc2reader class
    #printFormattedList(getAttributesWithValues(replay, True))

    #Print out the abilities used in the replay
    print json.dumps(getAbilityIDs(replay), indent = 2)

    #Print out command events in the replay in chronological order
    print printFormattedList(getCommandEvents(replay))

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

def getAbilityIDs(replay):
    '''Returns a dictionary of ability IDs mapped to ability names'''
    abilities = {}
    for event in replay.events:
        if hasattr(event, 'ability') and event.ability_id not in abilities:
            abilities[event.ability_id] = event.ability_name
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
