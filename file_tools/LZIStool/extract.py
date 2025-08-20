bit_list = []

with open('/config.ini', 'rb') as f:
    byte = f.read(1)
    while byte:
        # Convert byte to 8-bit binary string, e.g., '01101001'
        bits = format(ord(byte), '08b')
        # Extend the list with individual bits (as characters)
        bit_list.extend(bits)
        byte = f.read(1)

def read_bits(num):
    global bitOffset
    
    bit_str = ''.join(bit_list[bitOffset:bitOffset+num])

    bitOffset += num

    return int(bit_str, 2)

def readTable(length):
   
    length_bits = read_bits(2) + 2
    # print(f'Length bits: {length_bits}')

    table = []

    for _ in range(length):
        if length_bits > 0:
            value = read_bits(length_bits)
        else:
            value = 0
        table.append(value)
    
    return table

def generate_huffman_codes(lengths):

    num_entries = len(lengths)
    
    # Step 1: Find the maximum bit length
    max_length = max(lengths) if lengths else 0

    # Step 2: Count the number of codes for each bit length
    bl_count = [0] * (max_length + 1)
    for length in lengths:
        if length > 0:
            bl_count[length] += 1

    # Step 3: Determine the starting code for each bit length
    code = 0
    next_code = [0] * (max_length + 1)
    for bits in range(1, max_length + 1):
        code = (code + bl_count[bits - 1]) << 1
        next_code[bits] = code

    # Step 4: Assign codes to symbols
    huffman_codes = {}
    for symbol, length in enumerate(lengths):
        if length != 0:
            huffman_codes[symbol] = next_code[length]
            next_code[length] += 1

    # Step 5: Validate final code set (canonical Huffman validation)
    total_codes = sum(1 << (max_length - i) for i in range(1, max_length + 1) if bl_count[i])
    used_codes = next_code[max_length]
    if (used_codes - 1) & used_codes != 0:
        raise ValueError("INVALIDFORMAT: Generated codes are not canonical")

    return huffman_codes

bitOffset = 18*8

lengthsTable = readTable(0x11e)
# print(f'Code lengths: {lengthsTable}')

distanceTable = readTable(0x3c)
print(f'Distance lengths: {distanceTable}')

huffCodes = generate_huffman_codes(lengthsTable)
# print(f'Huffman codes: {huffCodes}')

#print the codes
# for symbol, code in huffCodes.items():
#     print(f'Symbol: {symbol}, Code: {code:0{lengthsTable[symbol]}b}')

huffDistances = generate_huffman_codes(distanceTable)
print(f'Huffman distance codes: {huffDistances}')


# 0 0 0 0 0 0 0 0 1 1 1 1 2 2 2 2 3 3 3 3 4 4 4 4 5 5 5

# 30v

# 0x0003
# 0x0004  
# 0x0005
# 0x0006
# 0x0007
# 0x0008  
# 0x0009
# 0x000A
# 0x000B
# 0x000D 
# 0x000F
# 0x0011
# 0x0013
# 0x0017 
# 0x001B
# 0x001F
# 0x0023
# 0x002B
# 0x0033
# 0x003B
# 0x0043
# 0x0053  
# 0x0063
# 0x0073
# 0x0083
# 0x00A3
# 0x00C3
# 0x00E3 
# 0x1002
# 0x1003  

# # 28v

# 0x00
# 0x00
# 0x00
# 0x00  
# 0x00
# 0x00
# 0x00
# 0x00  
# 0x01
# 0x01
# 0x01
# 0x01  
# 0x02
# 0x02
# 0x02
# 0x02  
# 0x03
# 0x03
# 0x03
# 0x03  
# 0x04
# 0x04
# 0x04
# 0x04  
# 0x05
# 0x05
# 0x05
# 0x05 

# 31v 0x7d9208

# 0x01
# 0x02  
# 0x03
# 0x04
# 0x05
# 0x07  
# 0x09
# 0x0D
# 0x11
# 0x19
# 0x21
# 0x31
# 0x41
# 0x61
# 0x81
# 0xC1
# 0x0101 
# 0x0181   
# 0x0201 
# 0x0301 
# 0x0401 
# 0x0601  
# 0x0801 
# 0x0C01 
# 0x1001 
# 0x1801   
# 0x2001 
# 0x3001 
# 0x4001 
# 0x6001   
# 0x8001 

# 31v 0x7d9288

# 0x00
# 0x00
# 0x00  
# 0x00
# 0x00
# 0x01
# 0x01  
# 0x02
# 0x02
# 0x03
# 0x03 
# 0x04
# 0x04
# 0x05
# 0x05  
# 0x06
# 0x06
# 0x07
# 0x07  
# 0x08
# 0x08
# 0x09
# 0x09  
# 0x0A
# 0x0A
# 0x0B
# 0x0B 
# 0x0C
# 0x0C
# 0x0D
# 0x0D


