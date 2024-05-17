from game import location
import game.config as config
from game.display import announce
from game.events import *
from game.items import Item
import game.items
from game.events import lily_pirate_crew
from game.events.lily_pirate_crew import Lily_prate_crew
from game.combat import *

class Lily_island (location.Location):

    def __init__ (self, x, y, w):
        '''init island with 2 puzzle rooms and an optional encounter'''
        super().__init__(x, y, w)
        self.name = "island"
        self.symbol = 'I'
        self.visitable = True
        self.starting_location = Arival_beach(self)
        self.locations = {}
        self.locations["beach"] = self.starting_location
        self.locations["church"] = Church(self)
        self.locations["church_inside"] = Church_inside(self)
        self.locations['basement'] = Church_basement(self)
        self.locations['sub_basement'] = Sub_basement(self)
        self.locations['sub_basement_north'] = Sub_basement_north(self)
        self.locations['sub_basement_east'] = Sub_basement_east(self)
        self.locations['sub_basement_south'] = Sub_basement_south(self)
        #self.locations['thief_ship'] = Thief_ship(self)

        #island variables
        self.gold = False
        self.light = False
        self.puzzleN_done = False
        self.puzzleE_done = False
        self.treasure_taken = False
        self.daimonds_taken = False
        self.thieves_beat = False
        self.flead = False
        self.map = False
        self.gold_taken = False

        #island items
        self.gold = Gold()   
        self.daimond_eyes = Diamonds()     
        self.treasure = Treasure()    
          

    def enter (self, ship):
        print ("arrived at an island")

    def visit (self):
        config.the_player.location = self.starting_location
        config.the_player.location.enter()
        super().visit()

class Arival_beach(location.SubLocation):
    def __init__(self, m):
        '''init beach'''
        super().__init__(m)
        self.name = 'beach'
        self.verbs['north'] = self
        self.verbs['south'] = self
        self.verbs['east'] = self
        self.verbs['west'] = self
        self.verbs['go on the ship'] = self
        self.verbs['go on other ship'] = self
        self.verbs['explore ship'] = self
        self.verbs['explore the ship'] = self
        self.verbs['go on ship'] = self
        self.verbs['explore'] = self

    def enter(self):
        discription = "\nYou arrive at the beach.\n"
        if self.main_location.flead == False and self.main_location.treasure_taken == False:
            discription += "\nYour ship is anchored next to another pirate ship at the west side of the island."
            discription += "\nYou can't see a way to go on the ship but you hear angry shouts about hidden treasure."
        if self.main_location.flead == True:
            discription += "\nThe ship that was anchored next to yours has left with the treasure."
        if self.main_location.flead == False and self.main_location.treasure_taken == True:
            discription += "\nYour ship is anchored next to another pirate ship at the west side of the island."
            discription += "\nThe ship next to yours appears empty now."
            #discription += "\nThe ship next to yours now has the gangplank down. You can now 'go explore' the ship."        
        discription += "\nYou can see the top of a building in the center of the island.\n"
        announce(discription)

    def process_verb(self, verb, cmd_list, nouns):
        if (verb == "west"):
            announce ("You return to your ship.")
            config.the_player.next_loc = config.the_player.ship
            config.the_player.visiting = False
        if (verb == "north" or verb == "south"):
            announce ("You walk all around the island on the beach. You notice a building in the center of the island.\n")
        if (verb == "east" or verb == "to building"):
            config.the_player.next_loc = self.main_location.locations["church"]

