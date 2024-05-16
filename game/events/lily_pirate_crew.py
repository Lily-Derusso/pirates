import game.event as event
import random
import game.combat as combat
import game.superclasses as superclasses
from game.display import announce
from game.combat import Monster



class Lily_prate_crew (event.Event):
    '''
    A combat encounter with a crew of pirates on the location lily_island.
    When the event is drawn, creates a combat encounter with 2 to 6 pirates, kicks control over to the combat code to resolve the fight, then adds itself and a simple success message to the result
    '''

    def __init__ (self):
        self.name = "Pirate"

    def process (self, world):
        '''Process the event. Populates a combat with pirates. The first pirate may be modified into a "Pirate captain" by buffing its speed and health.'''
        result = {}

        won = "the Pirate crew is defeated! The Treasure is yours!"
        victory = "\nAs the final thief falls by your hand, you look around to see what was worth this bloodshed."
        items = "\nIn the room are 3 chests overflowing with gold."
        thought = '\nYou wonder "How had a church gotten so much gold to begin with?"'

        result["message"] = won + victory + items + thought
        monsters = []
        min = 2
        uplim = 6
        if 1 == 1:
            min = 4
            uplim = 6
            monsters.append(combat.Drowned("Pirate captain"))
            monsters[0].speed = 1.2*monsters[0].speed
            monsters[0].health = 3*monsters[0].health
        n_appearing = random.randrange(min, uplim)
        n = 1
        while n <= n_appearing:
            monsters.append(Lily_prate_crew.Pirates("Pirate "+str(n)))
            n += 1
        announce ("You are attacked by a crew of pirates!")
        combat.Combat(monsters).combat()
        result["newevents"] = [ self ]
        return result

    class Pirates(Monster):
        def __init__ (self, name):
            attacks = {}
            attacks["slash"] = ["slashes",random.randrange(35,51), (5,15)]
            attacks["shoot"] = ["shoots",random.randrange(35,51), (1,10)]
            attacks["punch"] = ["punches",random.randrange(35,51), (1,10)]
            #7 to 19 hp, bite attack, 65 to 85 speed (100 is "normal")
            super().__init__(name, random.randrange(7,20), attacks, 75 + random.randrange(-10,11))