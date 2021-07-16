import interactor
import pyautogui
import emulator
import threading

# A class to manage multiple emulators by assigning each emulator a thread
class Manager:
    # We use the `prefix` to identify emulators. Any window containing `prefix` will be treated as an emulator.
    # Choose your prefixes wisely!
    def __init__(self, prefix):
        self.__interactor = interactor.Interactor()
        self.__emulators = list(map(lambda x: emulator.Emulator(x), pyautogui.getWindowsWithTitle(prefix)))
        self.__threads = list()

    def start(self):

        for e in self.__emulators:
            t = threading.Thread(target=e.main_loop, args=(self.__interactor, ))

            self.__threads.append(t)

            t.start()

        for thread in self.__threads:
            thread.join()
