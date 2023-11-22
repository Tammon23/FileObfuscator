from textwrap import wrap
from fileobfuscator.Ciphers.Cipher import Cipher


class DEC(Cipher):
    @staticmethod
    def encode(string: str) -> str:
        return "".join([str(ord(letter)).zfill(3) for letter in string])

    @staticmethod
    def decode(string: str) -> str:
        return "".join([chr(int(ascii_char)) for ascii_char in wrap(string, 3)])
