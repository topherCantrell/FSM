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

  randSeq := cnt

  ' Main loop
  mainLoop(@SPLASH)
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

' Called by state machine

PRI setButtonColor  | val
  val := FSM.getFunctionParameter(0)
  BUTTON.setButtonLEDs(val)
  
PRI drawImage | ptr
  ptr := FSM.getFunctionParameter(0)
  drawRawPicture(@@ptr)

PRI andNotImageBuffer | ptr, img 
  img := FSM.getFunctionParameter(0)
  ptr := currentPicture
  ptr := imageANDN(ptr, @@img)
  drawRawPicture(ptr)

PRI orImageBuffer | ptr, img, col
  img := FSM.getFunctionParameter(0)
  col := FSM.getFunctionParameter(1)
  ptr := currentPicture
  case col
    0: ptr := imageOR(ptr, @@img, @im_solid_0)
    1: ptr := imageOR(ptr, @@img, @im_solid_1)
    2: ptr := imageOR(ptr, @@img, @im_solid_2)
    3: ptr := imageOR(ptr, @@img, @im_solid_3)    
  drawRawPicture(ptr)

PRI drawBoard | im, x
  im := @im_Board
  repeat x from 0 to 8
    case board[x]
      1: im := imageOR(im,@im_cell0+x*16, @im_solid_1)
      2: im := imageOR(im,@im_cell0+x*16, @im_solid_2)
      3: im := imageOR(im,@im_cell0+x*16, @im_solid_3)
  drawRawPicture(im)

PRI advanceCursor
  repeat
    cursorPos := cursorPos + 1
    if cursorPos > 8
      cursorPos := 0
    if board[cursorPos] == 0
      return 0

PRI setCellAtCursor | val
  val := FSM.getFunctionParameter(0)
  board[cursorPos] := val  

PRI newGame | x
  repeat x from 0 to 8
    board[x] := 0
  cursorPos := 8  

PRI pickCPU
  opponent := randSeq?
  if opponent < 0
    opponent := -opponent
  opponent := opponent // 3
  case opponent
    0: injectEvent := @STR_RANDOM
    1: injectEvent := @STR_ONEDER
    2: injectEvent := @STR_CAT 
  
PRI pickFirstPlayer | x
  x := randSeq?
  if x < 0
    x := -x
  x := x // 2
  case x
    0: injectEvent := @STR_HUMAN
    1: injectEvent := @STR_CPU

PRI getGameState | winner
  winner := doBoardCheck

  ' 0 = PLAY
  ' 1 = CPU
  ' 2 = HUMAN
  ' 3 = TIE

  case winner
    0: injectEvent := @STR_PLAY
    1: injectEvent := @STR_CPU
    2: injectEvent := @STR_HUMAN
    3: injectEvent := @STR_TIE

PRI getCPUMove | move, x
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

' Helper functions

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

  ' 0 = PLAY
  ' 1 = CPU
  ' 2 = HUMAN
  ' 3 = TIE

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
   
' Event strings to pass to state machine
STR_DOWN   word "##down##"
STR_UP     word "##up##"
STR_HUMAN  word "##human##"
STR_CPU    word "##cpu##"
STR_TIE    word "##tie##"
STR_PLAY   word "##play##"
STR_RANDOM word "##random##"
STR_ONEDER word "##oneder##"
STR_CAT    word "##cat##"

DAT

' Board
im_Board byte $24,$24,$24,$24,$FF,$FF,$24,$24,$24,$24,$FF,$FF,$24,$24,$24,$24

' Solid colors
im_solid_0 byte 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0
im_solid_1 byte $00,$FF,$00,$FF, $00,$FF,$00,$FF, $00,$FF,$00,$FF, $00,$FF,$00,$FF
im_solid_2 byte $FF,$00,$FF,$00, $FF,$00,$FF,$00, $FF,$00,$FF,$00, $FF,$00,$FF,$00
im_solid_3 byte $FF,$FF,$FF,$FF, $FF,$FF,$FF,$FF, $FF,$FF,$FF,$FF, $FF,$FF,$FF,$FF

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


