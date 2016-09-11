"""
A stand-alone application for the Turing Tape GUI and the Euclid
state-machine-runner.

Note that the states themselves are translated from Roger Penrose's
work in The Emperor's New Mind. This is Dr. Penrose's state machine to
implement Euclid's algorithm for finding the GCD of two numbers defined
in unary.
"""

from PyDictStateMachine import PyDictStateMachine
from TuringTapeGUI import TuringTapeGUI

fsm = None  # The state machine runner
tape = None  # The tape GUI


def _readCallback(val):
    """Pass the tape value directly into the state machine"""
    fsm.event(str(val))


def read():
    """State machine requests a tape-read"""
    tape.requestTapeRead()


def writeAndMove(val, direc):
    """State machine requests a tape-write-and-move"""
    tape.writeAndMove(val, direc)


def halt():
    """State machine requests a halt"""
    tape.halt()

RIGHT = "right"
LEFT = "left"

stateMachineStates = {
    "StateA": {
        "@": [read],
        "0": ["StateA", writeAndMove, 0, RIGHT],
        "1": ["StateB", writeAndMove, 1, LEFT],
    },

    "StateB": {
        "@": [read],
        "0": ["StateC", writeAndMove, 1, RIGHT],
        "1": ["StateB", writeAndMove, 1, LEFT],
    },

    "StateC": {
        "@": [read],
        "0": ["StateK", writeAndMove, 0, RIGHT],
        "1": ["StateD", writeAndMove, 0, RIGHT],
    },

    "StateD": {
        "@": [read],
        "0": ["StateE", writeAndMove, 0, RIGHT],
        "1": ["StateD", writeAndMove, 1, RIGHT],
    },

    "StateE": {
        "@": [read],
        "0": ["StateE", writeAndMove, 0, RIGHT],
        "1": ["StateF", writeAndMove, 0, RIGHT],
    },

    "StateF": {
        "@": [read],
        "0": ["StateH", writeAndMove, 0, LEFT],
        "1": ["StateG", writeAndMove, 1, LEFT],
    },

    "StateG": {
        "@": [read],
        "0": ["StateG", writeAndMove, 0, LEFT],
        "1": ["StateB", writeAndMove, 1, LEFT],
    },

    "StateH": {
        "@": [read],
        "0": ["StateH", writeAndMove, 0, LEFT],
        "1": ["StateI", writeAndMove, 1, LEFT],
    },

    "StateI": {
        "@": [read],
        "0": ["StateJ", writeAndMove, 0, LEFT],
        "1": ["StateI", writeAndMove, 1, LEFT],
    },

    "StateJ": {
        "@": [read],
        "0": ["StateC", writeAndMove, 0, RIGHT],
        "1": ["StateB", writeAndMove, 1, LEFT],
    },

    "StateK": {
        "@": [read],
        "0": ["StateA", [writeAndMove, 0, RIGHT], halt],
        "1": ["StateK", writeAndMove, 1, RIGHT],
    },
}

firstState = "StateA"

initialTape = "000000000|0|001111110111111111"

if __name__ == "__main__":

    # Initialize the GUI and a sample tape
    tape = TuringTapeGUI(39, _readCallback, 100)
    tape.setTape(initialTape)

    # Initialize the state machine
    fsm = PyDictStateMachine(stateMachineStates)
    fsm.goToState(firstState)

    # GUI loop
    tape.mainLoop()