class Church(location.SubLocation):
    '''outside of church. can either go inside or downstairs'''
    def __init__(self, m):
        super().__init__(m)
        self.name = "church"
        self.verbs['north'] = self
        self.verbs['south'] = self
        self.verbs['east'] = self
        self.verbs['west'] = self
        self.verbs["in cellar"] = self

    def enter(self):
        description = "\nYou walk to the building. It is a weathered building with the front doors hanging off their hinges."
        description = description + "\nYou also spot an enterance to the buildings cellar.\n\nWould you like to go inside or go downstairs?\n"
        announce(description)

    def process_verb(self, verb, cmd_list, nouns):
        if (verb == "west"):
            config.the_player.next_loc = self.main_location.locations["beach"]
        if (verb == "north" or verb == "south" or verb == "east"):
            announce("You walk around the island and end up back at your ship")
            config.the_player.next_loc = self.main_location.locations['beach']
        if (verb == "in cellar" or verb == "downstairs" or verb == "in basement" or verb == "down"):
            config.the_player.next_loc = self.main_location.locations["basement"]
        if (verb == "inside" or verb == "into the church" or verb == "inside church" or verb == 'in'):
            config.the_player.next_loc = self.main_location.locations["church_inside"]

class Church_inside(location.SubLocation):
    '''location contains a note talking about treasure downstairs as well as a gold disk'''
    def __init__(self, m):
        super().__init__(m)
        self.name = "church_inside"
        self.verbs['talk'] = self
        self.verbs['take'] = self
        self.verbs['leave'] = self
        self.verbs['east'] = self
        self.verbs['north'] = self
        self.verbs['south'] = self
        self.verbs['west'] = self
        #room variables
        self.note = True
        

    def enter(self):
        description = "\nYou walk through the broken doors and enter what used to be a church. The room is lit by light streaming in through the large holes in the roof.\n"
        note = "\nAs you enter you spot a person in tattered robes sitting on a rotting pew with their back facing you. They say nothing but maybe you can talk with them."
        gold = "\nYou spot the shine of gold on the puplit across the room from where you stand."
        if self.main_location.gold_taken == False and self.note ==True:
            announce(description + note + gold)
        elif self.main_location.gold_taken == False and self.note == False:
            announce(description + gold)
        elif self.main_location.gold_taken == True and self.note == True:
            announce(description + note)
        else:
            announce(description)

    def process_verb(self, verb, cmd_list, nouns):
        if (verb == "west" or verb == 'back' or verb == 'outside'):
            config.the_player.next_loc = self.main_location.locations["church"]
        if (verb == "north" or verb == "south" or verb == "east"):
            announce("The only door is to the west.")
        if (verb == 'leave'):
            config.the_player.next_loc = self.main_location.locations["church"]
            config.the_player.go = True
        if (verb == "talk"):
            announce("\nAs you approch the person you realize this person has been dead a long time. They are cluching a peice of paper in their hand.\n")

        if verb == "take":
            if self.note == False and self.main_location.gold_taken == True:
                announce ("You don't see anything to take.")
            elif len(cmd_list) > 1:
                at_least_one = False #Track if you pick up an item, print message if not.
                if self.note != False and (cmd_list[1] == 'note' or cmd_list[1] == 'paper' or cmd_list[1] == "all"):
                    announce ("\nYou take the note from the corpse.\n")
                    announce('The note reads "The other monks went to claim the treasure below the cellar.\nThey have not come back and I am losing hope. I will join my brothers soon."\n')
                    self.note = False
                    config.the_player.go = True
                    at_least_one = True
                if self.main_location.gold_taken == False and (cmd_list[1] == 'gold' or cmd_list[1] == "all"):
                    announce ("\nYou pick up a golden plate from the pulpit. It has strange writing on it.\n")
                    config.the_player.add_to_inventory([self.main_location.gold])
                    self.main_location.gold_taken = True
                    announce("50 shillings of gold has been added to your inventory.\n")
                    config.the_player.go = True
                    at_least_one = True
                if at_least_one == False:
                    announce ("\nYou don't see one of those around.")


