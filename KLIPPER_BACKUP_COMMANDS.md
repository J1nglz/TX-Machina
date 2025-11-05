# Klipper-Backup Quick Reference

Quick command reference for using klipper-backup with your TX-Machina repository.

## Common Commands

### Manual Backup
Trigger a backup immediately:
```bash
klipper-backup
```

### Check Backup Status
Check if the backup service is running:
```bash
sudo systemctl status klipper-backup
```

### View Backup Logs
See recent backup activity:
```bash
journalctl -u klipper-backup -n 50
```

### Restart Backup Service
If you've changed configuration:
```bash
sudo systemctl restart klipper-backup
```

### Stop/Start Automatic Backups
```bash
sudo systemctl stop klipper-backup
sudo systemctl start klipper-backup
```

### Disable/Enable Automatic Backups
```bash
sudo systemctl disable klipper-backup
sudo systemctl enable klipper-backup
```

## Backup Configuration Location

Configuration file:
```bash
nano ~/.klipper_backup/backup.cfg
```

Local repository clone:
```bash
cd ~/.klipper_backup/TX-Machina
```

## Manual Git Operations

Sometimes you may need to manually interact with the backup repository:

### View Recent Commits
```bash
cd ~/.klipper_backup/TX-Machina
git log --oneline -10
```

### View What Changed
```bash
cd ~/.klipper_backup/TX-Machina
git diff HEAD~1
```

### Pull Latest Changes from GitHub
```bash
cd ~/.klipper_backup/TX-Machina
git pull origin main
```

### Force Push (Use with Caution)
If you need to force push (only if absolutely necessary):
```bash
cd ~/.klipper_backup/TX-Machina
git push -f origin main
```

## Checking SSH Connection

Verify SSH authentication to GitHub:
```bash
ssh -T git@github.com
```

Expected output:
```
Hi J1nglz! You've successfully authenticated, but GitHub does not provide shell access.
```

### Verbose SSH Test
If having issues, use verbose mode:
```bash
ssh -Tv git@github.com
```

## Configuration File Format

Example `~/.klipper_backup/backup.cfg`:
```ini
[repo]
url = git@github.com:J1nglz/TX-Machina.git
branch = main

[paths]
klipper_config = ~/printer_data/config
klipper_logs = ~/printer_data/logs

[backup]
interval = 3600
commit_message = Backup {timestamp}
```

## Troubleshooting Commands

### Check SSH Key
```bash
ls -la ~/.ssh/
cat ~/.ssh/id_ed25519.pub
```

### Test Git Remote
```bash
cd ~/.klipper_backup/TX-Machina
git remote -v
git fetch origin
```

### View Local Changes (Not Yet Committed)
```bash
cd ~/.klipper_backup/TX-Machina
git status
git diff
```

### Reset Local Changes (CAUTION: Loses Local Edits)
```bash
cd ~/.klipper_backup/TX-Machina
git reset --hard origin/main
```

## Customization Tips

### Custom Commit Messages
Edit `backup.cfg` to customize commit messages:
```ini
commit_message = Backup from TX-Machina - {timestamp}
```

### Exclude Files
Add files to `.gitignore` in the repository to exclude them from backups.

### Change Backup Frequency
Modify the `interval` value in `backup.cfg` (in seconds):
- 1800 = 30 minutes
- 3600 = 1 hour
- 7200 = 2 hours
- 86400 = 24 hours

## Getting Help

- **klipper-backup Issues**: https://github.com/Staubgeborener/klipper-backup/issues
- **Full Setup Guide**: See [KLIPPER_BACKUP_SETUP.md](KLIPPER_BACKUP_SETUP.md)
- **GitHub SSH Help**: https://docs.github.com/en/authentication/connecting-to-github-with-ssh
