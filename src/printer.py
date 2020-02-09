# Photobooth. Python application designed to run a photobooth setup with
# a Raspberry Pi, DSLR camera and a printer.
# Copyright (C) 2020  Aaron Basharain

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

import cups

class Printer():

    def __init__(self):
        cups.setServer("localhost")
        self.printer_name = self.load_default_printer()
        self.conn = ""

    def get_name(self):
        return self.printer_name
    def start(self):
        success = False
        try:
            self.printer_name = self.load_default_printer()
            self.conn = cups.Connection()
            printers = self.conn.getPrinters()

            while not self.printer_name in printers:
                self.change_default_printer()

            success = True
        except RuntimeError:
            print("Runtime Error when trying to connect to printer...")
            success = False

        return success

    def change_default_printer(self):
        printers = self.conn.getPrinters()
        print("{:25} - {:25}".format("Name", "Device URI"))
        for printer in printers:
            print("{:25} - {:25}".format(printer, printers[printer]['device-uri']))
        self.printer_name = input("Enter the exact name of printer to use: ")
        save_default = input("Save this as default printer? (y/n): ")
        if save_default == "y" or save_default == "Y":
            self.save_default_printer()
            
    def save_default_printer(self):
        try:
            file = open("default_printer.txt", 'w+')
            file.write(self.printer_name)
            file.close()
            
        except IOError:
            print("Error opening default printer file...")
        
    def load_default_printer(self):
        try:
            file = open("default_printer.txt", 'r')
            name = file.read()
            file.close()
        except IOError:
            print("Error opening default printer file...")
            name = ""
            
        return name
    
    def print_image(self, img):
        self.conn.printFile(self.printer_name, img, "final image", {})
