from StateMachine import *
from LED import *

PIN_BUTTON  = 14
PIN_RED     = 15
PIN_GREEN   = 16

board = None
winner = None
currentPicture = None
wipePtr = None
wipePos = None
opp = None
cursorPos = 8

im_Board = '\x24\x24\x24\x24\xFF\xFF\x24\x24\x24\x24\xFF\xFF\x24\x24\x24\x24'

# Used to blank the display
im_Wiper_B1 = '\xFF\xFF\x81\x81\x81\x81\x81\x81\x81\x81\x81\x81\x81\x81\xFF\xFF'
im_Wiper_B2 = '\x42\x42\xFF\xFF\x42\x42\x42\x42\x42\x42\x42\x42\xFF\xFF\x42\x42'
im_Wiper_B3 = '\x18\x18\x18\x18\x18\x18\xFF\xFF\xFF\xFF\x18\x18\x18\x18\x18\x18'
#
im_Wiper_V1 = '\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01'
im_Wiper_V2 = '\x02\x02\x02\x02\x02\x02\x02\x02\x02\x02\x02\x02\x02\x02\x02\x02'
im_Wiper_V3 = '\x04\x04\x04\x04\x04\x04\x04\x04\x04\x04\x04\x04\x04\x04\x04\x04'
im_Wiper_V4 = '\x08\x08\x08\x08\x08\x08\x08\x08\x08\x08\x08\x08\x08\x08\x08\x08'
im_Wiper_V5 = '\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10'
im_Wiper_V6 = '\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20'
im_Wiper_V7 = '\x40\x40\x40\x40\x40\x40\x40\x40\x40\x40\x40\x40\x40\x40\x40\x40'
im_Wiper_V8 = '\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80'
#
im_Wiper_H1 = '\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xFF\xFF'
im_Wiper_H2 = '\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xFF\xFF\x00\x00'
im_Wiper_H3 = '\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xFF\xFF\x00\x00\x00\x00'
im_Wiper_H4 = '\x00\x00\x00\x00\x00\x00\x00\x00\xFF\xFF\x00\x00\x00\x00\x00\x00'
im_Wiper_H5 = '\x00\x00\x00\x00\x00\x00\xFF\xFF\x00\x00\x00\x00\x00\x00\x00\x00'
im_Wiper_H6 = '\x00\x00\x00\x00\xFF\xFF\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
im_Wiper_H7 = '\x00\x00\xFF\xFF\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
im_Wiper_H8 = '\xFF\xFF\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
#
im_Wiper_D1 = '\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01\x01'
im_Wiper_D2 = '\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01\x01\x02\x02'
im_Wiper_D3 = '\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01\x01\x02\x02\x04\x04'
im_Wiper_D4 = '\x00\x00\x00\x00\x00\x00\x00\x00\x01\x01\x02\x02\x04\x04\x08\x08'
im_Wiper_D5 = '\x00\x00\x00\x00\x00\x00\x01\x01\x02\x02\x04\x04\x08\x08\x10\x10'
im_Wiper_D6 = '\x00\x00\x00\x00\x01\x01\x02\x02\x04\x04\x08\x08\x10\x10\x20\x20'
im_Wiper_D7 = '\x00\x00\x01\x01\x02\x02\x04\x04\x08\x08\x10\x10\x20\x20\x40\x40'
im_Wiper_D8 = '\x01\x01\x02\x02\x04\x04\x08\x08\x10\x10\x20\x20\x40\x40\x80\x80'
im_Wiper_D9 = '\x02\x02\x04\x04\x08\x08\x10\x10\x20\x20\x40\x40\x80\x80\x00\x00'
im_Wiper_D10 = '\x04\x04\x08\x08\x10\x10\x20\x20\x40\x40\x80\x80\x00\x00\x00\x00'
im_Wiper_D11 = '\x08\x08\x10\x10\x20\x20\x40\x40\x80\x80\x00\x00\x00\x00\x00\x00'
im_Wiper_D12 = '\x10\x10\x20\x20\x40\x40\x80\x80\x00\x00\x00\x00\x00\x00\x00\x00'
im_Wiper_D13 = '\x20\x20\x40\x40\x80\x80\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
im_Wiper_D14 = '\x40\x40\x80\x80\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
im_Wiper_D15 = '\x80\x80\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'