class Church_basement(location.SubLocation):
    '''basement, small puzzle to find hidden door behind shelf'''
    def __init__(self, m):
        super().__init__(m)
        self.name = "basement"
        self.verbs['leave'] = self
        self.verbs['east'] = self
        self.verbs['north'] = self
        self.verbs['south'] = self
        self.verbs['west'] = self
        self.verbs['shelf'] = self
        self.verbs['search'] = self
        self.verbs['move shelf'] = self
        self.verbs["follow"] = self
        self.verbs["open"] = self
        #location variables 
        self.hint1 = False
        self.hint2 = False
        self.hint = 0
        self.found = False
        

    def enter(self):
        description = "\nAs you get to the bottom of the stairs you see a large room with rows of shelves lining the walls and junk littering dusty stone floor."
        description += f"\nYou spot that there are footprints visible in the dust.\n"
        hint1 = "\nThere is a strange breeze running through this cellar.\n"
        hint2 = "\nA wooden shelf in the back of the room looks like it can be pulled from the wall.\n"
        found = "\nNow that you moved the shelf there is a passage at the east end of the room"
        self.hint += 1
        if self.found == False:
            if self.hint1 == True and self.hint2 ==True:
                announce(description + hint1 + hint2)
            elif self.hint1 == True and self.hint2 == False:
                announce(description + hint1)
            else:
                announce(description)
        else:
            announce(description + found)

    def process_verb(self, verb, cmd_list, nouns):
        if (verb == "west" or verb == 'back' or verb == 'outside' or verb == "leave"):
            config.the_player.next_loc = self.main_location.locations["church"]
            config.the_player.go = True
        if (verb == "shelf" or verb == 'move shelf' or verb == 'search' or verb == "follow" or verb == "open"):
            self.found = True
            announce("\nYou find a hidden stairwell behind a shelf! Now that you moved the shelf there is a passage at the east end of the room\n")
        if (verb == 'east' or verb == 'to the passage' or verb == 'down'):
            if self.found == False:
                if self.hint > 0:
                    self.hint1 = True
                if self.hint > 1:
                    self.hint2 = True
            elif self.found == True:
                config.the_player.next_loc = self.main_location.locations["sub_basement"]
                config.the_player.go = True
        else: 
            if self.hint > 0:
                self.hint1 = True
            if self.hint > 1:
                self.hint2 = True
            if self.hint > 2 and self.found == False:
                announce("\nMaybe you should search the room?")
            config.the_player.go = True

class Sub_basement(location.SubLocation):
    '''main room in sub basement. need to take lantern to see. contains a north and east puzzle room.
    once rooms are completed southern treasure/combat room is unlocked'''
    def __init__(self, m):
        super().__init__(m)
        self.name = "sub_basement"
        self.verbs['leave'] = self        
        self.verbs['north'] = self
        self.verbs['south'] = self
        self.verbs['east'] = self
        self.verbs['west'] = self
        self.verbs['grab'] = self
        self.verbs['grab lantern'] = self
        self.verbs['take lantern'] = self
        self.verbs['lantern'] = self
        self.verbs['take'] =self
        self.verbs['look'] = self
        

    def enter(self):
        description = "At the end of the passage is a large dark room. You can't see very far in the darkness."
        description += f"\nHanging on the wall next to you is an unlit lantern.\n"
        lantern = f"\nThe light shines on hundreds of sharp spikes sticking out of the ground."
        lantern += f"\nThere is a narrow pathway that between all of the spikes. The path leads to 2 doors. \nOne door to the north."
        lantern += f"\nOne door to the east.\n"
        if self.main_location.puzzleN_done == True and self.main_location.puzzleE_done == True:
            lantern += f"\nThere is now a door on the southern wall\n"
        if self.main_location.puzzleN_done == True and self.main_location.puzzleE_done == False:
            announce("A new path has appeared. It doesn't seem to lead to anything yet.\n")
        if self.main_location.puzzleN_done == False and self.main_location.puzzleE_done == True:
            announce("A new path has appeared. It doesn't seem to lead to anything yet.\n")
        
        if self.main_location.light == True:
            announce(lantern)
        else:
            announce(description)

    def process_verb(self, verb, cmd_list, nouns):
        if (verb == "west" or verb == 'back' or verb == 'outside' or verb == 'leave'):
            config.the_player.next_loc = self.main_location.locations["basement"]
            config.the_player.go = True
        if (verb == "take lantern" or verb == 'grab lantern' or verb == 'grab' or verb == "lantern" or verb == "take"):
            self.main_location.light = True
            announce("\nYou take the rusted lantern off the wall and light it. The ghostly light illuminates the room.")
            self.enter()
        if self.main_location.light == True:
            if (verb == 'north'):
                config.the_player.next_loc = self.main_location.locations["sub_basement_north"]
                config.the_player.go = True
            if (verb == 'east'):
                config.the_player.next_loc = self.main_location.locations["sub_basement_east"]
                config.the_player.go = True
            if (verb == 'south'):
                config.the_player.next_loc = self.main_location.locations["sub_basement_south"]
                config.the_player.go = True
        else:
            announce("\nIt's to dark to safely go that way.\n")

