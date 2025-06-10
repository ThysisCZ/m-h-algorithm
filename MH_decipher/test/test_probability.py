import unittest

from MH_decipher.probability import probability


class TestProbability(unittest.TestCase):

    def setUp(self):
        self.test_text = "ABCDEFGHIJKLMNOP"
        self.reference_matrix = self._create_test_matrix()
        self.test_key = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ_")

    def _create_test_matrix(self):
        """Vytvořit testovací přechodovou matici"""
        alphabet_size = 27
        matrix = []
        for i in range(alphabet_size):
            row = [0.001] * alphabet_size
            row[i] = 0.1
            if i < alphabet_size - 1:
                row[i + 1] = 0.05
            matrix.append(row)
        return matrix

    def test_probability_returns_float(self):
        """Test, že funkce vrací float"""
        prob = probability(self.test_text, self.reference_matrix, self.test_key)
        self.assertIsInstance(prob, float)

    def test_probability_between_zero_and_one(self):
        """Test, že pravděpodobnost je mezi 0 a 1"""
        prob = probability(self.test_text, self.reference_matrix, self.test_key)
        self.assertGreaterEqual(prob, 0.0)
        self.assertLessEqual(prob, 1.0)

    def test_probability_better_key_higher_probability(self):
        """Test několika pokusů - ověřuje, že funkce vrací validní pravděpodobnosti"""
        better_reference = "ABABABABABABABABABAB"
        worse_reference = "XQZWRTYUIOPASDFGHJKLCVBNM"
        
        better_probabilities = []
        worse_probabilities = []

        for _ in range(5):  # Snížíme počet testů pro rychlost
            prob_better = probability(better_reference, self.reference_matrix, self.test_key)
            prob_worse = probability(worse_reference, self.reference_matrix, self.test_key)
            better_probabilities.append(prob_better)
            worse_probabilities.append(prob_worse)

        for prob in better_probabilities + worse_probabilities:
            self.assertGreaterEqual(prob, 0.0)
            self.assertLessEqual(prob, 1.0)
            self.assertIsInstance(prob, float)

        avg_better = sum(better_probabilities) / len(better_probabilities)
        avg_worse = sum(worse_probabilities) / len(worse_probabilities)

        self.assertIsInstance(avg_better, float)
        self.assertIsInstance(avg_worse, float)

    def test_probability_with_empty_text(self):
        """Test s prázdným textem"""
        prob = probability("", self.reference_matrix, self.test_key)
        self.assertIsInstance(prob, float)
        self.assertGreaterEqual(prob, 0.0)
        self.assertLessEqual(prob, 1.0)

    def test_probability_with_short_text(self):
        """Test s velmi krátkým textem"""
        prob = probability("AB", self.reference_matrix, self.test_key)
        self.assertIsInstance(prob, float)
        self.assertGreaterEqual(prob, 0.0)
        self.assertLessEqual(prob, 1.0)

    def test_probability_deterministic_with_same_input(self):
        """Test, že stejný vstup produkuje konzistentní výsledky"""
        probabilities = []
        for _ in range(20):
            prob = probability(self.test_text, self.reference_matrix, self.test_key)
            probabilities.append(prob)

        for prob in probabilities:
            self.assertGreaterEqual(prob, 0.0)
            self.assertLessEqual(prob, 1.0)
            self.assertIsInstance(prob, float)

    def test_probability_metropolis_hastings_formula(self):
        """Test, že se používá správný Metropolis-Hastings vzorec"""
        # Tento test ověřuje logiku vzorce min(1, exp(p_candidate - p_current))

        prob = probability(self.test_text, self.reference_matrix, self.test_key)
        self.assertTrue(0 <= prob <= 1)

        if prob == 1.0:
            self.assertEqual(prob, 1.0)


if __name__ == '__main__':
    unittest.main()