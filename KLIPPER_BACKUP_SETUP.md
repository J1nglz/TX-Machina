# Klipper-Backup SSH Setup Guide

This guide will help you set up klipper-backup to automatically backup your Klipper configuration files to this GitHub repository using SSH authentication.

## Overview

klipper-backup is a tool that automatically backs up your Klipper 3D printer configuration files to a GitHub repository. This ensures you never lose your printer configurations and can track changes over time.

## Prerequisites

- Klipper installed on your 3D printer (e.g., on a Raspberry Pi)
- SSH access to your Klipper machine
- This GitHub repository (TX-Machina)

## Step 1: Generate SSH Key on Your Klipper Machine

SSH keys provide secure authentication without needing to enter passwords. You'll need to generate an SSH key pair on your Klipper machine.

1. SSH into your Klipper machine:
   ```bash
   ssh pi@your-printer-ip
   ```

2. Generate a new SSH key pair:
   ```bash
   ssh-keygen -t ed25519 -C "klipper-backup@tx-machina"
   ```
   
   When prompted:
   - File location: Press Enter to use default (`/home/pi/.ssh/id_ed25519`)
   - Passphrase: Press Enter twice for no passphrase (recommended for automation)

3. Display your public key:
   ```bash
   cat ~/.ssh/id_ed25519.pub
   ```
   
   Copy the entire output (starts with `ssh-ed25519` and ends with the comment).

## Step 2: Add SSH Key to GitHub

You have two options for adding the SSH key to GitHub:

### Option A: Deploy Key (Recommended for Single Repository)

Deploy keys are specific to a single repository and are ideal for klipper-backup.

1. Go to your repository: https://github.com/J1nglz/TX-Machina
2. Click **Settings** → **Deploy keys** → **Add deploy key**
3. Title: `Klipper Backup - TX-Machina`
4. Key: Paste your public key from Step 1
5. ✅ Check **Allow write access** (required for pushing backups)
6. Click **Add key**

### Option B: SSH Key in Your Account (For Multiple Repositories)

If you want to use the same key for multiple repositories:

1. Go to GitHub Settings: https://github.com/settings/keys
2. Click **New SSH key**
3. Title: `Klipper Machine - TX-Machina`
4. Key type: **Authentication Key**
5. Key: Paste your public key from Step 1
6. Click **Add SSH key**

## Step 3: Test SSH Connection

Before setting up klipper-backup, verify that SSH authentication works:

```bash
ssh -T git@github.com
```

You should see:
```
Hi J1nglz! You've successfully authenticated, but GitHub does not provide shell access.
```

If you see a warning about authenticity, type `yes` to continue.

## Step 4: Install klipper-backup

On your Klipper machine:

```bash
cd ~
git clone https://github.com/Staubgeborener/klipper-backup.git
cd klipper-backup
./install.sh
```

## Step 5: Configure klipper-backup

1. Edit the configuration file:
   ```bash
   nano ~/.klipper_backup/backup.cfg
   ```

2. Set the following configuration:
   ```ini
   [repo]
   # Use SSH URL for the repository
   url = git@github.com:J1nglz/TX-Machina.git
   branch = main
   
   [paths]
   # Paths to backup (adjust based on your setup)
   klipper_config = ~/printer_data/config
   klipper_logs = ~/printer_data/logs
   
   [backup]
   # How often to check for changes (in seconds)
   interval = 3600
   
   # Commit message template
   commit_message = Backup {timestamp}
   ```

3. Save and exit (Ctrl+X, Y, Enter)

## Step 6: Initialize the Backup

Run the initial backup to set up the repository:

```bash
klipper-backup
```

This will:
- Clone the repository to your Klipper machine
- Copy your configuration files
- Create an initial commit
- Push to GitHub

## Step 7: Enable Automatic Backups

klipper-backup can run automatically using a systemd service:

```bash
sudo systemctl enable klipper-backup
sudo systemctl start klipper-backup
```

To check the status:
```bash
sudo systemctl status klipper-backup
```

## What Gets Backed Up?

Typical files backed up include:
- `printer.cfg` - Main Klipper configuration
- `moonraker.conf` - Moonraker configuration
- Macro files (`*.cfg`)
- Saved variables
- Custom configurations

## Recommended Repository Structure

After backup, your repository might look like:
```
TX-Machina/
├── .gitignore
├── README.md
├── KLIPPER_BACKUP_SETUP.md (this file)
├── printer.cfg
├── moonraker.conf
├── macros/
│   ├── start_print.cfg
│   ├── end_print.cfg
│   └── ...
└── config/
    └── ...
```

## Troubleshooting

### Permission Denied (publickey)

If you see this error:
```
Permission denied (publickey)
```

Solutions:
1. Verify the SSH key was added to GitHub correctly
2. Test SSH connection: `ssh -T git@github.com`
3. Check SSH key permissions: `chmod 600 ~/.ssh/id_ed25519`
4. Ensure the correct key is being used: `ssh-add -l`

### Repository Not Found

If you see:
```
fatal: repository 'git@github.com:J1nglz/TX-Machina.git' not found
```

Solutions:
1. Verify the repository URL in `backup.cfg`
2. Ensure you have access to the repository
3. Check if the deploy key has write access (if using deploy key)

### Merge Conflicts

If you make changes on GitHub and on your Klipper machine:
1. SSH into your Klipper machine
2. Navigate to the backup directory: `cd ~/.klipper_backup/TX-Machina`
3. Pull changes: `git pull origin main`
4. Resolve conflicts if any
5. Run backup again: `klipper-backup`

## Manual Backup

To trigger a backup manually at any time:
```bash
klipper-backup
```

## Security Notes

1. **SSH Keys**: Keep your private key (`id_ed25519`) secure and never share it
2. **Deploy Keys**: Use deploy keys when possible for better security isolation
3. **Sensitive Data**: Avoid committing sensitive information like API keys or passwords
4. **Public Repository**: Be aware this is a public repository. Consider making it private if it contains sensitive configurations

## Fine-Grained Personal Access Tokens (Alternative)

If you prefer using HTTPS with a Personal Access Token instead of SSH:

1. Go to GitHub Settings: https://github.com/settings/tokens?type=beta
2. Click **Generate new token** (Fine-grained token)
3. Token name: `Klipper Backup - TX-Machina`
4. Repository access: **Only select repositories** → Select `TX-Machina`
5. Permissions:
   - Repository permissions → **Contents**: Read and write
   - Repository permissions → **Metadata**: Read-only (automatically selected)
6. Click **Generate token** and copy it immediately (you won't see it again!)
7. Use HTTPS URL in `backup.cfg`:
   ```ini
   url = https://YOUR_TOKEN@github.com/J1nglz/TX-Machina.git
   ```

**Note**: SSH is generally preferred over tokens for automated backups as it's more secure and doesn't expire.

## Additional Resources

- [klipper-backup GitHub Repository](https://github.com/Staubgeborener/klipper-backup)
- [GitHub SSH Documentation](https://docs.github.com/en/authentication/connecting-to-github-with-ssh)
- [Klipper Documentation](https://www.klipper3d.org/)

## Support

For issues specific to:
- **klipper-backup**: Check the [klipper-backup issues](https://github.com/Staubgeborener/klipper-backup/issues)
- **This repository**: Open an issue in this repository
- **Klipper**: Visit [Klipper Discourse](https://community.klipper3d.org/)
