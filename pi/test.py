import smbus
bus = smbus.SMBus(1)

ADDRESS = 0x72

from hardware import LED8x8
from hardware import LightButton

disp = LED8x8(bus,ADDRESS)

but = LightButton(11,13,15)

print(str(but.get_button()))

but.set_color(0)
