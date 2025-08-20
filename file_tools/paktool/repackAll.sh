#!/bin/bash

# Ensure a path is provided
if [ -z "$1" ]; then
  echo "Usage: $0 <path>"
  exit 1
fi

INPUT_PATH="$1"

# Function to process directories and create .pak files
create_pak_files() {
  local SOURCE_BASE="$1"
  local OUTPUT_BASE="$2"

  if [ ! -d "$SOURCE_BASE" ]; then
    echo "Directory not found: $SOURCE_BASE"
    return
  fi

  find "$SOURCE_BASE" -mindepth 1 -maxdepth 1 -type d | while read -r srcdir; do
    # Extract the folder name to use as the pak file name
    pakname=$(basename "$srcdir")
    
    # Define the output .pak file path
    output_pak="$OUTPUT_BASE/$pakname.pak"

    echo "Packing $srcdir to $output_pak"

    # Run the Python packing tool
    python3 tools/paktool/createPak.py "$srcdir" "$output_pak"
  done
}

# Create .pak files from Packs and local folders
create_pak_files "assets/Packs" "$INPUT_PATH/Packs"
create_pak_files "assets/local" "$INPUT_PATH/local"
