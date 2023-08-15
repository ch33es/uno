"""
# UNO!
A single-player game of UNO.
"""
import random
import os
import time

displaysize = os.get_terminal_size().columns

if __name__ == "__main_":
    # player(computer) count
    playercount = int(input("How many players? (4 by default) "))

    # value of cards / player
    if playercount > 10:
        print("Each player will get 7 cards, but the number of players seem rather large.")
        cardcount = input("value of cards for each player? (<7 recommended)")
    else:
        cardcount = input("Everyone gets 7 cards as per the rules. Ok? ")

COLORS = ["Red", "Green", "Yellow", "Blue"] # "Wild" will also be considered a color
VALUES = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, "+2", "Skip", "Reverse"]
WILDS = ["Choose Color", "+4"]

cards = []

class tClr: # CLI text colors
    WILD = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    WHITE = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'

class card:
    def __init__(self,color,value):
        self.color = color
        self.value = value
    def __str__(self):
        if self.color == "Red":
            return f"{tClr.RED}{self.color} {self.value}{tClr.END}"
        elif self.color == "Green":
            return f"{tClr.GREEN}{self.color} {self.value}{tClr.END}"
        elif self.color == "Blue":
            return f"{tClr.BLUE}{self.color} {self.value}{tClr.END}"
        elif self.color == "Yellow":
            return f"{tClr.YELLOW}{self.color} {self.value}{tClr.END}"
        else: # wild
            return f"{tClr.WILD}{self.color} {self.value}{tClr.END}"

class player:
    def __init__(self,name):
        self.name = name
        self.hand = []
        self.won = False

NAMES = ['Bot 1','Bot 2','Bot 3','Bot 4','Bot 5','Bot 6','Bot 7','Bot 8','Bot 9']
playercount = 4
human = player('swj')
players = [human]
for p in range(playercount-1):
    players.append(player(NAMES[p]))

def generateCards():
    """
     There's a total of 108 cards.
     Each color contains a single 0 card
     and 2 sets of cards for values [1-9], +2, Skip, Reverse.
     There are 4 of each wild card type.
     """
    for c in COLORS:
        for v in VALUES:
            if v == 0:
                cards.append(card(c,v)) # "single 0 card"
            else:
                cards.extend([card(c,v)]*2) # "2 sets of cards"
    for w in WILDS:
        for r in range(4): # "4 of"
            cards.append(card("Wild",w)) # "each wild card"

generateCards()

def shuffleCards():
    for cardPosition in range(108):
        newPosition = random.randint(0,107)
        # swapping places:
        cards[cardPosition], cards[newPosition] = cards[newPosition], cards[cardPosition]

shuffleCards()

def drawCards(numberOfCards:int, plyr:player):
    drawnCards = cards[-numberOfCards:]
    del cards[-numberOfCards:]
    plyr.hand.extend(drawnCards)
    return drawnCards.pop()

def handCards(cardcount=7):
    for p in players:
        drawCards(cardcount,p)

handCards()

cChoices = {
    "R": "Red",
    "G": "Green",
    "B": "Blue",
    "Y": "Yellow"
}

def playCard(crd:card,player:player,recursed=False):
    global chosenColor
    global turn
    global Reversed
    global drawCount
    if crd.color == "Wild":
        if crd.value == "+4":
            drawCount += 4
        else:
            drawCount += 2
        if turn == 0:
            if not recursed:
                cChoice = input(f"Choose a color {tClr.RED}R{tClr.END}ed, {tClr.GREEN}G{tClr.END}reen, {tClr.BLUE}B{tClr.END}lue or {tClr.YELLOW}Y{tClr.END}ellow ·")
            try:
                chosenColor = cChoices[cChoice[0].upper()]
            except Exception:
                cChoice = input("That doesn't seem like a valid color name. Try again ·")
                playCard(recursed=True)
        cards.insert(0,crd)
        player.hand.remove(crd)
    elif crd.value == "Reverse":
        print(tClr.WILD+"The direction of the game has been changed."+tClr.END)
        if Reversed:
            Reversed = False
        else:
            Reversed = True
    else:
        cards.insert(0,crd)
        player.hand.remove(crd)

def autoPlay(plyr:player):
    """
    Will enhance it later.
    """
    global chosenColor
    if hasPlayableCards(plyr):
        playablecards = []
        for card in plyr.hand:
            if playable(card):
                playablecards.append(card)
        theCard = random.choice(playablecards)
        if theCard.color == "Wild":
            chosenColor = cChoices[random.choice(['R','G','B','Y'])]
        playCard(theCard,plyr)
        changeTurn(1)
        return plyr.name + " has played a " + str(theCard)
    else:
        if last.value == "+4" or last.value == "+2":
            cantStack(last.value)
            return plyr.name + " has drawn " + last.value.removeprefix("+") + " cards."
        else:
            drawCards(1,plyr)
            changeTurn(1)
            return plyr.name + " has drawn a card."

def checkWins():
    global gameRunning
    winners = []
    for plyr in players:
        if len(plyr.hand) == 0:
            plyr.won = True
            winners.append(plyr)
            print(f"{tClr.WILD}{plyr.name} has won the game!{tClr.END}")
            print("But we'll keep playing anyway.")
    if len(winners) == len(players)-1:
        loser = None
        for plyr in players:
            if plyr. won == False:
                loser = plyr
                break
        print("Only 1 player remains, so the game is over.")
        print("The loser: "+loser.name)
        gameRunning = False

