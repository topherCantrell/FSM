from Adafruit_LED_Backpack import BicolorMatrix8x8

# Copied from the baseclass.

class Display(BicolorMatrix8x8.BicolorMatrix8x8):
    
    # Color values as convenient globals.
    # This is a bitmask value where the first bit is green, and the second bit is
    # red.  If both bits are set the color is yellow (red + green light).
    COLOR_OFF = 0
    COLOR_GREEN = 1
    COLOR_RED = 2
    COLOR_YELLOW = 3
    
    def __init__(self, **kwargs):
        """Initialize display.  All arguments will be passed to the HT16K33 class
        initializer, including optional I2C address and bus number parameters.
        """
        super(Display, self).__init__(**kwargs)
        self.begin()
        self.clear()
        
    def set_pixel(self, x, y, value):
        """Set pixel at position x, y to the given value.  X and Y should be values
        of 0 to 8.  Value should be OFF, GREEN, RED, or YELLOW.
        """
        
        # Rotation and mirroring
        a = x
        x = y
        y = 7-a
        
        # From the baseclass
        if x < 0 or x > 7 or y < 0 or y > 7:
            # Ignore out of bounds pixels.
            return
        # Set green LED based on 1st bit in value.
        self.set_led(y * 16 + x, 1 if value & Display.COLOR_GREEN > 0 else 0)
        # Set red LED based on 2nd bit in value.
        self.set_led(y * 16 + x + 8, 1 if value & Display.COLOR_RED > 0 else 0)
        
    def draw_ascii_image(self, img, xo, yo):
        for y in range(len(img)):
            for x in range(len(img[y])):
                c = img[y][x]
                v = Display.COLOR_OFF
                if c=='R':
                    v = Display.COLOR_RED
                elif c=='G':
                    v = Display.COLOR_GREEN
                elif c=='Y':
                    v = Display.COLOR_YELLOW
                self.set_pixel(x+xo,y+yo,v)
                
    def draw_v_line(self,x,color):
        for y in range(8):
            self.set_pixel(x,y,color)
            
    def draw_h_line(self,y,color):
        for x in range(8):
            self.set_pixel(x,y,color)