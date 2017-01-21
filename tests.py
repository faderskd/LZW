import os
import unittest

import compressor


class LZWTest(unittest.TestCase):

    def test_compress(self):
        compress_gen = compressor.compress('tark')
        next(compress_gen)
        compressed_array = compress_gen.send('tatarak')
        compress_gen.close()
        self.assertEqual(compressed_array, [0, 1, 4, 2, 1, 3])

        compress_gen = compressor.compress('abcd_')
        next(compress_gen)
        comressed_array = compress_gen.send('abccd_abccd_acd_acd_acd_')
        compress_gen.close()
        self.assertEqual(comressed_array, [0, 1, 2, 2, 3, 4, 5, 7, 9, 0, 8, 10, 15, 14, 9])

    def test_decompress(self):
        decompress_gen = compressor.decompress('tark')
        next(decompress_gen)
        decompressed_string = decompress_gen.send([0, 1, 4, 2, 1, 3])
        decompress_gen.close()
        self.assertEqual(decompressed_string, 'tatarak')

        decompress_gen = compressor.decompress('abcd_')
        next(decompress_gen)
        decompressed_string = decompress_gen.send([0, 1, 2, 2, 3, 4, 5, 7, 9, 0, 8, 10, 15, 14, 9])
        decompress_gen.close()
        self.assertEqual(decompressed_string, 'abccd_abccd_acd_acd_acd_')

    def test_size_compressed_file(self):
        compressor.compress_file('input', 'compressed')

        input_file_info = os.stat('input')
        compressed_file_info = os.stat('compressed')
        input_file_size = input_file_info.st_size
        compressed_file_size = compressed_file_info.st_size

        self.assertTrue(input_file_size > compressed_file_size)

    def test_size_decompressed_file(self):
        compressor.compress_file('input', 'compressed')
        compressor.decompress_file('compressed', 'decompressed')

        compressed_file_info = os.stat('compressed')
        decompressed_file_info = os.stat('decompressed')
        compressed_file_size = compressed_file_info.st_size
        decompressed_file_size = decompressed_file_info.st_size

        self.assertTrue(compressed_file_size < decompressed_file_size)

if __name__ == '__main__':
    unittest.main()