
https://learn.adafruit.com/mp3-playback-rp2040


```

import board
import digitalio
import busio

pin_red = digitalio.DigitalInOut(board.GP12)
pin_green = digitalio.DigitalInOut(board.GP13)
pin_green.direction = digitalio.Direction.OUTPUT
pin_green.value = 1
pin_red.direction = digitalio.Direction.OUTPUT
pin_red.value = 1

bt = digitalio.DigitalInOut(board.GP10)
bt.pull = digitalio.Pull.DOWN
a = bt.value # False for open, True for pushed

# spk = digitalio.DigitalInOut(board.GP11)
# spk.direction = digitalio.Direction.OUTPUT

i2c = busio.I2C(scl=board.GP1,sda=board.GP0)
i2c.try_lock()
i2c.writeto(0x70, bytes([0b00100001]))  # 0010_xxx1 Turn the oscillator on 
i2c.writeto(0x70, bytes([0b11101111]))  # 1110_1111 Full brightness
i2c.writeto(0x70, bytes([0b10000001]))  # 1000_x001 Blinking off, display on
i2c.writeto(0x70, bytes([0, 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]))

i2c.writeto(0x70, bytes([0, 1,0,0,0,1,0,0,0,1,0,0,0,0,0,0,1]))


```