class Sub_basement_north(location.SubLocation):
    '''norther puzzle room. press button and spiked walls close in on player. pressing button only resets walls.
    to solve the player has to wait instead of pressing the button'''
    def __init__(self, m):
        super().__init__(m)
        self.name = "sub_basement_north"
        self.verbs['leave'] = self        
        self.verbs['north'] = self
        self.verbs['south'] = self
        self.verbs['east'] = self
        self.verbs['west'] = self
        
        self.verbs['press'] = self
        self.verbs['press button'] = self
        self.verbs['do nothing'] = self
        self.verbs['nothing'] = self
        self.verbs['wait'] = self
        self.verbs["escape"] = self

        self.button_pressed = False
        self.press = 0
        self.hint = 0

    def enter(self):
        if self.main_location.puzzleN_done == False:
            if self.button_pressed == True:
                announce("\nWith a loud groan the walls move closer to you!!\n")
            else:
                description = "\nYou enter a rectangular roon and the door slams behind you. In front of you is a pedestal with a button on it.\n"
                announce(description)
        else:
            announce("There is nothing left for you in this room")
        
    def process_verb(self, verb, cmd_list, nouns):
        if (verb == "south" or verb == 'back' or verb == 'outside' or verb == 'leave'):
            if self.main_location.puzzleN_done == False:
                announce("\nThe door behind you is sealed shut\n")
            else:
                config.the_player.next_loc = self.main_location.locations["sub_basement"]
                config.the_player.go = True
        if (verb == "press" or verb == 'press button'):
            if self.button_pressed == False:
                self.button_pressed = True
                config.the_player.go = True
            else:
                announce("\nThe walls slowly move back to where they started. Then begin moving towards you again!\n")
                self.press += 1
                if self.press >= 1:
                    announce("Maybe there is a trick to geting out of this room?\n")
                    self.press += 1
                if self.press >= 3:
                    announce('You wonder "What would happen if I just wait?"\n')
                    self.press += 1
        if (verb == 'wait' or verb == 'do nothing' or verb == 'nothing'):
            announce("\nAs you wait the walls move closer and closer then suddenly stop right before squishing you!")
            announce('A booming voice speaks from the pedistal. "You have proven your bravery. You pass this trial!\n')
            if self.main_location.puzzleE_done == True:
                announce("\nYou have proven yourself worthy to of the treasure in our southern room!")
            announce("\nThe walls move back into place and you hear the door behind you unlock.\n")
            self.main_location.puzzleN_done = True

        else:
            if self.main_location.puzzleN_done == False and verb != "press" and verb != "press button":
                announce("\nThe walls continue to close in!!!\n")
                self.hint += 1
                if self.hint >= 2 and self.press < 3:
                    announce("\nMaybe pressing the button again will help?\n")

