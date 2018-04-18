
numLED = 0x72

currentPicture = None

def initDisplay(num):
    global numLED
    
    numLED = num << 1   # R/-W bit = 0 (write)
    
    i2cInit(False)      # No pullups needed
    
    setOscillator(True) # Start the oscillator
    setBrightness(15)   # Full brightness
    clearDisplay()      # Nothing showing
    setBlink(0,True)    # Display on, not blinking
    
def drawPicture(data):
    global numLED,currentPicture
    currentPicture = data
    i2cWrite(chr(numLED)+'\x00'+data,1,False)

def clearDisplay():
    global numLED
    i2cWrite(chr(numLED)+'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00',1,False)
    
def setOscillator(power):
    global numLED
    if power:
        power = 0x21
    else:
        power = 0x20
    i2cWrite(chr(numLED)+chr(power),1,False)    
    
def setBrightness(b):
    global numLED
    if b<0 or b>15:
        b = 0
    b = b | 0xE0
    i2cWrite(chr(numLED)+chr(b),1,False)
        
def setBlink(rate,power):
    global numLED
    if rate<0 or rate>3:
        rate = 0
    rate = rate << 1
    if power:
        rate = rate | 1
    rate = rate | 0x80
    i2cWrite(chr(numLED)+chr(rate),1,False)
        