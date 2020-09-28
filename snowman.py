from pathlib import Path
from random import randint
import linecache
import string


class Word:
    
    def __init__(self, word):
        self.word = word
        self.mask = [0]*len(word)

    def __eq__(self, other):
        return self.word == other.word

    def __ne__(self, other):
        return self.word != other.word
    
    def __hash__(self):
        return hash(self.word)

    def __str__(self):
        return self.word

    def is_in_word(self, letter):
        if letter in self.word:
            self.__update_mask(letter)
            return True
        return False

    def __update_mask(self, letter):
        idx = 0
        while True:
            idx = self.word.find(letter, idx)
            if idx == -1:
                break
            self.mask[idx] = 1
            idx += 1

    def is_word_guessed(self):
        return len(self.word) == sum(self.mask)

    def get_word(self):
        return " ".join([sign[0].upper() if sign[1]==1 else "_" for sign in zip(self.word, self.mask)])

    def set_mask_true(self):
        self.mask = [1]*len(self.word)


class Dictionary:

    def __init__(self, lang):
        self.file_path = Path("dictionaries", f"{lang}.txt").resolve()
        self.length = self.find_dict_len()

    def find_dict_len(self):
        with open(self.file_path) as file:
            for i, _ in enumerate(file.readlines(), 1):
                pass
        return i

    def draw_random_word(self, forbidden):
        word = None
        while True:
            idx = randint(1, self.length)
            word = Word(linecache.getline(str(self.file_path), idx).rstrip())
            if word not in forbidden:
                break
        return word


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
        self.dictionary = Dictionary(lang)
        self.word_to_guess = self.draw_random_word()

    def draw_random_word(self):
        word = self.dictionary.draw_random_word(self.words_used)
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
        return self.word_to_guess.get_word()
    
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
        if not self.word_to_guess.is_in_word(letter):
            self.letters_missed.add(letter)
        self.letters_used.add(letter)
        return True

    def is_win(self):
        return self.word_to_guess.is_word_guessed()

    def is_lost(self):
        return len(self.letters_missed) == len(self.snowman)-1

    def reset_game_state(self):
        self.letters_missed = set()
        self.letters_used = set()
        self.word_to_guess = self.draw_random_word()  