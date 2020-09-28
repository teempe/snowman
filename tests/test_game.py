import unittest
from unittest.mock import patch
from pathlib import Path
from sys import path

base_path = Path(__file__).parent.joinpath("..").resolve()
path.insert(0, str(base_path))

import snowman as sm


@patch("snowman.Dictionary")
class TestGame(unittest.TestCase):

    def setUp(self):
        self.tword = sm.Word("snowman")

    def test_draw_random_word(self, mock_dict):
        mock_dict.return_value.draw_random_word.return_value = self.tword
        tgame = sm.Game()
        
        self.assertEqual(len(tgame.words_used), 1, "Expected used words modified.")

    @patch("snowman.Word.get_word", return_value = "_ _ _ _ _ _ _")
    def test_show_game_when_game_starts(self, mock_word, mock_dict):
        mock_dict.return_value.draw_random_word.return_value = self.tword
        tgame = sm.Game()
        
        expected_snowman = "\n\n\n\n\n\n"
        expected_text = "\n\n\nWORD TO GUESS:      _ _ _ _ _ _ _\n\nMISSED LETTERS:     \n\nMISSINGS LEFT:      8\n\n"
        self.assertEqual(tgame.show_game(), f"{expected_snowman}{expected_text}", "Incorrect appearance when game start.")

    @patch("snowman.Word.get_word", return_value = "_ _ _ _ _ _ _")
    def test_show_game_when_all_possible_missed_letters(self, mock_word, mock_dict):
        mock_dict.return_value.draw_random_word.return_value = self.tword
        tgame = sm.Game()
        tgame.letters_missed = set("qrtyuipd")
        
        expected_snowman = '\n                       _\n                  \  _[_]_  /\n                   \ ( ">) /\n                    (__:__)\n                   /   :   \\\n                   \,_____,/\n'
        expected_text = "\n\nWORD TO GUESS:      _ _ _ _ _ _ _\n\nMISSED LETTERS:     D, I, P, Q, R, T, U, Y\n\nMISSINGS LEFT:      0\n\n"
        self.assertEqual(tgame.show_game(), f"{expected_snowman}{expected_text}", "Incorrect appearance when game end.")

    @patch("snowman.Word.get_word", return_value = "S N _ _ _ A N")
    def test_show_game_when_in_the_middle_of_the_game(self, mock_word, mock_dict):
        mock_dict.return_value.draw_random_word.return_value = self.tword
        tgame = sm.Game()
        tgame.letters_missed = set("qrty")
        tgame.letters_used = set("qrtysna")

        expected_snowman = '\n\n\n                     ( " )\n                    (__:__)\n                   /   :   \\\n                   \,_____,/\n'
        expected_text = "\n\nWORD TO GUESS:      S N _ _ _ A N\n\nMISSED LETTERS:     Q, R, T, Y\n\nMISSINGS LEFT:      4\n\n"
        self.assertEqual(tgame.show_game(), f"{expected_snowman}{expected_text}", "Incorrect appearance when in the mddle of the game.")

    def test_is_letter_correct_en(self, mock_dict):
        tgame = sm.Game("en")

        for letter in ["ę", "ó", "ą", "ś", "ł", "ż", "ź", "ć", "ń"]:
            self.assertFalse(tgame.is_letter_correct(letter), "Incorrect letter validation for english language.")

    def test_is_letter_correct_pl(self, mock_dict):
        tgame = sm.Game("pl")

        for letter in ["ę", "ó", "ą", "ś", "ł", "ż", "ź", "ć", "ń"]:
            self.assertTrue(tgame.is_letter_correct(letter), "Incorrect letter validation for polish language.")

    def test_is_letter_correct_no_language_specific(self, mock_dict):
        tgame = sm.Game()

        self.assertTrue(tgame.is_letter_correct("a"), "Incorrect letter validation.")
        self.assertFalse(tgame.is_letter_correct("1"), "Incorrect letter validation.")
        self.assertFalse(tgame.is_letter_correct("-"), "Incorrect letter validation.")
        self.assertFalse(tgame.is_letter_correct("abc"), "Incorrect letter validation.")
        self.assertFalse(tgame.is_letter_correct(""), "Incorrect letter validation.")
    
    @patch("snowman.Word.is_in_word", return_value=True)
    def test_process_letter_when_letter_in_word_and_not_used(self, mock_word, mock_dict):
        mock_dict.return_value.draw_random_word.return_value = self.tword
        tgame = sm.Game()

        result = tgame.process_letter("n")
        self.assertTrue(result, "Incorrect result.")
        self.assertEqual(len(tgame.letters_used), 1, "Expected letter added to set.")
        self.assertEqual(len(tgame.letters_missed), 0, "Expected letter not added to set.")

    @patch("snowman.Word.is_in_word", return_value=False)
    def test_process_letter_when_letter_not_in_word_and_not_used(self, mock_word, mock_dict):
        mock_dict.return_value.draw_random_word.return_value = self.tword
        tgame = sm.Game()

        result = tgame.process_letter("x")
        self.assertTrue(result, "Incorrect result.")
        self.assertEqual(len(tgame.letters_used), 1, "Expected letter added to set.")
        self.assertEqual(len(tgame.letters_missed), 1, "Expected letter added to set.")

    @patch("snowman.Word.is_in_word")
    def test_process_letter_when_letter_in_used_letters(self, mock_word, mock_dict):
        mock_dict.return_value.draw_random_word.return_value = self.tword
        tgame = sm.Game()
        tgame.letters_used = set(["n"])

        result = tgame.process_letter("n")
        mock_word.assert_not_called()
        self.assertFalse(result, "Incorrect result.")
        self.assertEqual(len(tgame.letters_used), 1, "Expected letter not added to set.")
        self.assertEqual(len(tgame.letters_missed), 0, "Expected letter not added to set.")

    @patch("snowman.Word.is_word_guessed", return_value=True)
    def test_is_win(self, mock_word, mock_dict):
        mock_dict.return_value.draw_random_word.return_value = self.tword
        tgame = sm.Game()

        self.assertTrue(tgame.is_win())

    def test_is_lost(self, mock_dict):
        tgame = sm.Game()
        tgame.letters_missed = set("qrtyuipd")

        self.assertTrue(tgame.is_lost())
    
    def test_reset_game_state(self, mock_dict):
        mock_dict.return_value.draw_random_word.return_value = self.tword
        tgame = sm.Game()
        tword2 = sm.Word("house")
        tgame.words_used.add(tword2)
        tgame.word_to_guess = tword2
        tgame.letters_missed = set("qrtyipd")
        tgame.letters_used = set("qrtyipdus")

        tgame.reset_game_state()
        self.assertIsInstance(tgame.letters_missed, set, "Expected type of set.")
        self.assertEqual(len(tgame.letters_missed), 0, "Expected empty set.")
        self.assertIsInstance(tgame.letters_used, set, "Expected type of set.")
        self.assertEqual(len(tgame.letters_used), 0, "Expected empty set.")
        self.assertNotEqual(tgame.word_to_guess, tword2, "Expected new word drawed.")


if __name__ == "__main__":
    unittest.main()
