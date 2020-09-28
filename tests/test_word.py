import unittest
from pathlib import Path
from sys import path

base_path = Path(__file__).parent.joinpath("..").resolve()
path.insert(0, str(base_path))

import snowman as sm


class TestWord(unittest.TestCase):
    
    def setUp(self):
        self.tword = sm.Word("snowman")

    def test_equality(self):
        tword2 = sm.Word("snowman")

        self.assertIsNot(self.tword, tword2, "Expected differen objects.")
        self.assertEqual(self.tword, tword2, "Expected objects to be equal.")

    def test_non_equality(self):
        tword2 = sm.Word("test")

        self.assertIsNot(self.tword, tword2, "Expected differen objects.")
        self.assertNotEqual(self.tword, tword2, "Expected objects not to be equal.")

    def test_hashable(self):
        tword2 = sm.Word("test")
        tword3 = sm.Word("snowman")

        tset = set()
        tset.add(self.tword)
        tset.add(tword2)
        tset.add(tword3)

        self.assertEqual(hash(self.tword), hash(tword3), "Expected the same hash for objects.")
        self.assertNotEqual(hash(self.tword), hash(tword2), "Expected different hashes for objects")
        self.assertEqual(len(tset), 2, "Expected two objects in set.")

    def test_string(self):
        self.assertEqual(str(self.tword), "snowman", "Incorrect string representation.")

    def test_is_in_word_when_letter_in_word(self):
        result = self.tword.is_in_word("n")
        self.assertTrue(result, "Expected True result.")
        self.assertListEqual(self.tword.mask, [0, 1, 0, 0, 0, 0, 1], "Expected mask modified.")

    def test_is_in_word_when_letter_not_in_word(self):
        result = self.tword.is_in_word("x")
        self.assertFalse(result, "Expected False result.")
        self.assertListEqual(self.tword.mask, [0, 0, 0, 0, 0, 0, 0], "Expected mask not modified.")

    def test_is_word_guessed_when_not_guessed(self):
        self.assertFalse(self.tword.is_word_guessed(), "Expected False result.")

    def test_is_word_guessed_when_is_guessed(self):
        self.tword.mask = [1, 1, 1, 1, 1, 1, 1]

        self.assertTrue(self.tword.is_word_guessed(), "Expected True result.")  
    
    def test_get_word_when_no_letters_guessed(self):
        self.assertEqual(self.tword.get_word(), "_ _ _ _ _ _ _", "Expected all underlines.")

    def test_get_word_when_all_letters_guessed(self):
        self.tword.mask = [1, 1, 1, 1, 1, 1, 1]

        self.assertEqual(self.tword.get_word(), "S N O W M A N", "Expected full word shown.")
    
    def test_get_word_when_some_letters_guessed(self):
        self.tword.mask = [1, 1, 0, 0, 0, 1, 1]

        self.assertEqual(self.tword.get_word(), "S N _ _ _ A N", "Expected some letters shown.")

    def test_set_mask_true(self):
        self.tword.set_mask_true()
        self.assertEqual(len(self.tword.word), sum(self.tword.mask), "Expected all items in mask to be 1.")


if __name__ == "__main__":
    unittest.main()