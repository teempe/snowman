from pathlib import Path
from random import randint
import linecache
import string


class Game:
    snowman = (
"""






""",
"""



                     __ __
                   /   :   \\
                   \,_____,/
""",
"""



                    (__:__)
                   /   :   \\
                   \,_____,/
""",
"""


                     (   )
                    (__:__)
                   /   :   \\
                   \,_____,/
""",
"""


                     ( " )
                    (__:__)
                   /   :   \\
                   \,_____,/
""",
"""


                     ( ">)
                    (__:__)
                   /   :   \\
                   \,_____,/
""",
"""
                       _
                     _[_]_
                     ( ">)
                    (__:__)
                   /   :   \\
                   \,_____,/
""",
"""
                       _
                  \  _[_]_
                   \ ( ">)
                    (__:__)
                   /   :   \\
                   \,_____,/
""",
"""
                       _
                  \  _[_]_  /
                   \ ( ">) /
                    (__:__)
                   /   :   \\
                   \,_____,/
"""
)

    def __init__(self, lang="en"):
        self.language = lang
        self.words_used = set()
        self.letters_missed = set()
        self.letters_used = set()
        self.dict_path = Path("dictionaries", f"{lang}.txt").resolve()
        self.dict_len = self.find_dict_len()
        self.word_to_guess = self.draw_random_word()
        self.word_mask = [0]*len(self.word_to_guess)

    def find_dict_len(self):
        """
        docstring
        """
        with open(self.dict_path) as file:
            for i, _ in enumerate(file.readlines(), 1):
                pass
        return i

    def draw_random_word(self):
        word = None
        while True:
            idx = randint(1, self.dict_len)
            word = linecache.getline(str(self.dict_path), idx).rstrip()
            if word not in self.words_used:
                break
        self.words_used.add(word)
        return word

    def show_game(self):
        return f"{self.__get_snowman()}\n\n" \
               f"{'WORD TO GUESS:':<20}{self.__get_word_to_guess()}\n\n" \
               f"{'MISSED LETTERS:':<20}{self.__get_missed_letters()}\n\n" \
               f"{'MISSINGS LEFT:':<20}{self.__get_missed_left()}\n\n"

    def __get_snowman(self):
        return self.snowman[len(self.letters_missed)]

    def __get_word_to_guess(self):
        return " ".join([sign[0].upper() if sign[1]==1 else "_" for sign in zip(self.word_to_guess, self.word_mask)])
    
    def __get_missed_letters(self):
        return ", ".join(sorted([let.upper() for let in self.letters_missed]))

    def __get_missed_left(self):
        return len(self.snowman)-1 - len(self.letters_missed)
    
    def is_letter_correct(self, letter):
        if len(letter) != 1:
            return False
        letters = string.ascii_letters
        if self.language == "pl":
            letters = letters + "ęóąśłżźćń"
        if letter not in letters:
            return False
        return True

    def process_letter(self, letter):
        if letter in self.letters_used:
            return False
        if letter in self.word_to_guess:
            self.__update_word_mask(letter)
        else:
            self.letters_missed.add(letter)
        self.letters_used.add(letter)
        return True

    def __update_word_mask(self, letter):
        idx = 0
        while True:
            idx = self.word_to_guess.find(letter, idx)
            if idx == -1:
                return
            self.word_mask[idx] = 1
            idx += 1

    def is_win(self):
        return len(self.word_to_guess) == sum(self.word_mask)

    def is_lost(self):
        return len(self.letters_missed) == len(self.snowman)-1

    def reset_game_state(self):
        self.letters_missed = set()
        self.letters_used = set()
        self.word_to_guess = self.draw_random_word()
        self.word_mask = [0]*len(self.word_to_guess)    