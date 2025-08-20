# Status
- Can extract and recreate the .pak files
- Untested with the game itself
- The generate file may be different as the order of the files is not yet taken in account (if there is any)

# File structure

The file is structured with an header, followed by a table of contents and the actual files. The table of contents contains information about each file, including its path, size, and offset within the archive.

## Header

* The first **16 bytes** represent the file magic:

  ```
  "HMMSYS PackFile\n"
  ```

* This is followed by a constant 16-byte header:

  ```
  1A 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  ```

* Then:

  * **4 bytes**: Number of files (little-endian).
  * **4 bytes**: Header length.

## File Path Decoding

File paths are decoded using a shared buffer that is reused across multiple entries. This allows efficient storage by only writing the parts of the path that change between files.

Each file entry specifies a slice of the buffer to overwrite:

1. Two bytes are read:  
   - **Low index**: Start position in the buffer  
   - **High index**: End position in the buffer

2. The next `(high - low)` bytes are read and inserted into the buffer at the given range.

3. The file path is then reconstructed by reading the buffer from the beginning up to the **high index**.

#### Example

- **File 1**
  - Indexes: `0 → 19`  
  - Data: `testfolder/test.txt`  
  - Resulting path: `testfolder/test.txt`

- **File 2**
  - Indexes: `19 → 11`  
  - Data: `ciao.txt`  
  - Buffer becomes: `testfolder/ciao.txt`  
  - Resulting path: `testfolder/ciao.txt`

> **Note:** Only the filename changes, while the folder prefix (`testfolder/`) is preserved from the previous buffer state.

---

### File Entry Format

Each file entry in the archive contains:

| Bytes   | Description                           |
|---------|---------------------------------------|
| 1 byte  | **High index** (end of insert range)  |
| 1 byte  | **Low index** (start of insert range) |
| N bytes | **File path segment** (ASCII)         |
| 4 bytes | **File offset** within the archive    |
| 4 bytes | **File size** in bytes                |


* This is then followed by the file contents, as referenced in the file table.


## Extraction

To extract all `.pak` files from the game:

```bash
tools/paktool/extractPakFromGame.sh path_to_game_root
```

This script will automatically extract all `.pak` files found in:

* `path_to_game_root/Packs`
* `path_to_game_root/local`


To extract a single `.pak` file manually:

```bash
python3 extractPak.py path_to_pak output_folder
```

**Example:**

```bash
python3 extractPak.py "game_path/Packs/UI.pak" "assets/Packs/UI"
```

---

## Packing

Repacking `.pak` files can be attempted using the same script, but be aware:

> Note: Although the packed files can be correctly unpacked, the game crashes when loading them, hinting at a potential issue with the packing process. It's 100% related to the unknown bytes after the TOC. Anyway, this is low priority as the game loads the unpacked files as well if they are put in the correct folder

To pack a folder into a `.pak` file:

```bash
python3 extractPak.py input_folder output_file.pak
```
