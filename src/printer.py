import cups

class Printer():

    def __init__(self):
        cups.setServer("localhost")
        self.printer_name = ""
        self.conn = ""

    def start(self):
        success = False
        try:
            self.conn = cups.Connection()
            printers = self.conn.getPrinters()

            print("{:15} - {:15}".format("Name", "Device URI"))
            for printer in printers:
                print("{:15} - {:15}".format(printer, printers[printer]['device-uri']))

            self.printer_name = input("Enter the exact name of printer to use: ")
            while not self.printer_name in printers:
                print("Please enter it exactly as shown above")
                self.printer_name = input("Enter the exact name of printer to use: ")

            success = True
        except RuntimeError:
            print("Runtime Error when trying to connect to printer...")
            success = False

        return success

    def print_image(self, img):
        self.conn.printFile(self.printer_name, img, "final image", {})
