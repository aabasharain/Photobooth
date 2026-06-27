# Photobooth

Python photobooth app for Raspberry Pi. Refactoring to support dual
camera backends: gphoto2 (DSLR USB control) and HDMI capture (USB
HDMI dongle via V4L2/OpenCV).

## Run

```bash
python main.py          # windowed
python main.py -f       # fullscreen
```

## Package

- `pyproject.toml` at root
- Source under `src/photobooth/`
- Dependencies: `gphoto2`, `pycups`, `pygame`, `gpiozero`, `opencv-python` (HDMI capture)

## Architecture — MVC

```
Model
├── CameraBase → Gphoto2Camera / HDMICamera
├── PrinterBase → CupsPrinter
├── PhotoStrip          — compositing (extracted from current create_final_image)
└── Config              — dataclass for settings

View (pure rendering, no model access)
└── Screens / per-state render functions

Controller
├── PhotoboothController — explicit state machine
├── InputHandler         — keyboard + GPIO → actions
└── owns Model instances, calls View
```

## State machine

Opening → Setup → Countdown → Capture(x3) → Compose → Print → Opening

## Controls

| Key | Action |
|-----|--------|
| ESC | Exit |
| F1 | Toggle fullscreen |
| F2 | Change printer |
| F4 | Refresh connections |
| Down / GPIO | Confirm |

## Tests

```bash
python -m pytest          # unit (mocked hardware)
python -m pytest --hw     # integration (real camera/printer)
```

## Conventions

- Camera and Printer behind ABCs for backend swapping
- Config via dataclass, not scattered constants
- Logging, not `DEBUG` globals
- No `sys.path` hacks — proper package
- Capture stills to `images/camera_pictures/<YYYYMMDD>/`
- `.pyc` files excluded from git (clean up legacy committed ones)