# Opponent indicators
im_MrRandom = '\x00\x00\x06\x00\x09\x00\xD1\x00\xD1\x00\x01\x00\x06\x00\x00\x00'
im_Oneder = '\x00\x00\x80\x80\xC0\xC0\xFF\xFF\xFF\xFF\xC6\xC6\x86\x86\x00\x00'
im_CatWoman = '\x0E\x0E\x05\x05\x2E\x0E\x20\x00\xE0\x00\x20\x09\x20\x09\x00\x06'

# Splash screens
im_Tic_T = '\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01\x00\x0F\x00\x01\x00'
im_Tic_I = '\x00\x00\x00\x09\x00\x0F\x00\x09\x00\x00\x01\x00\x0F\x00\x01\x00'
im_Tic_C = '\x00\x00\x00\x09\xA0\xAF\xA0\xA9\xE0\xE0\x01\x00\x0F\x00\x01\x00'
#
im_Tac_T = '\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01\x01\x0F\x0F\x01\x01'
im_Tac_A = '\x0E\x00\x05\x00\x05\x00\x0E\x00\x00\x00\x01\x01\x0F\x0F\x01\x01'
im_Tac_C = '\x0E\x00\x05\x00\x05\xA0\x0E\xA0\x00\xE0\x01\x01\x0F\x0F\x01\x01'
#
im_Toe_T = '\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01\x00\x07\x00\x01\x00\x00'
im_Toe_O = '\x07\x07\x05\x05\x07\x07\x00\x00\x00\x01\x00\x07\x00\x01\x00\x00'
im_Toe_E = '\x07\x07\x8D\x05\xAF\x07\xA8\x00\xF8\x01\x00\x07\x00\x01\x00\x00'

# Color masks
im_Black = '\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
im_Green = '\xFF\x00\xFF\x00\xFF\x00\xFF\x00\xFF\x00\xFF\x00\xFF\x00\xFF\x00'
im_Red = '\x00\xFF\x00\xFF\x00\xFF\x00\xFF\x00\xFF\x00\xFF\x00\xFF\x00\xFF'
im_Yellow = '\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF'

# Game cells
im_Cell0 = '\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x03\x03\x03\x03'
im_Cell1 = '\x00\x00\x00\x00\x00\x00\x03\x03\x03\x03\x00\x00\x00\x00\x00\x00'
im_Cell2 = '\x03\x03\x03\x03\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
im_Cell3 = '\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x18\x18\x18\x18'
im_Cell4 = '\x00\x00\x00\x00\x00\x00\x18\x18\x18\x18\x00\x00\x00\x00\x00\x00'
im_Cell5 = '\x18\x18\x18\x18\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
im_Cell6 = '\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xC0\xC0\xC0\xC0'
im_Cell7 = '\x00\x00\x00\x00\x00\x00\xC0\xC0\xC0\xC0\x00\x00\x00\x00\x00\x00'
im_Cell8 = '\xC0\xC0\xC0\xC0\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'


cells = (im_Cell0, im_Cell1, im_Cell2, im_Cell3, im_Cell4, im_Cell5, im_Cell6, im_Cell7, im_Cell8)

# Sequences of images for animations
#
seq_wiper_B = (im_Wiper_B1, im_Wiper_B2, im_Board, im_Wiper_B3, im_Board, im_Wiper_B2, im_Wiper_B1)
seq_wiper_B2 = (im_Wiper_B1, im_Wiper_B2, im_Board, im_Wiper_B3, im_Board)
seq_wiper_V = (im_Wiper_V1, im_Wiper_V2, im_Wiper_V3, im_Wiper_V4, im_Wiper_V5, im_Wiper_V6, im_Wiper_V7, im_Wiper_V8)
seq_wiper_H = (im_Wiper_H1, im_Wiper_H2, im_Wiper_H3, im_Wiper_H4, im_Wiper_H5, im_Wiper_H6, im_Wiper_H7, im_Wiper_H8)
seq_wiper_D = (im_Wiper_D1, im_Wiper_D2, im_Wiper_D3, im_Wiper_D4, im_Wiper_D5, im_Wiper_D6, im_Wiper_D7,
               im_Wiper_D8, im_Wiper_D9, im_Wiper_D10, im_Wiper_D11, im_Wiper_D12, im_Wiper_D13, im_Wiper_D14, im_Wiper_D15)

# Timing constants
Tw = 1  # Time between wiper animations
Ta = 2  # Time between letters in attract
Tah = 8  # Time to hold word in attract

