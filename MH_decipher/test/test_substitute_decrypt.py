import unittest

from MH_decipher.substitute_decrypt import substitute_decrypt


class TestMHDecipher(unittest.TestCase):

    def test_substitute_decrypt(self):
        text = "EAOCSRBGQLCYHFHUCSUYQLCPDMCYHFHUQLCPDMCEAOCODVNACFDV"
        key = "DEFGHIJKLMNOPQRSTUVWXYZ_ABC"
        output_expected = "BYL_POZDNI_VECER_PRVNI_MAJ_VECERNI_MAJ_BYL_LASKY_CAS"
        output_actual = substitute_decrypt(text, key)
        self.assertEqual(output_expected, output_actual)


if __name__ == '__main__':
    unittest.main()