' Wipers
IM_W_B1 byte $FF,$FF,$81,$81,$81,$81,$81,$81,$81,$81,$81,$81,$81,$81,$FF,$FF
IM_W_B2 byte $42,$42,$FF,$FF,$42,$42,$42,$42,$42,$42,$42,$42,$FF,$FF,$42,$42
IM_W_B3 byte $18,$18,$18,$18,$18,$18,$FF,$FF,$FF,$FF,$18,$18,$18,$18,$18,$18
'        
IM_W_V1 byte $01,$01,$01,$01,$01,$01,$01,$01,$01,$01,$01,$01,$01,$01,$01,$01
IM_W_V2 byte $02,$02,$02,$02,$02,$02,$02,$02,$02,$02,$02,$02,$02,$02,$02,$02
IM_W_V3 byte $04,$04,$04,$04,$04,$04,$04,$04,$04,$04,$04,$04,$04,$04,$04,$04
IM_W_V4 byte $08,$08,$08,$08,$08,$08,$08,$08,$08,$08,$08,$08,$08,$08,$08,$08
IM_W_V5 byte $10,$10,$10,$10,$10,$10,$10,$10,$10,$10,$10,$10,$10,$10,$10,$10
IM_W_V6 byte $20,$20,$20,$20,$20,$20,$20,$20,$20,$20,$20,$20,$20,$20,$20,$20
IM_W_V7 byte $40,$40,$40,$40,$40,$40,$40,$40,$40,$40,$40,$40,$40,$40,$40,$40
IM_W_V8 byte $80,$80,$80,$80,$80,$80,$80,$80,$80,$80,$80,$80,$80,$80,$80,$80
'        
IM_W_H1 byte $00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$FF,$FF
IM_W_H2 byte $00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$FF,$FF,$00,$00
IM_W_H3 byte $00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$FF,$FF,$00,$00,$00,$00
IM_W_H4 byte $00,$00,$00,$00,$00,$00,$00,$00,$FF,$FF,$00,$00,$00,$00,$00,$00
IM_W_H5 byte $00,$00,$00,$00,$00,$00,$FF,$FF,$00,$00,$00,$00,$00,$00,$00,$00
IM_W_H6 byte $00,$00,$00,$00,$FF,$FF,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00
IM_W_H7 byte $00,$00,$FF,$FF,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00
IM_W_H8 byte $FF,$FF,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00
'        
IM_W_D1  byte $00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$01,$01
IM_W_D2  byte $00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$01,$01,$02,$02
IM_W_D3  byte $00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$01,$01,$02,$02,$04,$04
IM_W_D4  byte $00,$00,$00,$00,$00,$00,$00,$00,$01,$01,$02,$02,$04,$04,$08,$08
IM_W_D5  byte $00,$00,$00,$00,$00,$00,$01,$01,$02,$02,$04,$04,$08,$08,$10,$10
IM_W_D6  byte $00,$00,$00,$00,$01,$01,$02,$02,$04,$04,$08,$08,$10,$10,$20,$20
IM_W_D7  byte $00,$00,$01,$01,$02,$02,$04,$04,$08,$08,$10,$10,$20,$20,$40,$40
IM_W_D8  byte $01,$01,$02,$02,$04,$04,$08,$08,$10,$10,$20,$20,$40,$40,$80,$80
IM_W_D9  byte $02,$02,$04,$04,$08,$08,$10,$10,$20,$20,$40,$40,$80,$80,$00,$00
IM_W_D10 byte $04,$04,$08,$08,$10,$10,$20,$20,$40,$40,$80,$80,$00,$00,$00,$00
IM_W_D11 byte $08,$08,$10,$10,$20,$20,$40,$40,$80,$80,$00,$00,$00,$00,$00,$00
IM_W_D12 byte $10,$10,$20,$20,$40,$40,$80,$80,$00,$00,$00,$00,$00,$00,$00,$00
IM_W_D13 byte $20,$20,$40,$40,$80,$80,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00
IM_W_D14 byte $40,$40,$80,$80,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00
IM_W_D15 byte $80,$80,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00

