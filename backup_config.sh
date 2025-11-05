#!/bin/sh
# Simple backup script for TX-Machina Klipper config

cd /root/printer_data/config || exit 1

# Add all changes
git add -A

# Check if there are changes to commit
if git diff --cached --quiet; then
    echo "No changes to backup"
    exit 0
fi

# Commit with timestamp
git commit -m "Config backup $(date)"

# Push to GitHub
git push origin main

echo "Backup completed successfully!"