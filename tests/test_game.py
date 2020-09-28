import unittest
from unittest.mock import patch
from pathlib import Path
from sys import path

base_path = Path(__file__).parent.joinpath("..").resolve()
path.insert(0, str(base_path))

import snowman as sm


@patch("snowman.Path.resolve", return_value="tdict.txt")
class GameTests(unittest.TestCase):
        
    def test_find_dict_len(self, mock_path):
        tgame = sm.Game()

        self.assertEqual(tgame.dict_len, 7, "Incorrect number of lines in file.")

    @patch("snowman.randint", return_value=3)
    def test_draw_random_word(self, mock_randint, mock_path):
        tgame = sm.Game()
        
        self.assertEqual(tgame.word_to_guess, "snowman", "Incorrect word.")
        self.assertEqual(len(tgame.words_used), 1, "Expected used words modified.")

    @patch("snowman.randint", return_value=3)
    def test_show_game_when_game_starts(self, mock_randint, mock_path):
        tgame = sm.Game()
        
        expected_snowman = "\n\n\n\n\n\n"
        expected_text = "\n\n\nWORD TO GUESS:      _ _ _ _ _ _ _\n\nMISSED LETTERS:     \n\nMISSINGS LEFT:      8\n\n"
        self.assertEqual(tgame.show_game(), f"{expected_snowman}{expected_text}", "Incorrect appearance when game start.")

    @patch("snowman.randint", return_value=3)
    def test_show_game_when_all_possible_missed_letters(self, mock_randint, mock_path):
        tgame = sm.Game()
        tgame.letters_missed = set("qrtyuipd")
        
        expected_snowman = '\n                       _\n                  \  _[_]_  /\n                   \ ( ">) /\n                    (__:__)\n                   /   :   \\\n                   \,_____,/\n'
        expected_text = "\n\nWORD TO GUESS:      _ _ _ _ _ _ _\n\nMISSED LETTERS:     D, I, P, Q, R, T, U, Y\n\nMISSINGS LEFT:      0\n\n"
        self.assertEqual(tgame.show_game(), f"{expected_snowman}{expected_text}", "Incorrect appearance when game end.")

    @patch("snowman.randint", return_value=3)
    def test_show_game_when_in_the_middle_of_the_game(self, mock_randint, mock_path):
        tgame = sm.Game()
        tgame.letters_missed = set("qrty")
        tgame.letters_used = set("qrtysna")
        tgame.word_mask = [1, 1, 0, 0, 0, 1, 1]

        expected_snowman = '\n\n\n                     ( " )\n                    (__:__)\n                   /   :   \\\n                   \,_____,/\n'
        expected_text = "\n\nWORD TO GUESS:      S N _ _ _ A N\n\nMISSED LETTERS:     Q, R, T, Y\n\nMISSINGS LEFT:      4\n\n"
        self.assertEqual(tgame.show_game(), f"{expected_snowman}{expected_text}", "Incorrect appearance when in the mddle of the game.")

    def test_is_letter_correct_en(self, mock_path):
        tgame = sm.Game("en")

        for letter in ["ę", "ó", "ą", "ś", "ł", "ż", "ź", "ć", "ń"]:
            self.assertFalse(tgame.is_letter_correct(letter), "Incorrect letter validation for english language.")

    def test_is_letter_correct_pl(self, mock_path):
        tgame = sm.Game("pl")

        for letter in ["ę", "ó", "ą", "ś", "ł", "ż", "ź", "ć", "ń"]:
            self.assertTrue(tgame.is_letter_correct(letter), "Incorrect letter validation for polish language.")

    def test_is_letter_correct_no_language_specific(self, mock_path):
        tgame = sm.Game()

        self.assertTrue(tgame.is_letter_correct("a"), "Incorrect letter validation.")
        self.assertFalse(tgame.is_letter_correct("1"), "Incorrect letter validation.")
        self.assertFalse(tgame.is_letter_correct("-"), "Incorrect letter validation.")
        self.assertFalse(tgame.is_letter_correct("abc"), "Incorrect letter validation.")
        self.assertFalse(tgame.is_letter_correct(""), "Incorrect letter validation.")
    
    @patch("snowman.randint", return_value=3)
    def test_process_letter_when_letter_in_word_and_not_used(self, mock_randint, mock_path):
        tgame = sm.Game()

        result = tgame.process_letter("n")
        self.assertTrue(result, "Incorrect result.")
        self.assertEqual(len(tgame.letters_used), 1, "Expected letter added to set.")
        self.assertEqual(len(tgame.letters_missed), 0, "Expected letter not added to set.")
        self.assertListEqual(tgame.word_mask, [0, 1, 0, 0, 0, 0, 1], "Expected word mask modified.")

    @patch("snowman.randint", return_value=3)
    def test_process_letter_when_letter_not_in_word_and_not_used(self, mock_randint, mock_path):
        tgame = sm.Game()

        result = tgame.process_letter("x")
        self.assertTrue(result, "Incorrect result.")
        self.assertEqual(len(tgame.letters_used), 1, "Expected letter added to set.")
        self.assertEqual(len(tgame.letters_missed), 1, "Expected letter added to set.")
        self.assertListEqual(tgame.word_mask, [0, 0, 0, 0, 0, 0, 0], "Expected word mask not modified.")

    @patch("snowman.randint", return_value=3)
    def test_process_letter_when_letter_in_used_letters(self, mock_randint, mock_path):
        tgame = sm.Game()
        tgame.letters_used = set(["n"])
        tgame.word_mask = [0, 1, 0, 0, 0, 0, 1]

        result = tgame.process_letter("n")
        self.assertFalse(result, "Incorrect result.")
        self.assertEqual(len(tgame.letters_used), 1, "Expected letter not added to set.")
        self.assertEqual(len(tgame.letters_missed), 0, "Expected letter not added to set.")
        self.assertListEqual(tgame.word_mask, [0, 1, 0, 0, 0, 0, 1], "Expected word mask not modified.")

    @patch("snowman.randint", return_value=3)
    def test_is_win(self, mock_randint, mock_path):
        tgame = sm.Game()
        tgame.word_mask = [1, 1, 1, 1, 1, 1, 1]

        self.assertTrue(tgame.is_win())

    @patch("snowman.randint", return_value=3)
    def test_is_lost(self, mock_randint, mock_path):
        tgame = sm.Game()
        tgame.letters_missed = set("qrtyuipd")

        self.assertTrue(tgame.is_lost())
    
    def test_reset_game_state(self, mock_path):
        tgame = sm.Game()
        tword = "house"
        tgame.words_used.add(tword)
        tgame.word_to_guess = tword
        tgame.letters_missed = set("qrtyipd")
        tgame.letters_used = set("qrtyipdus")
        tgame.word_mask = [0, 0, 1, 1, 0]

        tgame.reset_game_state()
        self.assertIsInstance(tgame.letters_missed, set, "Expected type of set.")
        self.assertEqual(len(tgame.letters_missed), 0, "Expected empty set.")
        self.assertIsInstance(tgame.letters_used, set, "Expected type of set.")
        self.assertEqual(len(tgame.letters_used), 0, "Expected empty set.")
        self.assertNotEqual(tgame.word_to_guess, tword, "Expected new word drawed.")
        self.assertEqual(sum(tgame.word_mask), 0, "Expected mask with all zeros.")


if __name__ == "__main__":
    unittest.main()
