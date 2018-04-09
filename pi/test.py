
ADDRESS = 0x72

from hardware import LED8x8
#from hardware import LightButton

#but = LightButton(11,13,15)
#print(str(but.get_button()))
#but.set_color(0)

disp = LED8x8(ADDRESS)

#disp.draw_raw_image([1,0,0,0,255,0,0,0])

#disp.draw_raw_image([0x0E,0x0E,0x05,0x05,0x2E,0x0E,0x20,0x00,0xE0,0x00,0x20,0x09,0x20,0x09,0x00,0x06])

sprite = ['1111',
          '1321',
          '1231',
          '1111']

disp.draw_sprite(0,2,sprite)
disp.refresh_display()