' CPU Players
IM_Random byte $00,$00,$06,$00,$09,$00,$D1,$00,$D1,$00,$01,$00,$06,$00,$00,$00
IM_Oneder byte $00,$00,$80,$80,$C0,$C0,$FF,$FF,$FF,$FF,$C6,$C6,$86,$86,$00,$00
IM_Cat    byte $0E,$0E,$05,$05,$2E,$0E,$20,$00,$E0,$00,$20,$09,$20,$09,$00,$06

' Splash screens
IM_S_TIC_1 byte $00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$01,$00,$0F,$00,$01,$00
IM_S_TIC_2 byte $00,$00,$00,$09,$00,$0F,$00,$09,$00,$00,$01,$00,$0F,$00,$01,$00
IM_S_TIC_3 byte $00,$00,$00,$09,$A0,$AF,$A0,$A9,$E0,$E0,$01,$00,$0F,$00,$01,$00
'
IM_S_TAC_1 byte $00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$01,$01,$0F,$0F,$01,$01
IM_S_TAC_2 byte $0E,$00,$05,$00,$05,$00,$0E,$00,$00,$00,$01,$01,$0F,$0F,$01,$01
IM_S_TAC_3 byte $0E,$00,$05,$00,$05,$A0,$0E,$A0,$00,$E0,$01,$01,$0F,$0F,$01,$01
'
IM_S_TOE_1 byte $00,$00,$00,$00,$00,$00,$00,$00,$00,$01,$00,$07,$00,$01,$00,$00
IM_S_TOE_2 byte $07,$07,$05,$05,$07,$07,$00,$00,$00,$01,$00,$07,$00,$01,$00,$00
IM_S_TOE_3 byte $07,$07,$8D,$05,$AF,$07,$A8,$00,$F8,$01,$00,$07,$00,$01,$00,$00

CON

T_splashLetters =  250 / 100 
T_splashWord    = 1000 / 100  
T_wipe          =  100 / 100      
T_wipeHold      =  250 / 100           
T_pickCPUOn     = 1000 / 100                
T_pickCPUOff    = 1000 / 100                     
T_pickCPUHold   = 2000 / 100  
T_winOn         =  500 / 100  
T_winOff        =  500 / 100  
T_inputDown     =  500 / 100  
T_inputHeld     = 1000 / 100  
T_cpuOn         =  500 / 100  
T_cpuOff        =  500 / 100   

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


SPLASH
FOR_PHOTO
        'word "##!##",     FN_drawImage, @IM_S_TOE_3, "%%", FN_setButtonColor, 1
        'word "**"
   
        word "##!##",     FN_setButtonColor,2, "%%", FN_drawImage, @IM_S_TIC_1
        word "##T##",     T_splashLetters, @Tic_TI
        word "##down##",  @PICKS
        word "**"
        
Tic_TI  
        word "##!##",     FN_drawImage, @IM_S_TIC_2
        word "##T##",     T_splashLetters, @Tic_TIC
        word "##down##",  @PICKS
        word "**"
        
Tic_TIC 
        word "##!##",     FN_drawImage, @IM_S_TIC_3
        word "##T##",     T_splashWord, @WipeH_1
        word "##down##",  @PICKS
        word "**"
                
        
WipeH_1 
        word "##!##",     FN_orImageBuffer, @IM_W_H1,3
        word "##T##",     T_wipe, @WipeH_2
        word "##down##",  @PICKS
        word "**"
        
WipeH_2 
        word "##!##",     FN_andNotImageBuffer,@IM_W_H1, "%%", FN_orImageBuffer, @IM_W_H2,3
        word "##T##",     T_wipe, @WipeH_3
        word "##down##",  @PICKS
        word "**"
        
