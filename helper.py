import os
import sys

import Utils

def hangman(file_path: str):
    print("Starting new game...")
    print("----------------------")
    wordlist = Utils.get_words_from_file(file_path)
    attemps = 0
    ask_pattern = True

    while True:
        # ask for the hidden letters
        if ask_pattern: 
            pattern = input("Enter the hidden letters: ")
            wordlist = Utils.filter_words_by_pattern(wordlist, pattern)

        # guess a letter
        possible_guesses = Utils.get_possible_guesses(wordlist)
        best_guesses = Utils.sort_guesses_by_entropy(wordlist, pattern, possible_guesses)

        # print the guess and ask if it's correct
        print(f"Best guess is '{best_guesses[0][0]}'. Did I guess correctly?")
        correct = input("Enter 'y' for yes, 'n' for no: ")

        if correct == 'y':
            ask_pattern = True
        else:
            ask_pattern = False
            wordlist = Utils.filter_words_by_excluded_letter(wordlist, best_guesses[0][0])
            
            attemps += 1
        
        os.system('cls' if os.name == 'nt' else 'clear')  # clear the console
            
if __name__ == "__main__":
    while True:
        hangman(sys.argv[1])