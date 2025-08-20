import os
from PIL import Image

# Typical header
header_hex = [
    0x44, 0x49, 0x52, 0x47,  # 'DIRG'
    0x10, 0x00, 0x00, 0x00,  # 16 bytes of unknown data
    0x01, 0x00, 0x00, 0x00,
    0x00, 0x08, 0x00, 0x00,
    0x00, 0x08, 0x00, 0x00
]

if len(os.sys.argv) != 3:
    print("Usage: python createPASS.py <input_image> <output_pass>")
    print("Example: python createPASS.py horse_pass.png horse.pass")
    exit()

# Get file paths
inputPath = os.sys.argv[1]
outputPath = os.sys.argv[2]

# Load image and convert to grayscale
img = Image.open(inputPath).convert('L')

# Convert to binary (0 or 1) based on threshold
width, height = img.size
pixels = list(img.getdata())
binary_matrix = []

for y in range(height):
    row = []
    for x in range(width):
        pixel = pixels[y * width + x]
        row.append(1 if pixel > 127 else 0)
    binary_matrix.append(row)

# Flip vertically (bottom to top)
binary_matrix.reverse()

header_bytes = bytes(header_hex)

# Open output file
with open(outputPath, 'wb') as f:
    # Write header
    f.write(header_bytes)

    for row in binary_matrix:
        for i in range(0, 120, 8):  # 15 bytes = 120 bits
            bits = row[i:i+8]
            if len(bits) < 8:
                bits += [0] * (8 - len(bits))  # Pad with zeros
            bits_reversed = bits[::-1]
            byte = int(''.join(str(b) for b in bits_reversed), 2)
            f.write(byte.to_bytes(1, 'big'))
        # End-of-line marker
        f.write(b'\x00')
