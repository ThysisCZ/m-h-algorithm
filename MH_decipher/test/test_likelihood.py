import unittest

from MH_decipher.likelihood import calculate_likelihood, compare_texts_likelihood


class TestLikelihood(unittest.TestCase):

    def setUp(self):
        self.alphabet = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ_")
        self.reference_text = "TOTO_JE_REFERECNI_TEXT_PRO_TESTOVANI_FUNKCE_LIKELIHOOD"
        
    def test_calculate_likelihood_same_text(self):
        """Test, že stejný text má nejvyšší věrohodnost"""
        likelihood = calculate_likelihood(self.reference_text, self.reference_text, self.alphabet)
        self.assertIsInstance(likelihood, float)
        self.assertGreater(likelihood, -1000)

    def test_calculate_likelihood_different_texts(self):
        """Test porovnání různých textů"""
        similar_text = "TOTO_JE_PODOBNY_TEXT_PRO_TESTOVANI_FUNKCE"

        random_text = "XQWERTY_RANDOM_ZNAKY_BEZ_SMYSLU_ABCDEF"
        
        likelihood_similar = calculate_likelihood(similar_text, self.reference_text, self.alphabet)
        likelihood_random = calculate_likelihood(random_text, self.reference_text, self.alphabet)

        self.assertGreater(likelihood_similar, likelihood_random)

    def test_calculate_likelihood_empty_text(self):
        """Test prázdného textu"""
        empty_text = ""
        likelihood = calculate_likelihood(empty_text, self.reference_text, self.alphabet)
        self.assertIsInstance(likelihood, float)
        self.assertLess(likelihood, -1000)

    def test_calculate_likelihood_short_text(self):
        """Test velmi krátkého textu"""
        short_text = "AB"
        likelihood = calculate_likelihood(short_text, self.reference_text, self.alphabet)
        self.assertIsInstance(likelihood, float)

    def test_compare_texts_likelihood(self):
        """Test porovnání dvou textů"""
        text1 = "TOTO_JE_DOBRY_TEXT_S_CESKOU_STRUKTUROU"
        text2 = "RANDOM_NONSENSE_WITHOUT_STRUCTURE_XYZ"
        
        likelihood1, likelihood2, better_index = compare_texts_likelihood(
            text1, text2, self.reference_text, self.alphabet
        )
        
        self.assertIsInstance(likelihood1, float)
        self.assertIsInstance(likelihood2, float)
        self.assertIn(better_index, [0, 1])

        self.assertEqual(better_index, 0)
        self.assertGreater(likelihood1, likelihood2)

    def test_calculate_likelihood_with_default_alphabet(self):
        """Test s výchozí abecedou"""
        likelihood = calculate_likelihood(self.reference_text, self.reference_text)
        self.assertIsInstance(likelihood, float)

    def test_calculate_likelihood_encrypted_vs_decrypted(self):
        """Test porovnání zašifrovaného a dešifrovaného textu"""
        # Simulace správně dešifrovaného textu
        decrypted_text = "BYLA_JEDNOU_JEDNA_PRINCEZNA_KTERA_ZILA_V_ZAMKU"
        
        # Simulace špatně dešifrovaného textu (náhodné znaky)
        wrong_decryption = "XQWE_RTYU_ASDF_GHJK_ZXCV_BNMQ_W_ERTY"
        
        czech_reference = "BYLO_NEBYLO_ZILO_SE_V_JEDNE_ZEMI_KRAL_A_KRALOVNA_A_MELI_DCERU"
        
        likelihood_correct = calculate_likelihood(decrypted_text, czech_reference, self.alphabet)
        likelihood_wrong = calculate_likelihood(wrong_decryption, czech_reference, self.alphabet)

        self.assertGreater(likelihood_correct, likelihood_wrong)


if __name__ == '__main__':
    unittest.main()