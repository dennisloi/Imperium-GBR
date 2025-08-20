#!/bin/bash

# Ensure a path is provided
if [ -z "$1" ]; then
  echo "Usage: $0 <path>"
  exit 1
fi

INPUT_PATH="$1"

# Function to process .pak files in a given directory with custom output base
process_pak_files() {
  local SEARCH_DIR="$1"
  local OUTPUT_BASE="$2"

  if [ ! -d "$SEARCH_DIR" ]; then
    echo "Directory not found: $SEARCH_DIR"
    return
  fi

  find "$SEARCH_DIR" -type f -name "*.pak" | while read -r pakfile; do
    # Extract the filename without path or extension
    pakname=$(basename "$pakfile" .pak)

    # Define the destination directory
    dest_dir="$OUTPUT_BASE/$pakname"

    echo "Extracting $pakfile to $dest_dir"

    # Run the Python extraction tool
    python3 tools/paktool/extractPak.py "$pakfile" "$dest_dir"
  done
}

# Process Packs and local folders
process_pak_files "$INPUT_PATH/Packs" "assets/Packs"
process_pak_files "$INPUT_PATH/local" "assets/local"
