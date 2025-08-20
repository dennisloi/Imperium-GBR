# file_tools
This folder contains scripts to extract, recreate and manipulate the various types of files used by the game.

So far, 5 file types have been discovered:
- **.pak** -> "Packs" multiple files in one, no compression is applied (unless is compressed after using LSIZ)
- **.BFPH**
- **LSIZ** -> Doesn't have a precise file extension, the main config.ini uses this, but also Packs/RandomMap.pak. Uses a compression like huffman encoding and DEFLATE to compress the files, not fully understood.
- **.pass** -> File used to store the buildings and units collisions.
- **.mmp** -> Stores images, or at least their header