def opponents():
    global turn
    opps = []
    for plyr in players[1:]:
        if plyr.won:
            opps.append(tClr.CYAN+plyr.name+tClr.END)
        elif plyr == players[turn]:
            opps.append(tClr.WILD+plyr.name+tClr.END)
        else:
            opps.append(tClr.WHITE+plyr.name+tClr.END)
    if Reversed:
        return ("↙  "+"  ←  ".join(opps)+"  ↖").center(displaysize)
    else:
        return ("↗  "+"  →  ".join(opps)+"  ↘").center(displaysize)

colorToClr = {
    "Red": tClr.RED,
    "Green": tClr.GREEN,
    "Blue": tClr.BLUE,
    "Yellow": tClr.YELLOW
}

def showStuff():
    os.system('cls')
    print(f"{tClr.UNDERLINE}Your opponents:{tClr.END}")
    print(opponents())
    print()
    print(f"{tClr.UNDERLINE}Last card:{tClr.END}".center(displaysize))
    print(str(last).center(displaysize))
    if last.color == "Wild":
        print(f"Chosen color is {colorToClr[chosenColor]}{chosenColor}{tClr.END}")
    print()
    if drawCount != 0:
        print(f"Card draw count is {drawCount}")
    print()
    if turn == 0:
        print(tClr.WHITE+"Your turn"+tClr.END)
    print(f"{tClr.UNDERLINE}Your hand:{tClr.END}")
    stack = []
    i = 0
    for card in human.hand:
        i += 1
        stack.append(f"{card} ·{i} |")
    hand = ' '.join(stack).removesuffix('|')
    print(hand.center(displaysize))

def hasPlayableCards(player:player):
    for card in player.hand:
        if playable(card):
            return True
    return False

def playable(card:card):
    if card.color == last.color or card.value == last.value or card.color == chosenColor:
        return True
    else:
        return False

def changeTurn(turns):
    global turn
    if turn == len(players)-1 and not Reversed:
        if turns == 2:
            turn = 1
        else:
            turn = 0
    elif Reversed and turn == 0:
        if turns == 2:
            turn = len(players)-3
        else:
            turn = len(players)-2
    else:
        if Reversed:
            turn -= turns
        else:
            turn += turns

def playPrompt(recursed=False):
    if not hasPlayableCards(human):
        if last.value == "+4" or last.value == "+2":
            cantStack(last.value)
        else:
            print(tClr.WHITE+"You don't have any playable cards."+tClr.END)
            print(tClr.CYAN+"Drawing 1 card."+tClr.END)
            drawn = drawCards(1,human)
            print("You have drawn a "+str(drawn))
            if playable(drawn):
                playq = input(f"Would you play the drawn card? {tClr.GREEN}Y{tClr.END}es / {tClr.RED}N{tClr.END}o ·")
                if playq.upper().startswith("Y"):
                    playCard(drawn,human)
                    return tClr.WHITE + "You have drawn and played a " + str(drawn) + "." + tClr.END
            changeTurn(1)
            return tClr.WHITE + "You have drawn a " + str(drawn) + "." + tClr.END
    else:
        if not recursed:
            print(tClr.UNDERLINE+"You can enter 0 to draw a card."+tClr.END)
            choice = int(input(f"Enter the {tClr.WHITE}serial number{tClr.END} of the card you wanna play ·"))
        else:
            choice = int(input(f"You cannot play that card. Try again ·"))
        chosen = human.hand[choice-1]
        if not chosen:
            drawCards(1,human)
            changeTurn(1)
        elif playable(chosen):
            playCard(chosen,human)
            changeTurn(1)
            return tClr.WHITE + "You have played a " + str(chosen) + "." + tClr.END
        else:
            playPrompt(recursed=True)

def cantStack(cardVal):
    if turn == 0:
        if cardVal == "+4":
            print("You don't have another +4 to stack.")
            print(tClr.CYAN+"Drawing " + drawCount + " cards."+tClr.END)
        else:
            print("You don't have another +2 to stack.")
            print(tClr.CYAN+"Drawing " + drawCount + " cards."+tClr.END)
    else:
        print(f"{players[turn]} has drawn {cardVal.removeprefix('+')} cards.")
    drawCards(cardVal,players[turn])
    changeTurn(1)

tClrs = [tClr.RED,tClr.GREEN,tClr.BLUE,tClr.YELLOW]

def progressBar():
    i = 0
    x = 0
    while x < displaysize:
        if i>3:
            i = 0
        time.sleep(0.01)
        print(tClrs[i]+"·"+tClr.END,end="",flush=True)
        i+=1
        x+=1
    print()

turn = 0
Reversed = False
gameRunning = True
chosenColor = None # color change / +4
drawCount = 0

while gameRunning:
    last = cards[0]
    checkWins()
    showStuff()

    if turn == 0:
        printText = playPrompt()
    elif players[turn].won:
        changeTurn(1)
    else:
        printText = autoPlay(players[turn])

    print(printText)
    progressBar()