# Translated from Roger Penrose's work in The Emperor's New Mind
# This is Dr. Penrose's state machine to implement Euclid's
# algorithm for finding the GCD of two numbers defined in unary.

#                     12           18
# Test tape: ...0001111111111110111111111111111111000...
#               ^
#
# GCD of 12 and 18 is 6
# Result tape should be:

#          6 
# ...000111111000...
#              ^  

from StateMachine import *

def read():
    """Pass the read-function to the tape"""
    rpc('\x00\x00\x20','read')
    
def writeAndMove(val,dir):
    """Pass the write-and-move to the tape"""
    rpc('\x00\x00\x20','writeAndMove',val,dir)
    
def halt():
    """Pass the halt to the tape"""
    rpc('\x00\x00\x20','halt')
    
stateMachineStates = (    
  ("A", 
    ("@",(read,) ),
    ("0", "A", (writeAndMove,0,'right') ),
    ("1", "B", (writeAndMove,1,'left') ),
  ),
  ("B", 
    ("@",(read,) ),
    ("0", "C", (writeAndMove,1,'right') ),
    ("1", "B", (writeAndMove,1,'left') ),
  ),
  ("C", 
    ("@",(read,) ),
    ("0", "K", (writeAndMove,0,'right') ),
    ("1", "D", (writeAndMove,0,'right') ),
  ),
  ("D", 
    ("@",(read,) ),
    ("0", "E", (writeAndMove,0,'right') ),
    ("1", "D", (writeAndMove,1,'right') ),
  ),
  ("E", 
    ("@",(read,) ),
    ("0", "E", (writeAndMove,0,'right') ),
    ("1", "F", (writeAndMove,0,'right') ),
  ),
  ("F", 
    ("@",(read,) ),
    ("0", "H", (writeAndMove,0,'left') ),
    ("1", "G", (writeAndMove,1,'left') ),
  ),
  ("G", 
    ("@",(read,) ),
    ("0", "G", (writeAndMove,0,'left') ),
    ("1", "B", (writeAndMove,1,'left') ),
  ),
  ("H", 
    ("@",(read,) ),
    ("0", "H", (writeAndMove,0,'left') ),
    ("1", "I", (writeAndMove,1,'left') ),
  ),
  ("I", 
    ("@",(read,) ),
    ("0", "J", (writeAndMove,0,'left') ),
    ("1", "I", (writeAndMove,1,'left') ),
  ),
  ("J", 
    ("@",(read,) ),
    ("0", "C", (writeAndMove,0,'right') ),
    ("1", "B", (writeAndMove,1,'left') ),
  ),
  ("K", 
    ("@",(read,) ),
    ("0", "A", (writeAndMove,0,'right'), (halt,) ),
    ("1", "K", (writeAndMove,1,'right') ),
  ),
)

@setHook(HOOK_STARTUP)
def _bootHook():
    goToState("A")     
 
@setHook(HOOK_100MS)
def _timerHook(tic):
    stateMachineTick(tic)
             