from dataclasses import dataclass, field
import random

# =============================
# CONSTANTS
# =============================

SPECIESCOUNT = 16  # number of familiars

ACTIVE = 0
DECK = 1
BENCH = 2
HAND = 3
DISCARDED = 4

INVOKER   = 1
BOOSTER   = 2
EFFECT    = 3
EQUIPABLE = 4

# =============================
# DATA STRUCTURES
# =============================

@dataclass
class Familiar:
    uname: str
    hearts: int
    element: int
    passive: int
    cooldown: int

@dataclass
class EffectCard:
    uname: str
    description: str

@dataclass
class Move:
    uname: str
    description: str
    power: int
    status: int
    cfcheck: int
    cfsecondary: int
    boosterscale: int

@dataclass
class Equipable:
    uname: str
    element: int
    addmove: int

@dataclass
class Passive:
    uname: str


# Game-state objects

@dataclass
class Card:
    cardtype: int
    subid: int
    position: int

@dataclass
class GameFam:
    species: int
    hp: int
    position: int
    equipped: int = 0
    boosters: int = 0
    status: int = 0


# =====================================================
# STATIC DEX / DATABASE (Familiars, Effects, Moves, etc)
# =====================================================

Familiars = {
    1: Familiar("ZUBRUTE",10,1,0,2), #A bipedal bison built like a tank
    2: Familiar("BOMBR",6,1,0,1), #A beaver that builds dams by nuking trees
    3: Familiar("KALASKRUK",5,1,0,0), #A mischevous crow armed with a semiautomatic gun
    4: Familiar("JEZMINA",6,1,1,3), #A mobile landmine hedhegog (passive: enemy receives recoil when hits)
    5: Familiar("ROBERT",6,2,0,1), #An old generation robot with bad accuracy, but deadly when he hits
    6: Familiar("BIEDRONE",3,2,2,0), #A tiny scout robotic ladybug (passive: accuracy check on hit)
    7: Familiar("STOZCNIK",11,2,0,3), #A colossal port crane-robot
    8: Familiar("WAVELTRON",8,2,0,2), #A robotic recreation of a mythical dragon from certain castle. Spits high octane fire
    9: Familiar("BIOSUK",4,3,0,0), #A disgusting skunk that leaves a trail of pestilence
    10: Familiar("GOOSTAV",12,3,3,4), #A sticky goo from the union of republics era. Passive: traps on contact
    11: Familiar("DOC MESTOS",7,3,3,1), #A mutant mad scientist armed with a huge syringe bazooka
    12: Familiar("RATDIO",4,4,0,0), #A tiny rat equiped with radiofrequence technology
    13: Familiar("SONARTA",6,4,0,0), #A mechanical songbird that emmits a terrible screech
    14: Familiar("STAYCJ",11,4,4,3), #A sturdy robotic girl that works as a beacon and brings allies to battle
    15: Familiar("PALANNA",8,5,5,1), #The spring's spirit. Bursts on fire when the winter ends. Passive: Doubles damage output when half hp (ignited)
    16: Familiar("TURON",9,5,0,2), #The jolly spirit of christmas with an alcohol addiction
}

Effects = {
    1: EffectCard("UNBOOSTER","REMOVES ONE BOOSTER FROM FOE"),
    2: EffectCard("TELEPORT","SWITCH FREELY IGNORING COOLDOWN"),
    3: EffectCard("GAMMA SHIELD","SHIELDS FOR 1HP AND ANY STATUS"),
    4: EffectCard("BRAINSTORM","DISCARD YOUR HAND AND DRAW 3 CARDS"),
    5: EffectCard("DEINVOKE","PUT BACK A BENCHED MONSTER IN HAND"),
    6: EffectCard("TAUNT DANCE","THE FOE CAN ONLY ATTACK THE NEXT TURN"),
    7: EffectCard("BLOOD BOOSTER","3 COINS. EACH HEAD = BOOSTER FOR 1HP"),
    8: EffectCard("GATHER ENERGY","DISCARD ALL BOOSTERS, HEAL 2HP PER BOOSTER"),
}

