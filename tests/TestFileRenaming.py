import unittest
from pathlib import Path
from typing import List
from unittest.mock import patch

from fileobfuscator.helper import ObfuscationMethods
from fileobfuscator.obfuscator import Obfuscator


# a helper function used to correctly merge 2 arrays to formulate
# the expected array used in unit testing
def create_expected(original: List[Path], modified: List[Path]):
    return [(res,) for res in zip(original, modified)]


class TestFileRenaming(unittest.TestCase):
    def setUp(self) -> None:
        self.obfuscator = Obfuscator()
        self.sample_directory: List[Path] = [Path('folder/file1.png'), Path('folder/file2.PNG'),
                                             Path('folder/file3.jpeg')]

    def test_encrypting_rot13(self):
        transformation = [Path('folder/svyr1.png'), Path('folder/svyr2.PNG'), Path('folder/svyr3.jpeg')]
        expected = create_expected(self.sample_directory, transformation)

        with (
            patch('os.rename') as rename,
            patch.object(Obfuscator, '_Obfuscator__load_all_items', return_value=self.sample_directory),
            patch("fileobfuscator.obfuscator.Path.is_dir", return_value=True)
        ):
            self.obfuscator.load(Path('folder'))
            self.obfuscator.obfuscate(ObfuscationMethods.ROT13)
            self.assertEqual(rename.call_args_list, expected)

    def test_decrypting_rot13(self):
        transformation = [Path('folder/svyr1.png'), Path('folder/svyr2.PNG'), Path('folder/svyr3.jpeg')]
        expected = create_expected(transformation, self.sample_directory)

        with (
            patch('os.rename') as rename,
            patch.object(Obfuscator, '_Obfuscator__load_all_items', return_value=transformation),
            patch("fileobfuscator.obfuscator.Path.is_dir", return_value=True)
        ):
            self.obfuscator.load(Path('folder'))
            self.obfuscator.deobfuscate(ObfuscationMethods.ROT13)
            self.assertEqual(rename.call_args_list, expected)

    def test_encrypting_hex(self):
        transformation = [Path('folder/66696c6531.png'), Path('folder/66696c6532.PNG'), Path('folder/66696c6533.jpeg')]
        expected = create_expected(self.sample_directory, transformation)

        with (
            patch('os.rename') as rename,
            patch.object(Obfuscator, '_Obfuscator__load_all_items', return_value=self.sample_directory),
            patch("fileobfuscator.obfuscator.Path.is_dir", return_value=True)
        ):
            self.obfuscator.load(Path('folder'))
            self.obfuscator.obfuscate(ObfuscationMethods.HEX)
            self.assertEqual(rename.call_args_list, expected)

    def test_decrypting_hex(self):
        transformation = [Path('folder/66696c6531.png'), Path('folder/66696c6532.PNG'), Path('folder/66696c6533.jpeg')]
        expected = create_expected(transformation, self.sample_directory)

        with (
            patch('os.rename') as rename,
            patch.object(Obfuscator, '_Obfuscator__load_all_items', return_value=transformation),
            patch("fileobfuscator.obfuscator.Path.is_dir", return_value=True)
        ):
            self.obfuscator.load(Path('folder'))
            self.obfuscator.deobfuscate(ObfuscationMethods.HEX)
            self.assertEqual(rename.call_args_list, expected)

    def test_encrypting_dec(self):
        transformation = [Path('folder/102105108101049.png'), Path('folder/102105108101050.PNG'),
                          Path('folder/102105108101051.jpeg')]
        expected = create_expected(self.sample_directory, transformation)

        with (
            patch('os.rename') as rename,
            patch.object(Obfuscator, '_Obfuscator__load_all_items', return_value=self.sample_directory),
            patch("fileobfuscator.obfuscator.Path.is_dir", return_value=True)
        ):
            self.obfuscator.load(Path('folder'))
            self.obfuscator.obfuscate(ObfuscationMethods.DEC)
            self.assertEqual(rename.call_args_list, expected)

    def test_decrypting_dec(self):
        transformation = [Path('folder/102105108101049.png'), Path('folder/102105108101050.PNG'),
                          Path('folder/102105108101051.jpeg')]
        expected = create_expected(transformation, self.sample_directory)

        with (
            patch('os.rename') as rename,
            patch.object(Obfuscator, '_Obfuscator__load_all_items', return_value=transformation),
            patch("fileobfuscator.obfuscator.Path.is_dir", return_value=True)
        ):
            self.obfuscator.load(Path('folder'))
            self.obfuscator.deobfuscate(ObfuscationMethods.DEC)
            self.assertEqual(rename.call_args_list, expected)


if __name__ == '__main__':
    unittest.main()
