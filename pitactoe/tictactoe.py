from Display import Display
from LEDButton import LEDButton

import time

display = Display(address=0x72)

button = LEDButton()

i_ticT = ["GGG",
          ".G.",
          ".G.",
          ".G."]
i_ticI = ["RRR",
          ".R.",
          ".R.",
          "RRR"]
i_ticC = ["YYY",
          "Y..",
          "YYY"]

i_tacT = ["YYY",
          ".Y.",
          ".Y.",
          ".Y."]
i_tacA = [".GG.",
          "G..G",
          "GGGG",
          "G..G"]
i_tacC = ["RRR",
          "R..",
          "RRR"]

i_toeT = ["RRR",
          ".R.",
          ".R."]
i_toeO = ["YYY",
          "Y.Y",
          "YYY"]
i_toeE = ["GGGG",
          "G...",
          "GGG.",
          "G...",
          "GGGG"]

i_CAT = ['.RR...Y.',
         'R....Y.Y',
         'R....YYY',
         '.RR..Y.Y',
         '........',
         '.GGGGG..',
         '...G....',
         '...G....']

i_ONE = ['...YY...',
         '.YYYY...',
         '.YYYY...',
         '...YY...',
         '...YY...',
         '...YY...',
         '..YYYY..',
         '.YYYYYY.']

i_RND = ['..YGR...',
         '.R...Y..',
         '.G...G..',
         '....R...',
         '...Y....',
         '........',
         '...G....',
         '...R....']

def set_cell(cell,color):
    pass

def get_cat_move():
    pass

def get_rnd_move():
    pass

def get_one_move():
    pass

def show_computer_move(cell):
    pass

def get_human_move():
    pass

def wipe_right():
    for i in range(9):
        display.draw_v_line(i-1,0)
        display.draw_v_line(i,3)
        display.write_display()
        if button.wait_for_button_state(True,100):
            return True
    return False

def wipe_left():
    for i in range(7,-2,-1):
        display.draw_v_line(i+1,0)
        display.draw_v_line(i,3)
        display.write_display()
        if button.wait_for_button_state(True,100):
            return True
    return False

def wipe_down():
    for i in range(9):
        display.draw_h_line(i-1,0)
        display.draw_h_line(i,3)
        display.write_display()
        if button.wait_for_button_state(True,100):
            return True
    return False

def wipe_board(full):
    for i in range(4):
        display.draw_h_line(i-1,0)
        display.draw_h_line(7-i+1,0)
        display.draw_v_line(i-1,0)
        display.draw_v_line(7-i+1,0)
        display.draw_h_line(i,3)
        display.draw_h_line(7-i,3)
        display.draw_v_line(i,3)
        display.draw_v_line(7-i,3)
        display.write_display()
        time.sleep(.10)
    r = 2
    if full:
        r = -1
    for i in range(3,r,-1):
        display.draw_h_line(i,0)
        display.draw_h_line(7-i,0)
        display.draw_v_line(i,0)
        display.draw_v_line(7-i,0)
        display.draw_h_line(i-1,3)
        display.draw_h_line(7-i+1,3)
        display.draw_v_line(i-1,3)
        display.draw_v_line(7-i+1,3)
        display.write_display()
        time.sleep(.10)  

def splash_three_letters(a,b,c):
    display.draw_ascii_image(a[0],a[1],a[2])
    display.write_display()
    if button.wait_for_button_state(True,500):
        return True    
    display.draw_ascii_image(b[0],b[1],b[2])
    display.write_display()
    if button.wait_for_button_state(True,500):
        return True
    display.draw_ascii_image(c[0],c[1],c[2])
    display.write_display()
    if button.wait_for_button_state(True,1000):
        return True    
    return False

def splash_mode():
    display.clear()
    button.set_color(LEDButton.COLOR_GREEN)
    while True:        
        if splash_three_letters((i_ticT,0,0),(i_ticI,4,0),(i_ticC,3,5)):
            return
        if wipe_right():
            return True
        if splash_three_letters((i_tacT,0,0),(i_tacA,4,0),(i_tacC,3,5)):
            return
        if wipe_left():
            return True
        if splash_three_letters((i_toeT,1,0),(i_toeO,5,0),(i_toeE,3,3)):
            return
        if wipe_down():
            return True

splash_mode()

button.set_color(LEDButton.COLOR_OFF)
display.clear()
display.write_display()

