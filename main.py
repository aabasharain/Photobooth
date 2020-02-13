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

import sys
sys.path.append("src/")

from photobooth import Photobooth

args = sys.argv

if len(args) > 1 and args[1] == "-f":
    fullscreen = True
else:
    fullscreen = False
    

pb = Photobooth(fullscreen = fullscreen)

pb.start()

