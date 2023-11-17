from typing import Mapping, Set, Union, Callable
from pathlib import Path
from math import inf
import codecs
import os
import csv
import json

from helper import ObfuscationMethods, SaveMethods


class Obfuscator:
    def __init__(self, exclusion_list: Union[Set[str], None] = None):

        self.exclusion_list: Set[str] = exclusion_list if exclusion_list else {}
        self.paths: Mapping[Path, Path | None] = {}

    def load(self, root: Path, depth: int = inf) -> None:
        if not root.is_file() and not root.is_dir():
            raise FileNotFoundError(root)

        if root.is_dir():
            self.__load_all_items(root, max_depth=depth)
        else:
            self.paths[root] = None

    def obfuscate(self, method: ObfuscationMethods) -> None:
        function_encoding: Callable[[str], str]

        match method:
            case ObfuscationMethods.ROT13:
                function_encoding = lambda x: codecs.encode(x, 'rot13')

            case _:
                function_encoding = lambda x: x

        for path in self.paths:
            new_path = f"{path.parent}/{function_encoding(path.stem)}{path.suffix}"
            self.paths[path] = Path(new_path)

            os.rename(path, new_path)

    def deobfuscate(self, method: ObfuscationMethods) -> None:
        function_decoding: Callable[[str], str]

        match method:
            case ObfuscationMethods.ROT13:
                function_decoding = lambda x: codecs.decode(x, 'rot13')

            case _:
                function_decoding = lambda x: x

        for path in self.paths:
            old_path = f"{path.parent}/{function_decoding(path.stem)}{path.suffix}"
            self.paths[path] = Path(old_path)

            os.rename(path, old_path)

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

    def __load_all_items(self, root: Path, max_depth: int = inf, current_depth: int = 0) -> None:
        exclusion_list = self.exclusion_list

        for item in root.iterdir():
            if item.name in exclusion_list:
                continue

            if item.is_file():
                self.paths[item] = None

            if item.is_dir() and current_depth < max_depth:
                self.__load_all_items(item, current_depth + 1, max_depth)
