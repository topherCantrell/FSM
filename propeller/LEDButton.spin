{{

   The button case has a normally-open push button and two
   LEDs (green and red). The LEDs are common anode.

   I wired one side of the button to the common anode.


      grn     • btn
   ┌──•     │
   ┣────•─┐            
   └──• │   │
      red └───• +

      
}}

var
  byte PIN_RED
  byte PIN_GREEN
  byte PIN_BUTTON

PUB init(pred, pgreen, pbutton)
  PIN_RED := pred
  PIN_GREEN := pgreen
  PIN_BUTTON := pbutton

PUB setButtonLEDs(color)
  case color
    0:
      dira[PIN_RED]   := 0
      dira[PIN_GREEN] := 0
    1:
      dira[PIN_RED]   := 1
      dira[PIN_GREEN] := 0
    2:
      dira[PIN_RED]   := 0
      dira[PIN_GREEN] := 1
    3:
      dira[PIN_RED]   := 1
      dira[PIN_GREEN] := 1

PUB isButton
  return ina[PIN_BUTTON]