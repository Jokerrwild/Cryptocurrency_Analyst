#!/bin/bash

# Change to a stable working directory to avoid getcwd() errors.
cd /a0/usr/workdir/ || exit 1

# Configuration
REPO_URL="git@github.com:Jokerrwild/MacReady.git"
REPO_PATH="/a0/usr/workdir/MacReady_repo_ssh"
SSH_KEY_PATH="/a0/secrets/github_deploy_key"

export GIT_SSH_COMMAND="ssh -i $SSH_KEY_PATH -o IdentitiesOnly=yes -o StrictHostKeyChecking=no"

rm -rf "$REPO_PATH"
git clone "$REPO_URL" "$REPO_PATH"

if [ ! -d "$REPO_PATH" ]; then
    echo "Failed to clone repository. Aborting."
    exit 1
fi

BACKUP_BASE_DIR="$REPO_PATH/mac_os"

mkdir -p "$BACKUP_BASE_DIR/prompts" "$BACKUP_BASE_DIR/skills" "$BACKUP_BASE_DIR/knowledge" "$BACKUP_BASE_DIR/configs/projects/crptocurrency_analyst" "$BACKUP_BASE_DIR/scripts"

# Copy core identity files from the correct legacy location
cp -r /a0/prompts/* "$BACKUP_BASE_DIR/prompts/"

# Copy other components
cp -r /a0/skills/* "$BACKUP_BASE_DIR/skills/"
cp -r /a0/usr/knowledge/* "$BACKUP_BASE_DIR/knowledge/"
cp -r /a0/usr/projects/crptocurrency_analyst/.a0proj/* "$BACKUP_BASE_DIR/configs/projects/crptocurrency_analyst/"
cp /a0/usr/workdir/hard_commit_backup.sh "$BACKUP_BASE_DIR/scripts/"

cd "$REPO_PATH" || exit

git config user.name "MacReady AI"
git config user.email "macready@agentzero.bot"
git add .
git commit -m "Hardened Commit: Integrated Core Objective of Continuous Evolution"
git push origin main

echo "Backup complete. Your repository has been updated with my true architectural state."

