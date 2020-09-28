import subprocess
import argparse
from snowman import Game


def get_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("-l", "--language",
                        dest="language",
                        choices={"pl", "en"},
                        default="en",
                        help="Select language for game dictionary (default: english)")
    args = parser.parse_args()
    return args.language

def print_game(game):
    subprocess.run("clear")
    print(game.show_game())

def is_play_again():
    inp = input("Do you want to play again? (y/n)").lower()
    return True if inp == "y" else False
   
def main_loop(game):
    while True:
        print_game(game)
        
        inp = input("Guess letter or type 'quit' to finish > ").lower()
        if inp == "quit":
            break
        
        if not game.is_letter_correct(inp):
            input("You can enter only single letters (press any key to continue).")
            continue
        
        game.process_letter(inp)
        
        if game.is_win():
            print_game(game)
            print("Congratulations! You guessed the word.")
            if is_play_again():
                game.reset_game_state()
                continue
            else:
                break

        if game.is_lost():
            print_game(game)
            print("Ups... seems you are a snowman.")
            if is_play_again():
                game.reset_game_state()
                continue
            else:
                break

if __name__ == "__main__":
    lang = get_arguments()
    game = Game(lang)
    main_loop(game)