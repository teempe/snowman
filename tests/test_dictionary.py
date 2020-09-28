import unittest
from unittest.mock import patch
from pathlib import Path
from sys import path

base_path = Path(__file__).parent.joinpath("..").resolve()
path.insert(0, str(base_path))

import snowman as sm


@patch("snowman.Path.resolve", return_value="tdict.txt")
class TestDictionary(unittest.TestCase):

    def test_find_dict_len(self, mock_path):
        tdict = sm.Dictionary("en")

        self.assertEqual(tdict.length, 7, "Incorrect number of lines in file.")

    @patch("snowman.randint", return_value=3)
    def test_draw_random_word(self, mock_randint, mock_path):
        tdict = sm.Dictionary("en")
        
        self.assertEqual(tdict.draw_random_word([]), sm.Word("snowman"), "Incorrect word.")

    def test_draw_random_word_when_forbidden_words_list_given(self, mock_path):
        tdict = sm.Dictionary("en")

        forbidden = []
        for word in ["test", "code", "snowman", "computer", "school", "house"]:
            forbidden.append(sm.Word(word))

        self.assertEqual(tdict.draw_random_word(forbidden), sm.Word("jacket"), "Incorrect word.")


if __name__ == "__main__":
    unittest.main()