import random
import sys

#Global Variables
pkmn_List = ["charmander","squirtle","bulbasaur"]

#p1 pokemon placeholder data
p1_file = ""
p1_name = "derp"
p1_species = "charmander"
p1_lvl = 10

#p2 pokemon placeholder data
p2_file = ""
p2_name = "face"
p2_species = "squirtle"
p2_lvl = 10

#Pokemon Superclass
class Pokemon:
    
    def __init__(self,name,type,lvl = 10):
        #pokemon data and battle stats
        self.name = name
        self.type = type
        self.lvl = lvl
        self.att = 10+ (0.5 * lvl)
        self.is_defending = False
        self.defence = 10 + (0.3 * lvl)
        self.speed = 10 + (0.4 * lvl)
        self.hp = round(10 + (3*lvl),2)
        self.max_hp = 10 +(3*lvl)
        self.type_multiplier = 1.0
        
    def attack(self,other):
        print(f"{self} used attack!")
        #damage output is dependent on pokemon's attack stat and other's defence stat
        dmg = round(((self.att-(0.15*other.defence)) * self.type_multiplier),2)
        if other.hp > dmg:
            other.hp -= dmg
            other.hp = round(other.hp,2)
            print(f"{self} did {dmg} damage!")
        else:
            #if more attack is dealt that the other pokemon has HP then it is simply set to 0
            print("Knockout!")
            other.hp = 0
        if other.is_defending:
            #if other pokemon was defending, they stop doing so.
            #only stop defending after they've been attacked
                other.is_defending = False
                other.defence -= 15
                
    def defend(self):
        #raises pokemon's defence stat for one attack
        self.is_defending = True
        self.defence +=15
        print(f"{self.name} has their guard up!")
        
    def __repr__(self):
        return self.name

    #getter functions
    def get_hp(self):
        return self.hp
    
    def get_max_hp(self):
        return self.max_hp
        
    def get_speed(self):
        return self.speed
        
    def did_lose(self):
    #boolean which determines whether or not the fight has ended
    #with a winner or loser
        if self.hp == 0:
            return True
        else:
            return False
            
    def vs_type(self,other):
        #compares two pokemon's types and determines who has an advantage
        #type multiplier is greater than 1 if they have the edge and less than 1
        #if they are at a disadvantage
        if self.type != other.type:
            if self.type == "fire" and other.type == "water":
                self.type_multiplier = 0.7
            elif self.type == "water" and other.type == "fire":
                self.type_multiplier = 1.3
            if self.type == "water" and other.type == "grass":
                self.type_multiplier = 0.7
            elif self.type == "grass" and other.type == "water":
                self.type_multiplier = 1.3    
            if self.type == "grass" and other.type == "fire":
                self.type_multiplier = 0.7
            elif self.type == "fire" and other.type == "grass":
                self.type_multiplier = 1.3
#end Pokemon



#Three pokemon subclasses which have their own unique stats and types
class Charmander(Pokemon):
    def __init__(self,name,lvl = 10):
        Pokemon.__init__(self, name, lvl)    
        self.name = name
        self.type = "fire"
        self.lvl = lvl
        self.att = 18 + (0.5*lvl)
        self.defence = 15 + (0.3*lvl)
        self.speed = 8 + (0.4*lvl)
        self.hp = round(47 + (4*lvl),2)
        self.max_hp = 47 +(4*lvl)
#end Charmander

class Squirtle(Pokemon):
    def __init__(self,name,lvl = 10):
        Pokemon.__init__(self, name, type)    
        self.name = name
        self.type = "water"
        self.lvl = lvl
        self.att = 19 + (0.5 * lvl)
        self.defence = 15 + (0.3 * lvl)
        self.speed = 20 + (0.4 *lvl)
        self.hp = round(43 + (4*lvl),2)
        self.max_hp = 43 + (4*lvl)
#end Squirtle

class Bulbasaur(Pokemon):
    def __init__(self,name,lvl = 10):
        Pokemon.__init__(self, name, type)    
        self.name = name
        self.type = "grass"
        self.lvl = lvl
        self.att = 17+ (0.5*lvl)
        self.defence = 25+ (0.3*lvl)
        self.speed = 5+ (0.4*lvl)
        self.hp = round(50+ (4*lvl),2)
        self.max_hp = 50+ (4*lvl)
#end Bulbasaur

