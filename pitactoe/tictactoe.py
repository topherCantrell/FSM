from Display import Display
from LEDButton import LEDButton

display = Display(address=0x72)
display.begin()
display.clear()

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

i_CAT = ['........',
         '........',
         '........',
         '........',
         '........',
         '........',
         '........',
         '........']

i_ONE = ['........',
         '........',
         '........',
         '........',
         '........',
         '........',
         '........',
         '........']

i_RND = ['...YY...',
         '.YY..YY.',
         '.....YY.',
         '...YY...',
         '...YY...',
         '........',
         '...YY...',
         '...YY...']

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

"""
def draw_h_line(display,x,c):
    for y in range(8):
        display.set_pixel(x,y,c)
        
def draw_v_line(display,y,c):
    for x in range(8):
        display.set_pixel(x,7-y,c)

def draw_ascii_image(display, img, xo, yo):
    for y in range(len(img)):
        for x in range(len(img[y])):
            c = img[y][x]
            v = 0
            if c=='R':
                v = 2
            elif c=='G':
                v = 1
            elif c=='Y':
                v = 3
            display.set_pixel(y+yo,7-(x+xo),v)

draw_ascii_image(display,i_ticT,0,0)
draw_ascii_image(display,i_ticI,4,0)
draw_ascii_image(display,i_ticC,3,5)
     
draw_ascii_image(display,i_tacT,0,0)
draw_ascii_image(display,i_tacA,4,0)
draw_ascii_image(display,i_tacC,3,5)
   
draw_ascii_image(display,i_toeT,1,0)
draw_ascii_image(display,i_toeO,5,0)
draw_ascii_image(display,i_toeE,3,3)
"""

display.draw_h_line(4,2)
display.draw_v_line(6,1)

#display.draw_ascii_image(i_ticT,2,4)

display.write_display()

button.set_color(0)

print(button.get_button())