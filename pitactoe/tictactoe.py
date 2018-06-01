from Display import Display
from LEDButton import LEDButton

import time
import random

display = Display(address=0x72)
button = LEDButton()

cursor_x = 2
cursor_y = 2

opponent = 2

wins = (
          # Horizontals
          ((0,0), (1,0), (2,0)),
          ((0,1), (1,1), (2,1)),
          ((0,2), (1,2), (2,2)),
          # Verticals
          ((0,0), (0,1), (0,2)),
          ((1,0), (1,1), (1,2)),
          ((2,0), (2,1), (2,2)),
          # Diagonals
          ((0,0), (1,1), (2,2)),
          ((2,0), (1,1), (0,2))
)

board = [ [0,0,0],
          [0,0,0],
          [0,0,0] ]

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

def draw_board():
    display.clear()
    display.draw_h_line(2,3)
    display.draw_h_line(5,3)
    display.draw_v_line(2,3)
    display.draw_v_line(5,3)
    for y in range(3):
        for x in range(3):
            display.set_pixel(x*3,y*3,board[y][x])
            display.set_pixel(x*3+1,y*3,board[y][x])
            display.set_pixel(x*3,y*3+1,board[y][x])
            display.set_pixel(x*3+1,y*3+1,board[y][x])
    display.write_display()

def wipe_right():
    for i in range(9):
        display.draw_v_line(i-1,0)
        display.draw_v_line(i,3)
        display.write_display()
        if button.wait_for_button_state(True,0.1):
            return True
    return False

def wipe_left():
    for i in range(7,-2,-1):
        display.draw_v_line(i+1,0)
        display.draw_v_line(i,3)
        display.write_display()
        if button.wait_for_button_state(True,0.1):
            return True
    return False

def wipe_down():
    for i in range(9):
        display.draw_h_line(i-1,0)
        display.draw_h_line(i,3)
        display.write_display()
        if button.wait_for_button_state(True,0.1):
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
    if button.wait_for_button_state(True,0.5):
        return True    
    display.draw_ascii_image(b[0],b[1],b[2])
    display.write_display()
    if button.wait_for_button_state(True,0.5):
        return True
    display.draw_ascii_image(c[0],c[1],c[2])
    display.write_display()
    if button.wait_for_button_state(True,1):
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
        
def show_opponent():
    for i in range(5):
        display.clear()
        display.write_display()
        time.sleep(0.2)        
        if opponent==0:
            display.draw_ascii_image(i_RND)
        elif opponent==1:
            display.draw_ascii_image(i_ONE)
        else:
            display.draw_ascii_image(i_CAT)
        display.write_display()
        time.sleep(0.2)  
        
def show_computer_move(x,y):
    for i in range(2):
        board[y][x] = 3
        draw_board()
        time.sleep(0.3)
        board[y][x] = 2
        draw_board()    
        time.sleep(0.3)    

def get_computer_move():
    button.set_color(2)
    if opponent==0:
        x,y = get_rnd_move()
    elif opponent==1:
        x,y = get_one_move()
    else:
        x,y = get_cat_move()
    show_computer_move(x,y)
    board[y][x] = 2
    
def get_cursor_input():
    if button.wait_for_button_state(True,0.5):
        board[cursor_y][cursor_x] = 3
        draw_board()
        if button.wait_for_button_state(False,0.5):
            return 1 # Advance cursor
        else:
            return 2 # Enter move
    else:
        return 0 # Nothing
    
def advance_cursor():
    global cursor_x,cursor_y
    while True:
        cursor_x = cursor_x + 1
        if cursor_x == 3:
            cursor_x = 0
            cursor_y = cursor_y + 1
            if cursor_y == 3:
                cursor_y = 0
        if board[cursor_y][cursor_x] == 0:
            break
    
