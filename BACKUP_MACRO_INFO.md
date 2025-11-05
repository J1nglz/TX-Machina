# Backup Config Macro

A macro button has been added to trigger manual configuration backups to GitHub.

## How to Use in Fluidd

1. Open Fluidd web interface (http://192.168.1.234/)
2. Navigate to the **Console** tab
3. Look for the **BACKUP_CONFIG** macro in the macros panel (usually on the right side)
4. Click the **BACKUP_CONFIG** button to trigger a backup

Alternatively, you can type in the console:
\\\
BACKUP_CONFIG
\\\

## What It Does

- Executes the klipper-backup script
- Commits any configuration changes
- Pushes to GitHub repository: https://github.com/J1nglz/TX-Machina
- Displays confirmation message in console

## Configuration

The macro is defined in \printer.cfg\:
\\\
[gcode_shell_command backup_to_github]
command: sh /root/klipper-backup/script.sh
timeout: 30.0
verbose: True

[gcode_macro BACKUP_CONFIG]
description: Backup config to GitHub
gcode:
    RUN_SHELL_COMMAND CMD=backup_to_github
    RESPOND MSG=Configuration backup initiated
\\\

## Automatic Backups

Note: Backups are already automated via Moonraker. This button is for manual on-demand backups.

