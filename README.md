# zip_null_patch

A module to enable null characters in `zipfile` path names.

## Motivation

In Python, the built-in `zipfile` module purposefully rejects paths containing null-byte characters.
The reasoning is to prevent unintended behaviour from viruses which abuse null-byte paths in archives.

```python
## CPython 3.6 -- zipfile.py

# Terminate the file name at the first null byte.  Null bytes in file
# names are used as tricks by viruses in archives.
null_byte = filename.find(chr(0))
if null_byte >= 0:
    filename = filename[0:null_byte]
```

However, if trying to *purposefully read* a zip created by a malicious program, Python provides no exit-hatch to forcefully
enable the parsing of paths containing null-bytes. This means that proper analysis of any null-byte-containing archive is impossible.

Enter: `zip_null_patch`. Simply call `zip_null_patch.patch_zipfile()` and the built-in `zipfile` module will now accept null-bytes!

## Usage

```python3
>>> import zipfile

>>> info = zipfile.ZipInfo(filename="abc\x00def")
>>> info.filename
'abc'

>>> import zip_null_patch
>>> zip_null_patch.patch_zipfile()

>>> info = zipfile.ZipInfo(filename="abc\x00def")
>>> info.filename
'abc\x00def'
```
