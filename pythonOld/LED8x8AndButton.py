from Tkinter import Tk, Button


class LED8x8AndButton(object):

    def __init__(self, buttonDownCallback=None, buttonUpCallback=None):
        self.root = Tk()
        self.root.title("8x8")

        self.buttonUpCallback = buttonUpCallback
        self.buttonDownCallback = buttonDownCallback

        self.pixels = []

        for y in xrange(8):
            for x in xrange(8):
                bt = Button(self.root,
                            bg="gray",
                            width=2, height=1,
                            state="disabled")
                self.pixels.append(bt)
                bt.grid(column=x, row=y)

        self.but = Button(self.root, text="#",
                          width=3, height=1)
        self.but.grid(column=3, row=8, columnspan=2)

        self.butColor = Button(self.root, state="disabled", width=3)
        self.butColor.grid(column=1, row=8, columnspan=2)

        self.orgColor = self.butColor.cget("bg")

        self.but.bind("<Button-1>", self._buttonDown)
        self.but.bind("<ButtonRelease-1>", self._buttonUp)

    def mainLoop(self):
        self.root.mainloop()

    def _setXY(self, x, y, val):
        if val == 0:
            self.pixels[y * 8 + x].configure(bg="gray")
        elif val == 1:
            self.pixels[y * 8 + x].configure(bg="green")
        elif val == 2:
            self.pixels[y * 8 + x].configure(bg="red")
        elif val == 3:
            self.pixels[y * 8 + x].configure(bg="orange")
        else:
            self.pixels[y * 8 + x].configure(bg="white")

    def setButtonColor(self, val):
        if val == 0:
            self.butColor.configure(bg=self.orgColor)
        elif val == 1:
            self.butColor.configure(bg="green")
        elif val == 2:
            self.butColor.configure(bg="red")
        elif val == 3:
            self.butColor.configure(bg="orange")
        else:
            self.butColor.configure(bg="white")

    def writeDisplay(self, image):
        pos = 0
        for x in xrange(8):
            sv = 1
            v1 = ord(image[pos])
            v2 = ord(image[pos + 1])
            pos = pos + 2
            for y in xrange(8):
                pv = 0
                if (v1 & sv) != 0:
                    pv = pv | 1
                if (v2 & sv) != 0:
                    pv = pv | 2
                sv = sv << 1
                self._setXY(7 - x, y, pv)

    def _buttonDown(self, event):
        if self.buttonDownCallback:
            self.buttonDownCallback()

    def _buttonUp(self, event):
        if self.buttonUpCallback:
            self.buttonUpCallback()

if __name__ == "__main__":

    def up():
        im = "\x0E\x00\x05\x00\x05\xA0\x0E\xA0\x00\xE0\x01\x01\x0F\x0F\x01\x01"
        emu.writeDisplay(im)
        emu.setButtonColor(0)
        print "UP"

    def down():
        emu.setButtonColor(1)
        print "DOWN"

    emu = LED8x8AndButton(down, up)
    emu.mainLoop()
