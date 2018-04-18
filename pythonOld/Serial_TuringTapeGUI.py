"""
Serial port interface to the TuringTapeGUI.

The remote node invokes 'read', 'writeAndMove' and 'halt' functions
on the tape. The tape injects the return value of 'read' as events
into the remote node's state machine.
"""

import serial
from TuringTapeGUI import TuringTapeGUI

connection = "COM3"


def _readCallback(val):
    """Called when the tape has read a value."""
    # print "Returning " + str(val)
    ser.write(str(val))


def serialTick():
    """This is called every 10MS to process serial events."""

    if ser.inWaiting() == 0:
        tape.root.after(10, serialTick)
        return

    c = ord(ser.read(1))

    if(c < 0xF0):
        tape.root.after(10, serialTick)
        # print "Report ", chr(c + 64)
        return

    if(c >= 0xF8):
        tape.requestTapeRead()
        # print "Tape Read"
        tape.root.after(10, serialTick)
        return

    w = (c & 4) >> 2
    d = (c & 2) >> 1
    h = (c & 1)

    if h == 1:
        # print "Halt"
        tape.halt()
        tape.root.after(10, serialTick)
        return

    if d == 1:
        d = "right"
    else:
        d = "left"

    # print "Write and Move"
    tape.writeAndMove(w, d)
    tape.root.after(10, serialTick)


ser = serial.Serial(port=connection, baudrate=9600)

# Initialize the GUI
tape = TuringTapeGUI(39, _readCallback, 50)

# Make a sample tape so the user just has to press RUN
tape.setTape("000000000|0|001111110111111111")
# tape.setTape("000000000|0|0011101110000000000")

# Add the snap-poller to the TK's loop
tape.root.after(10, serialTick)

# Start the GUI loop
tape.mainLoop()