WipeH_3 
        word "##!##",     FN_andNotImageBuffer,@IM_W_H2, "%%", FN_orImageBuffer, @IM_W_H3,3
        word "##T##",     T_wipe, @WipeH_4
        word "##down##",  @PICKS
        word "**"
        
WipeH_4 
        word "##!##",     FN_andNotImageBuffer,@IM_W_H3, "%%", FN_orImageBuffer, @IM_W_H4,3
        word "##T##",     T_wipe, @WipeH_5
        word "##down##",  @PICKS
        word "**"
        
WipeH_5 
        word "##!##",     FN_andNotImageBuffer,@IM_W_H4, "%%", FN_orImageBuffer, @IM_W_H5,3
        word "##T##",     T_wipe, @WipeH_6
        word "##down##",  @PICKS
        word "**"
        
WipeH_6 
        word "##!##",     FN_andNotImageBuffer,@IM_W_H5, "%%", FN_orImageBuffer, @IM_W_H6,3
        word "##T##",     T_wipe, @WipeH_7
        word "##down##",  @PICKS
        word "**"
        
WipeH_7 
        word "##!##",     FN_andNotImageBuffer,@IM_W_H6, "%%", FN_orImageBuffer, @IM_W_H7,3
        word "##T##",     T_wipe, @WipeH_8
        word "##down##",  @PICKS
        word "**"
        
WipeH_8 
        word "##!##",     FN_andNotImageBuffer,@IM_W_H7, "%%", FN_orImageBuffer, @IM_W_H8,3
        word "##T##",     T_wipe, @WipeH_HOLD
        word "##down##",  @PICKS
        word "**"
        
WipeH_HOLD 
        word "##!##",     FN_drawImage,@IM_SOLID_0
        word "##T##",     T_wipeHold, @Tac_T
        word "##down##",  @PICKS
        word "**"
        
        
Tac_T   
        word "##!##",     FN_drawImage, @IM_S_TAC_1
        word "##T##",     T_splashLetters, @Tac_TA
        word "##down##",  @PICKS
        word "**"
        
Tac_TA  
        word "##!##",     FN_drawImage, @IM_S_TAC_2
        word "##T##",     T_splashLetters, @Tac_TAC
        word "##down##",  @PICKS
        word "**"
        
Tac_TAC 
        word "##!##",     FN_drawImage, @IM_S_TAC_3
        word "##T##",     T_splashWord, @WipeV_1
        word "##down##",  @PICKS
        word "**"
        
        
WipeV_1 
        word "##!##",     FN_orImageBuffer, @IM_W_V1,3
        word "##T##",     T_wipe, @WipeV_2
        word "##down##",  @PICKS
        word "**"
        
WipeV_2 
        word "##!##",     FN_andNotImageBuffer,@IM_W_V1, "%%", FN_orImageBuffer, @IM_W_V2,3
        word "##T##",     T_wipe, @WipeV_3
        word "##down##",  @PICKS
        word "**"
        
WipeV_3 
        word "##!##",     FN_andNotImageBuffer,@IM_W_V2, "%%", FN_orImageBuffer, @IM_W_V3,3
        word "##T##",     T_wipe, @WipeV_4
        word "##down##",  @PICKS
        word "**"
        
WipeV_4 
        word "##!##",     FN_andNotImageBuffer,@IM_W_V3, "%%", FN_orImageBuffer, @IM_W_V4,3
        word "##T##",     T_wipe, @WipeV_5
        word "##down##",  @PICKS
        word "**"
        
WipeV_5 
        word "##!##",     FN_andNotImageBuffer,@IM_W_V4, "%%", FN_orImageBuffer, @IM_W_V5,3
        word "##T##",     T_wipe, @WipeV_6
        word "##down##",  @PICKS
        word "**"
        
WipeV_6 
        word "##!##",     FN_andNotImageBuffer,@IM_W_V5, "%%", FN_orImageBuffer, @IM_W_V6,3
        word "##T##",     T_wipe, @WipeV_7
        word "##down##",  @PICKS
        word "**"
        