Moves = {
    1: Move("SHAKEDOWN", "FLIPS A COIN. IF HEADS, REMOVES A FOE BOOSTER", 2,0,0,1,0),
    2: Move("SMACKDOWN", "IF HEADS, KICKS THE FOE TO THE BENCH", 3,0,0,1,0),
    3: Move("BEAVER BOMB", "IF TAILS, BOMBR RECEIVES 2HP OF RECOIL", 4,0,0,1,0),
    4: Move("BEAVER NUKE", "RECOIL REDUCED TO 1HP", 5,0,0,1,0),

    5: Move("ASSAULT CROW", "FLIPS 3 COINS, EACH TAILS DAMAGES", 2,0,0,0,0),
    6: Move("MINIGUN CROW", "EACH BOOSTER ADDS ONE MORE COIN", 2,0,0,0,0),

    7: Move("SPIKY SHIELD", "REDUCES INCOMING DAMAGE 1HP", 0,5,0,0,0),
    8: Move("MINE SHIELD", "EACH BOOSTER REDUCES DAMAGE ANOTHER 2HP", 0,5,0,0,0),

    9: Move("ZAPPER", "PARALYZES IF HEADS, FAILS IF TAILS", 2,1,1,0,0),
    10: Move("GAMMA ZAPPER", "EACH BOOSTER ADDS 2HP OF DAMAGE", 2,1,1,0,2),

    11: Move("INFILTRATE", "DAMAGES A RANDOM BENCHED FOE", 3,0,0,0,0),
    12: Move("ESPIONAGE", "PEEKS FOE BENCH AND DAMAGES CHOSEN FOE", 4,0,0,0,0),

    13: Move("CRANE PULL", "DRAWS TWO CARDS", 0,0,0,0,0),
    14: Move("CRANE GACHA", "DRAWS 2 CARDS AND A RANDOM FOE. DAMAGES HIM", 3,0,0,0,0),

    15: Move("SCORCHING FIRE", "IF HEADS, THE FOE IS BURNED", 3,2,0,1,0),
    16: Move("SCORCHING NAPALM", "THE BURN EFFECT IS GUARANTEED", 4,2,0,0,0),

    17: Move("GAS CLOUD", "THE FOE IS POISONED", 2,3,0,0,0),
    18: Move("GAS NOVA", "DOUBLE DAMAGE IF FOE IS POISONED", 3,0,0,0,0),

    19: Move("BLOB TRAP", "IF HEADS, THE FOE IS STUNNED A TURN", 0,4,1,0,0),
    20: Move("BLOB CANNON", "DEALS 1/3 OF GOOSTAV CURRENT HP", 0,0,0,0,0),

    21: Move("TRIPLE VIRAL", "MAY POISON, PARALYZE OR CONFUSE", 2,0,0,0,0),
    22: Move("TRIPLE TOXIN", "PROVOKES CONFUSION AND POISON SIMULTANEOUSLY", 2,6,0,0,0),

    23: Move("SINE WAVE", "EVERY TURN DEALS EXTRA 2HP", 2,0,0,0,0),
    24: Move("COSINE WAVE", "EVERY TURN DEALS 1HP LESS", 6,0,0,0,0),

    25: Move("SCREECH SONG", "IF HEADS, CONFUSES", 2,7,0,1,0),
    26: Move("SCREECH HYMN", "GUARANTEED CONFUSION", 2,7,0,0,0),

    27: Move("BEACON SIGNAL", "HEALS 1HP, IF HEADS, INVOKES A MONSTER", 0,0,0,1,0),
    28: Move("BEACON CALL", "SWITCHES WITH AN ALLY. HEALS 30HP PER BOOSTER", 0,0,0,0,0),

    29: Move("BLOOM", "HEALS BACK HALF OF THE DAMAGE DEALT", 2,0,0,0,0),
    30: Move("BLOSSOM", "HEALS AN ALLY ALL THE DAMAGE DEALT", 2,0,0,0,0),

    31: Move("VODKA GULP", "CAUSES SELF CONFUSION BUT HEALS 30HP", 0,8,0,0,0),
    32: Move("VODKA SPITE", "IF CONFUSED, HEALS IT AND CONFUSE FOE", 4,7,0,0,0),

    # Equipable-based moves
    33: Move("PRIMAL RAGE", "IF HEADS, DEALS DOUBLE DAMAGE IF 1/2 HP", 3,0,0,1,0),
    34: Move("HIBERNATE", "HEALS 4HP, BUT SLEEPS THE NEXT TURN", 0,0,0,0,0),
    35: Move("DOWNLOAD", "GAIN ONE OR THREE BOOSTERS ON COINFLIP", 0,0,1,0,0),
    36: Move("ELECTROCUTE", "THE USER LOSES 1 OR 2HP ON COINFLIP", 4,8,0,1,0),

    37: Move("PARASYTE", "1HP IS DRAINED PER TURN FROM FOE", 0,10,0,0,0),
    38: Move("CORRODER", "ROBOT FOES RECEIVE DOUBLE DAMAGE", 3,0,0,0,0),

    39: Move("AMPLIFIED WAVE", "DEALS EXTRA HP PER BOOSTER BUT KEEPS THEM", 2,0,0,0,1),
    40: Move("MODULO", "DEALS A THIRD OF THE FOE HP", 0,0,0,0,0),

    41: Move("MYTHIC SWORD", "THREE COINS. EACH COIN REDUCES DAMAGE", 5,0,0,0,0),
}




