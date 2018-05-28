import Display
import LEDButton

display = Display.Display(address=0x72)

display.clear()
display.write_display()

button = LEDButton.LEDButton()
button.set_color(0)

