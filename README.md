# Hangman Helper

This repository contains a Python program that uses information theory to assist the user in playing a game of Hangman.

## Usage

To use this program, you will need to have Python installed on your system. Once you have Python installed, follow these steps:

1. Clone the repository to your local machine.
2. Navigate to the directory where the repository was cloned.
3. Install the required packages by running pip install -r requirements.txt in your terminal.
4. Run the program by executing the following command in your terminal: `python helper.py FILE_PATH [MAX_ATTEMPS]`

The <file_path> argument is the path to the file containing the list of words to be used in the game.
<max_attempts> is an optional argument that sets the maximum number of attempts allowed to guess the hidden word. If this argument is not provided, there will be no attempt limit.

Once the program is running, you will be prompted to enter a pattern for the hidden word. The pattern should consist of underscores for each unknown letter and letters for each known letter. Here are some examples of valid patterns:

- `_i__a__` for `village`
- `_a_a_h___` for `parachute`
- `s____d` for `second`

The program will then filter the list of words based on the pattern and start guessing letters. The program will continue to guess letters and update the pattern until it either correctly guesses the word or runs out of attempts.

## License

This program is licensed under the MIT license. See the [LICENSE](LICENCE) file for more information.