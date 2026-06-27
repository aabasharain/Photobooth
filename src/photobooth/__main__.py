from photobooth.config import Config
from photobooth.photobooth import Photobooth


def main():
    import sys
    config = Config(fullscreen="-f" in sys.argv)
    pb = Photobooth(config=config)
    pb.start()


if __name__ == "__main__":
    main()
