from fileobfuscator.Exceptions.InvalidFileNameException import InvalidFileNameException
from fileobfuscator.helper import ObfuscationMethods, SaveMethods
from fileobfuscator.obfuscator import Obfuscator
from typing import Tuple, List
from pathlib import Path
from math import inf
import argparse

obfuscation_methods = ObfuscationMethods.get_methods()


def ValidateSaveFormat(root: str) -> Tuple[Path, SaveMethods]:
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
                    type=ValidateSaveFormat,
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
                    type=set,
                    help='Ignores all files with the provided list of extensions')

parser.add_argument('-iecs', '--ignore_extensions_case_sensitive',
                    action='store_true',
                    help='Specifies that the the list of ignored extensions should be considered as case sensitive')

parser.add_argument('-ip', '--ignore_paths',
                    nargs='+',
                    type=set,
                    help='Ignores all files/folders if it makes the relative path')

parser.add_argument('-ipcs', '--ignore_paths_case_sensitive',
                    action='store_true',
                    help='Specifies that the the list of ignored files/folders should be considered as case sensitive')


def main():
    args = parser.parse_args()

    obfuscator = Obfuscator(args.ignore_extensions, args.ignore_extensions_case_sensitive,
                            args.ignore_paths, args.ignore_paths_case_sensitive)

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

        print(f"Finished running through {obfuscator.get_number_of_renamed_files()} items...")


if __name__ == "__main__":
    main()
