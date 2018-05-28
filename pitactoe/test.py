import Display
import LEDButton

display = Display.Display(address=0x72)

display.set_pixel(0,0,1)
display.set_pixel(1,1,2)
display.set_pixel(2,2,3)

display.write_display()

button = LEDButton.LEDButton()
button.set_color(3)

print(button.get_button())
