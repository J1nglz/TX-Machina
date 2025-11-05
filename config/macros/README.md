# Macros Directory

This directory contains Klipper macro files for various printer operations.

## Common Macros

You can organize your macros here, such as:

- `start_print.cfg` - Start print macro with bed mesh, heating, etc.
- `end_print.cfg` - End print macro for cleanup
- `pause_resume.cfg` - Pause and resume macros
- `cancel_print.cfg` - Cancel print handling
- `filament_change.cfg` - Filament change procedures
- `maintenance.cfg` - Maintenance and calibration macros
- `custom_commands.cfg` - Custom G-code commands

## Usage

Include these files in your main `printer.cfg`:

```ini
[include config/macros/start_print.cfg]
[include config/macros/end_print.cfg]
# Add more as needed
```

## Tips

- Keep related macros together in single files
- Use descriptive names
- Add comments to explain complex macro logic
- Test macros thoroughly before use
