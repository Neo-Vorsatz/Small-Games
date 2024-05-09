# Black Jack
# Neo Vorsatz
# 10 April 2023

import random

listValues = ["Ace","2","3","4","5","6","7","8","9","10","Jack","Queen","King"]
listSuits = ["Spades","Clubs","Hearts","Diamonds"]
dealerCards = []
yourCards = []

def newDeck():
    global listValues
    global listSuits
    global deck
    global dealerCards
    global yourCards
    deck = []
    for val in listValues:
        for suit in listSuits:
            deck+=[val+"-"+suit]
    dealerCards = []
    yourCards = []    

def drawCard():
    global deck
    if len(deck)==0:
        return "no cards"
    else:
        card = deck[random.randint(0,len(deck)-1)]
        deck.remove(card)
        return [card]

def cardVal(card):
    global listValues
    pos = card.index("-")
    strValue = card[:pos]
    if strValue in ["Jack","Queen","King"]:
        value = 10
    else:
        value = listValues.index(strValue)+1
    return value

def handVal(hand):
    value = 0
    numAce = 0
    for card in hand:
        if cardVal(card)==1:
            numAce+=1
            value+=11
        else:
            value+=cardVal(card)
    while (numAce>0)and(value>21):
        numAce-=1
        value-=10
    return value

def startGame():
    global deck
    global dealerCards
    global yourCards
    newDeck()
    print("===BLACK JACK===")
    print("Dealer:")
    dealerCards+=drawCard()
    dealerCards+=drawCard()
    print(dealerCards[0])
    print("?-?")
    print("Your Cards:")
    yourCards+=drawCard()
    yourCards+=drawCard()
    print(yourCards[0])
    print(yourCards[1])
    print(handVal(yourCards))

startGame()
choice=""
while choice!="exit":
    print()
    choice = input("hit/fold/exit:\n").lower()
    while not(choice in ["hit","fold","exit"]):
        choice = input("hit/fold/exit:\n").lower()

    if choice=="hit":
        yourCards+=drawCard()
        print("You drew:",yourCards[-1])
        print("Total value:",handVal(yourCards))
        if handVal(yourCards)>21:
            print("You've gone bust! The dealer wins!\n")
            startGame()
    
    elif choice=="fold":
        while handVal(dealerCards)<16:
            dealerCards+=drawCard()
        print("Dealer:")
        for card in dealerCards:
            print(card)
        print(handVal(dealerCards))
        if handVal(dealerCards)>21:
            print("The dealer has gone bust! You win!")
        else:
            print("Your cards:")
            for card in yourCards:
                print(card)
            print(handVal(yourCards))
            if handVal(yourCards)==handVal(dealerCards):
                if len(yourCards)==len(dealerCards):
                    print("It\'s a draw!")
                elif len(yourCards)>len(dealerCards):
                    print("The dealer wins by having less cards!")
                elif len(yourCards)<len(dealerCards):
                    print("You win by having less cards!")
            elif handVal(yourCards)<handVal(dealerCards):
                print("The dealer wins by having a higher value!")
            elif handVal(yourCards)>handVal(dealerCards):
                print("You win by having a higher value!")
        print()
        startGame()

print("Thanks for playing!")
input()