class ItemBag:
    
    def __init__(self,num_of_items):
        #stores number of each item available
        self.num_of_potions = num_of_items
        self.num_of_attUp = num_of_items
        self.num_of_defUp = num_of_items
        
    def usePotion(self, pokemon):
        #Only uses item if the number available is greater than 0
        if self.num_of_attUp > 0:
            if (pokemon.max_hp - pokemon.hp) >=20:
                pokemon.hp += 20
            else:
                #pokemon only gains 20 hp if they have lost 20 or more hp.
                #otherwise, they just regain enough hp to reach max again.
                pokemon.hp += (pokemon.max_hp-pokemon.hp)
            self.num_of_potions -=1
            print(f"{pokemon} recovered 20 hp!")
            
    def useAttackUp(self, pokemon):
        if self.num_of_attUp > 0:
            pokemon.att += 5
            self.num_of_attUp -=1
            print(f"{pokemon}'s attack went up!")
            
    def useDefUp(self, pokemon):
        if self.num_of_defUp > 0:
            pokemon.defence += 5
            self.num_of_attUp -=1
            print(f"{pokemon}'s defence went up!")
#end ItemBag
            
#Function that gets the user to enter a number within a certain range
#with built in error catching
def get_number(text,min,max):
    while True:
        try:
            num = int(input(text))
            if num >= min and num <= max:
                return num
                break
            else:
                print("Out of Range!")
                continue
        except ValueError:
            print("Please enter an int!")
            continue
#end getNumber

#Save Function
def save(file, name,species,lvl):
    try:
        #opening file in write mode to store information on it
        File = open(file+".txt","w")
        #each line is dedicated to a data type (name, species, lvl)
        File.write(f"{name}\n{species}\n{lvl}")
        File.close()
        print("save complete!")
    except:
        print("Error Saving Game:\n File Not Found")


#load function which retrieves Pokemon species, name and type.
def load(file):
    name =""
    species = ""
    lvl = 0
    try:
       File = open(file+".txt","r")
       #reads the first three lines where the data for each player is stored
       file_found = True
       name = File.readline()[0:-1]
       species = File.readline()[0:-1]
       lvl = int(File.readline())

       print("File found!") 
    except FileNotFoundError: #if the file we're looking for doesn't exist
        print("File not found")
        file_found = False
    #returns data and file_found boolean
    return (name, species, lvl, file_found)

     

#welcome message
print("Welcome to Pokemon Battle Simulator!\n")
            
### Pokemon Initialization ###

# P1 Load Option #
answer = input("Player 1, would you like to load a pre-existing pokemon file?\n").lower()

if answer.startswith("y"):
    while True: #allows user to try again if they mispell a file       
        p1_file = input("Enter the name of the file you'd like to use: ")
        p1_data = load(p1_file)
        if p1_data[3]: #essentially "if file is found"
            p1_name = p1_data[0]
            p1_species = p1_data[1]
            p1_lvl = p1_data[2]
            print(f"Loaded {p1_name} the {p1_species} (lvl: {p1_lvl})")
            break
        try_again = input("Would you like to load a different file?")
        if try_again.startswith("y"):
            continue
        else:
            break
# P1 Pokemon creator #
else:      
    print("Player 1, choose you're pokemon:")
    for i in range(len(pkmn_List)):
       print(f"{i+1}. {pkmn_List[i]}")
        
    while True:
    #Error catching in case user makes a typo or chooses an unavailable pokemon
        p1_species = input("Enter a name from the list: ").lower()    
        if(p1_species in pkmn_List):
            break
        else:
            print("that is not a pokemon from the list! Try again")
            continue
    p1_name = input(f"What will you name your {p1_species}?: ")
    p1_lvl = get_number("Choose a level for your pokemon(1-99): ",1,99)

# P2 load option #
answer = input("Player 2, would you like to load a pre-existing pokemon file?\n").lower()
if answer.startswith("y"):
    while True: #allows user to try loading again if they make a typo
        p2_file = input("Enter the name of the file you'd like to use: ")
        p2_data = load(p2_file)
        if p2_data[3]: #essentially "if file is found"
            p2_name = p2_data[0]
            p2_species = p2_data[1]
            p2_lvl = p2_data[2]
            print(f"Loaded {p2_name} the {p2_species} (lvl: {p2_lvl})")
            break
        try_again = input("Would you like to load a different file?")
        if try_again.startswith("y"):
            continue
        else:
            break