def get_human_move():    
    button.set_color(1)
    while True:
        advance_cursor()
        while True:        
            
            board[cursor_y][cursor_x] = 3
            draw_board()
            m = get_cursor_input()
            if m==1:
                board[cursor_y][cursor_x] = 0
                draw_board()
                break # advance the cursor
            elif m==2:
                board[cursor_y][cursor_x] = 1
                draw_board()
                return
            
            board[cursor_y][cursor_x] = 0
            draw_board()
            m = get_cursor_input()
            if m==1:
                board[cursor_y][cursor_x] = 0
                draw_board()
                break # advance the cursor
            elif m==2:
                board[cursor_y][cursor_x] = 1
                draw_board()
                return            

def show_winner(winner):
    while button.get_button()==True:
        pass    
    while True:
        button.set_color(0)
        display.clear()
        display.write_display()
        if button.wait_for_button_state(True,0.25):
            while button.get_button()==True:
                pass
            wipe_board(True)
            return
        button.set_color(winner)
        draw_board()
        if button.wait_for_button_state(True,0.25):
            while button.get_button()==True:
                pass 
            wipe_board(True)
            return       

def check_status():    
    for w in wins:
        if count_tokens(w,1)==3:
            return 1
        elif count_tokens(w,2)==3:
            return 2    
    if count_free_spaces() == 0:
        return 3
    return 0

def count_free_spaces():
    ret = 0
    for y in range(3):
        for x in range(3):
            if board[y][x]==0:
                ret = ret + 1
    return ret            

def count_tokens(w,tok):
    ret = 0
    for c in w:
        if board[c[1]][c[0]] == tok:
            ret = ret + 1
    return ret

def get_cat_move():
    
    # Win or block has priority
    m = find_win_or_block()
    if m != None:
        return m
    
    # Now for the CAT logic
    c = count_free_spaces()
    if c==9: # computer gets first move -- take upper left
        return (0,0) # Take upper left
    if c==7: # computer gets third move -- take a corner
        if board[2][2]==0:
            return (2,2)       
        else:
            return (0,2)
        
    if c==8: # human went first -- we'll take middle or upper left 
        if board[1][1]==0:
            return (1,1)
        else:
            return (0,0)
        
    if c==6: # human in center -- take a non corner else take opposite corner or other corner
        if board[1][1]==1: # Human is in center ...
            return (0,1)   # ... take non-corner
        if board[2][2]==1: # Human is in opposite corner ...
            return (2,0)   # ... take another corner 
        return (2,2)       # Opposite corner is open -- take it
    
    # No other ideas ... take a random cell.
    # We could do better, but eh
    
    return get_rnd_move()

def find_win_or_block():
    for w in wins:
        if count_tokens(w,2)==2 and count_tokens(w,0)==1:
            # Winning move
            for c in w:
                if board[c[1]][c[0]]==0:
                    return c            
    for w in wins:
        if count_tokens(w,1)==2 and count_tokens(w,0)==1:
            # Blocking move
            for c in w:
                if board[c[1]][c[0]]==0:
                    return c 
    return None

def get_one_move():
    m = find_win_or_block()
    if m != None:
        return m
    return get_rnd_move()

def get_rnd_move():
    while True:
        x = random.randint(0,2)
        y = random.randint(0,2)
        if board[y][x]==0:
            return (x,y)

display.clear()
display.write_display()

while button.get_button() != True:
    pass
time.sleep(1)
        
while True:
    splash_mode()
    wipe_board(True)
    
    #opponent = random.randint(0,2)
    opponent = opponent+1
    if opponent == 3:
        opponent = 0
    show_opponent()    
    
    time.sleep(0.75)
    wipe_board(False)
    
    board = [ [0,0,0],
              [0,0,0], 
              [0,0,0] ]
    
    cursor_x = 2
    cursor_y = 2
    
    skip_human = (random.randint(0,1)==1)
        
    # loop here
    while True:
        if not skip_human:
            get_human_move()
            s = check_status()
            if s!=0:
                show_winner(s)
                break
        skip_human = False
        get_computer_move()
        s = check_status()
        if s!=0:
            show_winner(s)
            break