class Sub_basement_east(location.SubLocation):
    '''eastern puzzle room. must answer 3 riddles (all, egg, sound) to complete room.
    daimond eyes are an item if players choose to take them'''
    def __init__(self, m):
        super().__init__(m)
        self.name = "sub_basement_east"
        self.verbs['leave'] = self        
        self.verbs['north'] = self
        self.verbs['south'] = self
        self.verbs['east'] = self
        self.verbs['west'] = self
        #riddle 1 verbs
        self.verbs['all'] = self
        self.verbs['all of them'] = self
        self.verbs['all months'] = self
        self.verbs['12'] = self
        self.verbs['12 months'] = self
        self.verbs["february"] = self
        self.verbs["one"] = self
        self.verbs["1"] = self
        #riddle 2 verbs
        self.verbs['egg'] = self
        self.verbs['a egg'] = self
        self.verbs['an egg'] = self
        #riddle 3 verbs
        self.verbs['voice'] = self
        self.verbs['speach'] = self
        self.verbs['sound'] = self
        #daimond verbs
        self.verbs['take'] = self
        self.verbs['take daimond'] = self
        self.verbs['take daimonds'] = self
        self.verbs["take eyes"] = self
        #puzzle vars
        self.riddle1_done = False
        self.riddle2_done = False
        self.riddle3_done = False
        self.speach = False
        self.hint = 0

    def enter(self):
        if self.main_location.treasure_taken == False:
            if self.speach == False:
                description = "\nYou enter a rectangular room and the door slams behind you. In front of you is a large stone face with diamond inlaid eyes."
                mouth = f"\nAs The door seals behind you the mouth moves and speaks:"
                task = f"\nIn order to pass this trial you must prove yourself in a test of knowlege!\n"
                announce(description + mouth + task)
                self.speach = True
            if self.riddle1_done == False and self.riddle2_done == False and self.riddle3_done == False:
                riddle1 = "My first riddle: What month has 28 day?\n" #all of them
                announce(riddle1)
            if self.riddle1_done == True and self.riddle2_done == False and self.riddle3_done == False:
                riddle2 = "\nMy second riddle: What do you break before you use it?\n" #egg
                announce(riddle2)
            if self.riddle1_done == True and self.riddle2_done == True and self.riddle3_done == False:
                riddle3 = "\nMy third and final riddle: You can hear me, but you cannot see or touch me. What am I?\n" #voice
                announce(riddle3)
            if self.riddle3_done == True and self.main_location.daimonds_taken == False :
                if self.main_location.puzzleN_done == True:
                    done = "\nYou have proven yourself. You may now take the treasure in the southern room.\n"
                    announce(done)
                else:
                    announce("\nWell done! Only one trial left.\n")
        else:
            announce("\nThere is nothing left for you in this room.\n")
        
    def process_verb(self, verb, cmd_list, nouns):
        if (verb == "west" or verb == 'back' or verb == 'outside' or verb == 'leave' or verb == "go west"):
            if self.main_location.puzzleE_done == True:
                config.the_player.next_loc = self.main_location.locations["sub_basement"]
                config.the_player.go = True
            else:
                announce("\nThe door behind you is sealed shut.\n")
        if self.riddle1_done == False: #all months
            if (verb == "all" or verb == 'all of them' or verb == 'all months' or verb == '12' or verb == '12 months'):
                response = "\nWell done! Another one!\n"
                self.riddle1_done = True
                self.hint = 0
                announce(response)
                config.the_player.go = True
            if (verb == "february" or verb == "one" or verb == "1"):
                if self.hint > 0:
                    announce("\nThe stone face remains silent.\n")
                if self.hint >= 1 and self.hint < 2:
                    announce("\nMaybe were not thinking about the question right?\n")
                if self.hint >= 2:
                    announce('\nA voice in you head says "All months have 28 days, right?\n"')
                self.hint += 1
                config.the_player.go = True

        if self.riddle1_done == True and self.riddle2_done == False: #egg
            if (verb == "egg" or verb == 'a egg' or verb == 'an egg'):
                response = "\nWell done! One more!\n"
                self.riddle2_done = True
                self.hint = 0
                announce(response)
                config.the_player.go = True
            else:
                if self.hint > 0:
                    announce("\nThe stone face remains silent.\n")
                if self.hint >= 1 and self.hint < 2:
                    announce("\nMaybe were not thinking about the question right?n")
                if self.hint >= 2 and self.hint < 3:
                    announce('\nYour stomach rumbles. You think "Damn, I wish I had an egg for breakfast."\n')
                if self.hint >= 3:
                    announce("\nOh! The answer is an egg!\n")
                self.hint += 1
                config.the_player.go = True

        if self.riddle1_done == True and self.riddle2_done == True and self.riddle3_done == False: #voice
            if (verb == "voice" or verb == 'speach' or verb == 'sound'):
                self.main_location.puzzleE_done =True
                response = "\nExcellent! You've done it!"
                self.riddle3_done = True
                self.hint = 0
                announce(response)
                config.the_player.go = True
            else:
                if self.hint > 0:
                    announce("\nThe stone face remains silent.\n")
                if self.hint >= 1 and self.hint < 2:
                    announce("\nMaybe were not thinking about the question right?\n")
                if self.hint >= 2 and self.hint < 3:
                    announce('\nYour head begins hurting from the voice shouting in this room.\n')
                if self.hint >= 3:
                    announce("\nOh! The answer is sound!\n")
                self.hint += 1
                config.the_player.go = True

        if self.main_location.puzzleE_done == True:
            if self.main_location.daimonds_taken == False:
                if (verb == 'take' or verb == "take daimond" or verb == "take daimonds" or verb == "take eyes"):
                    config.the_player.add_to_inventory([self.main_location.daimond_eyes])
                    self.main_location.daimonds_taken == True
                    daimonds = "\nWith some difficulty you pry the daimond eyes out of the stones face. I hope these daimonds are worth it.\n"
                    announce(daimonds)
                    announce("\n2 daimonds valued at 250 shillings each have been added to your inventory.\n")
                    config.the_player.go = True

