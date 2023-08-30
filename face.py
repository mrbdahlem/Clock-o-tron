import neopixel

class Display(neopixel.NeoPixel):
    def __init__(self, pin, on_color, off_color):
        self._neopixels = neopixel.NeoPixel(pin, 16)
        self.on_color = on_color
        self.off_color = off_color

    def show(self, hour, minute, seconds):
        h = hour % 12
        if (h == 0):
            h = 12

        self._set_pixels(seconds, 0, 6) # seconds is pixels #0-5
        self._set_pixels(minute, 6, 6)  # minute is pixels #6-11
        self._set_pixels(h, 12, 4)   # hour is pixels #12-15

        self._neopixels.write()        

    def _set_pixels(self, number, start, count):
        for n in range(count):
            bit = number & 0x01
            number >>= 1

            if bit == 0:
                self._neopixels[start + n] = self.off_color
            else:
                self._neopixels[start + n] = self.on_color

        self._neopixels.write()
