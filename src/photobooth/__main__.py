from photobooth.photobooth import Photobooth


def main():
    import sys
    fullscreen = "-f" in sys.argv
    pb = Photobooth(fullscreen=fullscreen)
    pb.start()


if __name__ == "__main__":
    main()
