import os
from PIL import Image

# Typical header
header_hex = [
    0x44, 0x49, 0x52, 0x47, # 'DIRG'
    0x10, 0x00, 0x00, 0x00, # 16 bytes of unknown data
    0x01, 0x00, 0x00, 0x00,
    0x00, 0x08, 0x00, 0x00,
    0x00, 0x08, 0x00, 0x00
]

if len(os.sys.argv) != 3:
    print("Usage: python extractPASS.py <input_PASS> <output_directory>")
    exit()

# Get the pak file and output directory from the command line arguments
inputPath = os.sys.argv[1]
outputPath = os.sys.argv[2]

# Open the file
hexFile = []
with open(inputPath, 'rb') as f:
    byte = f.read(1)
    while byte:
        # Convert byte to a 2-character hex string
        hex_value = format(ord(byte), '02x')
        # Extend the list with the hex value
        hexFile.append(hex_value)
        byte = f.read(1)


# Check the magic
if hexFile[0:4] != [format(x, '02x') for x in header_hex[0:4]]:
    print("Invalid file format")
    exit(1)

for i in range(4, 20):
    if hexFile[i] != format(header_hex[i], '02x'):
        print(f"Different Header! {i}: expected {format(header_hex[i], '02x')}, got {hexFile[i]}")
        exit(1)

# Remove the first 20 bytes (header)
# magic + 16 bytes (unknown)
hexFile = hexFile[4+16:]

# The image width is always 16, so the rows number can be calculated
rows = len(hexFile) // 16

bit_array = []
for i in range(rows - 1, -1, -1):   
    row = []
    for j in range(15): # 15 as the last byte is end of line marker of some sort
        # Read one byte
        byte = hexFile[i  * 16 + j]
        # Convert it into bits
        bits = format(int(byte, 16), '08b')
        # Reverse the bits
        bits = bits[::-1]
        # Convert the bits to integers
        bits = [int(bit) for bit in bits]
        # Append the bits to the row
        row.extend(bits)
    bit_array.append(row)

# Convert bit_array to a PIL Image and save as PNG
height = len(bit_array)
width = len(bit_array[0]) if height > 0 else 0

img = Image.new('L', (width, height))
for y, row in enumerate(bit_array):
    for x, val in enumerate(row):
        img.putpixel((x, y), 255 if val else 0)

img.save(outputPath, format='PNG')
