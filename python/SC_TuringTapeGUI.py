"""
SnapConnect interface to the TuringTapeGUI.

The remote node invokes 'read', 'writeAndMove' and 'halt' functions
on the tape. The tape injects the return value of 'read' as events
into the remote node's state machine.
"""

from snapconnect import snap
from TuringTapeGUI import TuringTapeGUI

# Physical snap bridge
connection = (snap.SERIAL_TYPE_SNAPSTICK100, 0)


def _readCallback(val):
    """Called when the tape has read a value.
    Just pass it to the remote state machine"""
    comm.rpc('\x05\x47\x38', 'stateMachineEvent', str(val))


def snapTick():
    """This is called every 10MS to process SNAP events."""
    # Run SNAP events
    comm.poll()
    # Reschedule this event
    tape.root.after(10, snapTick)

# Initialize the GUI
tape = TuringTapeGUI(39, _readCallback, 50)

# Make a sample tape so the user just has to press RUN
tape.setTape("000000000|0|001111110111111111")

# Initialize snapconnect
funDir = {'read': tape.delayedReadTape,
          'writeAndMove': tape.writeAndMove,
          'halt': tape.halt}
comm = snap.Snap(funcs=funDir)
comm.open_serial(connection[0], connection[1])

# Add the snap-poller to the TK's loop
tape.root.after(10, snapTick)

# Start the GUI loop
tape.mainLoop()
