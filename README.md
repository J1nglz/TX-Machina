# TX-Machina Klipper Configuration

This is the Klipper configuration repository for the TX-Machina 3D printer - a completely overhauled Infimech TX.

## Current Status
- **Printer:** TX-Machina (Mellow Fly-Super8 v1.2)
- **MCU:** RP2040 (Katapult bootloader)
- **Toolhead MCU:** STM32F072xb (Klipper firmware)
- **Last Updated:** November 5, 2025

## Repository Contents
- printer.cfg - Main Klipper configuration
- moonraker.conf - Moonraker API configuration
- mainsail.cfg / luidd.cfg - Web interface configurations
- KAMP/ - Klipper Adaptive Meshing & Purging
- Automatic configuration backups with timestamps

## Klipper Backup Setup
This repository uses klipper-backup for automated configuration version control.

 **[Setup Instructions](KLIPPER_BACKUP_SETUP.md)** - Complete guide for SSH authentication and automatic backups

## Quick Access
SSH to printer: ssh -i ~/.ssh/tx_machina_key root@192.168.1.234

Config location: /root/printer_data/config/

## Hardware Info
- **MCU Devices:**
  - Main: usb-katapult_rp2040_12345-if00 (ttyACM1)
  - Toolhead: usb-Klipper_stm32f072xb_3E0032001057435633333820-if00 (ttyACM0)
