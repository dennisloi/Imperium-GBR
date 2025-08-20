import io
import os

if len(os.sys.argv) != 3:
    print("Usage: python createPak.py <input_directory> <output_pak>")
    exit()

# Get the pak file and output directory from the command line arguments
inputFolderPath = os.sys.argv[1]
outputPath = os.sys.argv[2]

def intToBytes(number, lenght=4, byteorder='little'):
    return number.to_bytes(lenght, byteorder=byteorder)


# Scan the input folder to create a list of files with relative paths
# TODO: the order of these files will be probably different from the one in the original file
# The logic in which order the files are stored in the pak file is not clear yet
files = []
for root, dirs, filenames in os.walk(inputFolderPath):
    for filename in filenames:
        # Get the relative path of the file
        relative_path = os.path.relpath(os.path.join(root, filename), inputFolderPath)
        # Append the relative path to the list
        files.append(relative_path)

# Create a memory buffer
buffer = io.BytesIO()

# Write the signature
buffer.write(b'HMMSYS PackFile\n')

# Write the constant part of the header
buffer.write(intToBytes(26, 16))

# Write the number of files
buffer.write(intToBytes(len(files), 4))

# The next bytes to be written contain the header length, so it needs to be computed before

header = []
pathBuffer = []

for path in files:

    # Ensure the buffer is large enough
    if len(pathBuffer) < len(path):
        pathBuffer.extend([''] * (len(path) - len(pathBuffer)))
    
    # Check if part of the path is already in the buffer
    highIndex = 0
    lowIndex = None
    for i, c in enumerate(path):
        # Check if the character is not already in the buffer
        if pathBuffer[i] != c:
            lowIndex = i
            break
    
    # If the path completely matches the buffer, two files have the same name
    if lowIndex is None:
        print(f'Error: File {path} duplicated')
        exit()
    
    highIndex = len(path)

    # Write only the new part of the path
    pathPart = path[lowIndex:highIndex]

    # Update the buffer for the next iteration
    pathBuffer[lowIndex:highIndex] = pathPart

    entry = {
        'fullPath': path,
        'path': pathPart,
        'highIndex': highIndex,
        'lowIndex': lowIndex,
    }

    header.append(entry)
    
# Calculate and write the size of the header
headerLength = 0
for entry in header:
    headerLength += len(entry['path']) + 10
buffer.write(intToBytes(headerLength, 4))

# Write the files header
filePosition = headerLength + 32 + 8 # 32 is the length of the main header
for entry in header:

    # Write the path slice indices
    buffer.write(intToBytes(entry['highIndex'], 1))
    buffer.write(intToBytes(entry['lowIndex'], 1))

    #TODO is this linux specific?
    # Write file path and name
    buffer.write(entry['path'].replace("/", "\\").encode('utf-8'))

    # Write the file position
    buffer.write(intToBytes(filePosition, 4))

    # Get the file size
    filePath = os.path.join(inputFolderPath, entry['fullPath'])
    fileSize = os.path.getsize(filePath)

    # Write the file size
    buffer.write(intToBytes(fileSize, 4))

    # Increment the file position
    filePosition += fileSize

# Add 4 bytes per file to the header (unknown purpose)
for entry in header:
    # Write the file size
    buffer.write(intToBytes(0, 4))

# Create the full output path if it doesn't exist
os.makedirs(os.path.abspath(os.path.dirname(outputPath)), exist_ok=True)

# Write the buffer to the output file
with open(outputPath, "wb") as outFile:
    # Write the buffer content to the file
    outFile.write(buffer.getvalue())
    print(f'Created: {outputPath}')

# Write the files
for f in files:

    # Get the file path
    filePath = os.path.join(inputFolderPath, f)

    # Read the file content
    with open(filePath, "rb") as inFile:
        fileData = inFile.read()

    # Write the file content to the output file
    with open(outputPath, "ab") as outFile:
        outFile.write(fileData)
        print(f'Added: {f}')
