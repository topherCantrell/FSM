import RPi.GPIO as GPIO
import smbus

class LED8x8:
    
# LSB at top, MSB at bottom
#                     col 7 green
#                     |   col 7 red
#                     |   |   col 6 green
#                     |   |   |   col 6 red
#                     |   |   |   |   col 5 green
#                     |   |   |   |   |   col 5 red
#                     |   |   |   |   |   |   col 4 green
#                     |   |   |   |   |   |   |   col 4 red
#                     |   |   |   |   |   |   |   |   col 3 green
#                     |   |   |   |   |   |   |   |   |   col 3 red
#                     |   |   |   |   |   |   |   |   |   |   col 2 green
#                     |   |   |   |   |   |   |   |   |   |   |   col 2 red
#                     |   |   |   |   |   |   |   |   |   |   |   |   col 1 green 
#                     |   |   |   |   |   |   |   |   |   |   |   |   |   col 1 red
#                     |   |   |   |   |   |   |   |   |   |   |   |   |   |   col 0 green
#                     |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   col 0 red
#                     |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |
#disp.draw_raw_image([0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0])
    
    def __init__(self,address):
        self._bus = smbus.SMBus(1)
        self._address = address;
        self._pixels = [0]*16        
        self._bus.write_block_data(self._address, 0x21, [])
        self._bus.write_block_data(self._address, 0xEF, [])
        self._bus.write_block_data(self._address, 0x81, [])        
        self.refresh_display()
        
    def refresh_display(self):
        self.draw_raw_image(self._pixels)        
        
    def draw_raw_image(self, image):
        # TODO ... why do I have to start at 15?
        self._bus.write_block_data(self._address, 15, image)
        
    def set_pixel(self,x,y,color):
        if x<0 or x>7 or y<0 or y>7:
            return
        # 0=black, 1=green, 2=red, 3=orange
        x = (7 - x)*2 # Point to green column
        y = 1 << y
        m = (~y)&255
        self._pixels[x] = self._pixels[x] & m
        self._pixels[x+1] = self._pixels[x+1] & m
        if color&1:
            self._pixels[x] = self._pixels[x] | y
        if color&2:
            self._pixels[x+1] = self._pixels[x+1] | y
            
    def draw_sprite(self,x,y,sprite):
        for yo in range(len(sprite)):
            for xo in range(len(sprite[yo])):
                color = sprite[yo][xo]
                if color=='.':
                    color = 0
                else:
                    color = int(color)
                self.set_pixel(x+xo,y+yo,color)

class LightButton:
    
    def __init__(self,green_pin, red_pin, switch_pin):
        self._green_pin = green_pin
        self._red_pin = red_pin
        self._switch_pin = switch_pin
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self._green_pin,GPIO.OUT)
        GPIO.setup(self._red_pin,GPIO.OUT)
        GPIO.setup(self._switch_pin,GPIO.IN)        
        self.set_color(0)        
        
    def set_color(self,color):
        if color==0:
            GPIO.output(self._green_pin, GPIO.HIGH)
            GPIO.output(self._red_pin, GPIO.HIGH)
        elif color==1:
            GPIO.output(self._green_pin, GPIO.LOW)
            GPIO.output(self._red_pin, GPIO.HIGH)
        elif color==2:
            GPIO.output(self._green_pin, GPIO.HIGH)
            GPIO.output(self._red_pin, GPIO.LOW)
        elif color==3:
            GPIO.output(self._green_pin, GPIO.LOW)
            GPIO.output(self._red_pin, GPIO.LOW)
        else:
            raise Exception("Invalid color "+str(color))
        
    def get_button(self):
        return GPIO.input(self._switch_pin)
        