WipeV_7 
        word "##!##",     FN_andNotImageBuffer,@IM_W_V6, "%%", FN_orImageBuffer, @IM_W_V7,3
        word "##T##",     T_wipe, @WipeV_8
        word "##down##",  @PICKS
        word "**"
        
WipeV_8 
        word "##!##",     FN_andNotImageBuffer,@IM_W_V7, "%%", FN_orImageBuffer, @IM_W_V8,3
        word "##T##",     T_wipe, @WipeV_HOLD
        word "##down##",  @PICKS
        word "**"
        
WipeV_HOLD 
        word "##!##",     FN_drawImage,@IM_SOLID_0
        word "##T##",     T_wipeHold, @Toe_T
        word "##down##",  @PICKS
        word "**"
        
        
Toe_T   
        word "##!##",     FN_drawImage, @IM_S_TOE_1
        word "##T##",     T_splashLetters, @Toe_TO
        word "##down##",  @PICKS
        word "**"
        
Toe_TO  
        word "##!##",     FN_drawImage, @IM_S_TOE_2
        word "##T##",     T_splashLetters, @Toe_TOE
        word "##down##",  @PICKS
        word "**"
        
Toe_TOE 
        word "##!##",     FN_drawImage, @IM_S_TOE_3
        word "##T##",     T_splashWord, @WipeB_1
        word "##down##",  @PICKS
        word "**"
        
        
WipeB_1 
        word "##!##",     FN_orImageBuffer, @IM_W_B1,3
        word "##T##",     T_wipe, @WipeB_2
        word "##down##",  @PICKS
        word "**"
        
WipeB_2 
        word "##!##",     FN_andNotImageBuffer,@IM_W_B1, "%%", FN_orImageBuffer, @IM_W_B2,3
        word "##T##",     T_wipe, @WipeB_3
        word "##down##",  @PICKS
        word "**"
        
WipeB_3 
        word "##!##",     FN_andNotImageBuffer,@IM_W_B2, "%%", FN_orImageBuffer, @IM_BOARD,3
        word "##T##",     T_wipe, @WipeB_4
        word "##down##",  @PICKS
        word "**"
        
WipeB_4 
        word "##!##",     FN_andNotImageBuffer,@IM_BOARD, "%%", FN_orImageBuffer, @IM_W_B3,3
        word "##T##",     T_wipe, @WipeB_5
        word "##down##",  @PICKS
        word "**"
        
WipeB_5 
        word "##!##",     FN_andNotImageBuffer,@IM_W_B3, "%%", FN_orImageBuffer, @IM_BOARD,3
        word "##T##",     T_wipe, @WipeB_6
        word "##down##",  @PICKS
        word "**"
        
WipeB_6 
        word "##!##",     FN_andNotImageBuffer,@IM_BOARD, "%%", FN_orImageBuffer, @IM_W_B2,3
        word "##T##",     T_wipe, @WipeB_7
        word "##down##",  @PICKS
        word "**"
        
WipeB_7 
        word "##!##",     FN_andNotImageBuffer,@IM_W_B2, "%%", FN_orImageBuffer, @IM_W_B1,3
        word "##T##",     T_wipe, @WipeB_HOLD
        word "##down##",  @PICKS
        word "**"
                
WipeB_HOLD 
        word "##!##",     FN_drawImage,@IM_SOLID_0
        word "##T##",     T_wipeHold, @SPLASH
        word "##down##",  @PICKS
        word "**"

PICKS 
        word "##!##",       FN_setButtonColor,0,"%%",FN_newGame, "%%",FN_pickCPU
        word "##random##",  @Opp_RANDOM
        word "##oneder##",  @Opp_ONEDER
        word "##cat##",     @Opp_CAT
        word "**"
        
        
Opp_RANDOM 
        word "##!##",  FN_drawImage, @IM_Random
        word "##T##",  T_pickCPUOn, @Opp_RANDOM2
        word "**"
        
