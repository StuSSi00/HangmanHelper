import os
import sys
import Utils

def hangman(file_path: str):
    os.system('cls' if os.name == 'nt' else 'clear')  # clear the console
    print("\033[92mStarting new game...\033[0m")
    print("----------------------")
    try:
        wordlist = Utils.get_words_from_file(file_path)
    except FileNotFoundError:
        print(f"\033[91mError: file '{file_path}' not found.\033[0m")
        return
    attemps = 0
    
    pattern = input("Enter the pattern: ")
    if "_" not in pattern:
        input()
        return
    print("\033[93mFiltering words...\033[0m")
    
    wordlist = Utils.filter_words_by_pattern(wordlist, pattern)
    guessed_letters = set()

    while True:
        if len(wordlist) == 1:
            print(f"\033[92mThe hidden word is: {list(wordlist)[0]}\033[0m")
            input()
            return
        
        # guess a letter
        print("\033[93mGetting possible guesses...\033[0m")
        possible_guesses = Utils.get_possible_guesses(wordlist)
        possible_guesses.difference_update(guessed_letters)
        print("\033[93mComputing best guess...\033[0m")
        best_guesses = Utils.sort_guesses_by_entropy(wordlist, pattern, possible_guesses)

        # print the guess and ask if it's correct
        print(f"\033[96mBest guess is '{best_guesses[0][0]}'.\033[0m")
        correct = input("Enter new patter if yes: ")
        
        os.system('cls' if os.name == 'nt' else 'clear')  # clear the console

        if correct:
            pattern = correct
            print("\033[93mFiltering words...\033[0m")
            wordlist = Utils.filter_words_by_pattern(wordlist, pattern)
            guessed_letters.add(best_guesses[0][0])
        else:
            ask_pattern = False
            print("\033[93mFiltering words...\033[0m")
            wordlist = Utils.filter_words_by_excluded_letter(wordlist, best_guesses[0][0])
            
            attemps += 1
            
def get_all_starts(wordlist):
    starts = set()
    
    for word in wordlist:
        pattern = '_' * len(word)
        pattern2 = Utils.get_word_pattern(word, pattern, word[0])
        pattern2 = Utils.get_word_pattern(word, pattern2, word[-1])
        starts.update((pattern, pattern2))
        
    return starts
            
if __name__ == "__main__":
    while True:
        if len(sys.argv) != 2:
            print("\033[91mError: missing file path argument.\033[0m")
        else:
            hangman(sys.argv[1])