class Sub_basement_south(location.SubLocation):
    '''treasure room/ combat encounter. pirates from other ship try and steal treasure. player can choose to leave or fight.
    if they leave the other crew take the treasure and leave on their ship.
    if fought and defeated crew gains treasure and brought back to the beach'''
    def __init__(self, m):
        super().__init__(m)
        self.name = "sub_basement_south"
        self.verbs['leave'] = self        
        self.verbs['north'] = self
        self.verbs['south'] = self
        self.verbs['east'] = self
        self.verbs['west'] = self
        #Treasure verbs
        self.verbs['take'] = self
        self.verbs['take treasure'] = self
        self.verbs['loot'] = self
        self.verbs['fight'] = self
        #room vars
        self.speach = False


    def enter(self):
        if self.main_location.treasure_taken == False:
            if self.speach == False:
                description = "\nYou enter the treasure chamber only to see someone has beaten you here!!!"
                description += "\nA pirate crew stands between you and your treasure."
                captain = '\nThe theives captain raises a sword and says\n"No need for a fight, just turn around and leave."'
                response = "\n\nWhat will you do 'leave' or 'fight'?\n"
                announce(description + captain + response)
                self.speach = True

        else:
            announce("\nThere is nothing left for you in this room.\n")
            self.events.clear()

    def process_verb(self, verb, cmd_list, nouns):
        if (verb == "north" or verb == 'back' or verb == 'outside' or verb == 'leave' or verb == "go north"):    
            if self.main_location.treasure_taken == False and self.main_location.thieves_beat == False: 
                announce("\nAfter a moment of thought, you decided some treasure wasn't worth you and your crews lives.\n")
                self.main_location.treasure_taken = True
                self.main_location.flead = True
                config.the_player.next_loc = self.main_location.locations["sub_basement"]
                config.the_player.go = True
        
        if (verb == "north" or verb == 'back' or verb == 'outside' or verb == 'leave' or verb == "go north"):    
            if self.main_location.treasure_taken == False and self.main_location.thieves_beat == True: 
                announce("\nYou killed for this treasure. You may as well take it.\n")

        if (verb == "north" or verb == 'back' or verb == 'outside' or verb == 'leave' or verb == "go north"):    
            if self.main_location.treasure_taken == True and self.main_location.thieves_beat == True: 
                config.the_player.next_loc = self.main_location.locations["sub_basement"]
                config.the_player.go = True        

        if (verb == "north" or verb == 'back' or verb == 'outside' or verb == 'leave' or verb == "go north"):    
            if self.main_location.treasure_taken == True and self.main_location.flead == True: 
                config.the_player.next_loc = self.main_location.locations["sub_basement"]
                config.the_player.go = True        

        if (verb == 'fight' or verb == 'south'):
            if (self.main_location.thieves_beat == False):
                self.event_chance = 100            
                self.events.append(lily_pirate_crew.Lily_prate_crew())
                config.the_player.go = True
                announce('\nThe captain shouts to their crew "Make them regret crossing us!\n')
                self.main_location.thieves_beat = True
                

            else:
                announce("\nThere is no one left to fight.\n")

        if (verb == "take" or verb == "take treasure" or verb == "loot"):
            if self.main_location.treasure_taken == False:
                announce("\nWith great effort you are able to bring all of your treasure to the ship.\n")
                self.main_location.treasure_taken = True
                config.the_player.add_to_inventory([self.main_location.treasure])
                announce("\n3000 shillings of treasure have been added to your inventory!\n")
                config.the_player.next_loc = self.main_location.locations["beach"]
                config.the_player.go = True
            else:
                announce("\nThe treasure has already been taken.\n")

