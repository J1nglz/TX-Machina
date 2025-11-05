# Hardware Configuration Directory

This directory contains hardware-specific configuration files for your Klipper setup.

## Purpose

Separating hardware configurations makes it easier to:
- Manage different hardware components
- Update individual components without affecting others
- Share hardware configs across different printer configurations
- Document hardware changes over time

## Common Hardware Configs

Examples of files you might keep here:

- `extruder.cfg` - Extruder settings and tuning
- `bed.cfg` - Heated bed configuration
- `steppers.cfg` - Stepper motor settings
- `sensors.cfg` - Temperature sensors, endstops, probes
- `fans.cfg` - Part cooling, hotend, controller fans
- `leds.cfg` - LED strip configurations (Neopixels, etc.)
- `display.cfg` - Display and menu configuration
- `accelerometer.cfg` - Input shaper / ADXL345 setup

## Usage

Include these files in your main `printer.cfg`:

```ini
[include config/hardware/extruder.cfg]
[include config/hardware/bed.cfg]
[include config/hardware/steppers.cfg]
# Add more as needed
```

## Tips

- Document any hardware modifications in comments
- Keep pin assignments clear and commented
- Note any specific calibration values and when they were determined
- Back up before making significant hardware changes
