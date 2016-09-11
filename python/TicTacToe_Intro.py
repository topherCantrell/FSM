
from PyDictStateMachine import PyDictStateMachine
from LED8x8AndButton import LED8x8AndButton

fsm = None  # The state machine runner
ttt = None  # The hardware emulator

currentPicture = None


def _buttonDownCallback():
    fsm.event("DN")


def _buttonUpCallback():
    fsm.event("UP")


def tick():
    fsm.tick()
    ttt.root.after(100, tick)


def light(val):
    ttt.setButtonColor(val)


def orImage(im):
    global currentPicture
    ni = ""
    for i in xrange(16):
        v = ord(im[i]) | ord(currentPicture[i])
        ni = ni + chr(v)
    draw(ni)


def maskImage(im):
    global currentPicture
    ni = ""
    for i in xrange(16):
        v = ord(currentPicture[i]) & (~ord(im[i]))
        ni = ni + chr(v)
    draw(ni)


def draw(im):
    global currentPicture
    currentPicture = im
    ttt.writeDisplay(im)


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


Tw = 1
Ta = 2
Th = 8

stateMachineStates = {
    "Attract": {
        "@": [light, 1],
        "T": [0, "WipeB1"],
    },
    "WipeB1": {
        "@": [orImage, im_Wiper_B1],
        "T": [Tw, "WipeB2"],
        "DN": ["Init"]
    },
    "WipeB2": {
        "@": [[maskImage, im_Wiper_B1], [orImage, im_Wiper_B2]],
        "T": [Tw, "WipeB3"],
        "DN": ["Init"]
    },
    "WipeB3": {
        "@": [[maskImage, im_Wiper_B2], [orImage, im_Board]],
        "T": [Tw, "WipeB4"],
        "DN": ["Init"]
    },
    "WipeB4": {
        "@": [[maskImage, im_Board], [orImage, im_Wiper_B3]],
        "T": [Tw, "WipeB5"],
        "DN": ["Init"]
    },
    "WipeB5": {
        "@": [[maskImage, im_Wiper_B3], [orImage, im_Board]],
        "T": [Tw, "WipeB6"],
        "DN": ["Init"]
    },
    "WipeB6": {
        "@": [[maskImage, im_Board], [orImage, im_Wiper_B2]],
        "T": [Tw, "WipeB7"],
        "DN": ["Init"]
    },
    "WipeB7": {
        "@": [[maskImage, im_Wiper_B2], [orImage, im_Wiper_B1]],
        "T": [Tw, "TicT"],
        "DN": ["Init"]
    },

    "TicT": {
        "@": [draw, im_Tic_T],
        "T": [Ta, "TicI"],
        "DN": ["Init"]
    },
    "TicI": {
        "@": [draw, im_Tic_I],
        "T": [Ta, "TicC"],
        "DN": ["Init"]
    },
    "TicC": {
        "@": [draw, im_Tic_C],
        "T": [Th, "WipeH1"],
        "DN": ["Init"]
    },


    "WipeH1": {
        "@": [orImage, im_Wiper_H1],
        "T": [Tw, "WipeH2"],
        "DN": ["Init"]
    },
    "WipeH2": {
        "@": [[maskImage, im_Wiper_H1], [orImage, im_Wiper_H2]],
        "T": [Tw, "WipeH3"],
        "DN": ["Init"]
    },
    "WipeH3": {
        "@": [[maskImage, im_Wiper_H2], [orImage, im_Wiper_H3]],
        "T": [Tw, "WipeH4"],
        "DN": ["Init"]
    },
    "WipeH4": {
        "@": [[maskImage, im_Wiper_H3], [orImage, im_Wiper_H4]],
        "T": [Tw, "WipeH5"],
        "DN": ["Init"]
    },
    "WipeH5": {
        "@": [[maskImage, im_Wiper_H4], [orImage, im_Wiper_H5]],
        "T": [Tw, "WipeH6"],
        "DN": ["Init"]
    },
    "WipeH6": {
        "@": [[maskImage, im_Wiper_H5], [orImage, im_Wiper_H6]],
        "T": [Tw, "WipeH7"],
        "DN": ["Init"]
    },
    "WipeH7": {
        "@": [[maskImage, im_Wiper_H6], [orImage, im_Wiper_H7]],
        "T": [Tw, "WipeH8"],
        "DN": ["Init"]
    },
    "WipeH8": {
        "@": [[maskImage, im_Wiper_H7], [orImage, im_Wiper_H8]],
        "T": [Tw, "TacT"],
        "DN": ["Init"]
    },

    "TacT": {
        "@": [draw, im_Tac_T],
        "T": [Ta, "TacA"],
        "DN": ["Init"]
    },
    "TacA": {
        "@": [draw, im_Tac_A],
        "T": [Ta, "TacC"],
        "DN": ["Init"]
    },
    "TacC": {
        "@": [draw, im_Tac_C],
        "T": [Th, "WipeV1"],
        "DN": ["Init"]
    },

    "WipeV1": {
        "@": [orImage, im_Wiper_V1],
        "T": [Tw, "WipeV2"],
        "DN": ["Init"]
    },
    "WipeV2": {
        "@": [[maskImage, im_Wiper_V1], [orImage, im_Wiper_V2]],
        "T": [Tw, "WipeV3"],
        "DN": ["Init"]
    },
    "WipeV3": {
        "@": [[maskImage, im_Wiper_V2], [orImage, im_Wiper_V3]],
        "T": [Tw, "WipeV4"],
        "DN": ["Init"]
    },
    "WipeV4": {
        "@": [[maskImage, im_Wiper_V3], [orImage, im_Wiper_V4]],
        "T": [Tw, "WipeV5"],
        "DN": ["Init"]
    },
    "WipeV5": {
        "@": [[maskImage, im_Wiper_V4], [orImage, im_Wiper_V5]],
        "T": [Tw, "WipeV6"],
        "DN": ["Init"]
    },
    "WipeV6": {
        "@": [[maskImage, im_Wiper_V5], [orImage, im_Wiper_V6]],
        "T": [Tw, "WipeV7"],
        "DN": ["Init"]
    },
    "WipeV7": {
        "@": [[maskImage, im_Wiper_V6], [orImage, im_Wiper_V7]],
        "T": [Tw, "WipeV8"],
        "DN": ["Init"]
    },
    "WipeV8": {
        "@": [[maskImage, im_Wiper_V7], [orImage, im_Wiper_V8]],
        "T": [Tw, "ToeT"],
        "DN": ["Init"]
    },

    "ToeT": {
        "@": [draw, im_Toe_T],
        "T": [Ta, "ToeO"],
        "DN": ["Init"]
    },
    "ToeO": {
        "@": [draw, im_Toe_O],
        "T": [Ta, "ToeE"],
        "DN": ["Init"]
    },
    "ToeE": {
        "@": [draw, im_Toe_E],
        "T": [Th, "WipeB1"],
        "DN": ["Init"]
    },

    "Init": {
        "@": [light, 3]
    },
}

if __name__ == "__main__":

    currentPicture = im_Black

    # Initialize the GUI and a sample tape
    ttt = LED8x8AndButton(_buttonDownCallback, _buttonUpCallback)

    # Initialize the state machine
    fsm = PyDictStateMachine(stateMachineStates)
    fsm.goToState("Attract")

    ttt.root.after(100, tick)

    # GUI loop
    ttt.mainLoop()
