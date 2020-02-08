import sys
sys.path.append("../src/")

from photobooth import Photobooth

pb = Photobooth()

pb.setup()

pb.start()
