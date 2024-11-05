import numpy as np
from typing import List
from ..letters import *


def unicode_to_text(unicode_list):
    """
    Convert a list of Unicode code points to the corresponding text.

    Parameters:
    unicode_list (list): A list of Unicode code points (integers).

    Returns:
    str: The corresponding text.
    """
    return ''.join([chr(code) for code in unicode_list])

def get_index(var: np.array, val: int) -> int:
    """
    Finds the index of a value within a numpy array, returning 100 if the value is not found.
    
    Args:
        var (numpy.ndarray): The array to search within.
        val: The value to find the index of.
    
    Returns:
        int: The index of `val` in `var`, or 100 if `val` is not found.
    """
    result = np.argwhere(var == val)
    if len(result) != 0:
        result = int(result)
    else:
        result = 100
    return result

def get_bin(tibetan: str) -> int:
    """
    Converts a Tibetan character to its binary representation.
    
    Args:
        tibetan (str): A Tibetan character.
    
    Returns:
        str: Binary representation of the character's Unicode code point.
    """
    unicode = tibetan.encode("unicode_escape")
    encoding = unicode.decode('utf-8')
    encoding = encoding.replace('\\u', '')
    encoding = bin(int(encoding, 16)).replace('0b1111', '')
    return encoding

def get_bin_list(tibetan_list: List[str]) -> List[int]:
    """
    Converts a list of Tibetan characters into their binary representations.
    
    Args:
        tibetan_list (list of str): List of Tibetan characters.
    
    Returns:
        list of str: List of binary representations for each character.
    """
    tibetan_list_code = []
    for letter in tibetan_list:
        tibetan_list_code.append(get_bin(letter))
    return tibetan_list_code

def short_to_tall(short: str) -> str:
    """
    Converts a "short" Tibetan letter to its "tall" counterpart using a predefined mapping.
    
    Args:
        short (str): A short Tibetan letter.
    
    Returns:
        str: The tall version of the short Tibetan letter.
    """
    tall = SHORT_TO_TALL[short]
    return tall

def tall_to_short(tall: str) -> str:
    """
    Converts a "tall" Tibetan letter to its "short" counterpart.
    
    Args:
        tall (str): A tall Tibetan letter.
    
    Returns:
        str: The short version of the tall Tibetan letter, or the original letter if no mapping is found.
    """
    for key, value in SHORT_TO_TALL.items():
        if tall == value:
            return key
    return tall

def short_to_tall_list(short_list: List[str]) -> List[str]:
    """
    Converts a list of "short" Tibetan letters to their "tall" counterparts.
    
    Args:
        short_list (list of str): List of short Tibetan letters.
    
    Returns:
        list of str: List of tall Tibetan letters corresponding to the input list.
    """
    tall_list = []
    for short in short_list:
        tall_list.append(short_to_tall(short))
    return tall_list