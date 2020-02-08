import cups

class Printer():

    def __init__(self):
        cups.setServer("localhost")

    def start(self):

        success = False
        try:
            conn = cups.Connection()
            printers = conn.getPrinters()

            success = True
        except RuntimeError:
            print("Runtime Error when trying to connect to printer...")
            success = False

        return success
