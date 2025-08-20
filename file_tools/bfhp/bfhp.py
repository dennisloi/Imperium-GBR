address = 0x0

def toHex(data):
    return ' '.join(f'{byte:02X}' for byte in data)

def parseTOC():
    print('TOC:')
    i = 0
    while (i < fileLength):
        info0 = f.read(4)
        entryType = f.read(2)
        length = int.from_bytes(f.read(2), byteorder='little')

        entry = f.read(length)
        entry_str = entry.decode('utf-8', errors='replace')
        info0_str = toHex(info0)
        info1_str = toHex(entryType)

        print(f'- {entry_str:<20} ', end="")
        print(f'{info0_str:<11} ', end="")
        print(f'({int.from_bytes(info0, byteorder='little'):<5}) ', end="")

        print(f'{info1_str:<5} ', end="")

        if(entryType == b'\x01\x00'): print("Folder?", end="")
        if(entryType == b'\x00\x00'): print("File?", end="")

        print()
        i += 8
        i += length

def readFile(length):
    file = f.read(length)
    try:
        text = file.decode('utf-8')  # or 'latin-1' if it's not UTF-8
        print(text)
    except UnicodeDecodeError:
        print("[Binary data]")

def seekAndPrint(offset):
    f.seek(offset)
    print(f'--> {hex(offset)}')

def seekNext():
    global address
    address += 0x200
    seekAndPrint(address)

# Open the file
f = open("", "rb")

# Read the first 4 bytes
header = f.read(4)
print(header)

# Read the rest of the header
header = f.read(25)

#print it in hex
print(toHex(header))

# Move the file pointer
seekNext()

# Read the next 4 bytes
fileLength = int.from_bytes(f.read(4), byteorder='little')
print(f'TOC length: {fileLength}')

# Read the rest
unk = f.read(5)
print(f'Unknown: {toHex(unk)}')

seekNext()
seekNext()

# Read TOC
parseTOC()

seekAndPrint(0x800)

fileLength = int.from_bytes(f.read(4), byteorder='little')
print(f'Length: {fileLength}')

unk = f.read(5)
print(f'Unknown: {toHex(unk)}')

seekAndPrint(0xA00)

readFile(fileLength)

f.close()