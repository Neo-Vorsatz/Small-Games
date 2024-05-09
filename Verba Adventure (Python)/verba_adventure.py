# Text-Based Role Playing Game
# Neo Vorsatz
# 17 February 2023 - 26 March 2023
# Last editted: 3 April 2023

import math
import random

#Common rounding off
def normRound(value):
    if (value%1)==0.5:
        return math.ceil(value)
    else:
        return round(value)

# Initialising data
listResources = ["wood","stone","steel","dragonscale","healingpotion"]
listResCost = [2,4,16,50,5]
listArmour = ["none","leatherarmour","studdedleatherarmour","chainshirt","breastplate","splintarmour","fullplatearmour","dragonarmour"]
listAmrCost = [0,15,20,27,36,47,60,200]
listAmrDef = [0,1,2,3,4,5,6,9]
listWeapons = ["none","shortsword","shortbow","scroll","dagger","sling","grimoire","rapier","lightcrossbow","enchantedamulet","longsword","heavycrossbow","elementalorb","claymore","longbow","runicstone"]
listWpnCost = [0,3,7,9,9,16,21,21,25,31,36,43,49,64,64,64]
listWpnDmgMin = [0,2,3,6,5, 6,9, 8, 8,11,11,11,14,15,14,16]
listWpnDmgMax = [0,4,7,6,7,10,9,10,12,11,13,15,14,17,18,16]
listArtefacts = ["compactshield","vitalitygem","solarcanon","camocloak","amplifier","echoinghilt","firequiver","cursedpin"]
listArtCost = [10,15,20,20,25,30,30,30]
hasArtefact = [False,False,False,False,False,False,False,False]
listEnyAttacks = ["spear","crossbow","battleaxe","scythe","claws","teeth","firebreath","magic spell"]
listEnyDmgMin = [5, 8, 8, 9,6,7,10,11]
listEnyDmgMax = [7,12,10,11,8,9,20,11]
listEnyCharge = [False,False,True,False,False,False,True,False]
listEnyBurning = [False,False,False,False,False,False,True,True]
listEnyCorrosion = [False,False,False,True,False,False,False,False]
listEnemies = ["wolf","goblin","archer goblin","ork","corrupted hunter","corrupted warlock","dragon"]
dictEnyMoves = {0: ["teeth","teeth","claws"],
               1: ["spear","spear","spear"],
               2: ["crossbow","crossbow","crossbow"],
               3: ["battleaxe","battleaxe","battleaxe"],
               4: ["scythe","scythe","scythe"],
               5: ["crossbow","magic spell","magic spell"],
               6: ["teeth","firebreath","firebreath"]
               }
                  #[Base HP] [+Level Hp] [+Level Dmg] [Defense]
dictEnyStats = {0: [30.0, 3.0, 0.6, 3.0],
                1: [25.0, 4.0, 1.0, 3.0],
                2: [25.0, 4.0, 0.6, 3.0],
                3: [40.0, 3.0, 1.2, 5.0],
                4: [50.0, 4.0, 1.6, 4.0],
                5: [45.0, 4.0, 1.8, 4.0],
                6: [100.0, 0.2, 0.9, 7.0]
                }
#Combat statis effects
inCombat = False
yourBurning = False
yourCorrosion = 0
oppBurning = False
oppCorrosion = 0
useCompactShield = False
useAmplifier = False
useEchoingHilt = False
dmgEchoingHilt = 0
useFireQuiver = False
useCursedPin = False
isOppTurn = False
oppCharged = 3

# Start of the game
print("Welcome to the world of Verba, adventurer!")
# Load saved game or start new one
choice = ""
while choice!="load" and choice!="new":
    choice=input("Would you like to start a new game or load a saved one? (load/new)\n")
    
# Loading a saved game
if choice=="load":
    loadSuccess = False
    while not(loadSuccess):
        saveString = input("Enter the text to load a save:\n")
        try:
            pos = saveString.index("|")
            yourLvl = int(saveString[0:pos])
            saveString = saveString[pos+1:]
            yourMaxHP = 30+5*yourLvl
            pos = saveString.index("|")
            yourHP = int(saveString[0:pos])
            saveString = saveString[pos+1:]
            pos = saveString.index("|")
            yourWeapon = saveString[0:pos]
            saveString = saveString[pos+1:]
            pos = saveString.index("|")
            yourArmour = saveString[0:pos]
            saveString = saveString[pos+1:]
            pos = saveString.index("|")
            yourSilver = int(saveString[0:pos])
            saveString = saveString[pos+1:]
            pos = saveString.index("|")
            yourWood = int(saveString[0:pos])
            saveString = saveString[pos+1:]
            pos = saveString.index("|")
            yourStone = int(saveString[0:pos])
            saveString = saveString[pos+1:]
            pos = saveString.index("|")
            yourSteel = int(saveString[0:pos])
            saveString = saveString[pos+1:]
            pos = saveString.index("|")
            yourScales = int(saveString[0:pos])
            saveString = saveString[pos+1:]
            pos = saveString.index("|")
            yourPotions = int(saveString[0:pos])
            saveString = saveString[pos+1:]
            pos = saveString.index("|")
            trackClues = int(saveString[0:pos])
            saveString = saveString[pos+1:]
            for i in range(len(hasArtefact)):
                hasArtefact[i] = (saveString[i]=="1")
            
            print("You continue your quest of bringing an end to the dragon...\n")
            loadSuccess = True
        except:
            print("This is an invalid text to load a save!\n")

# Starting a new game
elif choice=="new":
    yourLvl = 1
    yourSilver = 5
    yourWood = 0
    yourStone = 0
    yourSteel = 0
    yourScales = 0
    yourPotions = 0
    trackClues = 0
    print("\nChoose which class of adventurer you will be.")
    print("Your class will determine your starting equipment, but won't hinder you from gaining other equipment.")
    print("===Knight===\nWeapon: Short Sword (2-4 dmg)\nArmour: Studded Leather (2 def)\n")
    print("===Ranger===\nWeapon: Short Bow (3-7 dmg)\nArmour: Leather (1 def)\n")
    print("===Wizard===\nWeapon: Scroll (6 dmg)\nArmour: None (0 def)\n")
    while choice!="knight" and choice!="ranger" and choice!="wizard":
        choice = (input("Which class do you choose? (knight/ranger/wizard)\n: ")).lower()
    # Choosing Knight
    if choice=="knight":
        yourWeapon = "shortsword"
        yourArmour = "studdedleatherarmour"
    # Choosing Ranger
    elif choice=="ranger":
        yourWeapon = "shortbow"
        yourArmour = "leatherarmour"
    # Choosing Wizard
    elif choice=="wizard":
        yourWeapon = "scroll"
        yourArmour = "none"
    yourMaxHP = 35
    yourHP = yourMaxHP
    # Introduction to quest
    print("\n===Introduction===")
    print("You start your quest in the capital kingdom of Verba. The city streets are bustling and guards are patrolling.")
    print("An unfortunate event occurs; a DRAGON soars across the sky; covering the buildings with a carpet of shadow.")
    print("Many things get scorched by the dragon's fiery breath, but not your will. A bounty is on that dragon's head.")
    print("You task yourself with finding and killing the dragon.\n")

# Start of playing-game
print("Tutorial: Use commands to interact with the world, such as \"profile\", \"explore\" and \"shop\".")
print("Tutorial: Use \"help\" to get a list of command categories.\n")

