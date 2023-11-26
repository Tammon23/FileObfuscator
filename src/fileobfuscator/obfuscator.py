from typing import Mapping, Set, Union, Callable, List
from pathlib import Path
from math import inf
import os
import csv
import json

from fileobfuscator.Ciphers import ROT13, DEC, HEX
from fileobfuscator.Exceptions.InvalidFileNameException import InvalidFileNameException
from fileobfuscator.helper import ObfuscationMethods, SaveMethods


# MAX_FILENAME_LENGTH = os.path.getconf('/', 'PC_NAME_MAX')


class Obfuscator:
    def __init__(self,
                 ignored_extensions_set: Union[Set[str], None] = None,
                 extensions_case_sensitive: bool = False,
                 ignored_paths_set: Union[Set[str], None] = None,
                 paths_case_sensitive: bool = False
                 ):

        self.ignored_extensions_set: Set[str] = ignored_extensions_set if ignored_extensions_set else {}
        self.ignored_paths_set: Set[str] = ignored_paths_set if ignored_paths_set else {}

        self.extensions_case_sensitive: bool = extensions_case_sensitive
        self.paths_case_sensitive: bool = paths_case_sensitive

        # if we ignore case, change input to be all lower,
        # and use .lower() in load when checking if its in list
        if not extensions_case_sensitive:
            self.ignored_extensions_set = {extension.lower() for extension in ignored_extensions_set}

        if not paths_case_sensitive:
            self.ignored_paths_set = {path.lower() for path in ignored_paths_set}

        self.paths: Mapping[Path, Path | None] = {}

    def load(self, root: Path, depth: int = inf) -> None:
        if not root.is_file() and not root.is_dir():
            raise FileNotFoundError(root)

        if root.is_dir():
            found_paths = self.__load_all_items(root, max_depth=depth)
            self.paths = dict.fromkeys(found_paths)
        else:
            self.paths[root] = None

    def obfuscate(self, method: ObfuscationMethods) -> None:
        function_encoding: Callable[[str], str]

        match method:
            case ObfuscationMethods.ROT13:
                function_encoding = ROT13.encode

            case ObfuscationMethods.HEX:
                function_encoding = HEX.encode

            case ObfuscationMethods.DEC:
                function_encoding = DEC.encode

        try:
            for path in self.paths:
                new_path = f"{path.parent}/{function_encoding(path.stem)}{path.suffix}"  # NOQA
                self.paths[path] = Path(new_path)

            self.update()
        except ValueError:
            print("Unable to obfuscate, do all targeted file names match the chosen obfuscation method?")

    def deobfuscate(self, method: ObfuscationMethods) -> None:
        function_decoding: Callable[[str], str]

        match method:
            case ObfuscationMethods.ROT13:
                function_decoding = ROT13.decode

            case ObfuscationMethods.HEX:
                function_decoding = HEX.decode

            case ObfuscationMethods.DEC:
                function_decoding = DEC.decode

        try:
            for path in self.paths:
                old_path = f"{path.parent}/{function_decoding(path.stem)}{path.suffix}"  # NOQA
                self.paths[path] = Path(old_path)

            self.update()
        except ValueError:
            print("Unable to deobfuscate, do all targeted file names match the chosen deobfuscation method?")

    def update(self) -> bool:
        # do some type checking to make sure the new name is valid
        # for new_path in self.paths.values():
        #     if len(new_path) > MAX_FILENAME_LENGTH:
        #         raise InvalidFileNameException(
        #             f"During encoding/decoding, filename length exceeded max of {MAX_FILENAME_LENGTH}")

        for old_path, new_path in self.paths.items():
            os.rename(old_path, new_path)

        return True

    def save_changes(self, root: Path, method: SaveMethods) -> None:
        with open(root, 'w', newline='') as file:
            match method:
                case SaveMethods.CSV:
                    writer = csv.writer(file)
                    writer.writerow(["Old Name", "New Name"])

                    for old_name, new_name in self.paths.items():
                        writer.writerow([old_name.name, new_name.name])

                case SaveMethods.JSON:
                    json.dump({key.name: value.name for key, value in self.paths.items()}, file)

    def get_number_of_renamed_files(self) -> int:
        return len(self.paths)

    def __load_all_items(self, root: Path, max_depth: int = inf, current_depth: int = 0) -> List[Path]:
        ignored_extensions_set = self.ignored_extensions_set
        ignored_paths_set = self.ignored_paths_set

        extensions_case_sensitive = self.extensions_case_sensitive
        paths_case_sensitive = self.paths_case_sensitive
        temp: List[Path] = []

        for item in root.iterdir():
            extension = item.suffix.lstrip(".")
            if (extensions_case_sensitive and extension in ignored_extensions_set) or \
                    (not extensions_case_sensitive and extension.lower() in ignored_extensions_set):
                continue

            if (paths_case_sensitive and item.stem in ignored_paths_set) or \
                    (not paths_case_sensitive and item.stem.lower() in ignored_paths_set):
                continue

            if item.is_file():
                temp.append(item)

            if item.is_dir() and current_depth < max_depth:
                temp += self.__load_all_items(item, current_depth + 1, max_depth)

        return temp
