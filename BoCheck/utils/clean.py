import re
from ..letters import *


def whitespace_clean(text: str) -> str:
    """
    Cleans up a given text by removing leading and trailing whitespace, 
    replacing one or more newline characters with a single space,
    and collapsing multiple whitespace characters into a single space.
    
    Parameters:
    text (str): The input text to be cleaned.
    
    Returns:
    str: The cleaned text with leading and trailing whitespace removed, 
         newlines replaced with a single space, and extra spaces collapsed.
    """
    if type(text) != str: 
        raise ValueError("\"text\" is not a string, please input a string.")
    text = text.strip()                   # Remove leading and trailing whitespace characters
    text = re.sub(r'\n+', ' ', text)      # Replace one or more newline characters with a single space
    text = re.sub(r'\s+', ' ', text)      # Collapse multiple whitespace characters into a single space
    return text


def only_tibetan_clean(text: str) -> str:
    """
    Filters out non-Tibetan characters from the input text.

    Parameters:
    text (str): Input string to filter.

    Returns:
    str: A string containing only Tibetan characters.
    """
    if type(text) != str: 
        raise ValueError("\"text\" is not a string, please input a string.")
    filtered_text = [char for char in text if 0xF00 <= ord(char) <= 0xFFF]  
    return ''.join(filtered_text)


def corpus_clean(text: str) -> str:
    """
    Cleans up text by removing specific sets of characters and replacing them with spaces.

    Parameters:
    text (str): The input text to clean.
    
    Returns:
    str: The cleaned text with specific characters removed and extra spaces normalized.
    """
    if type(text) != str: 
        raise ValueError("\"text\" is not a string, please input a string.")
    to_remove = VERNACULAR + PUNCTUATION + OTHERS + ARABIC_NUMERALS + ['_']
    for t in to_remove:
        text = text.replace(t, ' ')
    text = re.sub(r'\s+', r' ', text)
    return text


def punctuation_clean(text: str) -> str:
    """
    Removes punctuation from the text.

    Parameters:
    text (str): Input string to process.

    Returns:
    str: Text with Tibetan punctuation removed.
    """
    if type(text) != str: 
        raise ValueError("\"text\" is not a string, please input a string.")
    for punctuation in PUNCTUATION:
        text = text.replace(punctuation, "")
    return text
