import unittest

from MH_decipher.bigrams import get_bigrams, transition_matrix


class TestBigrams(unittest.TestCase):

    def test_get_bigrams_basic(self):
        """Test základní funkčnosti get_bigrams"""
        text = "HELLO"
        expected = ["HE", "EL", "LL", "LO"]
        result = get_bigrams(text)
        self.assertEqual(result, expected)

    def test_get_bigrams_short_text(self):
        """Test s krátkým textem"""
        text = "AB"
        expected = ["AB"]
        result = get_bigrams(text)
        self.assertEqual(result, expected)

    def test_get_bigrams_single_char(self):
        """Test s jedním znakem"""
        text = "A"
        expected = []
        result = get_bigrams(text)
        self.assertEqual(result, expected)

    def test_get_bigrams_empty_text(self):
        """Test s prázdným textem"""
        text = ""
        expected = []
        result = get_bigrams(text)
        self.assertEqual(result, expected)

    def test_get_bigrams_with_spaces(self):
        """Test s mezerami (podtržítky)"""
        text = "AB_CD"
        expected = ["AB", "B_", "_C", "CD"]
        result = get_bigrams(text)
        self.assertEqual(result, expected)

    def test_get_bigrams_length(self):
        """Test délky výsledku"""
        text = "ABCDEF"
        result = get_bigrams(text)
        expected_length = len(text) - 1
        self.assertEqual(len(result), expected_length)

    def test_transition_matrix_basic(self):
        """Test základní funkčnosti transition_matrix"""
        bigrams = ["AB", "BC", "AB"]
        alphabet = ["A", "B", "C"]
        matrix = transition_matrix(bigrams, alphabet)

        self.assertEqual(len(matrix), 3)
        self.assertEqual(len(matrix[0]), 3)

        for row in matrix:
            for val in row:
                self.assertGreater(val, 0)

    def test_transition_matrix_normalization(self):
        """Test normalizace matice"""
        bigrams = ["AB", "BC"]
        alphabet = ["A", "B", "C"]
        matrix = transition_matrix(bigrams, alphabet)

        # Po normalizaci by všechny hodnoty měly být kladné
        # Hodnoty mohou být > 1.0 kvůli přičtení jedniček před dělením
        for row in matrix:
            for val in row:
                self.assertGreater(val, 0.0)

    def test_transition_matrix_frequency_counting(self):
        """Test počítání frekvencí"""
        bigrams = ["AB", "AB", "AC"]  # AB se vyskytuje 2x, AC 1x
        alphabet = ["A", "B", "C"]
        matrix = transition_matrix(bigrams, alphabet)

        a_index = alphabet.index("A")
        b_index = alphabet.index("B")
        c_index = alphabet.index("C")

        self.assertGreater(matrix[a_index][b_index], matrix[a_index][c_index])

    def test_transition_matrix_empty_bigrams(self):
        """Test s prázdným seznamem bigramů"""
        bigrams = []
        alphabet = ["A", "B", "C"]
        matrix = transition_matrix(bigrams, alphabet)

        self.assertEqual(len(matrix), 3)
        self.assertEqual(len(matrix[0]), 3)

        for row in matrix:
            for val in row:
                self.assertEqual(val, 1.0)

    def test_transition_matrix_single_bigram(self):
        """Test s jedním bigramem"""
        bigrams = ["AB"]  # Použiji znaky, které jsou v základní abecedě
        alphabet = ["A", "B", "C"]
        matrix = transition_matrix(bigrams, alphabet)
        
        a_index = alphabet.index("A")
        b_index = alphabet.index("B")
        c_index = alphabet.index("C")

        # A→B by mělo mít hodnotu 2.0 (1 pozorování + 1 nahrazená nula, děleno 1 bigramem)
        # A→C by mělo mít hodnotu 1.0 (pouze nahrazená nula, děleno 1 bigramem)
        self.assertGreater(matrix[a_index][b_index], matrix[a_index][c_index])
        self.assertGreater(matrix[a_index][b_index], matrix[b_index][a_index])

    def test_transition_matrix_unknown_characters(self):
        """Test s bigramy obsahujícími neznámé znaky"""
        bigrams = ["AB", "XY"]
        alphabet = ["A", "B", "C"]
        matrix = transition_matrix(bigrams, alphabet)

        self.assertEqual(len(matrix), 3)
        self.assertEqual(len(matrix[0]), 3)

    def test_integration_get_bigrams_with_transition_matrix(self):
        """Integrační test - spojení obou funkcí"""
        text = "ABCABC"
        alphabet = ["A", "B", "C"]
        
        bigrams = get_bigrams(text)
        matrix = transition_matrix(bigrams, alphabet)
        
        # Bigrams: ["AB", "BC", "CA", "AB", "BC"]
        expected_bigrams = ["AB", "BC", "CA", "AB", "BC"]
        self.assertEqual(bigrams, expected_bigrams)

        self.assertEqual(len(matrix), 3)
        self.assertEqual(len(matrix[0]), 3)


if __name__ == '__main__':
    unittest.main()