class Gold(game.items.Item):
    '''gold disk from inside church'''
    def __init__(self):
        super().__init__("golden disk", 50)    

class Diamonds(game.items.Item):
    '''damond eyes from northern puzzle room'''
    def __init__(self):
        super().__init__("diamond eyes", 500) 

class Treasure(game.items.Item):
    '''treasure from southern room gained after defeating other pirate crew'''
    def __init__(self):
        super().__init__("Treasure from the church basement", 3000)


######cut content due to time constrains and handling issue
""" class Thief_ship(location.SubLocation):
    '''crew can explore other crews ship to gain extra treasure once defeating crew and completing dungeon'''
    def __init__(self, m):
        super().__init__(m)
        self.name = "thief_ship"
        self.verbs['leave'] = self        
        self.verbs['north'] = self
        self.verbs['south'] = self
        self.verbs['east'] = self
        self.verbs['west'] = self
        #Treasure verbs
        self.verbs['take'] = self
        self.verbs['take map'] = self
        self.verbs['loot'] = self
        #deck verbs
        self.verbs["investigate"] = self
        self.verbs["investigate sound"] = self
        #treasure var
        self.search = False
        


    def enter(self):
        description = "You explore above and below deck and find nothing of value."
        description += "\nNo wonder these sad excueses for pirates couldn't figure out how to get the treasure themselves."
        plot = '\nAs you approach the captains quaters you hear a loud shattering noise!'
        question = "\nWhat will you do, 'investigate' or leave?"
        if self.main_location.map == False and self.search == False:
            announce(description + plot + question)

    def process_verb(self, verb, cmd_list, nouns):
        if (verb == 'back' or verb == 'outside' or verb == 'leave'):  
            if self.main_location.map == False:  
                announce("This worthless ship isn't worth your time.")
                config.the_player.next_loc = self.main_location.locations["beach"]
                config.the_player.go = True

        if (verb == "investigate" or verb == 'investigate sound'):    
            action = "You throw open the doors to the captains quaters!"
            action += "\nA terrified parrot startles you as it flies out of the room and into the sky."
            action += "\nInside the room you spot a shattered bottle with a small ship laying amonst the shards."
            action += "\nYou also spot a strange map in a mysterious language pinned to a table."
            action += "\nDo you dare take the map?"
            self.search = True
            announce(action)

        
        if (verb == "take" or verb == "take map" or verb == "loot"):
            if self.main_location.map == False and self.search == True:
                announce("You pick up the map. Maybe someone on your adventure can read it.")
                announce("With map in hand you leave the ship.")
                self.main_location.map = True
                config.the_playernext_loc = self.main_location.locations["beach"]
                config.the_player.go = True """
