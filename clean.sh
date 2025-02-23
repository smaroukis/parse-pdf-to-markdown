#!/bin/bash

# Define the sandbox directory (modify this path as needed)
SANDBOX_DIR="sandbox"

# Ensure the directory exists
if [ ! -d "$SANDBOX_DIR" ]; then
    echo "Error: Directory $SANDBOX_DIR does not exist."
    exit 1
fi

# Remove everything except the .obsidian folder
find "$SANDBOX_DIR" -mindepth 1 -not -path "$SANDBOX_DIR/.obsidian*" -exec rm -rf {} +

mkdir "sandbox/z_attachments"

echo "Cleanup complete. Preserved .obsidian folder and blank z_attachment folder in sandbox."