Opp_RANDOM2 
        word "##!##",  FN_drawImage, @IM_SOLID_0
        word "##T##",  T_pickCPUOff, @Opp_RANDOM3        
        word "**"
        
Opp_RANDOM3 
        word "##!##",  FN_drawImage, @IM_Random
        word "##T##",  T_pickCPUHold, @PickWipe_1
        word "**"
                
        
Opp_ONEDER 
        word "##!##",  FN_drawImage, @IM_oneder
        word "##T##",  T_pickCPUOn, @Opp_ONEDER2
        word "**"
        
Opp_ONEDER2 
        word "##!##",  FN_drawImage, @IM_SOLID_0
        word "##T##",  T_pickCPUOff, @Opp_ONEDER3       
        word "**"
        
Opp_ONEDER3 
        word "##!##",  FN_drawImage, @IM_oneder
        word "##T##",  T_pickCPUHold, @PickWipe_1
        word "**"
        
        
Opp_CAT 
        word "##!##",  FN_drawImage, @IM_Cat
        word "##T##",  T_pickCPUOn, @Opp_CAT2
        word "**"
        
Opp_CAT2 
        word "##!##",  FN_drawImage, @IM_SOLID_0
        word "##T##",  T_pickCPUOff, @Opp_CAT3  
        word "**"
        
Opp_CAT3 
        word "##!##",  FN_drawImage, @IM_Cat
        word "##T##",  T_pickCPUHold, @PickWipe_1
        word "**"
                
        

PickWipe_1 
        word "##!##",  FN_orImageBuffer, @IM_W_B1,3
        word "##T##",  T_wipe, @PickWipe_2
        word "**"
        
PickWipe_2 
        word "##!##",  FN_andNotImageBuffer,@IM_W_B1, "%%", FN_orImageBuffer, @IM_W_B2,3
        word "##T##",  T_wipe, @PickWipe_3
        word "**"
        
PickWipe_3 
        word "##!##",  FN_andNotImageBuffer,@IM_W_B2, "%%", FN_orImageBuffer, @IM_BOARD,3
        word "##T##",  T_wipe, @PickWipe_4
        word "**"
        
PickWipe_4 
        word "##!##",  FN_andNotImageBuffer,@IM_BOARD, "%%", FN_orImageBuffer, @IM_W_B3,3
        word "##T##",  T_wipe, @PickWipe_5
        word "**"
        
PickWipe_5 
        word "##!##",  FN_andNotImageBuffer,@IM_W_B3, "%%", FN_orImageBuffer, @IM_BOARD,3
        word "##T##",  T_wipeHold, @Pick2
        word "**"
                
        
Pick2 
        word "##!##",  FN_pickFirstPlayer
        word "##human##",  @PLAY_HUMAN
        word "##cpu##",    @PLAY_CPU    
        word "**"
        
        
        
OVER_HUMAN 
        word "##!##",  FN_setButtonColor,2, "%%", FN_drawBoard
        word "##T##",  T_winOn, @OVER_HUMAN2
        word "##down##",  @OverWipe_1
        word "**"
        
OVER_HUMAN2 
        word "##!##",  FN_setButtonColor,0, "%%", FN_drawImage, @IM_SOLID_0
        word "##T##",  T_winOff, @OVER_HUMAN
        word "##down##",  @OverWipe_1
        word "**"
        
        
OVER_CPU 
        word "##!##",  FN_setButtonColor,1, "%%", FN_drawBoard
        word "##T##",  T_winOn, @OVER_CPU2
        word "##down##",  @OverWipe_1
        word "**"
        
OVER_CPU2 
        word "##!##",  FN_setButtonColor,0, "%%", FN_drawImage, @IM_SOLID_0
        word "##T##",  T_winOff, @OVER_CPU
        word "##down##",  @OverWipe_1
        word "**"
        
        