# length_code_table = {
#     256: (0x01   ,0x00),
#     257: (0x02   ,0x00),
#     258: (0x03   ,0x00),
#     259: (0x04   ,0x00),
#     260: (0x05   ,0x00),
#     261: (0x07   ,0x01),
#     262: (0x09   ,0x01),
#     263: (0x0D   ,0x02),
#     264: (0x11   ,0x02),
#     265: (0x19   ,0x03),
#     266: (0x21   ,0x03),
#     267: (0x31   ,0x04),
#     268: (0x41   ,0x04),
#     269: (0x61   ,0x05),
#     270: (0x81   ,0x05),
#     271: (0xC1   ,0x06),
#     272: (0x0101 ,0x06),
#     273: (0x0181 ,0x07),
#     274: (0x0201 ,0x07),
#     275: (0x0301 ,0x08),
#     276: (0x0401 ,0x08),
#     277: (0x0601 ,0x09),
#     278: (0x0801 ,0x09),
#     279: (0x0C01 ,0x0A),
#     280: (0x1001 ,0x0A),
#     281: (0x1801 ,0x0B),
#     282: (0x2001 ,0x0B),
#     283: (0x3001 ,0x0C),
#     284: (0x4001 ,0x0C),
#     285: (0x6001 ,0x0D),
#     286: (0x8001 ,0x0D),
# }

length_code_table = {
    256: (0x0003 ,0x00),
    257: (0x0004 ,0x00),
    258: (0x0005 ,0x00),
    259: (0x0006 ,0x00),
    260: (0x0007 ,0x00),
    261: (0x0008 ,0x00),
    262: (0x0009 ,0x00),
    263: (0x000A ,0x00),
    264: (0x000B ,0x01),
    265: (0x000D ,0x01),
    266: (0x000F ,0x01),
    267: (0x0011 ,0x01),
    268: (0x0013 ,0x02),
    269: (0x0017 ,0x02),
    270: (0x001B ,0x02),
    271: (0x001F ,0x02),
    272: (0x0023 ,0x03),
    273: (0x002B ,0x03),
    274: (0x0033 ,0x03),
    275: (0x003B ,0x03),
    276: (0x0043 ,0x04),
    277: (0x0053 ,0x04),
    278: (0x0063 ,0x04),
    279: (0x0073 ,0x04),
    280: (0x0083 ,0x05),
    281: (0x00A3 ,0x05),
    282: (0x00C3 ,0x05),
    283: (0x00E3 ,0x05),
    284: (0x1002 ,0x00),
    285: (0x1003 ,0x00),
}

class HuffmanNode:
    def __init__(self, symbol=None):
        self.symbol = symbol
        self.left = None
        self.right = None

# Insert a Huffman code into the tree
def insert_huffman_code(tree_root, code, symbol):
    node = tree_root
    for bit in code:
        if bit == '0':  # Move left
            if node.left is None:
                node.left = HuffmanNode()
            node = node.left
        elif bit == '1':  # Move right
            if node.right is None:
                node.right = HuffmanNode()
            node = node.right
    node.symbol = symbol  # Assign the symbol at the leaf node

def build_decoding_tree(huffman_codes, lengths_table):
    root = HuffmanNode()  # The root of the Huffman tree
    for symbol, code in huffman_codes.items():
        bit_length = lengths_table[symbol]
        binary_code = format(code, f'0{bit_length}b')  # Format to a binary string
        insert_huffman_code(root, binary_code, symbol)
    return root

# Build the Huffman decoding tree
tree_root = build_decoding_tree(huffCodes, lengthsTable)

# Build the distance tree
distance_tree_root = build_decoding_tree(huffDistances, distanceTable)

print("Distance Tree:")
def print_distance_tree(node, prefix=""):
    if node.symbol is not None:
        print(f"Symbol: {node.symbol}, Path: {prefix}")
    else:
        if node.left is not None:
            print_distance_tree(node.left, prefix + "0")
        if node.right is not None:
            print_distance_tree(node.right, prefix + "1")

print_distance_tree(distance_tree_root)

