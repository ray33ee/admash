import numpy as np
import pyautogui

from time import sleep

# Class representing the window of the emulator
class Emulator:

    TitleBarHeight = 31
    ToolBarWidth = 31

    def __init__(self, window):
        self.__window = window

    def title(self):
        return self.__window.title

    # Restore the window and activate it
    def show(self, delay=0.2):
        # self.__window.restore()
        self.__window.activate()

        sleep(delay)  # Wait for the contents of the window to render

    # Minimise the window
    def hide(self, delay=1):
        # sleep(delay)  # wait a few seconds for the screen to resize before we minimise

        # self.__window.minimize()
        pass

    # Obtain a cropped screenshot of the window
    def screenshot(self):

        screen = np.array(pyautogui.screenshot())

        window_screenshot = screen[self.__window.topleft.y + self.TitleBarHeight: self.__window.topleft.y + self.__window.height,
                            self.__window.topleft.x: self.__window.topleft.x + self.__window.width - self.ToolBarWidth]

        return window_screenshot

    # Click on the window using coordinates local to the emulator window itself. Move to and then click
    def click_local(self, x, y):

        global_x, global_y = (self.__window.topleft.x + x, self.__window.topleft.y + y + self.TitleBarHeight)

        pyautogui.moveTo(global_x, global_y)

        pyautogui.click()

    def main_loop(self, interactor):
        while True:
            # Click the watch button
            print(self.title() + " " + str(interactor.click_watch(self)))

            # Wait initial 20 seconds, no ads wil finish faster than this
            for i in range(60):
                print(self.title() + " (initial) ad wait " + str(i))
                sleep(1)

            # If a blackscreen appears, handle it then continue the loop. See Interactor.blackscreen_handler.
            if interactor.blackscreen_handler():
                continue

            # Try and close ad
            print(self.title() + " " + str(interactor.click_x(self)))

            sleep(1)

            # Wait for the screen to settle
            for i in range(10):
                print(self.title() + " wait for 'Ok' " + str(150 - i))
                sleep(1)

            # Click 'Ok'
            print(self.title() + " " + str(interactor.click_ok(self)))

            # Wait 2.5 minutes minus the 'Ok' delay since the cooldown timer starts from the moment the ad ends,
            # regardless of whether the user selects the 'Ok' button

            for i in range(140):
                print(self.title() + " cooldown " + str(140 - i))
                sleep(1)
