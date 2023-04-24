import os
import typer

import Utils

app = typer.Typer()

@app.command()
def hangman(file_path: str = typer.Argument(..., help="File path containing the list of words.")) -> None:
    """Play a game of hangman by guessing a hidden word.

    Parameters
    ----------
    file_path : str
        File path containing the list of words.
    """
    os.system('cls' if os.name == 'nt' else 'clear')  # clear the console
    typer.secho("Starting new game...", fg=typer.colors.GREEN)
    typer.echo("----------------------")
    try:
        wordlist = Utils.get_words_from_file(file_path)
    except FileNotFoundError:
        typer.secho(f"Error: file '{file_path}' not found.", fg=typer.colors.RED)
        return
    attempts = 0
    
    pattern = typer.prompt(typer.style("Enter the pattern: ", fg=typer.colors.MAGENTA))
    if "_" not in pattern:
        input()
        return
    typer.secho("Filtering words...", fg=typer.colors.YELLOW)
    
    wordlist = Utils.filter_words_by_pattern(wordlist, pattern)
    guessed_letters = set()

    while True:
        if len(wordlist) == 1:
            typer.secho(f"The hidden word is: {list(wordlist)[0]}", fg=typer.colors.GREEN)
            input()
            return
        
        elif len(wordlist) == 0:
            typer.secho(f"The hidden word is'nt in the wordlist.", fg=typer.colors.RED)
            input()
            return
        
        # guess a letter
        typer.secho("Getting possible guesses...", fg=typer.colors.YELLOW)
        possible_guesses = Utils.get_possible_guesses(wordlist)
        possible_guesses.difference_update(guessed_letters)
        typer.secho("Computing best guess...", fg=typer.colors.YELLOW)
        best_guesses = Utils.sort_guesses_by_entropy(wordlist, pattern, possible_guesses)

        # print the guess and ask if it's correct
        typer.secho(f"Best guess is '{best_guesses[0][0]}'.", fg=typer.colors.CYAN)
        correct = typer.prompt(typer.style("Enter new pattern if yes: ", fg=typer.colors.MAGENTA))
        if correct and not Utils.validate_new_pattern(pattern, correct):
            typer.secho("Error: the pattern is'nt valid.", fg=typer.colors.RED)
        
        os.system('cls' if os.name == 'nt' else 'clear')  # clear the console

        if correct:
            pattern = correct
            typer.secho("Filtering words...", fg=typer.colors.YELLOW)
            wordlist = Utils.filter_words_by_pattern(wordlist, pattern)
            guessed_letters.add(best_guesses[0][0])
        else:
            typer.secho("Filtering words...", fg=typer.colors.YELLOW)
            wordlist = Utils.filter_words_by_excluded_letter(wordlist, best_guesses[0][0])
            
            attempts += 1

if __name__ == "__main__":
    app() 