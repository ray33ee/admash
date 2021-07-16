import threading
import cv2 as cv
import numpy as np
import pytesseract

from importlib.machinery import SourceFileLoader


foo = SourceFileLoader("module.name", "..\\adentify\\adentify.py").load_module()

# A class representing all interactions with the desktop,
# including screenshots, mouse control, and minimising/maximising
# This Object must use a lock
class Interactor:
    def __init__(self):
        self.__lock = threading.Lock()

    def __try_adentify(self, emulator):

        window_screenshot = emulator.screenshot()

        ad = foo.adentify(window_screenshot, sizes=[200])

        if "point" in ad:
            return ad["point"]

        return None

    def __locate_orange_buttons(self, emulator):

        image = emulator.screenshot()

        results = {
            "watch": None,
            "ok": None
        }

        grey = cv.cvtColor(image, cv.COLOR_BGR2GRAY)

        cropped = cv.Canny(grey, 200, 255)

        contours, hierarchy = cv.findContours(cropped, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)

        buff = np.zeros(image.shape)

        for index in range(len(contours)):
            cont = contours[index]

            poly = cv.approxPolyDP(cont, 3, True)

            sides = len(poly)

            x, y, w, h = cv.boundingRect(cont)

            snippet = grey[y: y + h, x: x + w]

            # Get a histogram of the snippet
            hist = cv.calcHist([snippet], [0], None, [256], [0, 256])

            # Buttons are mostly orange with a little white. We obtain a fraction representing the orange and white
            # pixels divided by the total number of pixels.
            ratio = (hist[74] + hist[255]) / (w * h)

            if sides == 4 and ratio > 0.5:

                ret, snippet = cv.threshold(snippet, 150, 170, cv.THRESH_BINARY)

                button_text = pytesseract.image_to_string(snippet, config="--psm 10")

                if button_text.lower().__contains__("watch"):
                    results["watch"] = (int(x + w / 2), int(y + h / 2))
                    return results

                if "ok" in button_text.lower() or "0k" in button_text.lower():
                    results["ok"] = (int(x + w / 2), int(y + h / 2))
                    return results

                buff.fill(0)

        return results

    def __click_button(self, emulator, text):
        with self.__lock:
            emulator.show()

            result = self.__locate_orange_buttons(emulator)[text]

            if result is not None:
                emulator.click_local(*result)

            emulator.hide()

            return result

    # This function will search the emulator for the 'Watch' button and click it.
    def click_watch(self, emulator, ):
        return self.__click_button(emulator, "watch")

    # This function will search the emulator for the 'Ok' button and click it.
    def click_ok(self, emulator):
        return self.__click_button(emulator, "ok")

    # This function will search the emulator for 'X' button to close the ad, then click it
    def click_x(self, emulator):
        with self.__lock:
            emulator.show()

            result = self.__try_adentify(emulator)

            if result is not None:
                emulator.click_local(*result)

            emulator.hide()

            return result

    # Occasionally at the end of adverts a black screen will appear instead of the usual final screen. This function
    # will detect and handle it (quit the emulator, load the app, scroll to bottom). If this function returns true, a black
    # screen has been detected.
    def blackscreen_handler(self):
        return False