To = 5  # Time between opponent-picture flashes in init
Toh = 8  # Time to hold opponent-picture
Tov = 5  # Time between animations in game-over

Tc = 4  # Time between player cursor blinks
Tch = 10  # Time button must be help to register move
Toc = 4  # Time between opponent cursor blinks
        
def _maskImage(io, i):
    bn = ""
    z = 0
    while z<16:
        io_c = ord(io[z])
        i_c = ord(i[z])        
        io_c = io_c & ~i_c
        bn = bn + chr(io_c)
        z = z + 1
    return bn

def _orImage(io, i, colorMask):
    bn = ""
    z = 0
    while z<16:
        io_c = ord(io[z])
        i_c = ord(i[z])
        m_c = ord(colorMask[z])
        io_c = io_c | (i_c & m_c)
        bn = bn + chr(io_c)
        z = z + 1
    return bn
    
def _countMoves():
    global board
    cnt = 0
    x = 0
    while(x<9):
        if ord(board[x])>0:
            cnt = cnt + 1
        x = x + 1
    return cnt
    
def _doBoardCheck(brd):

    # Yes. Brute-force. Nice, eh?

    # 3 in a rows
    if ord(brd[0]) != 0 and brd[0] == brd[1] and brd[0] == brd[2]:
        return ord(brd[0])
    if ord(brd[3]) != 0 and brd[3] == brd[4] and brd[3] == brd[5]:
        return ord(brd[3])
    if ord(brd[6]) != 0 and brd[6] == brd[7] and brd[6] == brd[8]:
        return ord(brd[6])

    if ord(brd[0]) != 0 and brd[0] == brd[3] and brd[0] == brd[6]:
        return ord(brd[0])
    if ord(brd[1]) != 0 and brd[1] == brd[4] and brd[1] == brd[7]:
        return ord(brd[1])
    if ord(brd[2]) != 0 and brd[2] == brd[5] and brd[2] == brd[8]:
        return ord(brd[2])

    if ord(brd[0]) != 0 and brd[0] == brd[4] and brd[0] == brd[8]:
        return ord(brd[0])
    if ord(brd[2]) != 0 and brd[2] == brd[4] and brd[2] == brd[6]:
        return ord(brd[2])

    # Check for CAT
    if _countMoves() == 9:
        return 3

    # Game continues
    return 0

# state machines functions

def rand(upper):
    v = random() % upper
    stateMachineEvent(str(v))
    return v
    
def pickOpp():
    global opp, board
    board = '\x00\x00\x00\x00\x00\x00\x00\x00\x00'
    opp = random() % 3    

def light(v):
    if v==1:
        writePin(PIN_GREEN,False)
        writePin(PIN_RED,True)
    elif v==2:
        writePin(PIN_GREEN,True)
        writePin(PIN_RED,False)
    elif v==3:
        writePin(PIN_GREEN,False)
        writePin(PIN_RED,False)
    else:
        writePin(PIN_GREEN,True)
        writePin(PIN_RED,True)

def initWipe(ptr):
    global wipePtr, wipePos
    wipePtr = ptr
    wipePos = 0

def doWipe():
    global wipePtr, wipePos, currentPicture, currentStateName
    if wipePos >= len(wipePtr):
        return None
    ni = currentPicture
    if wipePos > 0:
        ni = _maskImage(ni, wipePtr[wipePos - 1])
    ni = _orImage(ni, wipePtr[wipePos], im_Yellow)
    draw(ni)
    wipePos += 1
    return currentStateName

def draw(im):
    drawPicture(im)

def drawOpp():
    global opp
    if opp == 0:
        draw(im_MrRandom)
    elif opp == 1:
        draw(im_Oneder)
    else:
        draw(im_CatWoman)

def drawBoard():
    global im_Board, cells, im_Green, im_Red, im_Yellow, board
    im = im_Board
    x = 0
    while(x<9):    
        if ord(board[x]) == 1:
            im = _orImage(im, cells[x], im_Green)
        elif ord(board[x]) == 2:
            im = _orImage(im, cells[x], im_Red)
        elif ord(board[x]) == 3:
            im = _orImage(im, cells[x], im_Yellow)
        x = x + 1
    drawPicture(im)

def lightWin():
    light(winner)
    
topherCount = -1
def topherTest():
    global topherCount
    while True:
        topherCount += 1
        if topherCount>8:
            topherCount = 0
        return None
    
