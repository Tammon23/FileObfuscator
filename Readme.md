# File Obfuscator
A client-line interface that automatically obfuscates and deobfuscates filenames located anywhere on your computer

# How To Install
🚧 Work In Progress

# How To Use
 To display this help message simply use the -h/--help argument as shown: python main.py -h
```text
positional arguments:
  path                  The filename or folder to perform obfuscation on

options:
  -h, --help            show this help message and exit
  -d [DEEP], --deep [DEEP]
                        Look for files within folders, optionally specifiy max depth (default is infinite). Only valid when -f used
  -s SAVE, --save SAVE  Save old to new name mappings at specified location. Valid types: CSV, JSON
  -m {rot13}, --method {rot13}
                        Define the obfuscation method
  -de, --deobfuscate    Undoes the obfuscation
```

The following is an example of how to decimal encode all file name inside the folder `testFolder` recursively, with no depth limit.
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
- Add obfuscation filters
  - Target specific file extension or file names that match a certain pattern
  - Blacklist certain files from being obfuscated
- Implement more obfuscation techniques and methods for a user to define their own