OVER_TIE 
        word "##!##",  FN_setButtonColor,3, "%%", FN_drawBoard
        word "##T##",  T_winOn, @OVER_TIE2
        word "##down##",  @OverWipe_1
        word "**"
        
OVER_TIE2 
        word "##!##",  FN_setButtonColor,0, "%%", FN_drawImage, @IM_SOLID_0
        word "##T##",  T_winOff, @OVER_TIE
        word "##down##",  @OverWipe_1
        word "**"
        
        
OverWipe_1 
        word "##!##",  FN_setButtonColor,0,"%%",FN_orImageBuffer, @IM_W_D1,3
        word "##T##",  T_wipe, @OverWipe_2
        word "**"
        
OverWipe_2 
        word "##!##",  FN_andNotImageBuffer,@IM_W_D1, "%%", FN_orImageBuffer, @IM_W_D2,3
        word "##T##",  T_wipe, @OverWipe_3
        word "**"
        
OverWipe_3 
        word "##!##",  FN_andNotImageBuffer,@IM_W_D2, "%%", FN_orImageBuffer, @IM_W_D3,3
        word "##T##",  T_wipe, @OverWipe_4
        word "**"
        
OverWipe_4 
        word "##!##",  FN_andNotImageBuffer,@IM_W_D3, "%%", FN_orImageBuffer, @IM_W_D4,3
        word "##T##",  T_wipe, @OverWipe_5
        word "**"
        
OverWipe_5 
        word "##!##",  FN_andNotImageBuffer,@IM_W_D4, "%%", FN_orImageBuffer, @IM_W_D5,3
        word "##T##",  T_wipe, @OverWipe_6
        word "**"
        
OverWipe_6 
        word "##!##",  FN_andNotImageBuffer,@IM_W_D5, "%%", FN_orImageBuffer, @IM_W_D6,3
        word "##T##",  T_wipe, @OverWipe_7
        word "**"
        
OverWipe_7 
        word "##!##",  FN_andNotImageBuffer,@IM_W_D6, "%%", FN_orImageBuffer, @IM_W_D7,3
        word "##T##",  T_wipe, @OverWipe_8
        word "**"
        
OverWipe_8 
        word "##!##",  FN_andNotImageBuffer,@IM_W_D7, "%%", FN_orImageBuffer, @IM_W_D8,3
        word "##T##",  T_wipe, @OverWipe_9
        word "**"
        
OverWipe_9 
        word "##!##",  FN_andNotImageBuffer,@IM_W_D8, "%%", FN_orImageBuffer, @IM_W_D9,3
        word "##T##",  T_wipe, @OverWipe_10
        word "**"
        
OverWipe_10 
        word "##!##",  FN_andNotImageBuffer,@IM_W_D9, "%%", FN_orImageBuffer, @IM_W_D10,3
        word "##T##",  T_wipe, @OverWipe_11
        word "**"
        
OverWipe_11 
        word "##!##",  FN_andNotImageBuffer,@IM_W_D10, "%%", FN_orImageBuffer, @IM_W_D11,3
        word "##T##",  T_wipe, @OverWipe_12
        word "**"
        
OverWipe_12 
        word "##!##",  FN_andNotImageBuffer,@IM_W_D11, "%%", FN_orImageBuffer, @IM_W_D12,3
        word "##T##",  T_wipe, @OverWipe_13
        
OverWipe_13 
        word "##!##",  FN_andNotImageBuffer,@IM_W_D12, "%%", FN_orImageBuffer, @IM_W_D13,3
        word "##T##",  T_wipe, @OverWipe_14
        word "**"
        
OverWipe_14 
        word "##!##",  FN_andNotImageBuffer,@IM_W_D13, "%%", FN_orImageBuffer, @IM_W_D14,3
        word "##T##",  T_wipe, @OverWipe_15
        word "**"
        
OverWipe_15 
        word "##!##",  FN_andNotImageBuffer,@IM_W_D14, "%%", FN_orImageBuffer, @IM_W_D15,3
        word "##T##",  T_wipe, @OverWipe_HOLD
        word "**"
                
