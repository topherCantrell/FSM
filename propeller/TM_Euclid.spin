CON
  _clkmode        = xtal1 + pll16x
  _xinfreq        = 5_000_000    

OBJ
    FSM  : "FSMRunner"
    PST  : "Parallax Serial Terminal"

PRI read | c  
  PST.char(%11111_00_0) ' Request read tape 

PRI writeAndMove | w, m, v
  w := FSM.getFunctionParameter(0)
  m := FSM.getFunctionParameter(1)  
  v := %11110_00_0 | (w<<2) | (m<<1)
  PST.char(v)  

PRI doHalt | v
  v := %11110_00_1 
  PST.char(v)

DAT 
  
' Event strings to pass to state machine
STR_ZERO word "##0##"         
STR_ONE  word "##1##"

PRI GetEvent | c

  ' Incoming value from the tape

  c := PST.RxCount
  if c ==0
    return 0

  c := PST.CharIn

  if c== "0"
    return @STR_ZERO
  
  if c== "1"
    return @STR_ONE

  return 0

pri PauseMSec(Duration)
  waitcnt(((clkfreq / 1_000 * Duration - 3932) #> 381) + cnt)
        
PUB Main 
    
  PauseMSec(2000)   ' Time to start GUI
  PST.Start(9600)   ' Start the serial interface
  
  mainLoop(@StateA) ' State machine starts at StateA 


CON
  RIGHT = 1
  LEFT = 0
  
' ----- ---------------------------- -----
' ----- FSM GENERATED CODE HERE DOWN -----
' ----- ---------------------------- -----

PRI mainLoop(state) | fn, retVal

FSM.init(state,@@0)
repeat
  ' Wait for a function request
  repeat while FSM.isFunctionRequest == 0

  ' Dispatch the function
  fn := FSM.getFunctionNumber
  retVal := dispatch(fn)

  ' Return any response
  FSM.replyToFunctionRequest(retVal)

DAT

fsmData

StateA
  word "##!##", FN_read
  word "##1##", @StateB, FN_writeAndMove, 1, LEFT
  word "##0##", @StateA, FN_writeAndMove, 0, RIGHT
  word "@@"

StateB
  word "##!##", FN_read
  word "##1##", @StateB, FN_writeAndMove, 1, LEFT
  word "##0##", @StateC, FN_writeAndMove, 1, RIGHT
  word "@@"

StateC
  word "##!##", FN_read
  word "##1##", @StateD, FN_writeAndMove, 0, RIGHT
  word "##0##", @StateK, FN_writeAndMove, 0, RIGHT
  word "@@"

StateD
  word "##!##", FN_read
  word "##1##", @StateD, FN_writeAndMove, 1, RIGHT
  word "##0##", @StateE, FN_writeAndMove, 0, RIGHT
  word "@@"

StateE
  word "##!##", FN_read
  word "##1##", @StateF, FN_writeAndMove, 0, RIGHT
  word "##0##", @StateE, FN_writeAndMove, 0, RIGHT
  word "@@"

StateF
  word "##!##", FN_read
  word "##1##", @StateG, FN_writeAndMove, 1, LEFT
  word "##0##", @StateH, FN_writeAndMove, 0, LEFT
  word "@@"

StateG
  word "##!##", FN_read
  word "##1##", @StateB, FN_writeAndMove, 1, LEFT
  word "##0##", @StateG, FN_writeAndMove, 0, LEFT
  word "@@"

StateH
  word "##!##", FN_read
  word "##1##", @StateI, FN_writeAndMove, 1, LEFT
  word "##0##", @StateH, FN_writeAndMove, 0, LEFT
  word "@@"

StateI
  word "##!##", FN_read
  word "##1##", @StateI, FN_writeAndMove, 1, LEFT
  word "##0##", @StateJ, FN_writeAndMove, 0, LEFT
  word "@@"

StateJ
  word "##!##", FN_read
  word "##1##", @StateB, FN_writeAndMove, 1, LEFT
  word "##0##", @StateC, FN_writeAndMove, 0, RIGHT
  word "@@"

StateK
  word "##!##", FN_read
  word "##1##", @StateK, FN_writeAndMove, 1, RIGHT
  word "##0##", @StateA, FN_writeAndMove, 0, RIGHT, "%%", FN_halt
  word "@@"

CON
  FN_read = 256
  FN_writeAndMove = 257
  FN_halt = 258

PRI dispatch(fn)
  CASE fn
    0:
      return GetEvent
    FN_read:
      return read
    FN_writeAndMove:
      return writeAndMove
    FN_halt:
      return doHalt
