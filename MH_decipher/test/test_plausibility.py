import unittest
import math

from MH_decipher.plausibility import plausibility


class TestPlausibility(unittest.TestCase):

    def setUp(self):
        self.alphabet = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ_")
        # Vytvoříme jednoduchou referenční matici pro testování
        self.simple_reference_matrix = self._create_simple_matrix()

    def _create_simple_matrix(self):
        """Vytvoří jednoduchou referenční matici pro testování"""
        size = len(self.alphabet)
        matrix = []
        for i in range(size):
            row = [0.001] * size
            row[i] = 0.1
            if i < size - 1:
                row[i + 1] = 0.05
            matrix.append(row)
        return matrix

    def test_plausibility_returns_float(self):
        """Test, že funkce vrací float"""
        text = "ABCDEF"
        result = plausibility(text, self.simple_reference_matrix, self.alphabet)
        self.assertIsInstance(result, float)

    def test_plausibility_negative_value(self):
        """Test, že věrohodnost je záporná (log-likelihood)"""
        text = "ABCDEF"
        result = plausibility(text, self.simple_reference_matrix, self.alphabet)
        self.assertLess(result, 0)

    def test_plausibility_better_text_higher_likelihood(self):
        """Test, že lepší text má vyšší věrohodnost"""
        good_text = "ABCDEFGHIJKLMNOPQRSTUVWXYZ_A"
        bad_text = "AZXQWERTYLKJHGFDSAMN"
        
        good_likelihood = plausibility(good_text, self.simple_reference_matrix, self.alphabet)
        bad_likelihood = plausibility(bad_text, self.simple_reference_matrix, self.alphabet)

        self.assertGreater(good_likelihood, bad_likelihood)

    def test_plausibility_empty_text(self):
        """Test s prázdným textem"""
        text = ""
        result = plausibility(text, self.simple_reference_matrix, self.alphabet)
        self.assertIsInstance(result, float)
        self.assertEqual(result, 0.0)

    def test_plausibility_single_character(self):
        """Test s jedním znakem"""
        text = "A"
        result = plausibility(text, self.simple_reference_matrix, self.alphabet)
        self.assertIsInstance(result, float)
        self.assertEqual(result, 0.0)

    def test_plausibility_two_characters(self):
        """Test s dvěma znaky (jeden bigram)"""
        text = "AB"
        result = plausibility(text, self.simple_reference_matrix, self.alphabet)
        self.assertIsInstance(result, float)
        self.assertLess(result, 0)

    def test_plausibility_same_text_same_result(self):
        """Test konzistence - stejný text by měl dát stejný výsledek"""
        text = "ABCDEF"
        result1 = plausibility(text, self.simple_reference_matrix, self.alphabet)
        result2 = plausibility(text, self.simple_reference_matrix, self.alphabet)
        self.assertEqual(result1, result2)

    def test_plausibility_longer_text_different_likelihood(self):
        """Test s delším textem"""
        short_text = "ABC"
        long_text = "ABCDEFGHIJKLMN"
        
        short_likelihood = plausibility(short_text, self.simple_reference_matrix, self.alphabet)
        long_likelihood = plausibility(long_text, self.simple_reference_matrix, self.alphabet)

        self.assertNotEqual(short_likelihood, long_likelihood)

    def test_plausibility_log_calculation(self):
        """Test, že se používá logaritmus správně"""
        text = "AB"
        result = plausibility(text, self.simple_reference_matrix, self.alphabet)

        a_index = self.alphabet.index('A')
        b_index = self.alphabet.index('B')
        expected_component = math.log(self.simple_reference_matrix[a_index][b_index])

        self.assertLess(result, 0)
        self.assertIsInstance(result, float)

    def test_plausibility_with_underscore(self):
        """Test s podtržítkem (mezerou)"""
        text = "AB_CD"
        result = plausibility(text, self.simple_reference_matrix, self.alphabet)
        self.assertIsInstance(result, float)
        self.assertLess(result, 0)

    def test_plausibility_repeated_bigrams(self):
        """Test s opakujícími se bigramy"""
        text = "ABABAB"  # Opakující se bigram AB
        result = plausibility(text, self.simple_reference_matrix, self.alphabet)
        self.assertIsInstance(result, float)
        self.assertLess(result, 0)

    def test_plausibility_different_matrix_different_result(self):
        """Test, že různé matice dávají různé výsledky"""
        text = "ABCD"

        different_matrix = []
        size = len(self.alphabet)
        for i in range(size):
            row = [0.01] * size
            different_matrix.append(row)
        
        result1 = plausibility(text, self.simple_reference_matrix, self.alphabet)
        result2 = plausibility(text, different_matrix, self.alphabet)

        self.assertNotEqual(result1, result2)


if __name__ == '__main__':
    unittest.main()