ln = ""
while ln!="exit":
    if inCombat:
        ln = (input("!: ")).lower()
    else:
        ln = (input(": ")).lower()
    # Help commands
    if ln=="help":
        print("===Help===")
        print("Use \"help [category]\" to view commands in a specific category.")
        print("Categories:\n-Menu\n-Activities\n-Shopping\n-Crafting\n-Combat\n")
    elif ln=="help menu":
        print("===Help-Menu===")
        print("-profile: Shows you your character's statistics.")
        print("-inventory: Shows you your equipment and items.")
        print("-save: Gives a code which you can use to reload your progress.")
        print("-exit: stops the game/program\n")
    elif ln=="help activities":
        print("===Help-Activities===")
        print("-pray: Restores your HP to maximum.")
        print("-gather: Collect some raw materials in the wild. The value will scale off your level.")
        print("-explore: Explore the wilds to find something interesting.")
        print("-track: Increases the chance of finding the dragon when you Explore.")
        print("-chat: Talk with people in the town; they may have something valuable.\n")
    elif ln=="help shopping":
        print("===Help-Shopping===")
        print("-shop: Displays a list of items to purchace.")
        print("-buy [item] [number]: Buys [number] of [item] from the shop.")
        print("-sell [item] [number]: Sells [number] of [item] to the shop.\n")
    elif ln=="help crafting":
        print("===Help-Crafting===")
        print("-craft: Displays a list of items you can craft.")
        print("-craft [item] [number]: Crafts [number] of [item].\n")
    elif ln=="help combat":
        print("===Help-Combat===")
        print("NOTE: In combat many other commands are disabled.")
        print("-attack: Use your weapon to attack with.")
        print("-heal: Use a Healing Potion.")
        print("-[name of artifact]: Use that artifact.")
        print("-retreat: Attempt to escape combat. (1/3 chance)")
        print("\nRULES: In combat you will choose an action, which will be one of the combat commands.")
        print("Your action happens first, then your enemy will have an action.")
        print("This repeats until either side dies, or combat ends in another way.\n")
        print("If you win the combat you\'ll level up. If you lose then you\'ll lose 2 levels. Fleeing won\'t cause anything.")
        print("Your health is increased by 5 per level, and your damage is increased by 1 per level.\n")
        print("During combat the Burning or Corrosion effect can be applied:")
        print("The Burning effect deals an additional +3dmg per turn.")
        print("The Corrosion effect reduces Def by 2, and can stack.\n")
    
    # Menu commands
    elif ln=="profile":
        print("===Profile===")
        if inCombat:
            print("NOTE: IN COMBAT")
        print("Level:",yourLvl)
        print("HP: ",yourHP,"/",yourMaxHP,sep="")
        # Calculating defense
        currentDef = listAmrDef[listArmour.index(yourArmour)]
        if useCompactShield:
            currentDef+=2
        currentDef-=2*yourCorrosion
        if currentDef<0:
            currentDef = 0
        # Calculating average damage
        wpnIndex = listWeapons.index(yourWeapon)
        wpnMax = listWpnDmgMax[wpnIndex]
        wpnMin = listWpnDmgMin[wpnIndex]
        avgDmg = (wpnMin+wpnMax)/2 #Weapon bonus
        if hasArtefact[listArtefacts.index("solarcanon")]: #SolarCanon alternative
            if 3*yourLvl>avgDmg:
                avgDmg = 3*yourLvl
        avgDmg+=yourLvl #Level bonus
        if hasArtefact[listArtefacts.index("amplifier")]: #Amplifier bonus
            if 2*currentDef>avgDmg:
                avgDmg = (avgDmg+2*currentDef)/2
        wpnCategory = wpnIndex%3
        if (hasArtefact[listArtefacts.index("firequiver")])and(wpnCategory==1): #FireQuiver bonus
            avgDmg+=3
        print("Average Damage:",avgDmg)
        print("Defence:",currentDef)
        print("Silver Pieces:",yourSilver)
        print("Tracking Clues:",trackClues)
        print()
        
    elif ln=="inventory":
        print("===Inventory===")
        if inCombat:
            print("NOTE: IN COMBAT")
        wpnIndex = listWeapons.index(yourWeapon)
        wpnMax = listWpnDmgMax[wpnIndex]
        wpnMin = listWpnDmgMin[wpnIndex]
        print("-Your Weapon: ",yourWeapon," (",wpnMin,"-",wpnMax," dmg)",sep="")
        print("-Your Armour:",yourArmour,end="")
        if yourArmour=="dragonarmour":
            print(" (immune to Burning)")
        else:
            print()
        if yourPotions>0:
            print("-HealingPotions:",yourPotions,"(heals 20HP)")
        if yourWood>0:
            print("-Wood:",yourWood)
        if yourStone>0:
            print("-Stone:",yourStone)
        if yourSteel>0:
            print("-Steel:",yourSteel)
        if yourScales>0:
            print("-DragonScales:",yourScales)
        if hasArtefact[listArtefacts.index("compactshield")]:
            print("-CompactShield")
        if hasArtefact[listArtefacts.index("vitalitygem")]:
            print("-VitalityGem")
        if hasArtefact[listArtefacts.index("solarcanon")]:
            print("-SolarCanon")
        if hasArtefact[listArtefacts.index("camocloak")]:
            print("-CamoCloak")
        if hasArtefact[listArtefacts.index("amplifier")]:
            print("-Amplifier")
        if hasArtefact[listArtefacts.index("echoinghilt")]:
            print("-EchoingHilt")
        if hasArtefact[listArtefacts.index("firequiver")]:
            print("-FireQuiver")
        if hasArtefact[listArtefacts.index("cursedpin")]:
            print("-CursedPin")
        print()
        
    elif ln=="save":
        if inCombat:
            print("You can not use this command while in combat!\nOnly fighting or fleeing will save you now.\n")
        else:
            saveString = str(yourLvl)+"|"
            saveString+=str(yourHP)+"|"
            saveString+=yourWeapon+"|"
            saveString+=yourArmour+"|"
            saveString+=str(yourSilver)+"|"
            saveString+=str(yourWood)+"|"
            saveString+=str(yourStone)+"|"
            saveString+=str(yourSteel)+"|"
            saveString+=str(yourScales)+"|"
            saveString+=str(yourPotions)+"|"
            saveString+=str(trackClues)+"|"
            for i in hasArtefact:
                if i:
                    saveString+="1"
                else:
                    saveString+="0"
            saveString+="|"
            print("Use this text to load this game:")
            print(saveString+"\n")
    
    # Activities commands
    elif ln=="pray":
        if inCombat:
            print("You can not use this command while in combat!\nPraying for your life?\n")
        else:
            print("You go to one of the temples in the city and pray; the divine look upon you lovingly.")
            print("Your wounds have been treated.\n")
            yourHP = yourMaxHP
            
    elif ln=="gather":
        if inCombat:
            print("You can not use this command while in combat!\nMore like gathering your sanity.\n")
        else:
            gatherWood = random.randint(yourLvl-1,math.ceil(yourLvl*1.2))
            gatherStone = random.randint(yourLvl-1,yourLvl)
            gatherSteel = random.randint(0,yourLvl)-4
            if gatherSteel<0:
                gatherSteel = 0
            if gatherWood+gatherStone+gatherSteel == 0:
                print("You didn't manage to collect anything...\n")
            else:
                print("You gathered",end=" ")
                if gatherWood!=0:
                    print(gatherWood,"wood",end="")
                    if gatherStone+gatherSteel!=0:
                        print(",",end=" ")
                if gatherStone!=0:
                    print(gatherStone,"stone",end="")
                    if gatherSteel!=0:
                        print(",",gatherSteel,"steel",end="")
                print(".\n")
            yourWood += gatherWood
            yourStone += gatherStone
            yourSteel += gatherSteel
            
    elif ln=="explore":
        if inCombat:
            print("You can not use this command while in combat!\nYou want to explore the many ways you can die?\n")
        else:
            rndm = round(3*math.sqrt(random.randint(1,6+4*trackClues+2*yourLvl)))
            if rndm==1:
                print("You find a sword stabbed into a stone.")
                if random.randint(0,9)==0:
                    print("You manage to pry it out...")
                    print("It's just the bottom half of a sword.")
                    print("+2 steel\n")
                    yourSteel+=2
                else:
                    print("You try pry it out, but fail. Maybe come back later.\n")
            elif rndm in [2,3,4,5]:
                print("You come across an abundance of resources.")
                gatherWood = random.randint(2,5)
                gatherStone = random.randint(1,3)
                print("+",gatherWood," wood",sep="")
                print("+",gatherStone," stone",sep="")
                print()
                yourWood+=gatherWood
                yourStone+=gatherStone
            elif rndm in [6,7]:
                print("You find a lost pouch of silver laying on the ground.")
                choice=""
                while (choice!="yes")and(choice!="no"):
                    choice = input("Do you want to pick it up? (yes/no)\n").lower()
                if choice=="yes":
                    print("You pick up the pouch, and find 7 silver pieces inside!")
                    print("+7 silver pieces\n")
                    yourSilver+=7
                else:
                    print("You continue walking and leave the pouch behind.\n")
            else:
                if rndm==8:
                    print("You hear a howling in the woods...")
                    print("A wolf jumps out to attack you!")
                    print("You\'re now in combat.")
                    inCombat = True
                    oppName = "wolf"
                elif rndm in [9,10]:
                    print("You encounter a goblin camp!")
                    print("A goblin runs at you in aims of protecting the camp.")
                    print("You\'re now in combat.")
                    inCombat = True
                    oppName = "goblin"
                elif rndm==11:
                    print("You encounter a goblin camp!")
                    print("A goblin begins shooting you from the border of the camp.")
                    print("You\'re now in combat.")
                    inCombat = True
                    oppName = "archer goblin"
                elif rndm==12:
                    print("The ground shakes a bit as this beast walks...")
                    print("A furious ork crosses your path!")
                    print("You\'re now in combat.")
                    inCombat = True
                    oppName = "ork"
                elif rndm==13:
                    print("You find a lost pouch of silver laying on the ground.")
                    choice=""
                    while (choice!="yes")and(choice!="no"):
                        choice = input("Do you want to pick it up? (yes/no)\n").lower()
                    if choice=="yes":
                        print("You bend down to pick up the pouch, but it vanishes! An illusion!")
                        print("A being, who emanates corrupt energy, approaches you from behind a tree.")
                        print("The blade of their scythe glimmers in the sunlight.")
                        print("You\'re now in combat.")
                        inCombat = True
                    else:
                        print("You continue walking and leave the pouch behind.\n")
                    oppName = "corrupted hunter"
                elif rndm==14:
                    print("You come across an isolated tower made of stone brick;")
                    print("a perfect place for someone studying magic...")
                    print("A powerful warlock, emanating corrupt energy, walks out the door.")
                    print("You\'re now in combat.")
                    inCombat = True
                    oppName = "corrupted warlock"
                else:
                    print("The sky turned dark for a moment... a thunderous roar fills your ear.")
                    print("THUD; the blood red dragon lands in front you; flames escaping its jaw.")
                    print("You\'re now in combat.")
                    trackClues = 0
                    inCombat = True
                    oppName = "dragon"
                if inCombat:
                    #Combat statis effects
                    yourBurning = False
                    yourCorrosion = 0
                    oppBurning = False
                    oppCorrosion = 0
                    useCompactShield = False
                    useAmplifier = False
                    useEchoingHilt = False
                    dmgEchoingHilt = 0
                    useFireQuiver = False
                    useCursedPin = False
                    isOppTurn = False
                    oppCharged = 3
                    #[Base HP] [+Level Hp] [+Level Dmg] [Defense]
                    #Opponent's stats
                    oppIndex = listEnemies.index(oppName)
                    oppMaxHP = normRound(dictEnyStats[oppIndex][0] +yourLvl*dictEnyStats[oppIndex][1])
                    oppHP = oppMaxHP
                    oppDmg = normRound(yourLvl*dictEnyStats[oppIndex][2])
                    oppDef = normRound(dictEnyStats[oppIndex][3])
                    print("The ",oppName,"\'s HP: ",oppHP,"/",oppMaxHP,sep="",)
                print()
                    
    elif ln=="track":
        if inCombat:
            print("You can not use this command while in combat!\nFocus on the situation at hand.\n")
        else:
            rndm = random.randint(1,14)
            if rndm in [1,2,3,4,5,6]:
                print("You find some claw marks on a boulder.")
                print("+1 clue\n")
                trackClues += 1
            elif rndm in [7,8,9,10]:
                print("A layer of soot covers a nearby patch of grass.")
                print("+1 clue\n")
                trackClues += 1
            elif rndm in [11]:
                print("Something glimmers in your eyes; light reflecting off a shed dragon scale.")
                print("+1 clue\n+1 dragon scale\n")
                trackClues += 1
                yourScales += 1
            elif rndm in [12,13,14]:
                print("You hear a deafening roar in the distance.")
                print("+2 clues\n")
                trackClues += 2
                
    elif ln=="chat":
        if inCombat:
            print("You can not use this command while in combat!\nExcuse me? You want to chat with your enemy?\n")
        else:
            rndm = random.randint(1,10)
            if rndm in [1,2,3,4,5]:
                print("You chat with one of the locals. The conversation was relaxing, but not very valuable.\n")
            elif rndm==6:
                print("You chat with a hunter. They give you information about the dragon.")
                print("+2 clues\n")
                trackClues += 2
            elif rndm==7:
                print("You chat with a farmer. They gladly give you their spare wood.")
                print("+4 wood\n")
                yourWood += 4
            elif rndm==8:
                print("You chat with the blacksmith. They have some impure steel they don't need.")
                print("+1 stone\n+1 steel\n")
                yourStone += 1
                yourSteel += 1
            elif rndm==9:
                print("You chat with the alchemist. They pity you, and give you healing potions.")
                print("+3 healing potions\n")
                yourPotions += 3
            elif rndm==10:
                print("You chat with a roaming child. They say, \"What do you call a fly without wings?\"")
                print("\"A walk! Hahahaha!\"\n")
                
    # Shopping commands
    elif ln=="shop":
        if inCombat:
            print("You can not use this command while in combat!\nThe battlefield is not a casual shopping market!\n")
        else:
            print("===Shop===")
            print("Note: When you sell items, you get half the price back, rounded down.")
            # Resources
            print("Resources:")
            print("-Wood: 2 silver\n-Stone: 4 silver\n-Steel: 16 silver\n-DragonScales: 50 silver")
            print("-HealingPotion (heals 20HP): 5 silver")
            # Armour
            print("Armour (You can only have 1 armour set at a time):")
            print("-LeatherArmour (1 def): 15 silver\n-StuddedLeatherArmour (2 def): 20 silver")
            print("-ChainShirt (3 def): 27 silver\n-Breastplate (4 def): 36 silver")
            print("-SplintArmour (5 def): 47 silver\n-FullPlateArmour (6 def): 60 silver")
            # Weapons
            print("Weapons (You can only have 1 weapon at a time):")
            # price = rounded up( ( avg dmg / 2)^2 )
            print("-ShortSword (2-4 dmg): 3 silver\n-ShortBow (3-7 dmg): 7 silver\n-Scroll (6 dmg): 9 silver")
            print("-Dagger (5-7 dmg): 9 silver\n-Sling (6-10 dmg): 16 silver\n-Grimoire (9 dmg): 21 silver")
            print("-Rapier (8-10 dmg): 21 silver\n-LightCrossbow (8-12 dmg): 25 silver\n-EnchantedAmulet (11 dmg): 31 silver")
            print("-LongSword (11-13 dmg): 36 silver\n-HeavyCrossbow (11-15 dmg): 43 silver\n-ElementalOrb (14 dmg): 49 silver")
            print("-Claymore (15-17 dmg): 64 silver\n-LongBow (14-18 dmg): 64 silver\n-RunicStone (16 dmg): 64 silver")
            # Artefacts
            print("Artefacts:")
            print("-CompactShield (+2 Def. Use only once): 10 silver")
            print("-VitalityGem (Heals 5xLvl HP): 15 silver")
            print("-SolarCanon (Does 3xLvl dmg) (no effect from FireQuiver): 20 silver")
            print("-CamoCloak (Allows you to retreat with 2/3 success rate): 20 silver")
            print("-Amplifier (+2xDef as dmg for your next \"attack\"): 25 silver")
            print("-EchoingHilt (Your next melee attack gets +dmg for the dmg you take this turn): 30 silver")
            print("-FireQuiver (Your next ranged attack applies the Burning effect) 30 :silver") #Burning is +3dmg
            print("-CursedPin (Your next magical attack applies a stack of Corrosion) 30 :silver") #Corrosion is -2def
            print()
            
    elif ln[:4]=="buy ":
        if inCombat:
            print("You can not use this command while in combat!\nBribing your enemy to leave you alone won't work here.\n")
            continue
        posSpace = (ln+" ").index(" ",4)
        buyItem = ln[4:posSpace]
        # Buying resources
        if buyItem in listResources:
            buyIndex = listResources.index(buyItem)
            if ln=="buy "+buyItem:
                buyQuantity = 1
            else:
                try:
                    buyQuantity = int(ln[posSpace+1:])
                    if buyQuantity<0:
                        buyQuantity = 1
                except:
                    buyQuantity = 1
            buyPrice = listResCost[buyIndex]*buyQuantity
            if yourSilver>=buyPrice:
                print("You bought ",buyQuantity," ",buyItem,", for ",buyPrice," silver pieces.\n",sep="")
                yourSilver -= buyPrice
                if buyItem=="wood":
                    yourWood += buyQuantity
                elif buyItem=="stone":
                    yourStone += buyQuantity
                elif buyItem=="steel":
                    yourSteel += buyQuantity
                elif buyItem=="dragonscale":
                    yourScales += buyQuantity
                elif buyItem=="healingpotion":
                    yourPotions += buyQuantity
            else:
                print("You need",buyPrice-yourSilver,"more silver pieces.\n")
        # Buying armour
        elif buyItem in listArmour:
            buyIndex = listArmour.index(buyItem)
            buyPrice = listAmrCost[buyIndex]
            sellPrice = listAmrCost[listArmour.index(yourArmour)]//2
            if yourSilver+sellPrice>=buyPrice:
                if not(yourArmour=="none"):
                    print("You sold your ",yourArmour,", for ",sellPrice," silver pieces.",sep="")
                    yourSilver+=sellPrice
                print("You bought ",buyItem,", for ",buyPrice," silver pieces.\n",sep="")
                yourSilver-=buyPrice
                yourArmour = buyItem
            else:
                print("You need",buyPrice-yourSilver-sellPrice,"more silver pieces.\n")
        # Buying weapons
        elif buyItem in listWeapons:
            buyIndex = listWeapons.index(buyItem)
            buyPrice = listWpnCost[buyIndex]
            sellPrice = listWpnCost[listWeapons.index(yourWeapon)]//2
            if yourSilver+sellPrice>=buyPrice:
                if not(yourWeapon=="none"):
                    print("You sold your ",yourWeapon,", for ",sellPrice," silver pieces.",sep="")
                    yourSilver+=sellPrice
                print("You bought ",buyItem,", for ",buyPrice," silver pieces.\n",sep="")
                yourSilver-=buyPrice
                yourWeapon = buyItem
            else:
                print("You need",buyPrice-yourSilver-sellPrice,"more silver pieces.\n")
        # Buying artefacts
        elif buyItem in listArtefacts:
            buyIndex = listArtefacts.index(buyItem)
            if hasArtefact[buyIndex]:
                print("You already have a ",buyItem,".\n",sep="")
            else:
                buyPrice = listArtCost[buyIndex]
                if yourSilver>=buyPrice:
                    print("You bought ",buyItem,", for ",buyPrice," silver pieces.\n",sep="")
                    yourSilver-=buyPrice
                    hasArtefact[buyIndex] = True
                else:
                    print("You need",buyPrice-yourSilver,"more silver pieces.\n")
        # Failed to buy item
        else:
            print("The item \"",buyItem,"\" was not recognised.\n",sep="")
            
    elif ln[:5]=="sell ":
        if inCombat:
            print("You can not use this command while in combat!\nYour property is not enough, your enemy wants your life.\n")
            continue
        posSpace = (ln+" ").index(" ",5)
        sellItem = ln[5:posSpace]
        # Selling resources
        if sellItem in listResources:
            sellIndex = listResources.index(sellItem)
            if ln=="sell "+sellItem:
                sellQuantity = 1
            else:
                try:
                    sellQuantity = int(ln[posSpace+1:])
                    if sellQuantity<0:
                        sellQuantity = 1
                except:
                    sellQuantity = 1
            sellPrice = (listResCost[sellIndex]//2)*sellQuantity
            sellSuccess = False
            if sellItem=="wood":
                if yourWood>=sellQuantity:
                    yourWood-=sellQuantity
                    sellSuccess = True
                else:
                    print("You don\'t have enough wood.\n")
            elif sellItem=="stone":
                if yourStone>=sellQuantity:
                    yourStone-=sellQuantity
                    sellSuccess = True
                else:
                    print("You don\'t have enough stone.\n")
            elif sellItem=="steel":
                if yourSteel>=sellQuantity:
                    yourSteel-=sellQuantity
                    sellSuccess = True
                else:
                    print("You don\'t have enough steel.\n")
            elif sellItem=="dragonscale":
                if yourScales>=sellQuantity:
                    yourScales-=sellQuantity
                    sellSuccess = True
                else:
                    print("You don\'t have enough dragonscales.\n")
            elif sellItem=="healingpotion":
                if yourPotions>=sellQuantity:
                    yourPotions-=sellQuantity
                    sellSuccess = True
                else:
                    print("You don\'t have enough healingpotions.\n")
            if sellSuccess:
                print("You sold ",sellQuantity," ",sellItem,", for ",sellPrice," silver pieces.\n",sep="")
                yourSilver+=sellPrice
        # Selling armour
        elif sellItem in listArmour:
            sellIndex = listArmour.index(sellItem)
            sellPrice = listAmrCost[sellIndex]//2
            if yourArmour==sellItem:
                print("You sold your ",yourArmour,", for ",sellPrice," silver pieces.\n",sep="")
                yourSilver+=sellPrice
                yourArmour = "none"
            else:
                print("You don\'t have ",sellItem,".\n",sep="")
        # Selling weapons
        elif sellItem in listWeapons:
            sellIndex = listWeapons.index(sellItem)
            sellPrice = listWpnCost[sellIndex]//2
            if yourWeapon==sellItem:
                print("You sold your ",yourWeapon,", for ",sellPrice," silver pieces.\n",sep="")
                yourSilver+=sellPrice
                yourWeapon = "none"
            else:
                print("You don\'t have ",sellItem,".\n",sep="")
        # Selling artefacts
        elif sellItem in listArtefacts:
            sellIndex = listArtefacts.index(sellItem)
            if hasArtefact[sellIndex]:
                sellPrice = listArtCost[sellIndex]//2
                print("You sold your ",sellItem,", for ",sellPrice," silver pieces.\n",sep="")
                yourSilver+=sellPrice
                hasArtefact[sellIndex] = False
            else:
                print("You don\'t have a ",sellItem,".\n",sep="")
        # Failed to sell item
        else:
            print("The item \"",sellItem,"\" was not recognised.\n",sep="")
            
    # Crafting commands
    elif ln=="craft":
        if inCombat:
            print("You can not use this command while in combat!\nTrying to be crafty, I see?\n")
        else:
            print("===Crafting===")
            # Resources
            print("Resources:")
            print("-Steel: 5 Stone")
            # Armour
            print("Armour (You can only have 1 armour set at a time):")
            print("-ChainShirt (3 def): 3 Steel")
            print("-SplintArmour (5 def): 4 Steel and 5 Wood")
            print("-DragonArmour (9 def)(immune to Burning): 4 DragonScales")
            # Weapons
            print("Weapons (You can only have 1 weapon at a time):")
            print("-Dagger (5-7 dmg): 1 Steel")
            print("-Sling (6-10 dmg): 1 Steel and 1 Wood")
            print("-Grimoire (9 dmg): 1 Steel and 10 Wood")
            print("-LongSword (11-13 dmg): 3 Steel and 5 Wood")
            print("-HeavyCrossbow (11-15 dmg): 2 Steel and 20 Wood")
            print("-ElementalOrb (14 dmg): 4 Steel and 7 Wood")
            print()
            
    elif ln[:6]=="craft ":
        if inCombat:
            print("You can not use this command while in combat!\nTrying to be crafty, I see?\n")
        else:
            posSpace = (ln+" ").index(" ",6)
            craftItem = ln[6:posSpace]
            if craftItem=="steel":
                if ln=="craft "+craftItem:
                    craftQuantity = 1
                else:
                    try:
                        craftQuantity = int(ln[posSpace+1:])
                        if craftQuantity<0:
                            craftQuantity = 1
                    except:
                        craftQuantity = 1
                if yourStone>=5*craftQuantity:
                    print("You crafted",craftQuantity,"steel with",5*craftQuantity,"stone.\n")
                    yourStone-=5*craftQuantity
                    yourSteel+=craftQuantity
                else:
                    print("You need",5*craftQuantity-yourStone,"more stone.\n")
                
            elif craftItem=="chainshirt":
                if yourSteel>=3:
                    if yourArmour!="none":
                        sellPrice = listAmrCost[listArmour.index(yourArmour)]//2
                        print("You sold your",yourArmour,"for",sellPrice,"silver.")
                        yourSilver+=sellPrice
                    print("You crafted chainshirt with 3 steel.\n")
                    yourSteel-=3
                    yourArmour = "chainshirt"
                else:
                    print("You need",3-yourSteel,"more steel.\n")
                
            elif craftItem=="splintarmour":
                if yourSteel>=4:
                    if yourWood>=5:
                        if yourArmour!="none":
                            sellPrice = listAmrCost[listArmour.index(yourArmour)]//2
                            print("You sold your",yourArmour,"for",sellPrice,"silver.")
                            yourSilver+=sellPrice
                        print("You crafted splintarmour with 4 steel and 5 wood.\n")
                        yourSteel-=4
                        yourWood-=5
                        yourArmour = "splintarmour"
                    else:
                        print("You need",5-yourWood,"more wood.\n")
                else:
                    print("You need",4-yourSteel,"more steel.\n")
                
            elif craftItem=="dragonarmour":
                if yourScales>=4:
                    if yourArmour!="none":
                        sellPrice = listAmrCost[listArmour.index(yourArmour)]//2
                        print("You sold your",yourArmour,"for",sellPrice,"silver.")
                        yourSilver+=sellPrice
                    print("You crafted dragonarmour with 4 dragonscale.\n")
                    yourScales-=4
                    yourArmour = "dragonarmour"
                else:
                    print("You need",3-yourScales,"more dragonscales.\n")
                
            elif craftItem=="dagger":
                if yourSteel>=1:
                    if yourWeapon!="none":
                        sellPrice = listWpnCost[listWeapons.index(yourWeapon)]//2
                        print("You sold your",yourWeapon,"for",sellPrice,"silver.")
                        yourSilver+=sellPrice
                    print("You crafted dagger with 1 steel.\n")
                    yourSteel-=1
                    yourWeapon = "dagger"
                else:
                    print("You need",1-yourSteel,"more steel.\n")
                
            elif craftItem=="sling":
                if yourSteel>=1:
                    if yourWood>=1:
                        if yourWeapon!="none":
                            sellPrice = listWpnCost[listWeapons.index(yourWeapon)]//2
                            print("You sold your",yourWeapon,"for",sellPrice,"silver.")
                            yourSilver+=sellPrice
                        print("You crafted sling with 1 steel and 1 wood.\n")
                        yourSteel-=1
                        yourWood-=1
                        yourWeapon = "sling"
                    else:
                        print("You need",1-yourWood,"more wood.\n")
                else:
                    print("You need",1-yourSteel,"more steel.\n")
                
            elif craftItem=="grimoire":
                if yourSteel>=1:
                    if yourWood>=10:
                        if yourWeapon!="none":
                            sellPrice = listWpnCost[listWeapons.index(yourWeapon)]//2
                            print("You sold your",yourWeapon,"for",sellPrice,"silver.")
                            yourSilver+=sellPrice
                        print("You crafted grimoire with 1 steel and 10 wood.\n")
                        yourSteel-=1
                        yourWood-=10
                        yourWeapon = "grimoire"
                    else:
                        print("You need",10-yourWood,"more wood.\n")
                else:
                    print("You need",1-yourSteel,"more steel.\n")
                
            elif craftItem=="longsword":
                if yourSteel>=3:
                    if yourWood>=5:
                        if yourWeapon!="none":
                            sellPrice = listWpnCost[listWeapons.index(yourWeapon)]//2
                            print("You sold your",yourWeapon,"for",sellPrice,"silver.")
                            yourSilver+=sellPrice
                        print("You crafted longsword with 3 steel and 5 wood.\n")
                        yourSteel-=3
                        yourWood-=5
                        yourWeapon = "longsword"
                    else:
                        print("You need",5-yourWood,"more wood.\n")
                else:
                    print("You need",3-yourSteel,"more steel.\n")
                
            elif craftItem=="heavycrossbow":
                if yourSteel>=2:
                    if yourWood>=20:
                        if yourWeapon!="none":
                            sellPrice = listWpnCost[listWeapons.index(yourWeapon)]//2
                            print("You sold your",yourWeapon,"for",sellPrice,"silver.")
                            yourSilver+=sellPrice
                        print("You crafted heavycrossbow with 2 steel and 20 wood.\n")
                        yourSteel-=2
                        yourWood-=20
                        yourWeapon = "heavycrossbow"
                    else:
                        print("You need",20-yourWood,"more wood.\n")
                else:
                    print("You need",2-yourSteel,"more steel.\n")
                
            elif craftItem=="elementalorb":
                if yourSteel>=4:
                    if yourWood>=7:
                        if yourWeapon!="none":
                            sellPrice = listWpnCost[listWeapons.index(yourWeapon)]//2
                            print("You sold your",yourWeapon,"for",sellPrice,"silver.")
                            yourSilver+=sellPrice
                        print("You crafted elementalorb with 4 steel and 7 wood.\n")
                        yourSteel-=4
                        yourWood-=7
                        yourWeapon = "elementalorb"
                    else:
                        print("You need",7-yourWood,"more wood.\n")
                else:
                    print("You need",4-yourSteel,"more steel.\n")
                
            elif craftItem=="mine":
                print("Did you mean Minecraft!?\n")
            else:
                print("The item \"",craftItem,"\" can\'t be crafted.\n",sep="")
    
    elif ln=="attack":
        if not(inCombat):
            print("You can not use this command while outside of combat!\nAttack who? Attack what? Don\'t be so aggressive.\n")
        else:
            print("You attack using your ",yourWeapon,"!",sep="")
            isOppTurn = True
            #["compactshield","vitalitygem","solarcanon","camocloak","amplifier","echoinghilt","firequiver","cursedpin"]
            wpnIndex = listWeapons.index(yourWeapon)
            wpnMax = listWpnDmgMax[wpnIndex]
            wpnMin = listWpnDmgMin[wpnIndex]
            totDmg = random.randint(wpnMin,wpnMax)
            dmgString = "["+str(totDmg)+"]"
            totDmg+=yourLvl
            dmgString = dmgString+"+"+str(yourLvl)
            if useAmplifier:
                useAmplifier = False
                print("Your amplifier is unleashed!")
                # Calculating defense
                currentDef = listAmrDef[listArmour.index(yourArmour)]
                if useCompactShield:
                    currentDef+=2
                currentDef-=2*yourCorrosion
                if currentDef<0:
                    currentDef = 0
                # Applying defense
                totDmg+=2*currentDef
                dmgString = dmgString+"+"+str(2*currentDef)
            wpnCategory = wpnIndex%3
            if hasArtefact[listArtefacts.index("echoinghilt")] and wpnCategory==1:
                if dmgEchoingHilt==0:
                    print("Your EchoingHilt is not vibrating.")
                    dmgString = dmgString+"+0"
                else:
                    print("The vibration of your EchoingHilt empowers your strike!")
                    totDmg+=dmgEchoingHilt
                    dmgString = dmgString+"+"+str(dmgEchoingHilt)
                    dmgEchoingHilt = 0
            if oppBurning:
                print("Flames eat away at your opponent\'s flesh.")
                totDmg+=3
                dmgString = dmgString+"+3"
            print(dmgString)
            print("=",totDmg,"damage")
            oppCurrentDef = oppDef -2*oppCorrosion
            if oppCurrentDef<0:
                oppCurrentDef = 0
            totDmg-=oppCurrentDef
            if totDmg<0:
                totDmg = 0
            print("The",oppName,"takes",totDmg,"damage.")
            oppHP-=totDmg
            if oppHP<0:
                oppHP = 0
            print("The ",oppName,"\'s HP: ",oppHP,"/",oppMaxHP,sep="")
            if (wpnCategory==2)and(useFireQuiver):
                if oppName=="dragon":
                    print("The fire of your attack doesn\'t affect the dragon..")
                else:
                    print("Your flaming projectiles from your FireQuiver set your opponent alight!")
                    oppBurning = True
                useFireQuiver = False
            if (wpnCategory==0)and(useCursedPin):
                if (oppName=="corrupted hunter")or(oppName=="corrupted warlock"):
                    print("Curses do not affect the souls of those who are already corrupt.")
                else:
                    print("Magic soaks into your opponents flesh... their flesh begins to corrode and wither.")
                    oppCorrosion+=1
                useCursedPin = False
            print()
    
    elif ln=="heal":
        if not(inCombat):
            print("You can not use this command while outside of combat!\nYou and I should both know that you shouldn't waste your potions.\n")
        else:
            if yourPotions<1:
                print("You don't have any more healing potions...\n")
            else:
                print("You chug down a healing potion, restoring up to 20HP!")
                yourPotions-=1
                isOppTurn = True
                yourHP+=20
                if yourHP>yourMaxHP:
                    yourHP = yourMaxHP
                print("Your HP: ",yourHP,"/",yourMaxHP,sep="")
                # Side Burning
                if oppBurning:
                    print("Flames eat away at your opponent\'s flesh.")
                    oppCurrentDef = oppDef -2*oppCorrosion
                    if oppCurrentDef<0:
                        oppCurrentDef = 0
                    totDmg = 3-oppCurrentDef
                    if totDmg<0:
                        totDmg = 0
                    print("The",oppName,"takes",totDmg,"damage.")
                    oppHP-=totDmg
                    if oppHP<0:
                        oppHP = 0
                    print("The ",oppName,"\'s HP: ",oppHP,"/",oppMaxHP,"\n",sep="")
                print()            
    elif ln in listArtefacts:
        if not(inCombat):
            print("You can not use this command while outside of combat!\nUsing artefacts outside of combat is pointless.\n")
        else:
            artIndex = listArtefacts.index(ln)
            if not(hasArtefact[artIndex]):
                print("You don't have a ",ln,".\n",sep="")
            else:
                #["compactshield","vitalitygem","solarcanon","camocloak","amplifier","echoinghilt","firequiver","cursedpin"]
                if ln=="compactshield":
                    if useCompactShield:
                        print("You are already holding your compactshield.\n")
                    else:
                        print("You pull out and expand your compactshield!")
                        isOppTurn = True
                        useCompactShield = True
                        # Side Burning
                        if oppBurning:
                            print("Flames eat away at your opponent\'s flesh.")
                            oppCurrentDef = oppDef -2*oppCorrosion
                            if oppCurrentDef<0:
                                oppCurrentDef = 0
                            totDmg = 3-oppCurrentDef
                            if totDmg<0:
                                totDmg = 0
                            print("The",oppName,"takes",totDmg,"damage.")
                            oppHP-=totDmg
                            if oppHP<0:
                                oppHP = 0
                            print("The ",oppName,"\'s HP: ",oppHP,"/",oppMaxHP,sep="")
                        print()
                elif ln=="vitalitygem":
                    if yourHP==yourMaxHP:
                        print("You are already at full health.\n")
                    else:
                        print("The gem glows, and you feel your wounds closing.")
                        isOppTurn = True
                        print("You were healed ",5*yourLvl,"HP!",sep="")
                        yourHP+=5*yourLvl
                        if yourHP>yourMaxHP:
                            yourHP = yourMaxHP
                        print("Your HP: ",yourHP,"/",yourMaxHP,sep="")
                        # Side Burning
                        if oppBurning:
                            print("Flames eat away at your opponent\'s flesh.")
                            oppCurrentDef = oppDef -2*oppCorrosion
                            if oppCurrentDef<0:
                                oppCurrentDef = 0
                            totDmg = 3-oppCurrentDef
                            if totDmg<0:
                                totDmg = 0
                            print("The",oppName,"takes",totDmg,"damage.")
                            oppHP-=totDmg
                            if oppHP<0:
                                oppHP = 0
                            print("The ",oppName,"\'s HP: ",oppHP,"/",oppMaxHP,sep="")
                        print()
                elif ln=="solarcanon":
                    print("You shoot a beam of light using your SolarCanon!")
                    isOppTurn = True
                    totDmg = 3*yourLvl
                    dmgString = "["+str(totDmg)+"]"
                    totDmg+=yourLvl
                    dmgString = dmgString+"+"+str(yourLvl)
                    if useAmplifier:
                        useAmplifier = False
                        print("Your amplifier is unleashed!")
                        # Calculating defense
                        currentDef = listAmrDef[listArmour.index(yourArmour)]
                        if useCompactShield:
                            currentDef+=2
                        currentDef-=2*yourCorrosion
                        if currentDef<0:
                            currentDef = 0
                        # Applying defense
                        totDmg+=2*currentDef
                        dmgString = dmgString+"+"+str(2*currentDef)
                    if oppBurning:
                        print("Flames eat away at your opponent\'s flesh.")
                        totDmg+=3
                        dmgString = dmgString+"+3"
                    print(dmgString)
                    print("=",totDmg,"damage")
                    oppCurrentDef = oppDef -2*oppCorrosion
                    if oppCurrentDef<0:
                        oppCurrentDef = 0
                    totDmg-=oppCurrentDef
                    if totDmg<0:
                        totDmg = 0
                    print("The",oppName,"takes",totDmg,"damage.")
                    oppHP-=totDmg
                    if oppHP<0:
                        oppHP = 0
                    print("The ",oppName,"\'s HP: ",oppHP,"/",oppMaxHP,sep="")
                    print()
                elif ln=="camocloak":
                    print("You surround yourself with your cloak!")
                    print("You dash behind cover; attempting to escape your enemy!")
                    # Side Burning
                    if oppBurning:
                        print("Flames eat away at your opponent\'s flesh.")
                        oppCurrentDef = oppDef -2*oppCorrosion
                        if oppCurrentDef<0:
                            oppCurrentDef = 0
                        totDmg = 3-oppCurrentDef
                        if totDmg<0:
                            totDmg = 0
                        print("The",oppName,"takes",totDmg,"damage.")
                        oppHP-=totDmg
                        if oppHP<0:
                            oppHP = 0
                        print("The ",oppName,"\'s HP: ",oppHP,"/",oppMaxHP,sep="")                    
                    isOppTurn = True
                    rndm = random.randint(0,2)
                    if rndm < 2:
                        print("The",oppName,"could not find you. You escaped combat.\n")
                        inCombat = False
                        if (random.randint(1,3)==3)and(oppName=="dragon"):
                            print("You collected a scale from the dragon!\n+1 dragon scale")
                            yourScales+=1
                    else:
                        print("The",oppName,"was too perceptive. You couldn't hide from them.\n")
                elif ln=="amplifier":
                    print("You charge up your amplifier in preparation of your next attack!")
                    isOppTurn = True
                    useAmplifier = True
                    # Side Burning
                    if oppBurning:
                        print("Flames eat away at your opponent\'s flesh.")
                        oppCurrentDef = oppDef -2*oppCorrosion
                        if oppCurrentDef<0:
                            oppCurrentDef = 0
                        totDmg = 3-oppCurrentDef
                        if totDmg<0:
                            totDmg = 0
                        print("The",oppName,"takes",totDmg,"damage.")
                        oppHP-=totDmg
                        if oppHP<0:
                            oppHP = 0
                        print("The ",oppName,"\'s HP: ",oppHP,"/",oppMaxHP,sep="")
                    print()
                elif ln=="echoinghilt":
                    print("You grasp your echoinghilt tightly; bracing for an attack!")
                    isOppTurn = True
                    useEchoingHilt = True
                    # Side Burning
                    if oppBurning:
                        print("Flames eat away at your opponent\'s flesh.")
                        oppCurrentDef = oppDef -2*oppCorrosion
                        if oppCurrentDef<0:
                            oppCurrentDef = 0
                        totDmg = 3-oppCurrentDef
                        if totDmg<0:
                            totDmg = 0
                        print("The",oppName,"takes",totDmg,"damage.")
                        oppHP-=totDmg
                        if oppHP<0:
                            oppHP = 0
                        print("The ",oppName,"\'s HP: ",oppHP,"/",oppMaxHP,sep="")
                    print()
                elif ln=="firequiver":
                    print("You draw a projectile from your firequiver. The projectile is soon to set ablaze!")
                    isOppTurn = True
                    useFireQuiver = True
                    # Side Burning
                    if oppBurning:
                        print("Flames eat away at your opponent\'s flesh.")
                        oppCurrentDef = oppDef -2*oppCorrosion
                        if oppCurrentDef<0:
                            oppCurrentDef = 0
                        totDmg = 3-oppCurrentDef
                        if totDmg<0:
                            totDmg = 0
                        print("The",oppName,"takes",totDmg,"damage.")
                        oppHP-=totDmg
                        if oppHP<0:
                            oppHP = 0
                        print("The ",oppName,"\'s HP: ",oppHP,"/",oppMaxHP,sep="")
                    print()
                elif ln=="cursedpin":
                    print("Tapping the cursed pin; you feel dark magic seep form it.")
                    isOppTurn = True
                    useCursedPin = True
                    # Side Burning
                    if oppBurning:
                        print("Flames eat away at your opponent\'s flesh.")
                        oppCurrentDef = oppDef -2*oppCorrosion
                        if oppCurrentDef<0:
                            oppCurrentDef = 0
                        totDmg = 3-oppCurrentDef
                        if totDmg<0:
                            totDmg = 0
                        print("The",oppName,"takes",totDmg,"damage.")
                        oppHP-=totDmg
                        if oppHP<0:
                            oppHP = 0
                        print("The ",oppName,"\'s HP: ",oppHP,"/",oppMaxHP,sep="")
                    print()
                else:
                    print("There was an error processing this artifact command.\n")
    elif ln=="retreat":
        if not(inCombat):
            print("You can not use this command while outside of combat!\nWhat... are you retreating from? Crippling debt?\n")
        else:
            if hasArtefact[listArtefacts.index("camocloak")]:
                print("You surround yourself with your cloak!")
                escapeChance = 2
            else:
                escapeChance = 1
            print("You dash behind cover; attempting to escape your enemy!")
            # Side Burning
            if oppBurning:
                print("Flames eat away at your opponent\'s flesh.")
                oppCurrentDef = oppDef -2*oppCorrosion
                if oppCurrentDef<0:
                    oppCurrentDef = 0
                totDmg = 3-oppCurrentDef
                if totDmg<0:
                    totDmg = 0
                print("The",oppName,"takes",totDmg,"damage.")
                oppHP-=totDmg
                if oppHP<0:
                    oppHP = 0
                print("The ",oppName,"\'s HP: ",oppHP,"/",oppMaxHP,"\n",sep="")            
            isOppTurn = True
            rndm = random.randint(0,2)
            if rndm < escapeChance:
                print("The",oppName,"could not find you. You escaped combat.")
                inCombat = False
                if (random.randint(1,3)==3)and(oppName=="dragon"):
                    print("You collected a scale from the dragon!\n+1 dragon scale")
                    yourScales+=1
            else:
                print("The",oppName,"was too perceptive. You couldn't hide from them.")
            print()
    
    elif ln!="exit":
        print("^ This command is not recognised.\n")
    
    #Opponents turn
    if inCombat and isOppTurn:
        isOppTurn = False
        if oppHP==0:
            print("You successfully killed the ",oppName,"!",sep="")
            inCombat = False
            yourCorrosion = 0
            if oppName=="dragon":
                print("You did it... your grand quest is complete.")
                print("Through blood, sweat and tears you overcame a nearly impossible challenge.")
                print("Thank you for playing.")
                break
            else:
                if oppName=="wolf":
                    earnedSilver = 0
                elif (oppName=="goblin")or(oppName=="goblin archer"):
                    earnedSilver = random.randint(5,10)
                elif oppName=="ork":
                    earnedSilver = random.randint(7,12)
                elif oppName=="corrupted hunter":
                    earnedSilver = random.randint(12,15)
                elif oppName=="corrupted warlock":
                    earnedSilver = random.randint(9,12)
                print("You gained",earnedSilver,"silver from the fight.")
                yourSilver+=earnedSilver
                print("You levelled up to level ",yourLvl+1,"!\n",sep="")
                yourLvl+=1
                yourMaxHP+=5
                yourHP+=5
        else:
            if oppCharged!=3:
                print("<) The ",oppName," attacks you with their ",dictEnyMoves[oppIndex][oppCharged],"!",sep="")
                atkIndex = listEnyAttacks.index(dictEnyMoves[oppIndex][oppCharged])
                rndm = random.randint(listEnyDmgMin[atkIndex],listEnyDmgMax[atkIndex])
                dmgString = "["+str(rndm)+"]+"+str(oppDmg)
                totDmg = rndm+oppDmg
                if yourBurning:
                    print("Flames eat away at your flesh.")
                    totDmg+=3
                    dmgString = dmgString+"+3"
                print(dmgString," = ",totDmg," dmg",sep="")
                # Calculating defense
                currentDef = listAmrDef[listArmour.index(yourArmour)]
                if useCompactShield:
                    currentDef+=2
                currentDef-=2*yourCorrosion
                if currentDef<0:
                    currentDef = 0                
                totDmg-=currentDef
                if totDmg<0:
                    totDmg = 0
                print("You take",totDmg,"damage.")
                yourHP-=totDmg
                if yourHP<0:
                    yourHP = 0
                print("Your HP: ",yourHP,"/",yourMaxHP,sep="")
                oppCharged = 3
                if useEchoingHilt:
                    if totDmg>0:
                        if dmgEchoingHilt>0:
                            print("The impact causes your EchoingHilt to vibrate more aggressively!")
                        else:
                            print("The impact causes your EchoingHilt to start vibrating!")
                        dmgEchoingHilt+=totDmg
                    else:
                        print("Your EchoingHilt absorbs no vibrations.")
                    useEchoingHilt = False
                if listEnyBurning[atkIndex]:
                    if yourArmour=="dragonarmour":
                        print("Flames attempt to linger on you, but your DragonArmour resists it!")
                    else:                    
                        print("Flames begin festering on your clothes!")
                        yourBurning = True
                if listEnyCorrosion[atkIndex]:
                    print("The dark corruption begins to corrode away at you!")
                    yourCorrosion+=1
                print()
            else:
                rndm = random.randint(0,2)
                atkIndex = listEnyAttacks.index(dictEnyMoves[oppIndex][rndm])
                if listEnyCharge[atkIndex]:
                    print("<) The ",oppName," charges up their ",listEnyAttacks[atkIndex],"!",sep="")
                    oppCharged = rndm
                    # Side Burning
                    if yourBurning:
                        print("Flames eat away at your flesh.")
                        # Calculating defense
                        currentDef = listAmrDef[listArmour.index(yourArmour)]
                        if useCompactShield:
                            currentDef+=2
                        currentDef-=2*yourCorrosion
                        if currentDef<0:
                            currentDef = 0
                        totDmg = 3-currentDef
                        if totDmg<0:
                            totDmg = 0
                        print("You take",totDmg,"damage.")
                        yourHP-=totDmg
                        if yourHP<0:
                            yourHP = 0
                        print("Your HP: ",yourHP,"/",yourMaxHP,sep="")
                    print()
                else:
                    print("<) The ",oppName," attacks you with their ",listEnyAttacks[atkIndex],"!",sep="")
                    rndm = random.randint(listEnyDmgMin[atkIndex],listEnyDmgMax[atkIndex])
                    dmgString = "["+str(rndm)+"]+"+str(oppDmg)
                    totDmg = rndm+oppDmg
                    if yourBurning:
                        print("Flames eat away at your flesh.")
                        totDmg+=3
                        dmgString = dmgString+"+3"
                    print(dmgString," = ",totDmg," dmg",sep="")
                    # Calculating defense
                    currentDef = listAmrDef[listArmour.index(yourArmour)]
                    if useCompactShield:
                        currentDef+=2
                    currentDef-=2*yourCorrosion
                    if currentDef<0:
                        currentDef = 0
                    totDmg-=currentDef
                    if totDmg<0:
                        totDmg = 0
                    print("You take",totDmg,"damage.")
                    yourHP-=totDmg
                    if yourHP<0:
                        yourHP = 0
                    print("Your HP: ",yourHP,"/",yourMaxHP,sep="")
                    if useEchoingHilt:
                        if totDmg>0:
                            if dmgEchoingHilt>0:
                                print("The impact causes your EchoingHilt to vibrate more aggressively!")
                            else:
                                print("The impact causes your EchoingHilt to start vibrating!")
                            dmgEchoingHilt+=totDmg
                        else:
                            print("Your EchoingHilt absorbs no vibrations.")
                        useEchoingHilt = False
                    if listEnyBurning[atkIndex]:
                        if yourArmour=="dragonarmour":
                            print("Flames attempt to linger on you, but your DragonArmour resists it!")
                        else:
                            print("Flames begin festering on your clothes!")
                            yourBurning = True
                    if listEnyCorrosion[atkIndex]:
                        print("The dark corruption begins to corrode away at you!")
                        yourCorrosion+=1
                    print()
            if yourHP==0:
                print("The",oppName,"has slayed you...")
                inCombat = False
                if yourLvl>=3:
                    yourMaxHP-=10
                    yourLvl-=2
                else:
                    yourMaxHP-=5*(yourLvl-1)
                    yourLvl = 1
                yourHP = yourMaxHP
                print("You respawn within the kingdom walls, at level ",yourLvl,".\n",sep="")

print("=====\nGaming session has ended.")
saveString = str(yourLvl)+"|"
saveString+=str(yourHP)+"|"
saveString+=yourWeapon+"|"
saveString+=yourArmour+"|"
saveString+=str(yourSilver)+"|"
saveString+=str(yourWood)+"|"
saveString+=str(yourStone)+"|"
saveString+=str(yourSteel)+"|"
saveString+=str(yourScales)+"|"
saveString+=str(yourPotions)+"|"
saveString+=str(trackClues)+"|"
for i in hasArtefact:
    if i:
        saveString+="1"
    else:
        saveString+="0"
saveString+="|"
print("Save data:\n"+saveString)
input()