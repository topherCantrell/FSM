"""
This module provides a visualization of the Turing tape. The GUI is a window
into a much longer tape that grows as needed on both ends. Thus the tape
behaves somewhat as if it is infinite.

The GUI allows you to slide the window left and right over the long tape
with "<<" and ">>". Sliding the window does not change the position of the
tape head.

The tape head is shown in blue. This is the spot where the Turing machine
will read from next. You have the ability to move the tape head left and
right with "<" and ">".

You can mark the value under the tape head with "0" or "1".

The Turing machine can call several functions on the GUI:
 - writeAndMove    : write a value to the tape and move the head left or right
 - requestTapeRead : initiate a tape-read (the value comes back later)
 - halt            : stop the machine until the user presses "run" or "step"

When the machine is paused the GUI delays processing the "tape read" request.
When you press "Run" or "Step" then the read completes and the machine
continues on.
"""

from Tkinter import Tk, Button, Label, W, E, SOLID


class TuringTapeGUI(object):

    def __init__(self, numCells, readCallback, tickTime=1000):

        self.readCallback = readCallback
        self.tapeReadPending = False
        self.tickTime = tickTime

        self.root = Tk()

        self.NUM_CELLS = numCells  # Number of tape cells shown on GUI

        TOFS = self.NUM_CELLS / 2 - 5  # Layout for the tape-control buttons
        COFS = self.NUM_CELLS / 2 - 5  # Layout for the machine-control buttons

        self.headPos = self.NUM_CELLS / 2  # Start out head in the middle
        self.windPos = 0  # No window offset

        self.tape = []  # Running tape contents
        self.cells = []  # Screen cells

        self.defColor = None
        self.headColor = 'Blue'
        self.haltColor = 'green'

        # 'stopped', 'running', 'stepping'
        self.machineState = 'stopped'

        # Buttons will enable/disable each other
        self.btRun = None
        self.btStep = None
        self.btReset = None
        self.btStop = None

        # -- Build the GUI

        self.root.title('Turing Tape')

        Button(self.root, command=self._tapeLeft, text="<<",
               font=("Helvetica", 12)).grid(column=TOFS + 0, row=0,
                                            columnspan=2, sticky=W + E,
                                            pady=(10, 10))
        Button(self.root, command=self._headLeft, text="<",
               font=("Helvetica", 12)).grid(column=TOFS + 3, row=0,
                                            sticky=W + E)
        Button(self.root, command=self._headZero, text="0",
               font=("Helvetica", 12)).grid(column=TOFS + 4, row=0,
                                            sticky=W + E)
        Button(self.root, command=self._headOne, text="1",
               font=("Helvetica", 12)).grid(column=TOFS + 5, row=0,
                                            sticky=W + E)
        Button(self.root, command=self._headRight, text=">",
               font=("Helvetica", 12)).grid(column=TOFS + 6, row=0,
                                            sticky=W + E)
        Button(self.root, command=self._tapeRight, text=">>",
               font=("Helvetica", 12)).grid(column=TOFS + 8, row=0,
                                            columnspan=2, sticky=W + E)

        for x in xrange(self.NUM_CELLS):
            c = Label(self.root, text="0", relief=SOLID,
                      font=("Helvetica", 30))
            self.defColor = c.cget("bg")
            c.grid(column=x, row=1)
            self.cells.append(c)
            self.tape.append(0)

        self.btRun = Button(self.root, command=self._conRun, text="Run",
                            font=("Helvetica", 12))
        self.btRun.grid(column=COFS + 2, row=3, columnspan=2, pady=(10, 10))

        self.btStop = Button(self.root, command=self._conStop, text="Stop",
                             font=("Helvetica", 12), state='disabled')
        self.btStop.grid(column=COFS + 4, row=3, columnspan=2)

        self.btStep = Button(self.root, command=self._conStep, text="Step",
                             font=("Helvetica", 12))
        self.btStep.grid(column=COFS + 6, row=3, columnspan=2)

        # First "idle" processing tick. It will reschedule itself.
        self.root.after(tickTime, self._handleIdle)

        self._drawTape()

    def mainLoop(self):
        """Start the Tk GUI Loop"""
        self.root.mainloop()

    def _handleIdle(self):
        """Periodic tick to handle read requests from the Turing machine"""
        if self.machineState == 'stopped':
            self.root.after(self.tickTime, self._handleIdle)
            return

        if self.tapeReadPending:
            self.tapeReadPending = False
            self.readCallback(self._readTape())

        if self.machineState == 'stepping':
            self.machineState = 'stopped'

        self.root.after(self.tickTime, self._handleIdle)

    # -- Called by the Turing Machine

    def writeAndMove(self, val, direc):
        if val == 1:
            self._headOne()
        else:
            self._headZero()

        if direc == "right":
            self._headRight()
        else:
            self._headLeft()

    def requestTapeRead(self):
        self.tapeReadPending = True

    def halt(self):
        self.btRun.configure(bg=self.haltColor)
        self.btRun.configure(state='normal')
        self.btStep.configure(state='normal')
        self.btStop.configure(state='disabled')
        self.machineState = 'stopped'

    # -- A tape initialization function. This can be used to set the
    #    initial state of the tape.

    def setTape(self, nt):

        self._unshowHead()

        pos = None

        newTape = []
        p = 0
        for n in nt:
            if n == "|":
                if pos is None:
                    pos = p
                continue
            newTape.append(ord(n) - 0x30)
            p = p + 1

        if pos is None:
            pos = 0

        self.headPos = pos
        x = len(self.tape)
        while(len(newTape) < x):
            newTape = newTape + [0]
        self.tape = newTape

        self._drawTape()

    # -- Functions for the GUI

    def _unshowHead(self):
        sp = self.headPos - self.windPos
        if sp >= 0 and sp < self.NUM_CELLS:
            self.cells[sp].configure(bg=self.defColor)

    def _drawTape(self):
        for x in xrange(self.NUM_CELLS):
            self.cells[x].configure(text=str(self.tape[x + self.windPos]))
        sp = self.headPos - self.windPos
        if sp >= 0 and sp < self.NUM_CELLS:
            self.cells[sp].configure(bg=self.headColor)

    def _tapeLeft(self):

        self._unshowHead()

        self.windPos -= 1

        if self.windPos < 0:
            self.tape = [0] + self.tape
            self.windPos = 0
            self.headPos += 1  # We injected on the left of the head

        self._drawTape()

    def _tapeRight(self):

        self._unshowHead()

        self.windPos += 1

        if (self.windPos + self.NUM_CELLS) > len(self.tape):
            self.tape = self.tape + [0]

        self._drawTape()

    def _headLeft(self):

        self._unshowHead()

        self.headPos -= 1
        if self.headPos == (self.windPos - 1):
            self._tapeLeft()
        else:
            self._drawTape()

    def _headRight(self):

        self._unshowHead()

        self.headPos += 1
        if self.headPos == (self.windPos + self.NUM_CELLS):
            self._tapeRight()
        else:
            self._drawTape()

        self._drawTape()

    def _headOne(self):
        self.tape[self.headPos] = 1
        self._drawTape()

    def _headZero(self):
        self.tape[self.headPos] = 0
        self._drawTape()

    def _readTape(self):
        return self.tape[self.headPos]

    def _conRun(self):
        self.btRun.configure(bg=self.defColor)
        self.btRun.configure(state='disabled')
        self.btStep.configure(state='disabled')
        self.btStop.configure(state='normal')
        self.machineState = 'running'

    def _conStop(self):
        self.btRun.configure(bg=self.defColor)
        self.btRun.configure(state='normal')
        self.btStep.configure(state='normal')
        self.btStop.configure(state='disabled')
        self.machineState = 'stopped'

    def _conStep(self):
        self.btRun.configure(bg=self.defColor)
        self.machineState = 'stepping'

if __name__ == "__main__":

    """Simple test case. Writes 5 1's."""

    testCount = 5

    def tapeReadResponse(val):
        global testCount

        testCount = testCount - 1
        if testCount < 0:
            FSMTape.halt()
            testCount = 5
        else:
            FSMTape.writeAndMove(1, "right")

        FSMTape.requestTapeRead()

    FSMTape = TuringTapeGUI(39, tapeReadResponse)
    FSMTape.requestTapeRead()

    FSMTape.mainLoop()
