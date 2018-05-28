import RPi.GPIO as GPIO
import time

PIN_GREEN = 11
PIN_RED = 13
PIN_SWITCH = 15

class LEDButton:
    
    COLOR_OFF = 0
    COLOR_GREEN = 1
    COLOR_RED = 2
    COLOR_YELLOW = 3
    
    def __init__(self):
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(PIN_RED,GPIO.OUT)
        GPIO.setup(PIN_GREEN,GPIO.OUT)
        GPIO.setup(PIN_SWITCH,GPIO.IN)
        GPIO.output(PIN_RED,True)
        GPIO.output(PIN_GREEN,True)
        
    def set_color(self,color):
        if color==1:
            GPIO.output(PIN_RED,True)
            GPIO.output(PIN_GREEN,False)
        elif color==2:
            GPIO.output(PIN_RED,False)
            GPIO.output(PIN_GREEN,True)
        elif color==3:
            GPIO.output(PIN_RED,False)
            GPIO.output(PIN_GREEN,False)
        else:
            GPIO.output(PIN_RED,True)
            GPIO.output(PIN_GREEN,True)
            
    def get_button(self):
        return GPIO.input(PIN_SWITCH)
    
    def wait_for_button_state(self,state,timeout_s):
        # Return true if state was found
        # Return false if timeout
        for h in range(int(timeout_s*100.0)):
            if self.get_button() == state:
                return True
            time.sleep(0.01)
        