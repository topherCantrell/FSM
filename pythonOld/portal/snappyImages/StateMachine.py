"""
Tuple-Defined State Machine Runner
  
"""

timerRunning = False # True if the current state is handling a timer
countDown = 0        # Count of 100MS if timer is running
currentState = None  # Current state object
targetState = None   # For edge-functions ... where the machine is going (if allowed)
currentStateName = None

def _findEvent(state,eventName):
    x = len(state)
    y = 1
    while(y<x):
        if state[y][0]==eventName:
            return state[y]
        y = y + 1
    return None

def _findState(stateName):
    x = len(stateMachineStates)
    y = 0
    while(y<x):
        if stateMachineStates[y][0] == stateName:
            return stateMachineStates[y]
        y = y + 1
    return None

def _callFunctions(evt,sp):
    rval = None
    while sp<len(evt):        
        if len(evt[sp])==2:
            rval = evt[sp][0](evt[sp][1])
        elif len(evt[sp])==3:
            rval = evt[sp][0](evt[sp][1],evt[sp][2])
        elif len(evt[sp])==4:
            rval = evt[sp][0](evt[sp][1],evt[sp][2],evt[sp][3])
        else:
            rval = evt[sp][0]()
        sp = sp + 1
    return rval

def init(val):
    global stateMachineStates
    stateMachineStates = val

def goToState(stateName):
    """Transition to the named state. Start the timer if the state needs it."""
    global currentState,countDown,timerRunning,currentStateName
     
    # Stop any timer that is running now
    timerRunning = False
     
    # Find the target state
    s = _findState(stateName)
    if s==None:
        ##print "Did not find state "+stateName ##
        return
    currentStateName = stateName
    currentState = s
    
    ##print "Entering state "+stateName ##
     
    # Handle any "enter state" functions
    con = _findEvent(currentState,"@")
    if con!=None:
        _callFunctions(con,1)
     
    # Start the timer if requested
    ev = _findEvent(s,"T")
    if ev!=None:
        countDown = ev[1]
        if countDown==0:
           stateMachineEvent("TIME")
        else:
           timerRunning = True
           
def stateMachineEvent(event):
    """Handle an event in the current state."""
    global currentState,targetState
    ##print "Event "+event ##
         
    # Time events have a shorter name in the definition (because they are common) and
    # an extra parameter (the time value).
    p = 1
    if event=="TIME":
        event = "T"
        p = 2
     
    # Find the event definition (if any)
    ev = _findEvent(currentState, event)
    if ev==None:
        # Look for wildcard match
        ev = _findEvent(currentState,"*")       
    if ev==None:
        ##print "Ignoring" ##
        return
     
    # Target state
    targetState = ev[p]
    p = p + 1
     
    # Edge function
    ns = _callFunctions(ev,p)
    # Edge functions can change destination
    if ns!=None:
        targetState = ns
     
    goToState(targetState)       
  
def stateMachineTick(tic):
    """Called from the 100MS timer hook. This handles any running timer."""
    global countDown,timerRunning   
    if timerRunning:
        countDown = countDown -1
        if countDown<=0:
            timerRunning = False
            stateMachineEvent("TIME")