#P2 Pokemon creator #
else:
    print("Player 2, choose you're pokemon:")
    
    for i in range(len(pkmn_List)):
        print(f"{i+1}. {pkmn_List[i]}")
        
    while True:
    #Error catching in case user makes a typo or chooses an unavailable pokemon
        p2_species = input("Enter a name from the list: ").lower()    
        if(p2_species in pkmn_List):
            break
        else:
            print("that is not a pokemon from the list! Try again")
            continue
    p2_name = input(f"What will you name your {p2_species}?: ")
    p2_lvl = get_number("Choose a level for your pokemon(1-99): ",1,99)

#initiates the coresponding sub-class with pokemon species
if(p1_species == "charmander"):
    p1_pkmn = Charmander(p1_name,p1_lvl)
elif(p1_species == "squirtle"):
    p1_pkmn = Squirtle(p1_name,p1_lvl)
else:
    p1_pkmn = Bulbasaur(p1_name,p1_lvl)
    
if(p2_species == "charmander"):
    p2_pkmn = Charmander(p2_name,p2_lvl)
elif(p2_species == "squirtle"):
    p2_pkmn = Squirtle(p2_name,p2_lvl)
else:
    p2_pkmn = Bulbasaur(p2_name,p2_lvl)

#Determining type Advantage
p1_pkmn.vs_type(p2_pkmn)
p2_pkmn.vs_type(p1_pkmn)

#item bags for respective players
p1_bag = ItemBag(3)
p2_bag = ItemBag(3)

#list of options players can take when its their turn
moves = ["attack","defend","Item","Run Away"]
#list of items (back will bring them back to moves list)
items = ["potion","attack up","defence up","back"]


### Main Battle Loop ###

print("Battle Start!\n")
while True:
    #variables which hold the value of both user's choices
    first_choice = 0
    first_item_choice = 0
    second_choice = 0
    second_item_choice = 0
    
    #determining which pokemon(the faster one) gets to go first
    if p1_pkmn.get_speed() > p2_pkmn.get_speed():
        #assigning new values to class instances based on which pokemon gets to attack first
        #the value of these temporary instances will be transported back to the original ones at the end of each 
        #loop
        goes_first = p1_pkmn
        first_bag = p1_bag
        
        goes_second = p2_pkmn
        second_bag = p2_bag
        
    elif p2_pkmn.get_speed() > p1_pkmn.get_speed():
        goes_first = p2_pkmn
        first_bag = p2_bag
        
        goes_second = p1_pkmn
        second_bag = p1_bag
        
    else: #if speed stats are even, the pokemon that gets to go first is 
    #randomly selected.
        flip = random.choice(["heads","tails"])
        if flip == "heads":
            goes_first = p1_pkmn
            first_bag = p1_bag
            
            goes_second = p2_pkmn
            second_bag = p2_bag
        else:
            goes_first = p2_pkmn
            first_bag = p2_bag
            
            goes_second = p1_pkmn
            second_bag = p1_bag

## P1 Moves ##
    #Looping through the menu options (moves and items) until the first user makes a choice
    while True:
        print(f"\n{goes_first}'s Moves:")
        for i in range(len(moves)):
            print(f"{i+1}. {moves[i]}")
        print("")
        print(f"{goes_first}: {goes_first.get_hp()}/{goes_first.get_max_hp()}")
        print(f"{goes_second}: {goes_second.get_hp()}/{goes_second.get_max_hp()}\n")
        choice = get_number(f"What would {goes_first} like to do ?(1-4): ",1,4)
        
        #If items menu is chosen
        if choice == 3:
            for i in range(len(items)):
               print(f"{i+1}. {items[i]}")
               first_choice = choice
        else:
            first_choice = choice
            break
        print("")
        choice = get_number(f"What item would you like to use on {goes_first}?(1-4): ",1,4)
        # When user selects back
        if choice == 4:
            continue
        else:
            #Telling user when they've run out of items
            if first_bag.num_of_potions == 0 and choice == 1:
                print("You're out of those!")
                continue
            elif first_bag.num_of_attUp == 0 and choice == 2:
                print("You're out of those!")
                continue
            elif first_bag.num_of_defUp == 0 and choice == 3:
                print("You're out of those!")
                continue
            else:
                    first_item_choice = choice
                    break
