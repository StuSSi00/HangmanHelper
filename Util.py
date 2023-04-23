from math import log2

def get_words_from_file(file_path: str) -> set[str]:
    """Reads a file and returns a set of unique words in it.

    Parameters
    ----------
    file_path : str
        The path to the file to be read.

    Returns
    -------
    set[str]
        A set of unique words in the file.
    """
    
    with open(file_path, 'r', encoding='utf8') as f:
        # Read each line in the file and strip any leading or trailing whitespace
        # to get the words.
        wordlist = {line.strip() for line in f}
        
        return wordlist

def get_word_pattern(word: str, prev_pattern: str, guess: str) -> str:
    """Generates a new pattern based on the previous pattern and the guess.
    
    If the guess is in the word, the new pattern will have the guess in the
    correct positions, and '_' in the rest of the positions. If there was
    no previous pattern, the new pattern will be all '_' characters.

    Parameters
    ----------
    word : str
        The word to be guessed.
    prev_pattern : str
        The previous pattern for the word.
    guess : str
        The current guess for the word.

    Returns
    -------
    str
        The new pattern for the word.
    """
    if not prev_pattern:
        prev_pattern = '_' * len(word)
    
    if prev_pattern:
        return ''.join(char if char == guess else prev_char for char, prev_char in zip(word, prev_pattern))

def check_word_pattern(word: str, pattern: str) -> bool:
    """Check if a given word matches a given pattern, where '_' can match any character.

    Parameters
    ----------
    word : str
        The word to check against the pattern.
    pattern : str
        The pattern to check the word against. '_' can match any character.

    Returns
    -------
    bool
        True if the word matches the pattern, False otherwise.
    """
    
    if len(word) != len(pattern):
        return False

    for word_char, pattern_char in zip(word, pattern):
        if pattern_char != '_' and pattern_char != word_char:
            return False

    return True


def filter_words_by_pattern(wordlist: set[str], pattern: str) -> set[str]:
    """Returns a set of words from `wordlist` that match a given `pattern` and do not contain any excluded letters.

    Parameters
    ----------
    wordlist : set[str]
        A set of words to filter.
    pattern : str
        The pattern that words in the output set should match. Can contain letters and/or underscores (representing 
        unknown letters). For example, "c_t" would match "cat" and "cot".

    Returns
    -------
    set[str]
        A set of words from `wordlist` that match the given `pattern`.
    """
    
    filtered_words = set()
    for word in wordlist:
        if check_word_pattern(word, pattern):
            filtered_words.add(word)
            
    return filtered_words

def filter_words_by_excluded_letter(wordlist: set[str], excluded_letter: str) -> set[str]:
    """Return a set of words from the input `wordlist` that do not contain the given `excluded_letter`.

    Parameters
    ----------
    wordlist : set[str]
        A set of words to filter.
    excluded_letter : str
         A single character that should not appear in any of the words in the output set.

    Returns
    -------
    set[str]
        A set of words from the input `wordlist` that do not contain the given `excluded_letter`.
    """
    
    return {word for word in wordlist if excluded_letter not in word}

def get_all_patterns(wordlist: set[str], current_pattern: str, guess: str) -> dict[str, int]:
    """Get all the patterns for the words in the given wordlist based on the current pattern and guess.

    Parameters
    ----------
    wordlist : set[str]
        The current pattern of the guessed word, where guessed letters are filled in with the guessed letter
        and unknown letters are represented by underscores '_'.
    current_pattern : str
        a string representing the pattern of the secret word
    guess : str
        The current guess for the word.

    Returns
    -------
    possible_patterns : dict[str, int]
        possible patterns as keys and their count as values.
    """
    possible_patterns = {}
    for word in wordlist:
        pattern = get_word_pattern(word, current_pattern, guess)

        possible_patterns[pattern] = possible_patterns.get(pattern, 0) + 1
            
    return possible_patterns

def get_entropy(possible_patterns: dict[str, int]) -> float:
    """Calculate the entropy of a given set of possible patterns

    Parameters
    ----------
    possible_patterns : dict[str, int]
        A dictionary containing the count of each possible pattern.

    Returns
    -------
    float
        The entropy value of the possible patterns.
        
    Raises
    -------
    ZeroDivisionError
        If the total count of possible patterns is zero.
    """
    total_words_count = sum(possible_patterns.values())
    
    entropy = 0
    
    for posibilities in possible_patterns.values():
        prob = posibilities/total_words_count
        entropy -= prob * log2(prob)
        
    return entropy

def sort_guesses_by_entropy(wordlist: set[str], current_pattern: str, possible_guesses: set[str]) -> list[tuple[str, int]]:
    """Sort possible guesses based on their entropy score.

    Parameters
    ----------
    wordlist : set[str]
        a set of strings representing the list of valid words
    current_pattern : str
        a string representing the pattern of the secret word
    possible_guesses : set[str]
        a set of strings representing the possible guesses

    Returns
    -------
    list[tuple[str, int]]
        possible guesses and their corresponding entropy score, sorted by descending entropy score.
    """
    guesses_entropy = [(guess, get_entropy(get_all_patterns(wordlist, current_pattern, guess))) for guess in possible_guesses]
    
    return sorted(guesses_entropy, key=lambda g: g[1], reverse=True)