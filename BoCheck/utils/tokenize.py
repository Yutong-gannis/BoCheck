import re
from typing import List
from ..letters import *


def punctuation_split_sentence(text: str) -> List[str]:
    """
    Splits the text into sentences based on Tibetan punctuation.

    Parameters:
    text (str): Input string to split.

    Returns:
    list: List of sentences.
    """
    if type(text) != str: 
        raise ValueError("\"text\" is not a string, please input a string.")
    sentences = re.split('།|༎|༏|༐|༑', text)
    sentences = [item for item in sentences if item != ""]
    return sentences


def space_split_sentence(text: str) -> List[str]:
    """
    Splits a given text into a list of words or segments based on spaces.

    Args:
        text (str): The input text to split.

    Returns:
        List[str]: A list of words or segments split by spaces.
    """
    if type(text) != str: 
        raise ValueError("\"text\" is not a string, please input a string.")
    sentences = text.split(' ')
    return sentences


def split_word(text: str) -> List[str]:
    """
    Splits the text into individual words based on Tibetan delimiters.

    Parameters:
    text (str): Input string to split.

    Returns:
    list: List of individual words.
    """
    if type(text) != str: 
        raise ValueError("\"text\" is not a string, please input a string.")
    word_list = re.split('་|༌', text)
    return word_list
    

def split_number(text: List[str]) -> List[str]:
    """
    Splits words in the text based on the presence of Tibetan numerals.

    Parameters:
    text (list): List of words to process.

    Returns:
    list: Modified list with separate numerals as individual entries.
    """
    if type(text) != list: 
        raise ValueError("\"text\" is not a list, please input a list.")
    if type(text[0]) != str: 
        raise ValueError("\"text\" is not a string list, please input a string list.")
    result_text = []
    for word in text:
        flag = 0
        for i in range(len(word)):
            if word[i] in NUMBER and len(word) > 1:
                flag = 1
                result_text.append(word[i])
        if flag == 1:
            result_text.append(word[i + 1:])
        if flag == 0:
            result_text.append(word)
    return result_text


def split_auxiliary(text: List[str]) -> List[str]:
    """
    Splits auxiliary characters, like subscripts or certain vowel modifications, from Tibetan words.

    Parameters:
    text (list): List of words to process.

    Returns:
    list: List of words with auxiliary components split.
    """
    if type(text) != list: 
        raise ValueError("\"text\" is not a list, please input a list.")
    if type(text[0]) != str: 
        raise ValueError("\"text\" is not a string list, please input a string list.")
    result_text = []
    for word in text:
        base, vowel = 0, 0
        word_copy = word
        for i in range(1, len(word_copy)):
            if word_copy[i] == 'འ':
                base += 1
                word_copy = word_copy[:i] + word_copy[i + 1:]
                break
        for j in range(len(word)):
            if word[j] in VOWEL:
                vowel += 1
                
        if vowel == 2:
            result_text.extend([word[:j - 1], word[j - 1:]])
        else:
            if base == 1:
                for k in range(len(word_copy)):
                    if word_copy[k] in ROOT_LETTER:
                        base += 1
                        break
                    if word_copy[k] in SUBSCRIPT_LETTER and k < i:
                        base += 1
                        break
                if base == 2:
                    result_text.extend([word[:i], word[i:]])
                else:
                    result_text.append(word)
            else:
                result_text.append(word)
    return result_text


def convert_sanskrit(text: List[str]) -> List[str]:
    """
    Converts specific characters that resemble Sanskrit letters in the Tibetan script.

    Parameters:
    text (list): List of words to process.

    Returns:
    list: Modified list with converted Sanskrit characters.
    """
    if type(text) != list: 
        raise ValueError("\"text\" is not a list, please input a list.")
    if type(text[0]) != str: 
        raise ValueError("\"text\" is not a string list, please input a string list.")
    for i in range(len(text)):
        if text[i] == 'སིཊ':
            text[i] = 'སིགས'
    return text