from Exceptions.InvalidFileNameException import InvalidFileNameException
from helper import ObfuscationMethods, SaveMethods
from obfuscator import Obfuscator
from typing import Tuple
from pathlib import Path
from math import inf
import argparse

obfuscation_methods = ObfuscationMethods.get_methods()


def ValidSaveFormat(root: str) -> Tuple[Path, SaveMethods]:
    root = Path(root)
    match root.suffix.lower():
        case ".csv":
            method = SaveMethods.CSV

        case ".json":
            method = SaveMethods.JSON

        case _:
            raise argparse.ArgumentTypeError("Accepted save file types are: {csv, json}")

    return root, method


parser = argparse.ArgumentParser(prog="FileObfuscator",
                                 description='Obfuscates the name of a file or files in a specific folder')

parser.add_argument('path',
                    type=Path,
                    help="The filename or folder to perform obfuscation on")

parser.add_argument('-d', '--deep',
                    nargs='?',
                    const=inf,
                    default=inf,
                    type=int,
                    help='Look for files within folders, optionally specify max depth (default is infinite)')

parser.add_argument('-s', '--save',
                    nargs=1,
                    type=ValidSaveFormat,
                    help="Save old to new name mappings at specified location. Valid types: CSV, JSON")

parser.add_argument('-m', '--method',
                    choices=obfuscation_methods,
                    default=ObfuscationMethods.ROT13,
                    help='Define the obfuscation method')

parser.add_argument('-de', '--deobfuscate',
                    action='store_true',
                    help='Undoes the obfuscation')

parser.add_argument('-ie', '--ignore_extensions',
                    nargs='+',
                    default=list(),
                    help='Ignores all files with the provided list of extensions')

parser.add_argument('-iecs', '--ignore_extensions_case_sensitive',
                    action='store_true',
                    help='Specifies that the the list of ignored extensions should be considered as case sensitive')

parser.add_argument('-ip', '--ignore_path',
                    nargs='+',
                    default=list(),
                    help='Ignores all files/folders if it makes the relative path')

parser.add_argument('-ipcs', '--ignore_path_case_sensitive',
                    action='store_true',
                    help='Specifies that the the list of ignored files/folders should be considered as case sensitive')

if __name__ == "__main__":
    args = parser.parse_args()

    obfuscator = Obfuscator()
    obfuscator.load(args.path, args.deep)

    try:
        method = ObfuscationMethods[args.method.upper()]
        if args.deobfuscate:
            obfuscator.deobfuscate(method)
        else:
            obfuscator.obfuscate(method)

    except InvalidFileNameException as error:
        print(error)

    else:
        if args.save is not None:
            save_location, save_method = args.save[0]
            obfuscator.save_changes(save_location, save_method)

        print(f"Finished renaming {obfuscator.get_number_of_renamed_files()} folders...")
