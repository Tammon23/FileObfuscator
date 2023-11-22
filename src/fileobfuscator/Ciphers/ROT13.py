from fileobfuscator.Ciphers.Cipher import Cipher
import codecs


class ROT13(Cipher):
    @staticmethod
    def encode(string: str) -> str:
        return codecs.encode(string, 'rot13')

    @staticmethod
    def decode(string: str) -> str:
        return codecs.decode(string, 'rot13')
