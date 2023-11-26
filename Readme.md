# File Obfuscator
A client-line interface that automatically obfuscates and deobfuscates filenames located anywhere on your computer

# How To Install
🚧 Work In Progress

# How To Use
 To display this help message simply use the -h/--help argument as shown: python main.py -h
```text
usage: FileObfuscator [-h] [-d [DEEP]] [-s SAVE] [-m {rot13,hex,dec}] [-de] [-ie IGNORE_EXTENSIONS [IGNORE_EXTENSIONS ...]] [-iecs] [-ip IGNORE_PATHS [IGNORE_PATHS ...]] [-ipcs] path

Obfuscates the name of a file or files in a specific folder

positional arguments:
  path                  The filename or folder to perform obfuscation on

options:
  -h, --help            show this help message and exit
  -d [DEEP], --deep [DEEP]
                        Look for files within folders, optionally specify max depth (default is infinite)
  -s SAVE, --save SAVE  Save old to new name mappings at specified location. Valid types: CSV, JSON
  -m {rot13,hex,dec}, --method {rot13,hex,dec}
                        Define the obfuscation method
  -de, --deobfuscate    Undoes the obfuscation
  -ie IGNORE_EXTENSIONS [IGNORE_EXTENSIONS ...], --ignore_extensions IGNORE_EXTENSIONS [IGNORE_EXTENSIONS ...]
                        Ignores all files with the provided list of extensions
  -iecs, --ignore_extensions_case_sensitive
                        Specifies that the the list of ignored extensions should be considered as case sensitive
  -ip IGNORE_PATHS [IGNORE_PATHS ...], --ignore_paths IGNORE_PATHS [IGNORE_PATHS ...]
                        Ignores all files/folders if it makes the relative path
  -ipcs, --ignore_paths_case_sensitive
                        Specifies that the the list of ignored files/folders should be considered as case sensitive
```

The following is an example of how to decimal encode all file names inside the folder `testFolder` recursively, with no depth limit.
Followed by how to decode the same files under the same method

```shell
# encode
python3.10 main.py testFolder -d -m dec
# decode
python3.10 main.py testFolder -d -m dec -de
```

# Future Plans
- Add the ability to obfuscate/deobfuscate folder names as well
- Add the option to do multilayered obfuscation combining a series of methods
- Implement more obfuscation techniques and methods for a user to define their own
