## Photobooth
Photobooth application written in Python designed to be used with a Raspberry Pi, a DSLR camera that is supported by [libgphoto2](http://gphoto.org/proj/libgphoto2/support.php), and a printer that is supported by [CUPS](https://www.cups.org/).

## Hardware Requirements
Raspberry Pi (with power cable, mouse and keyboard)

DSLR Camera

Printer

Button (Optional with keyboard)

HDMI Monitor/Screen

## Required Python Libraries
[gphoto2](https://pypi.org/project/gphoto2/)

[pycups](https://pypi.org/project/pycups/)

[pygame](https://www.pygame.org/)

[gpiozero](https://pypi.org/project/gpiozero/)

## Current Status

This is still a work in progress, I will update this readme with instructions on setup when I am done.

### Known bugs

- There is still an issue with the very first countdown, it consistently skips from 3 to 1 too quickly, however the countdowns after that work as intended. This only happens on the *very first* countdown, so if you do multiple rounds of pictures without exiting the program it works fine on any of them after the first one.

## Setup

Clone the repository to your preferred destination.

I recommend using a python virtual environment to install all of your libraries, but this is optional.

Install all of the required libraries with pip, the links above should have instructions on how to install each library.

Connect your button to GPIO pin 25 (Pin 25 is set by default, but you can change in src/user_interface.py on line 22) and ground on the raspberry pi. See [Raspberry Pi Documentation](https://www.raspberrypi.org/documentation/usage/gpio/)

Connect DSLR camera into one of the pi's USB ports and turn the camera on. The Pi will not power your camera, unless that is a feature of your particular camera.

Connect printer into one of the pi's USB ports. You will need to configure and setup your printer with CUPS, you can find documentation and instructions online for that. Turn on printer.

Run the "main.py" file in the root folder of the project.

```
python main.py
```

During the initial setup, you will have to enter the printer you want to use in the command line. This part is not that user friendly, but it was the simplest setup and you only need to do it once if you use the same printer. A window will pop up when you first run, click off of that into the command line, you will see a list of all available printers. Enter the name of the printer *exactly* and press enter.

After you enter the name you should see a setup screen in the window. It will show the status of the camera and printer connections as well as the name of the printer it is currently connected to. From there you can follow on screen prompts to continue and use the photobooth.

## License

Licensed under GNU General Public License v3.0 (see [LICENSE](https://github.com/aabasharain/Photobooth/blob/master/LICENSE))