Equipables = {
    1: Equipable("FURY MUZZLE",1,33),  
    2: Equipable("SLEEPING BAG",1,34),
    3: Equipable("NET UPGRADE",2, 35),
    4: Equipable("HI-VOLT CABLE", 2, 36),
    5: Equipable("SYMBION", 3, 37),
    6: Equipable("ACID GUN", 3, 38),
    7: Equipable("PARABOLIC", 4, 39),
    8: Equipable("ALGEBRA", 4, 40),
    9: Equipable("SWORD OF TALES", 5, 41)
}

#unimplemented

Passives = {
    1: Passive("Some Passive"), 
}


# =============================
# GAME STATE INITIALIZATION
# =============================


#the actual deck and monster decks are two independent stacks:

def init_deck():
    PlayerDeck = []
    FoeDeck    = []

    for _ in range(40):
        r = random.randint(1,40)
        if r <= 10:
            PlayerDeck.append(Card(INVOKER,0,DECK))
        elif r <= 23:
            PlayerDeck.append(Card(BOOSTER,0,DECK))
        elif r <= 31:
            PlayerDeck.append(Card(EFFECT,r-23,DECK))
        else:
            PlayerDeck.append(Card(EQUIPABLE,r-31,DECK))

    for _ in range(40):
        r = random.randint(1,40)
        if r < 10:
            FoeDeck.append(Card(INVOKER,0,DECK))
        elif r < 23:
            FoeDeck.append(Card(BOOSTER,0,DECK))
        elif r < 31:
            FoeDeck.append(Card(EFFECT,r-23,DECK))
        else:
            FoeDeck.append(Card(EQUIPABLE,r-31,DECK))

    return PlayerDeck, FoeDeck


#the monster deck is separate. running out of monsters
#or having no benched monsters upon losing one, ends the game

def init_mon():
    PlayerMon = []
    FoeMon    = []

    for _ in range(6):
        r = random.randint(1,SPECIESCOUNT)
        PlayerMon.append(GameFam(r, Familiars[r].hearts, DECK))

    for _ in range(6):
        r = random.randint(1,SPECIESCOUNT)
        FoeMon.append(GameFam(r, Familiars[r].hearts, DECK))

    PlayerMon[0].position = ACTIVE
    FoeMon[0].position = ACTIVE
    return PlayerMon, FoeMon