def topherTest2():
    global topherCount
    while True:
        topherCount += 1
        if topherCount>8:
            topherCount = 0
        break
    return None

def advanceCursor():
    global cursorPos, board
    while True:
        cursorPos += 1
        if cursorPos > 8:
            cursorPos = 0
        if ord(board[cursorPos]) == 0:
            return

def _setCell(pos,value):
    global board
    p = 0
    bn = ""
    while p<9:
        if p==pos:
            bn = bn + chr(value)
        else:
            bn = bn + board[p]
        p = p + 1
    board = bn
    
def setCurCell(value):
    global cursorPos
    _setCell(cursorPos,value)

def checkBoard():
    global winner, board

    winner = _doBoardCheck(board)

    if winner > 0:
        stateMachineEvent("Over")
    else:
        stateMachineEvent("Play")
        
def _getMoveOneder():
    global board

    # Look for a win
    x = 0
    while x<9:    
        if ord(board[x]) == 0:
            _setCell(x,2)
            w = _doBoardCheck(board)
            _setCell(x,0)
            if w == 2:
                return x
        x = x + 1

    # Look for a block
    x = 0
    while x<9:
        if ord(board[x]) == 0:
            _setCell(x,1)
            w = _doBoardCheck(board)
            _setCell(x,0)
            if w == 1:
                return x
        x = x + 1

    # Nothing one-ahead
    return -1


def _getMoveCAT():
    # Some simple rules to not get beaten:
    #
    # Moves made (computer goes first):
    # - 0: Pick upper left
    # - 2: Pick center if free or bottom right
    # - 4: If opponent in 1 - take 3. If opponent in 3 - take 6
    #
    # Moves made (human goes first):
    # - 1: Pick center if free or random corner (bottom right ... same as 2 above)
    # - 3: Pick random middle

    mn = _countMoves()

    if mn == 0:
        return 0
    
    if mn == 1 or mn == 2:
        if ord(board[4]) == 0:
            return 4
        return 8
    
    if mn == 3:
        #return [1, 3, 5, 7][random.randint(0, 3)]
        mn = random() & 3 # 0,1,2,3
        mn = mn * 2 # 0,2,4,6
        return mn +1 # 1,3,5,7
    if mn == 4:
        if ord(board[1]) > 0:
            return 3
        if ord(board[3]) > 0:
            return 6

    return -1

def getMove():
    
    global opp, cursorPos
    
    move = -1
    
    if opp == 1:  # Oneder
        move = _getMoveOneder()

    elif opp == 2:  # CatWoman
        move = _getMoveOneder()
        if move < 0:
            move = _getMoveCAT()
    
    if move >= 0:
        cursorPos = move
    else:
        # Random move
        x = random() & 7 + 1
        while x>0:    
            advanceCursor()
            x = x -1

