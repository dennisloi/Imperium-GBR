# Status
- Can extract and recreate the .pass files
- Untested with the game itself
- Some unknowns in the header

## TODO
- Create a class with the used method so it can be imported, create a python with argparse

# PASS
The .PASS file is used to store collision information for entities in the game. It consists of an header, followed by a bit array.

## Header

The header is made up of two parts:

- file magic -> 'DIRG', in hex 0x44, 0x49, 0x52, 0x47. [4 bytes]
- unknown header part -> not sure what's stored here, so far is always the same
```
    0x10, 0x00, 0x00, 0x00, //maybe image width?
    0x01, 0x00, 0x00, 0x00,
    0x00, 0x08, 0x00, 0x00,
    0x00, 0x08, 0x00, 0x00
```

## Bit array

Each bit in the bit array represents a single location in the game grid. The image is stored in rows of 16 (this needs to be verified to check if it's a constant or stored in the header). The image is also stored in reverse-row order, meaning that the last rows are stored first. 