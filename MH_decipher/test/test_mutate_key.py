import unittest

from MH_decipher.mutate_key import mutate_key


class TestMutateKey(unittest.TestCase):

    def test_mutate_key_length_unchanged(self):
        """Test, že délka klíče zůstává stejná"""
        original_key = ['A', 'B', 'C', 'D', 'E']
        mutated_key = mutate_key(original_key)
        self.assertEqual(len(mutated_key), len(original_key))

    def test_mutate_key_contains_same_elements(self):
        """Test, že mutovaný klíč obsahuje stejné prvky"""
        original_key = ['A', 'B', 'C', 'D', 'E', 'F']
        mutated_key = mutate_key(original_key)
        self.assertEqual(sorted(mutated_key), sorted(original_key))

    def test_mutate_key_different_from_original(self):
        """Test, že se klíč změnil (s vysokou pravděpodobností)"""
        original_key = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
        changed = False
        for _ in range(20):
            mutated_key = mutate_key(original_key)
            if mutated_key != original_key:
                changed = True
                break
        self.assertTrue(changed, "Klíč by se měl změnit alespoň jednou z 20 pokusů")

    def test_mutate_key_original_unchanged(self):
        """Test, že původní klíč zůstane nezměněný"""
        original_key = ['A', 'B', 'C', 'D', 'E']
        original_copy = original_key.copy()
        mutate_key(original_key)
        self.assertEqual(original_key, original_copy)

    def test_mutate_key_two_elements(self):
        """Test s minimálním klíčem (2 prvky)"""
        original_key = ['X', 'Y']
        mutated_key = mutate_key(original_key)
        self.assertEqual(len(mutated_key), 2)
        self.assertEqual(sorted(mutated_key), sorted(original_key))

    def test_mutate_key_single_element(self):
        """Test s jedním prvkem (speciální případ)"""
        original_key = ['Z']
        with self.assertRaises(ValueError):
            mutate_key(original_key)

    def test_mutate_key_alphabet(self):
        """Test s plnou abecedou"""
        alphabet = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ_")
        mutated_key = mutate_key(alphabet)
        self.assertEqual(len(mutated_key), len(alphabet))
        self.assertEqual(sorted(mutated_key), sorted(alphabet))

    def test_mutate_key_exactly_two_changes(self):
        """Test, že se změní přesně dvě pozice"""
        original_key = ['A', 'B', 'C', 'D', 'E', 'F']
        mutated_key = mutate_key(original_key)
        
        differences = 0
        for i in range(len(original_key)):
            if original_key[i] != mutated_key[i]:
                differences += 1

        self.assertIn(differences, [0, 2])


if __name__ == '__main__':
    unittest.main()