## P2 Moves ##
    #Looping through the menu options (moves and items) until the second user makes a choice    
    while True:
        print(f"\n{goes_second}'s Moves:\n")
        for i in range(len(moves)):
            print(f"{i+1}. {moves[i]}")
        print("")
        print(f"{goes_first}: {goes_first.get_hp()}/{goes_first.get_max_hp()}")
        print(f"{goes_second}: {goes_second.get_hp()}/{goes_second.get_max_hp()}\n")
        choice = get_number(f"What would {goes_second} like to do ?(1-4): ",1,4)
        
        #If items menu is chosen
        if choice == 3:
            for i in range(len(items)):
               print(f"{i+1}. {items[i]}")
               second_choice = choice
        else:
            second_choice = choice
            break
        print("")
        choice = get_number(f"What item would you like to use on {goes_second}(1-4)?: ",1,4)
        
        # When user selects back
        if choice == 4:
            continue
        
        else:
            #Telling user when they've run out of items
            if second_bag.num_of_potions == 0 and choice == 1:
                print("You're out of those!")
                continue
            elif second_bag.num_of_attUp == 0 and choice == 2:
                print("You're out of those!")
                continue
            elif second_bag.num_of_defUp == 0 and choice == 3:
                print("You're out of those!")
                continue
            else:
                    second_item_choice = choice
                    break

            
    #Carrying out the moves selected by the first pokemon (attack, defend, run away, item)
    if first_choice == 1:
        goes_first.attack(goes_second)
    elif first_choice == 2:
        goes_first.defend()
    elif first_choice == 4:
        print(f"{goes_first} Ran away!")
        break
    else:
        if first_item_choice == 1:
            first_bag.usePotion(goes_first)
        elif first_item_choice == 2:
            first_bag.useAttackUp(goes_first)
        elif first_item_choice ==3:
            first_bag.useDefUp(goes_first)
                
    #Carrying out the moves selected by the second pokemon 
    #Only if they haven't been knocked out (we don't need to check for goes_first
    #becuase they always get to move first).
    if not goes_second.did_lose():
        if second_choice == 1:
            goes_second.attack(goes_first)
        elif second_choice == 2:
            goes_second.defend()
        elif second_choice == 4:
            print(f"{goes_second} Ran away!")
            break
        else:
            if second_item_choice == 1:
                second_bag.usePotion(goes_second)
            elif second_item_choice == 2:
                second_bag.useAttackUp(goes_second)
            elif second_item_choice ==3:
                second_bag.useDefUp(goes_second)
    
    #Check for defeat
    if goes_first.did_lose():
        print(f"{goes_first} has Fainted!")
        break
    elif goes_second.did_lose():
       print(f"{goes_second} has Fainted!") 
       break
   
    #Set original instances to temporary values
    #as goes_first and goes_second only exist in the while loop.
    if goes_first.name == p1_pkmn.name:
        p1_pkmn = goes_first
        p2_pkmn = goes_second
    else:
        p2_pkmn = goes_first
        p1_pkmn = goes_second
        
#post Battle
print("Battle Over!")
if(not p1_pkmn.did_lose() and not p2_pkmn.did_lose()):
    print("No contest.")
elif(p1_pkmn.did_lose()):
    print(f"{p2_pkmn} is the Winner!")
    if p2_pkmn.lvl != 99:
        p2_pkmn.lvl += 1
        print(f"{p2_pkmn} has reached level {p2_pkmn.lvl}!")
elif(p2_pkmn.did_lose()):
    print(f"{p1_pkmn} is the Winner!")
    if p1_pkmn.lvl != 99:
        p1_pkmn.lvl +=1
        print(f"{p1_pkmn} has reached level {p1_pkmn.lvl}!")
    
print("")

#Save option
answer = input("Player 1, would you like to save your pokemon?\n").lower()

if answer.startswith("y"):
    
    if p1_file == "": #if the user is not using a previously saved pokemon
        p1_file = input("Name your save file: ")
    print("saving...")
    save(p1_file,p1_name,p1_species, p1_pkmn.lvl)
    
answer = input("Player 2, would you like to save your pokemon?\n").lower()

if answer.startswith("y"):
    if p2_file == "": #if the user is not using a previously saved pokemon
        p2_file = input("Name your save file: ")
    print("saving...")
    save(p2_file,p2_name,p2_species,p2_pkmn.lvl)

#Goodbye Message
print("Thanks for Playing! Goodbye!")
