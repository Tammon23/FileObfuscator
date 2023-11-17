from enum import Enum
from typing import List


class ObfuscationMethods(Enum):
    ROT13 = 1

    @staticmethod
    def get_methods() -> List[str]:
        return list(map(lambda x: x.name.lower(), ObfuscationMethods))


class SaveMethods(Enum):
    JSON = 1
    CSV = 2

    @staticmethod
    def get_methods() -> List[str]:
        return list(map(lambda x: x.name.lower(), SaveMethods))
