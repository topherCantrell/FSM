CON
  _clkmode        = xtal1 + pll16x
  _xinfreq        = 5_000_000 

  PIN_SCL    = 0
  'PIN_DAT   = 1
  PIN_BUTTON = 2
  PIN_GREEN  = 3
  PIN_RED    = 4  

OBJ    
    LED    : "HT16K33_Bicolor_8x8"
    FSM    : "FSMRunner"
    BUTTON : "LEDButton"

VAR
    byte curButtonState
    word injectEvent
    
    long randSeq        

    byte tempPic[16]
    word currentPicture

    word wipePtr
    word wipePos

    byte board[9]
    byte opponent
    byte winner

    byte cursorPos

pri imageANDN(image,imageMask) | z
  repeat z from 0 to 15
    tempPic[z] := byte[image+z] & (!byte[imageMask+z])
  return @tempPic

pri imageOR(image,imageBits,colorMask) | z
  repeat z from 0 to 15
    tempPic[z] := byte[image+z] | (byte[imageBits+z] & byte[colorMask+z])
  return @tempPic

pri drawRawPicture(ptr)
  currentPicture := ptr
  LED.writeDisplay(0,16,currentPicture)   
  
pri PauseMSec(Duration)
  waitcnt(((clkfreq / 1_000 * Duration - 3932) #> 381) + cnt)
      
PUB Main | fn, param, retVal

  BUTTON.init(PIN_RED, PIN_GREEN, PIN_BUTTON)

  LED.init($72,PIN_SCL)

  outa[PIN_RED]    := 0
  outa[PIN_GREEN]  := 0
  dira[PIN_RED]    := 0
  dira[PIN_GREEN]  := 0
  dira[PIN_BUTTON] := 0

  curButtonState := BUTTON.isButton

  injectEvent := 0

  PauseMSec(2000)
  'PST.Start(115200)

  randSeq := cnt

  ' Main loop
  mainLoop(@Attract)
  ' Does not return      

' ---- State machine called functions ----

PRI GetEvent | a

  ' If a called function results in an event
  '
  if injectEvent<>0
    a := injectEvent
    injectEvent := 0
    return a

  ' The button is a constant input -- always possible
  '
  a := BUTTON.isButton
  if a==curButtonState
    return 0

  curButtonState := a

  if a==1
    return @STR_DOWN
  else
    return @STR_UP  

PRI light | val
  val := FSM.getFunctionParameter(0)
  BUTTON.setButtonLEDs(val)

PRI draw | ptr
  ptr := FSM.getFunctionParameter(0)
  drawRawPicture(@@ptr)
  
PRI initWipe | ptr
  ptr := FSM.getFunctionParameter(0)  
  wipePtr := @@ptr
  wipePos := 0  

PRI doWipe | pic, ptr
  
  ' Get the current picture ptr
  pic := word[wipePtr] 

  ' Done if 0
  if pic == 0
    return 0

  ' ObjectRelative to absolute     
  pic := pic + @@0 

  ' If this isn't the first picture then mask off the last one
  ptr := currentPicture
  if wipePos>0
    ptr := imageANDN(ptr, word[wipePtr-2]+@@0)

  ' OR on the image
  ptr := imageOR(ptr, pic, @im_yellow)

  drawRawPicture(ptr)

  ' Ready for next time
  wipePos := wipePos + 1
  wipePtr := wipePtr + 2

  ' Stay in this state
  return FSM.getCurrentState  

PRI pickOpp | i

  repeat i from 0 to 8
    board[i] := 0
    
  opponent := randSeq?
  if opponent < 0
    opponent := -opponent
  opponent := opponent // 3

PRI drawOpp
  case opponent
    0: drawRawPicture(@im_MrRandom)
    1: drawRawPicture(@im_Oneder)
    2: drawRawPicture(@im_CatWoman)

PRI lightWin
  BUTTON.setButtonLEDs(winner)

PRI rand | v, uppr
  ' STR_RND  word "##0##"
  uppr := FSM.getFunctionParameter(0)
  v := randSeq?
  if v<0
    v := -v
  v := v // uppr
  v := v + $30
  word[@STR_RND+4] := v
  injectEvent := @STR_RND 

PRI drawBoard | x, im
  im := @im_Board
  repeat x from 0 to 8
    case board[x]
      1: im := imageOR(im,@im_cell0+x*16, @im_Green)
      2: im := imageOR(im,@im_cell0+x*16, @im_Red)
      3: im := imageOR(im,@im_cell0+x*16, @im_Yellow)
  drawRawPicture(im)     

PRI advanceCursor
  repeat
    cursorPos := cursorPos + 1
    if cursorPos > 8
      cursorPos := 0
    if board[cursorPos] == 0
      return 0

PRI setCurCell | val
  val := FSM.getFunctionParameter(0)
  board[cursorPos] := val  

PRI checkBoard
  winner := doBoardCheck

  if winner == 0
    injectEvent := @STR_PLAY
  else
    injectEvent := @STR_OVER

PRI getMove | x, move

  move := -1

  if opponent == 1
    move := getMoveOneder

  if opponent == 2
    move := getMoveOneder
    if move < 0
      move := getMoveCAT

  if move => 0
    cursorPos := move
    return 0

  x := randSeq?
  if x < 0
    x := -x
  x := x // 8
  x := x + 1
  repeat while x > 0
    advanceCursor
    x := x -1


pri getMoveOneder | x, w

  repeat x from 0 to 8
    if board[x] == 0
      board[x] := 2
      w := doBoardCheck
      board[x] := 0
      if w == 2
        return x

  repeat x from 0 to 8
    if board[x] == 0
      board[x] := 1
      w := doBoardCheck
      board[x] := 0
      if w == 1
        return x

  return -1  

pri getMoveCAT | mn

  mn := countMoves

  if mn == 0
    return 0

  if mn==1 or mn==2
    if board[4] == 0
      return 4
    return 8

  if mn == 3
    mn := randSeq?
    if mn<0
      mn := -mn
    mn := mn // 4  ' 0,1,2,3
    mn := mn * 2   ' 0,2,4,6
    mn := mn + 1   ' 1,3,5,7    
    return mn

  if mn==4
    if board[1]>0
      return 3
    if board[3]>0
      return 6 

  return -1

pri doBoardCheck

  if board[0]<>0 and board[0]==board[1] and board[0]==board[2]
    return board[0]
  if board[3]<>0 and board[3]==board[4] and board[3]==board[5]
    return board[3]
  if board[6]<>0 and board[6]==board[7] and board[6]==board[8]
    return board[6]

  if board[0]<>0 and board[0]==board[3] and board[0]==board[6]
    return board[0]
  if board[1]<>0 and board[1]==board[4] and board[1]==board[7]
    return board[1]
  if board[2]<>0 and board[2]==board[5] and board[2]==board[8]
    return board[2]

  if board[0]<>0 and board[0]==board[4] and board[0]==board[8]
    return board[0]
  if board[2]<>0 and board[2]==board[4] and board[2]==board[6]
    return board[2]

  if countMoves == 9
    return 3

  return 0

pri countMoves | count, x
  count := 0
  repeat x from 0 to 8
    if board[x]>0
      count := count + 1
  return count
      
DAT
 
im_Board byte $24,$24,$24,$24,$FF,$FF,$24,$24,$24,$24,$FF,$FF,$24,$24,$24,$24

' Used to blank the display
im_Wiper_B1 byte $FF,$FF,$81,$81,$81,$81,$81,$81,$81,$81,$81,$81,$81,$81,$FF,$FF
im_Wiper_B2 byte $42,$42,$FF,$FF,$42,$42,$42,$42,$42,$42,$42,$42,$FF,$FF,$42,$42
im_Wiper_B3 byte $18,$18,$18,$18,$18,$18,$FF,$FF,$FF,$FF,$18,$18,$18,$18,$18,$18
'
im_Wiper_V1 byte $01,$01,$01,$01,$01,$01,$01,$01,$01,$01,$01,$01,$01,$01,$01,$01
im_Wiper_V2 byte $02,$02,$02,$02,$02,$02,$02,$02,$02,$02,$02,$02,$02,$02,$02,$02
im_Wiper_V3 byte $04,$04,$04,$04,$04,$04,$04,$04,$04,$04,$04,$04,$04,$04,$04,$04
im_Wiper_V4 byte $08,$08,$08,$08,$08,$08,$08,$08,$08,$08,$08,$08,$08,$08,$08,$08
im_Wiper_V5 byte $10,$10,$10,$10,$10,$10,$10,$10,$10,$10,$10,$10,$10,$10,$10,$10
im_Wiper_V6 byte $20,$20,$20,$20,$20,$20,$20,$20,$20,$20,$20,$20,$20,$20,$20,$20
im_Wiper_V7 byte $40,$40,$40,$40,$40,$40,$40,$40,$40,$40,$40,$40,$40,$40,$40,$40
im_Wiper_V8 byte $80,$80,$80,$80,$80,$80,$80,$80,$80,$80,$80,$80,$80,$80,$80,$80
'
im_Wiper_H1 byte $00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$FF,$FF
im_Wiper_H2 byte $00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$FF,$FF,$00,$00
im_Wiper_H3 byte $00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$FF,$FF,$00,$00,$00,$00
im_Wiper_H4 byte $00,$00,$00,$00,$00,$00,$00,$00,$FF,$FF,$00,$00,$00,$00,$00,$00
im_Wiper_H5 byte $00,$00,$00,$00,$00,$00,$FF,$FF,$00,$00,$00,$00,$00,$00,$00,$00
im_Wiper_H6 byte $00,$00,$00,$00,$FF,$FF,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00
im_Wiper_H7 byte $00,$00,$FF,$FF,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00
im_Wiper_H8 byte $FF,$FF,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00
'
im_Wiper_D1 byte $00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$01,$01
im_Wiper_D2 byte $00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$01,$01,$02,$02
im_Wiper_D3 byte $00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$01,$01,$02,$02,$04,$04
im_Wiper_D4 byte $00,$00,$00,$00,$00,$00,$00,$00,$01,$01,$02,$02,$04,$04,$08,$08
im_Wiper_D5 byte $00,$00,$00,$00,$00,$00,$01,$01,$02,$02,$04,$04,$08,$08,$10,$10
im_Wiper_D6 byte $00,$00,$00,$00,$01,$01,$02,$02,$04,$04,$08,$08,$10,$10,$20,$20
im_Wiper_D7 byte $00,$00,$01,$01,$02,$02,$04,$04,$08,$08,$10,$10,$20,$20,$40,$40
im_Wiper_D8 byte $01,$01,$02,$02,$04,$04,$08,$08,$10,$10,$20,$20,$40,$40,$80,$80
im_Wiper_D9 byte $02,$02,$04,$04,$08,$08,$10,$10,$20,$20,$40,$40,$80,$80,$00,$00
im_Wiper_D10 byte $04,$04,$08,$08,$10,$10,$20,$20,$40,$40,$80,$80,$00,$00,$00,$00
im_Wiper_D11 byte $08,$08,$10,$10,$20,$20,$40,$40,$80,$80,$00,$00,$00,$00,$00,$00
im_Wiper_D12 byte $10,$10,$20,$20,$40,$40,$80,$80,$00,$00,$00,$00,$00,$00,$00,$00
im_Wiper_D13 byte $20,$20,$40,$40,$80,$80,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00
im_Wiper_D14 byte $40,$40,$80,$80,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00
im_Wiper_D15 byte $80,$80,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00

' Opponent indicators
im_MrRandom byte $00,$00,$06,$00,$09,$00,$D1,$00,$D1,$00,$01,$00,$06,$00,$00,$00
im_Oneder byte $00,$00,$80,$80,$C0,$C0,$FF,$FF,$FF,$FF,$C6,$C6,$86,$86,$00,$00
im_CatWoman byte $0E,$0E,$05,$05,$2E,$0E,$20,$00,$E0,$00,$20,$09,$20,$09,$00,$06

' Splash screens
im_Tic_T byte $00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$01,$00,$0F,$00,$01,$00
im_Tic_I byte $00,$00,$00,$09,$00,$0F,$00,$09,$00,$00,$01,$00,$0F,$00,$01,$00
im_Tic_C byte $00,$00,$00,$09,$A0,$AF,$A0,$A9,$E0,$E0,$01,$00,$0F,$00,$01,$00
'
im_Tac_T byte $00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$01,$01,$0F,$0F,$01,$01
im_Tac_A byte $0E,$00,$05,$00,$05,$00,$0E,$00,$00,$00,$01,$01,$0F,$0F,$01,$01
im_Tac_C byte $0E,$00,$05,$00,$05,$A0,$0E,$A0,$00,$E0,$01,$01,$0F,$0F,$01,$01
'
im_Toe_T byte $00,$00,$00,$00,$00,$00,$00,$00,$00,$01,$00,$07,$00,$01,$00,$00
im_Toe_O byte $07,$07,$05,$05,$07,$07,$00,$00,$00,$01,$00,$07,$00,$01,$00,$00
im_Toe_E byte $07,$07,$8D,$05,$AF,$07,$A8,$00,$F8,$01,$00,$07,$00,$01,$00,$00

' Color masks
im_Black byte $00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00
im_Green byte $FF,$00,$FF,$00,$FF,$00,$FF,$00,$FF,$00,$FF,$00,$FF,$00,$FF,$00
im_Red byte $00,$FF,$00,$FF,$00,$FF,$00,$FF,$00,$FF,$00,$FF,$00,$FF,$00,$FF
im_Yellow byte $FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF

' Game cells
im_Cell0 byte $00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$03,$03,$03,$03
im_Cell1 byte $00,$00,$00,$00,$00,$00,$03,$03,$03,$03,$00,$00,$00,$00,$00,$00
im_Cell2 byte $03,$03,$03,$03,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00
im_Cell3 byte $00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$18,$18,$18,$18
im_Cell4 byte $00,$00,$00,$00,$00,$00,$18,$18,$18,$18,$00,$00,$00,$00,$00,$00
im_Cell5 byte $18,$18,$18,$18,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00
im_Cell6 byte $00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$C0,$C0,$C0,$C0
im_Cell7 byte $00,$00,$00,$00,$00,$00,$C0,$C0,$C0,$C0,$00,$00,$00,$00,$00,$00
im_Cell8 byte $C0,$C0,$C0,$C0,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00 


' Sequences of images for animations
'
seq_wiper_B  word @im_Wiper_B1, @im_Wiper_B2, @im_Board, @im_Wiper_B3, @im_Board, @im_Wiper_B2, @im_Wiper_B1, 0
seq_wiper_B2 word @im_Wiper_B1, @im_Wiper_B2, @im_Board, @im_Wiper_B3, @im_Board, 0
seq_wiper_V  word @im_Wiper_V1, @im_Wiper_V2, @im_Wiper_V3, @im_Wiper_V4, @im_Wiper_V5, @im_Wiper_V6, @im_Wiper_V7, @im_Wiper_V8, 0
seq_wiper_H  word @im_Wiper_H1, @im_Wiper_H2, @im_Wiper_H3, @im_Wiper_H4, @im_Wiper_H5, @im_Wiper_H6, @im_Wiper_H7, @im_Wiper_H8, 0
seq_wiper_D  word @im_Wiper_D1, @im_Wiper_D2, @im_Wiper_D3, @im_Wiper_D4, @im_Wiper_D5, @im_Wiper_D6, @im_Wiper_D7
             word @im_Wiper_D8, @im_Wiper_D9, @im_Wiper_D10, @im_Wiper_D11, @im_Wiper_D12, @im_Wiper_D13, @im_Wiper_D14, @im_Wiper_D15, 0

  
' Event strings to pass to state machine
STR_DOWN word "##DN##"
STR_UP   word "##UP##"
STR_OVER word "##Over##"
STR_PLAY word "##Play##"

STR_RND  word "##0##" ' Number filled in

CON

Tw = 1    ' Time between wiper animations
Ta = 2    ' Time between letters in attract
Tah = 8   ' Time to hold word in attract

Tos = 5   ' Time between opponent-picture flashes in init
Toh = 8   ' Time to hold opponent-picture
Tov = 5   ' Time between animations in game-over

Tc = 4    ' Time between player cursor blinks
Tch = 10  ' Time button must be help to register move
Toc = 4   ' Time between opponent cursor blinks

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

Attract
  word "##!##", FN_light, 1
  word "##T##",0,@WipeB, FN_initWipe, @seq_wiper_B
  word "**"

WipeB
  word "##T##",Tw,@TicT, FN_doWipe
  word "##DN##", @Init
  word "**"

TicT
  word "##!##", FN_draw, @im_Tic_T
  word "##T##",Ta,@TicI
  word "##DN##", @Init
  word "**"

TicI
  word "##!##", FN_draw, @im_Tic_I
  word "##T##",Ta,@TicC
  word "##DN##", @Init
  word "**"

TicC
  word "##!##", FN_draw, @im_Tic_C
  word "##T##",Tah,@WipeH, FN_initWipe, @seq_wiper_H
  word "##DN##", @Init
  word "**"

WipeH
  word "##T##",Tw,@TacT, FN_doWipe
  word "##DN##", @Init
  word "**"

TacT
  word "##!##", FN_draw, @im_Tac_T
  word "##T##",Ta,@TacA
  word "##DN##", @Init
  word "**"

TacA
  word "##!##", FN_draw, @im_Tac_A
  word "##T##",Ta,@TacC
  word "##DN##", @Init
  word "**"

TacC
  word "##!##", FN_draw, @im_Tac_C
  word "##T##",Tah,@WipeV, FN_initWipe, @seq_wiper_V
  word "##DN##", @Init
  word "**"

WipeV
  word "##T##",Tw,@ToeT, FN_doWipe
  word "##DN##", @Init
  word "**"

ToeT
  word "##!##", FN_draw, @im_Toe_T
  word "##T##",Ta,@ToeO
  word "##DN##", @Init
  word "**"

ToeO
  word "##!##", FN_draw, @im_Toe_O
  word "##T##",Ta,@ToeE
  word "##DN##", @Init
  word "**"

ToeE
  word "##!##", FN_draw, @im_Toe_E
  word "##T##",Tah,@WipeB, FN_initWipe, @seq_wiper_B
  word "##DN##", @Init
  word "**"

Init
  word "##!##", FN_light, 0, "%%", FN_pickOpp
  word "##T##",0,@WipeD, FN_initWipe, @seq_wiper_D
  word "**"

WipeD
  word "##T##",Tw,@ShowOpp1, FN_doWipe
  word "**"

ShowOpp1
  word "##!##", FN_drawOpp
  word "##T##",Tos,@ShowOpp2
  word "**"

ShowOpp2
  word "##!##", FN_draw, @im_Black
  word "##T##",Tos,@ShowOpp3
  word "**"

ShowOpp3
  word "##!##", FN_drawOpp
  word "##T##",Toh,@WipeB2, FN_initWipe, @seq_wiper_B2
  word "**"

WipeB2
  word "##T##",Tw,@WhoFirst, FN_doWipe
  word "**"

WhoFirst
  word "##!##", FN_rand, 2
  word "##1##", @Opp
  word "##0##", @Player
  word "**"

Over
  word "##!##", FN_draw, @im_Black, "%%", FN_light, 0
  word "##T##",Tov,@Over2
  word "##DN##", @Attract
  word "**"

Over2
  word "##!##", FN_drawBoard, "%%", FN_lightWin
  word "##T##",Tov,@Over
  word "##DN##", @Attract
  word "**"

Player
  word "##!##", FN_light, 1, "%%", FN_advanceCursor
  word "##T##",0,@InputA
  word "**"

InputA
  word "##!##", FN_setCurCell, 3, "%%", FN_drawBoard
  word "##T##",Tc,@InputB
  word "##DN##", @InputC
  word "**"

InputB
  word "##!##", FN_setCurCell, 0, "%%", FN_drawBoard
  word "##T##",Tc,@InputA
  word "##DN##", @InputC
  word "**"

InputC
  word "##!##", FN_setCurCell, 3, "%%", FN_drawBoard
  word "##T##",Tch,@HMove
  word "##UP##", @Player, FN_setCurCell, 0
  word "**"

HMove
  word "##!##", FN_setCurCell, 1, "%%", FN_drawBoard
  word "##T##",Tc,@CheckH
  word "**"

CheckH
  word "##!##", FN_checkBoard
  word "##Over##", @Over
  word "##Play##", @Opp
  word "**"

Opp
  word "##!##", FN_light, 2, "%%", FN_getMove
  word "##T##",0,@OppC1
  word "**"

OppC1
  word "##!##", FN_setCurCell, 3, "%%", FN_drawBoard
  word "##T##",Toc,@OppC2
  word "**"

OppC2
  word "##!##", FN_setCurCell, 0, "%%", FN_drawBoard
  word "##T##",Toc,@OppC3
  word "**"

OppC3
  word "##!##", FN_setCurCell, 3, "%%", FN_drawBoard
  word "##T##",Toc,@OMove
  word "**"

OMove
  word "##!##", FN_setCurCell, 2, "%%", FN_drawBoard
  word "##T##",Toc,@CheckO
  word "**"

CheckO
  word "##!##", FN_checkBoard
  word "##Over##", @Over
  word "##Play##", @Player
  word "**"

CON
  FN_light = 256
  FN_initWipe = 257
  FN_doWipe = 258
  FN_draw = 259
  FN_pickOpp = 260
  FN_drawOpp = 261
  FN_rand = 262
  FN_drawBoard = 263
  FN_lightWin = 264
  FN_advanceCursor = 265
  FN_setCurCell = 266
  FN_checkBoard = 267
  FN_getMove = 268

PRI dispatch(fn)
  CASE fn
    0:
      return GetEvent
    FN_light:
      return light
    FN_initWipe:
      return initWipe
    FN_doWipe:
      return doWipe
    FN_draw:
      return draw
    FN_pickOpp:
      return pickOpp
    FN_drawOpp:
      return drawOpp
    FN_rand:
      return rand
    FN_drawBoard:
      return drawBoard
    FN_lightWin:
      return lightWin
    FN_advanceCursor:
      return advanceCursor
    FN_setCurCell:
      return setCurCell
    FN_checkBoard:
      return checkBoard
    FN_getMove:
      return getMove