stateMachineStates = (
    ("Attract",
        ("@", (light, 1,)),
        ("T", 0, "WipeB", (initWipe, seq_wiper_B,)),
    ),
    ("WipeB",
        ("T", Tw, "TicT", (doWipe,)),
        ("DN", "Init",),
    ),
    ("TicT",
        ("@", (draw, im_Tic_T,)),
        ("T", Ta, "TicI",),
        ("DN", "Init",),
    ),
    ("TicI",
        ("@", (draw, im_Tic_I,)),
        ("T", Ta, "TicC",),
        ("DN", "Init",),
    ),
    ("TicC",
        ("@", (draw, im_Tic_C,)),
        ("T", Tah, "WipeH", (initWipe, seq_wiper_H,)),
        ("DN", "Init",),
    ),
    ("WipeH",
        ("T", Tw, "TacT", (doWipe,)),
        ("DN", "Init",),
    ),
    ("TacT",
        ("@", (draw, im_Tac_T,)),
        ("T", Ta, "TacA",),
        ("DN", "Init",),
    ),
    ("TacA",
        ("@", (draw, im_Tac_A,)),
        ("T", Ta, "TacC",),
        ("DN", "Init",),
    ),
    ("TacC",
        ("@", (draw, im_Tac_C,)),
        ("T", Tah, "WipeV", (initWipe, seq_wiper_V,)),
        ("DN", "Init",),
    ),
    ("WipeV",
        ("T", Tw, "ToeT", (doWipe,)),
        ("DN", "Init",),
    ),
    ("ToeT",
        ("@", (draw, im_Toe_T,)),
        ("T", Ta, "ToeO",),
        ("DN", "Init",),
    ),
    ("ToeO",
        ("@", (draw, im_Toe_O,)),
        ("T", Ta, "ToeE",),
        ("DN", "Init",),
    ),
    ("ToeE",
        ("@", (draw, im_Toe_E,)),
        ("T", Tah, "WipeB", (initWipe, seq_wiper_B,)),
        ("DN", "Init",),
    ),
    ("Init",
        ("@", (light, 0,), (pickOpp,),),
        ("T", 0, "WipeD", (initWipe, seq_wiper_D,)),
    ),
    ("WipeD",
        ("T", Tw, "ShowOpp1", (doWipe,)),
    ),
    ("ShowOpp1",
        ("@", (drawOpp,)),
        ("T", To, "ShowOpp2",),
    ),
    ("ShowOpp2",
        ("@", (draw, im_Black,)),
        ("T", To, "ShowOpp3",),
    ),
    ("ShowOpp3",
        ("@", (drawOpp,)),
        ("T", Toh, "WipeB2", (initWipe, seq_wiper_B2,),),
    ),
    ("WipeB2",
        ("T", Tw, "WhoFirst", (doWipe,)),
    ),
    ("WhoFirst",
        ("@", (rand, 2,)),
        ("1", "Opp",),
        ("0", "Player",),
    ),
    ("Over",
        ("@", (draw, im_Black,), (light, 0,),),
        ("T", Tov, "Over2",),
        ("DN", "Attract",),
    ),
    ("Over2",
        ("@", (drawBoard,), (lightWin,),),
        ("T", Tov, "Over",),
        ("DN", "Attract",),
    ),
    ("Player",
        ("@", (light, 1,), (advanceCursor,),),
        ("T", 0, "InputA",),
    ),    
    ("InputA",
        ("@", (setCurCell, 3,), (drawBoard,),),
        ("T", Tc, "InputB",),
        ("DN", "InputC",),
    ),
    ("InputB",
        ("@", (setCurCell, 0,), (drawBoard,),),
        ("T", Tc, "InputA",),
        ("DN", "InputC",),
    ),
    ("InputC",
        ("@", (setCurCell, 3,), (drawBoard,),),
        ("T", Tch, "HMove",),
        ("UP", "Player", (setCurCell, 0,)),
    ),
    ("HMove",
        ("@", (setCurCell, 1,), (drawBoard,),),
        ("T", Tc, "CheckH",),
    ),
    ("CheckH",
        ("@", (checkBoard,)),
        ("Over", "Over",),
        ("Play", "Opp",),
    ),
    ("Opp",
        ("@", (light, 2,), (getMove,),),
        ("T", 0, "OppC1",),
    ),
    ("OppC1",
        ("@", (setCurCell, 3,), (drawBoard,),),
        ("T", Toc, "OppC2",),
    ),
    ("OppC2",
        ("@", (setCurCell, 0,), (drawBoard,),),
        ("T", Toc, "OppC3",),
    ),
    ("OppC3",
        ("@", (setCurCell, 3,), (drawBoard,),),
        ("T", Toc, "OMove",),
    ),
    ("OMove",
        ("@", (setCurCell, 2,), (drawBoard,),),
        ("T", Toc, "CheckO",),
    ),
    ("CheckO",
        ("@", (checkBoard,)),
        ("Over", "Over",),
        ("Play", "Player",),
    ),
)

@setHook(HOOK_STARTUP)
def _bootHook():
        
    initDisplay(0x72)    
    
    setPinDir(PIN_RED,True)
    setPinDir(PIN_GREEN,True)
    writePin(PIN_RED,True)
    writePin(PIN_GREEN,True)
            
    setPinDir(PIN_BUTTON, False)
    monitorPin(PIN_BUTTON, True)  
    
    drawPicture(im_Black)
    
    # This starts the state machine in the first state
    goToState("Attract") 
    
@setHook(HOOK_GPIN)
def _gpioHook(pin,state):
    if state:
        # Tell the state machine about a high-to-low transition
        stateMachineEvent("DN")
    else:
        # Tell the state machine about a low-to-high transition
        stateMachineEvent("UP")
 
@setHook(HOOK_100MS)
def _timerHook(tic):
    # The state machine needs this tick.
    stateMachineTick(tic)         
    
