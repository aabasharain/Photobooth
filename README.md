# Photobooth
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

This is still a work in progress, I will update this readme with more in depth instructions on the setup when I am done.

## Quick Setup

### Python installations

Clone the repository to your preferred destination.

I recommend using a python virtual environment to install all of your libraries, but this is optional.

Install all of the required libraries with pip, the links above should have instructions on how to install each library.

### Hardware connections

Connect your button to GPIO pin 25 (Pin 25 is set by default, but you can change in src/user_interface.py on line 22) and ground on the raspberry pi. See [Raspberry Pi Documentation](https://www.raspberrypi.org/documentation/usage/gpio/).

Connect your DSLR camera into one of the pi's USB ports and turn the camera on. The Pi will not power your camera, unless that is a feature of your particular camera. *Note: I have only tested this with the Canon t3i, but I believe this program should work with any camera compatible with libgphoto2. See [gPhoto2 Supported Cameras](http://gphoto.org/proj/libgphoto2/support.php).*

Connect your printer into one of the pi's USB ports. You will need to configure and setup your printer with CUPS, you can find documentation and instructions online for that. Turn on printer. *Note: I have only tested this with a couple printers, but I've found that if there is a Guten Print driver available it works well. See [Guten Print Supported Printers](http://gimp-print.sourceforge.net/p_Supported_Printers.php).*

Additionally, it is necessary to remove the capability for the Pi to use the camera as a USB drive:

"Raspbian ships with a utility called `gvfs` to allow mounting cameras as virtual file systems.
This enables you to access some camera models as if they were USB storage drives, however, it interferes with our use of the camera, as the operating system then claims exclusive access to the camera.
Thus, we have to disable these functionalities.

*Note: This might break file manager access etc. for some camera models.*

To remove these files, enter the following in a terminal:
```bash
sudo rm /usr/share/dbus-1/services/org.gtk.vfs.GPhoto2VolumeMonitor.service
sudo rm /usr/share/gvfs/mounts/gphoto2.mount
sudo rm /usr/share/gvfs/remote-volume-monitors/gphoto2.mount
sudo rm /usr/lib/gvfs/gvfs-gphoto2-volume-monitor
sudo rm /usr/lib/gvfs/gvfsd-gphoto2
```

You should reboot afterwards to make sure these changes are effective."

[reuterbal/photobooth/Install.md](https://github.com/reuterbal/photobooth/blob/master/INSTALL.md)

### Running the program
Run the "main.py" file in the root folder of the project.

```
python main.py
```
If you want to start in fullscreen, you can add a "-f" flag after main.py.

```
python main.py -f
```

### Default printer setup

During the initial setup, you will have to enter the printer you want to use in the command line. This part is not that user friendly, but it was the simplest setup and you only need to do it once if you use the same printer. A window will pop up when you first run, (if you started in fullscreen press F1 to exit fullscreen and then go to the terminal window) click off of that into the terminal, you will see a list of all available printers. Enter the name of the printer *exactly* and press enter.

After you enter the name you should see a setup screen in the window. It will show the status of the camera and printer connections as well as the name of the printer it is currently connected to. From there you can follow on screen prompts to continue and use the photobooth.

### Optional Shell Script

I recommend using a shell script (e.g. launcher.sh) to clear the printer queue before starting the program, something along the lines of:

launcher.sh:
```
# !/bin/bash

cancel -a
cd /home/pi/path/to/photobooth
python main.py -f
```

or if you are using a virtual environment:


```
# !/bin/bash

cancel -a
cd /home/pi/path/to/photobooth
env/bin/python main.py -f
```

Cancel in particular will cancel all jobs in the printer queue. This is not necessary, but a precaution so that when you start the photobooth you have a clean queue for the printer.

You can then make the shell script executable with chmod:

```
chmod 775 launcher.sh
```

Then start the program with:

```
sudo ./launcher.sh
```

## License

Licensed under GNU General Public License v3.0 (see [LICENSE](https://github.com/aabasharain/Photobooth/blob/master/LICENSE))
