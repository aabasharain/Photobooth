import logging

import cups

from photobooth._base import PrinterBase

logger = logging.getLogger(__name__)


class CupsPrinter(PrinterBase):

    def __init__(self):
        cups.setServer("localhost")
        self.printer_name = self._load_default_printer()
        self._conn = ""

    def get_name(self) -> str:
        return self.printer_name

    def start(self) -> bool:
        success = False
        try:
            self.printer_name = self._load_default_printer()
            self._conn = cups.Connection()
            printers = self._conn.getPrinters()
            if self.printer_name not in printers:
                success = False
            else:
                success = True
        except RuntimeError:
            logger.warning("Runtime error when trying to connect to printer")
            success = False
        return success

    def print_file(self, path: str) -> bool:
        try:
            self._conn.printFile(self.printer_name, path, "final image", {})
            return True
        except cups.IPPError:
            logger.warning("Not connected to a printer")
            return False

    def change_default_printer(self) -> None:
        printers = self._conn.getPrinters()
        print("{:25} - {:25}".format("Name", "Device URI"))
        for printer in printers:
            print("{:25} - {:25}".format(printer, printers[printer]['device-uri']))
        self.printer_name = input("Enter the exact name of printer to use: ")
        save_default = input("Save this as default printer? (y/n): ")
        if save_default.lower() == "y":
            self._save_default_printer()

    def _save_default_printer(self) -> None:
        try:
            with open("default_printer.txt", 'w') as f:
                f.write(self.printer_name)
        except IOError:
            logger.warning("Could not save default printer file")

    def _load_default_printer(self) -> str:
        try:
            with open("default_printer.txt") as f:
                return f.read()
        except IOError:
            logger.info("No default printer file found, will prompt on setup")
            return ""
