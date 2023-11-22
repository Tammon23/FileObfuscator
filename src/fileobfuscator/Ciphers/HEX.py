from fileobfuscator.Ciphers.Cipher import Cipher
import codecs


class HEX(Cipher):
    @staticmethod
    def encode(string: str) -> str:
        return codecs.encode(string.encode(), 'hex').decode("utf-8")

    @staticmethod
    def decode(string: str) -> str:
        return codecs.decode(string.encode(), 'hex').decode()
