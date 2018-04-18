"""
Tuple-Defined State Machine Runner
"""


class PyDictStateMachine(object):

    def __init__(self, states):
        self.stateMachineStates = states
        self.timerRunning = False
        self.countDown = 0
        self.currentStateName = None
        self.targetState = None

    def _callFunctions(self, evt, sp):
        rval = None
        while sp < len(evt):

            if type(evt[sp]) == list:
                rval = self._callFunctions(evt[sp], 0)
                sp = sp + 1

            else:
                args = evt[sp + 1:]
                return evt[sp](*args)

        return rval

    def getCurrentState(self):
        return self.currentStateName

    def getTargetState(self):
        return self.targetState

    def goToState(self, stateName):
        """Transition to the named state. Start the timer if the
        state needs it."""

        # Stop any timer that is running now
        self.timerRunning = False

        # Find the target state
        if stateName not in self.stateMachineStates:
            print "Did not find state " + stateName
            return
        self.currentState = self.stateMachineStates[stateName]
        self.currentStateName = stateName

        print "Entering state " + stateName

        # Handle any "enter state" functions
        if "@" in self.currentState:
            self._callFunctions(self.currentState["@"], 0)

        # Start the timer if requested
        if "T" in self.currentState:
            self.countDown = self.currentState["T"][0]
            if self.countDown == 0:
                self.event("TIME")
            else:
                self.timerRunning = True

    def event(self, event):
        """Handle an event in the current state."""
        print "Event " + event

        # Time events have a shorter name in the definition (because they are
        # common) and an extra parameter (the time value).
        p = 0
        if event == "TIME":
            event = "T"
            p = 1

        # Find the event definition (if any)

        ev = None
        if event in self.currentState:
            ev = self.currentState[event]
        if ev is None and "*" in self.currentState:
            ev = self.currentState["*"]

        if ev is None:
            print "Ignoring"
            return

        # Target state
        self.targetState = ev[p]
        p = p + 1

        # Edge function
        ns = self._callFunctions(ev, p)
        # Edge functions can change destination
        if ns is not None:
            self.targetState = ns

        self.goToState(self.targetState)

    def tick(self):
        """Called from the 100MS timer hook. This handles any running timer.
        You only need to call this if your state-machine uses timeouts.
        """
        if self.timerRunning:
            self.countDown = self.countDown - 1
            if self.countDown <= 0:
                self.timerRunning = False
                self.event("TIME")