OverWipe_HOLD 
        word "##!##",  FN_drawImage,@IM_SOLID_0
        word "##T##",  T_wipeHold, @SPLASH   
        word "**"     
                                               

        
PLAY_HUMAN 
        word "##!##",      FN_setButtonColor, 2, "%%", FN_advanceCursor
        word "##T##",      0, @InputA
        word "**"        
        
InputA 
        word "##!##",      FN_setCellAtCursor, 3, "%%", FN_drawBoard
        word "##T##",      T_inputDown, @InputB
        word "##down##",   @InputC
        word "**"        
        
InputB 
        word "##!##",      FN_setCellAtCursor, 0, "%%", FN_drawBoard
        word "##T##",      T_inputDown, @InputA
        word "##down##",   @InputC
        word "**"        
        
InputC 
        word "##!##",      FN_setCellAtCursor, 3, "%%", FN_drawBoard
        word "##T##",      T_inputHeld, @HMove
        word "##up##",     @InputD
        word "**"

InputD 
        word "##!##",      FN_setCellAtCursor, 0
        word "##T##",      0, @PLAY_HUMAN        
        word "**"        
                        
HMove 
        word "##!##",      FN_setCellAtCursor, 2, "%%",  FN_drawBoard, "%%", FN_getGameState
        word "##cpu##",    @OVER_CPU
        word "##human##",  @OVER_HUMAN
        word "##play##",   @PLAY_CPU
        word "##tie##",    @OVER_TIE
        word "**"            
        
                
PLAY_CPU 
        word "##!##",  FN_setButtonColor,1, "%%", FN_getCPUMove, "%%", FN_setCellAtCursor,1,"%%",FN_drawBoard
        word "##T##",  T_cpuOn, @OppC1
        word "**"
        
        
OppC1 
        word "##!##",  FN_setCellAtCursor,0, "%%", FN_drawBoard
        word "##T##",  T_cpuOff, @OppC2
        word "**"
        
        
OppC2 
        word "##!##",  FN_setCellAtCursor,1, "%%", FN_drawBoard
        word "##T##",  T_cpuOn, @OppC3
        word "**"
        
        
OppC3 
        word "##!##",  FN_setCellAtCursor,0, "%%", FN_drawBoard
        word "##T##",  T_cpuOff, @MoveCPU
        word "**"
        
        
    MoveCPU 
        word "##!##",      FN_setCellAtCursor,1, "%%", FN_drawBoard, "%%", FN_getGameState
        word "##cpu##",    @OVER_CPU
        word "##human##",  @OVER_HUMAN
        word "##play##",   @PLAY_HUMAN
        word "##tie##",    @OVER_TIE
        word "**"
                

CON
  FN_setButtonColor    = 256
  FN_drawImage         = 257
  FN_drawBoard         = 258
  FN_orImageBuffer     = 259
  FN_andNotImageBuffer = 260
  FN_newGame           = 261
  FN_pickCPU           = 262
  FN_pickFirstPlayer   = 263
  FN_advanceCursor     = 264
  FN_setCellAtCursor   = 265
  FN_getGameState      = 266
  FN_getCPUMove        = 267

PRI dispatch(fn)
  CASE fn
    0:
      return GetEvent

    FN_setButtonColor:
      return setButtonColor 
    FN_drawImage:
      return drawImage
    FN_drawBoard:
      return drawBoard
    FN_orImageBuffer:
      return orImageBuffer 
    FN_andNotImageBuffer:
      return andNotImageBuffer
    FN_newGame:
      return newGame    
    FN_pickCPU:
      return pickCPU 
    FN_pickFirstPlayer:
      return pickFirstPlayer    
    FN_advanceCursor:
      return advanceCursor 
    FN_setCellAtCursor:
      return setCellAtCursor 
    FN_getGameState:
      return getGameState   
    FN_getCPUMove:
      return getCPUMove
      