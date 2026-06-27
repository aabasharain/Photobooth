import logging
from pathlib import Path

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
            success = self.printer_name in printers
        except RuntimeError:
            logger.warning("Runtime error when trying to connect to printer")
            success = False
        return success

    def print_file(self, path: str) -> bool:
        try:
            self._conn.printFile(self.printer_name, path, "final image", {})
        except cups.IPPError:
            logger.warning("Not connected to a printer")
            return False
        else:
            return True

    def change_default_printer(self) -> None:
        printers = self._conn.getPrinters()
        print("{:25} - {:25}".format("Name", "Device URI"))
        for printer in printers:
            print("{:25} - {:25}".format(printer, printers[printer]["device-uri"]))
        self.printer_name = input("Enter the exact name of printer to use: ")
        save_default = input("Save this as default printer? (y/n): ")
        if save_default.lower() == "y":
            self._save_default_printer()

    def _save_default_printer(self) -> None:
        try:
            Path("default_printer.txt").write_text(self.printer_name)
        except OSError:
            logger.warning("Could not save default printer file")

    def _load_default_printer(self) -> str:
        try:
            return Path("default_printer.txt").read_text()
        except OSError:
            logger.info("No default printer file found, will prompt on setup")
            return ""
