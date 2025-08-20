import os
import shutil
import argparse

if len(os.sys.argv) != 3:
    print("Usage: python extractPak.py <input_pak> <output_directory>")
    exit()

# Get the pak file and output directory from the command line arguments
pakPath = os.sys.argv[1]
outputPath = os.sys.argv[2]

# Open the file
f = open(pakPath, "rb")

# Check signature
signature = f.read(16)
if signature != b'HMMSYS PackFile\n':
    print("Invalid Pak signature")
    exit()

# Constant header part
unknown = f.read(16)

# Read number of stored files
filesN = int.from_bytes(f.read(4), byteorder='little')

# Header length?
unknown2 = int.from_bytes(f.read(4), byteorder='little')

# Read the files
files = []
buffer = []

for i in range(filesN):

    # Read path slice indices
    highIndex = int.from_bytes(f.read(1), byteorder='little')
    lowIndex = int.from_bytes(f.read(1), byteorder='little')
    pathLength = highIndex - lowIndex

    # Ensure buffer is large enough
    if len(buffer) < highIndex:
        buffer.extend([''] * (highIndex - len(buffer)))

    # Read the new part of the path and decode it
    pathPart = f.read(pathLength)
    decodedPart = pathPart.decode('utf-8')

    # Update only the slice in the buffer
    buffer[lowIndex:highIndex] = list(decodedPart)

    # Join only up to high_index to form the path
    path = ''.join(buffer[:highIndex])
    print(f"File name: {path}")

    # Read metadata
    fileLocation = int.from_bytes(f.read(4), byteorder='little')
    fileSize = int.from_bytes(f.read(4), byteorder='little')

    # Create a dict and add it to files
    el = {
        "path" : path,
        "location" : fileLocation,
        "size" : fileSize
    }
    files.append(el)

# Create the output folder
os.makedirs(outputPath, exist_ok=True)

# Clean the output folder
for item in os.listdir(outputPath):
    item_path = os.path.join(outputPath, item)

    if os.path.isfile(item_path) or os.path.islink(item_path):
        os.remove(item_path)
    elif os.path.isdir(item_path):
        shutil.rmtree(item_path)

# Extract the files
for el in files:

    # Split the path
    pathSplit = el["path"].split("\\")

    # Remove the filename to maintain only the folders tree
    folders = pathSplit[:-1]

    # Extract the file name
    fileName = pathSplit[-1]

    # Navigate to the file location
    f.seek(el["location"])

    # Read the file
    fileData = f.read(el["size"])

    # Create folder structure
    full_path = os.path.join(outputPath, *folders)
    os.makedirs(full_path, exist_ok=True)

    # Write the file
    with open(os.path.join(full_path, fileName), "wb") as outFile:
        outFile.write(fileData)
        print(f'Extracted: {fileName}')

f.close()
