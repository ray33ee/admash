from manager import Manager
import sys


if __name__ == "__main__":
    if len(sys.argv) > 1:
        prefix = sys.argv[1]

        m = Manager(prefix)
        m.start()
    else:
        print("Invalid number of command line arguments")




