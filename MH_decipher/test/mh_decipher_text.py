import unittest

import MH_decipher.substitute_encrypt


class TestMHDecipher(unittest.TestCase):

    def test_substitute_encrypt(self):
        text = "BYL_POZDNI_VECER_PRVNI_MAJ_VECERNI_MAJ_BYL_LASKY_CAS"
        key = "DEFGHIJKLMNOPQRSTUVWXYZ_ABC"
        output_expected = "EAOCSRBGQLCYHFHUCSUYQLCPDMCYHFHUQLCPDMCEAOCODVNACFDV"
        output_actual = MH_decipher.substitute_encrypt.substitute_encrypt(text, key)
        self.assertEqual(output_expected, output_actual)


if __name__ == '__main__':
    unittest.main()
