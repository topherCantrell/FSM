import RPi.GPIO as GPIO

class LED8x8:
    
    def __init__(self,bus,address):
        self._bus = bus
        self._address = address;
        self._pixels = [0]*16        
        self._bus.write_byte(self._address, 0x21)
        self._bus.write_byte(self._address, 0xEF)
        self._bus.write_byte(self._address, 0x81)        
        self.refresh_display()
        
    def refresh_display(self):
        self.draw_image(self._pixels)        
        
    def draw_image(self, image):
        self._bus.write_block_data(self._address, 0, image)

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
        