# Decode a sequence of bits using the Huffman tree
def decode_with_tree(tree_root, bit_stream):
    decoded_symbols = []
    node = tree_root
    i = 0
    while i < len(bit_stream):
        bit = bit_stream[i]
        if bit == '0':
            node = node.left
        elif bit == '1':
            node = node.right
        i += 1
        
        if node.symbol is not None:  # If we've reached a leaf node

            # print(f'New symbol found: {node.symbol} at index {i}')

            # Check if it's a literal (<255), else is a length symbol
            if node.symbol < 256:
                decoded_symbols.append(node.symbol)

            elif node.symbol == 285:
                break  # End of stream symbol

            else:
                baseLength = length_code_table[node.symbol ][0]
                extraBits = length_code_table[node.symbol][1]
                # print(f'{i}: Symbol found: {node.symbol}: base length = {baseLength}, extra bits = {extraBits}')

                
                bit_str = ''.join(bit_stream[i:i+extraBits])
                i += extraBits 
                              
                
                lengthNode = distance_tree_root
                while True:
                    bit = bit_stream[i]
                    i += 1
                    if bit == '0':
                        lengthNode = lengthNode.left
                    elif bit == '1':
                        lengthNode = lengthNode.right

                    if lengthNode.symbol is not None:
                        break
                
                
                bits = bit_stream[i:i+2]
                print(f'Extra bits: {bits}')
                i +=2
                
                
                offset = 0
                if len(bit_str) > 0:
                    offset =  int(bit_str, 2)
                    print(f'offset: {offset}')

                distance = lengthNode.symbol + 1

                # print(f'{i}: Length found: {baseLength + offset}: distance = {distance}')

                # Perform LZ77-style copy
                if distance == 0 or distance > len(decoded_symbols):
                    print(f"[Warning] Invalid distance: {distance}")
                    break
                else:
                    for j in range(baseLength + offset):
                        if bits == '11':
                            decoded_symbols.append(decoded_symbols[distance - 1 +j])
                        else:
                            decoded_symbols.append(decoded_symbols[-distance])
                # print(distance)

            node = tree_root  # Reset to the root for the next symbol
            
            ascii_output = ''.join(chr(symbol) for symbol in decoded_symbols if symbol < 256)
            print(f'{ascii_output}')
        
    return decoded_symbols

# Now you can decode a bit stream
bit_stream = ''.join(bit_list[bitOffset:])  # Use the bit_list you have already extracted from the file

decoded_output = decode_with_tree(tree_root, bit_stream)
# print(f'Decoded output: {decoded_output}')

# Print as hex
# hex_output = ''.join(format(symbol, '02x') + ' ' for symbol in decoded_output)
# print(f'Hex output: {hex_output}')

# Convert the output in ascii
ascii_output = ''.join(chr(symbol) for symbol in decoded_output[:100] if symbol < 256)
print(f'ASCII output: \n{ascii_output}')

# expected = "[system]\r\n;WindowX = 1024\n;WindowY = 768\nDisableExceptionHandler = 0\r\nNoSplash = 0\r\nLogFile = logs/vxlog.log"

# for i in range(100):
#     for j in range (100):
#         for k in range (5):
#             length_code_table[i + 256] = (j, k)
#             print(j, k)
#             decoded_output = decode_with_tree(tree_root, bit_stream)
#             ascii_output = ''.join(chr(symbol) for symbol in decoded_output[:100] if symbol < 256)

#             # Compare the output with the expected
#             ok = True
#             if(len(ascii_output) >= len(expected)):
#                 for i, l in enumerate(expected):
#                     out = ascii_output[i]
#                     exp = l
#                     if out != exp:
#                         # print(f'Expected {l} at index {i}, got {ascii_output[i]}')
#                         ok = False
#                         break
#             else:
#                 ok = False

#             if ok:
#                 print(f'Found it! {j} {k}')
#                 exit()
#                 # # Write the output to file
#                 # with open('/config.ini', 'w') as f:
#                 #     f.write(ascii_output)
#                 #     f.write('\n')
#                 #     f.write(hex_output)
#                 #     f.write('\n')
#                 #     f.write(str(decoded_output))
#                 # break

# print("Nope")

# Write the output to file
# with open('/config.ini', 'w') as f:
#     f.write(ascii_output)
#     f.write('\n')
#     f.write(hex_output)
#     f.write('\n')
#     f.write(str(decoded_output))

# node = tree_root
# # node = distance_tree_root
# data = '110100010000100000'
# buffer = []
# for bit in data:
#     if bit == '0':
#         node = node.left
#     elif bit == '1':
#         node = node.right
    
#     buffer.append(bit)

#     if node.symbol is not None:
#         print(f'Found symbol: {node.symbol} "{''.join(chr(node.symbol))}" with bits: {"".join(buffer)}')
#         # break
#         node = tree_root
#         buffer = []

# def bruteforce_tree_for_character(tree_root, target_char):
#     target_ascii = ord(target_char)
#     stack = [(tree_root, "")]
#     while stack:
#         node, path = stack.pop()
#         if node.symbol == target_ascii:
#             return pathIMGRLE
#         print_distance_tree(node.right, prefix + "1")


