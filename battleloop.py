import protogdata, battleactions
from protogdata import Moves


PlayerMon, FoeMon = protogdata.init_mon()
PlayerDeck, FoeDeck = protogdata.init_deck()

#Tracking useful game state trackers

winCondition = False
winnerPlayer = False 
isSelfTurn = True
playerActiveMon = 0 #from the stack of monsters, current active one
foeActiveMon = 0
playerActions = 2   #remaining actions on turn
foeActions = 2
playerBenched = 0   #amount of monsters benched
foeBenched = 0
playerDeckPos = 0   #next card to draw
foeDeckPos = 0
playerStackpos = 1  #next monster to draw. the initial monster is already draw on init
foeStackpos = 1


def count_hand(deck):
    return sum(1 for card in deck if card.position == 3)

def get_hand_cards(deck):
    return [(i, card) for i, card in enumerate(deck) if card.position == 3]



def drawInitial(playerDeckPos, foeDeckPos):
    for _ in range(3):
        protogdata.PlayerDeck[playerDeckPos].position = 3
        protogdata.FoeDeck[foeDeckPos].position = 3
        playerDeckPos += 1
        foeDeckPos += 1
    return playerDeckPos, foeDeckPos

# playerDeckPos, foeDeckPos = drawInitial(playerDeckPos, foeDeckPos)

def drawAfterTurn(playerDeckPos, foeDeckPos):
    if count_hand(protogdata.PlayerDeck) > 6:
        print("Your hand is full, no cards will be drawn!")
    else:
        protogdata.PlayerDeck[playerDeckPos].position = 3
        playerDeckPos += 1
    if count_hand(protogdata.FoeDeck) > 6:
        print("The foe's hand is full, no cards drawn")
    else:
        protogdata.FoeDeck[foeDeckPos].position = 3
        foeDeckPos += 1
    return playerDeckPos, foeDeckPos

# navigates through the different menus for actions

def actionChoice():

    while True:
        print("Choose your action")
        print("1) Attack")
        print("2) Hand")
        print("3) Bench")
        print("4) Skip turn")
        choice = input("> ")

        if choice in ("1","2","3", "4"):
            return int(choice)      # exits function and returns value

        print("Invalid option, try again.\n")


# "attack" menu
# returns either the chosen move or nothing.
# if nothing is returned, goes back to the previous menu

def attackChoice():

    while True:
        monid = playerActiveMon               # index of active monster
        monsp = PlayerMon[monid].species      # species ID
        basemoveid  = (monsp * 2) - 1
        boostmoveid = (monsp * 2)

        boosters = PlayerMon[monid].boosters  # number of boosters this monster has

        print("")
        print(f"Press 1 - {Moves[basemoveid].uname}")
        print(f"Press 2 - View description of {Moves[basemoveid].uname}")

        # Show booster option only if booster available
        if boosters > 0:
            print(f"Press 3 - Use booster & attack with {Moves[boostmoveid].uname}")
            print(f"Press 4 - View description of {Moves[boostmoveid].uname}")
        else:
            print("Press 3 - [No boosters available]")
            print("Press 4 - [No boosters available]")

        print("Press 5 - Cancel/return")
        print("")

        choice = input("> ").strip()

        # VALIDATION
        if choice == "1":
            return basemoveid                 # choose base move
        
        elif choice == "2":
            print(Moves[basemoveid].description)
            continue                          # reopen menu

        elif choice == "3":
            if boosters > 0:
                return boostmoveid            # boosted move confirmed
            else:
                print("You have no boosters. Choose another option.")
                continue

        elif choice == "4":
            if boosters > 0:
                print(Moves[boostmoveid].description)
            else:
                print("No booster move available.")
            continue

        elif choice == "5":
            return None                       # cancel action

        else:
            print("Invalid input. Choose a number 1-5.")
            continue



def show_hand_and_choose():
    hand = get_hand_cards(protogdata.PlayerDeck)

    if not hand:
        print("No cards in hand.")
        return None  # this should return to the main menu
    print("Choose a card:") #from all the Cards on the playerDeck
    for option, (i, card) in enumerate(hand):
        print(f"{option}. {card.cardtype}, id={card.subid}, pos={i}")

    choice = int(input("Your selection: "))
    chosen_index, chosen_card = hand[choice]

    return chosen_index, chosen_card

    




