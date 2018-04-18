import RPi.GPIO as GPIO

PIN_GREEN = 11
PIN_RED = 13
PIN_SWITCH = 15

class LEDButton:
    
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
        