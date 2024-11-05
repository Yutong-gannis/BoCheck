import numpy as np
import pandas as pd
import re
from ..memristor.memristor import memristor
from ..utils.utils import get_bin_list, get_index, get_bin, short_to_tall
from ..utils.clean import *
from ..utils.tokenize import *
from ..letters import *


class Recognizer:
    def __init__(self):
        """
        Initializes the Recognizer class by loading different Tibetan script components,
        binary codes, and relationships for recognition.
        """
        self.prefix_letters = PERFIX_LETTER
        self.root_letters = ROOT_LETTER
        self.root_letters_short = ROOT_LETTER_SHORT
        self.superscript_letters = SUPERSCRIPT_LETTER
        self.subscript_letters = SUBSCRIPT_LETTER
        self.farther_subscript_letters = FARTHER_SUBSCRIPT_LETTER
        self.suffix_letters = SUFFIX_LETTER
        self.farther_suffix_letters = FARTHER_SHUFFIX_LETTER
        self.vowel = VOWEL
        self.stop = STOP
        self.punctuations = PUNCTUATION
        self.number = NUMBER
        self.root_letters = self.root_letters + self.number

        self.prefix_root_relation = PREFIX_ROOT_RELATION
        self.superscript_root_relation = SUPERSCRIPT_ROOT_RELATION
        self.subscript_root_relation = SUBSCRIPT_ROOT_RELATION
        self.suffix_relation = SUFFIX_RELATION

        self.mem = memristor()

        # Binary encodings for different character sets
        self.prefix_letters_code = get_bin_list(self.prefix_letters)
        self.superscript_letters_code = get_bin_list(self.superscript_letters)
        self.root_letters_code = get_bin_list(self.root_letters)
        self.root_letters_short_code = get_bin_list(self.root_letters_short)
        self.subscript_letters_code = get_bin_list(self.subscript_letters)
        self.farther_subscript_letters_code = get_bin_list(self.farther_subscript_letters)
        self.suffix_letters_code = get_bin_list(self.suffix_letters)
        self.farther_suffix_letters_code = get_bin_list(self.farther_suffix_letters)
        self.vowel_code = get_bin_list(self.vowel)
    
    def match(self, code, candidate):
        """
        Matches binary code for a character to the closest candidate character in a category.

        Parameters:
        code (str): Binary string of the character code.
        candidate (str): Character category to match.

        Returns:
        character: Matched character or None if no match is found.
        """
        crossbar_array = self.mem.crossbar()
        crossbar_array = self.mem.write_array(crossbar_array, eval('self.' + candidate + '_code'))
        result = self.mem.read_array(code, crossbar_array)
        index = get_index(result, 0.00064)
        
        try:
            character = eval('self.' + candidate)[index]
        except:
            character = None
        return character
    
    def match_ori(self, letter, candidate):
        """
        Matches a letter with a candidate character in the Tibetan script based on binary code.

        Parameters:
        letter (str): The letter to match.
        candidate (str): Candidate category to match against.

        Returns:
        character: Matched character or None if no match is found.
        """
        letter_code = get_bin(letter)
        candidate_code = get_bin_list(candidate)
        crossbar_array = self.mem.crossbar()
        crossbar_array = self.mem.write_array(crossbar_array, candidate_code)
        result = self.mem.read_array(letter_code, crossbar_array)
        index = get_index(result, 0.00064)
        
        try:
            character = candidate[index]
        except:
            character = None
        return character
    
    def recognize_two_components(self, tibetan, tibetan_code, tibetan_att):
        """
        Recognizes two-component Tibetan characters based on different relationships.

        Parameters:
        tibetan (list): List of two Tibetan letters to recognize.
        tibetan_code (list): Binary codes of the Tibetan letters.
        tibetan_att (dict): Dictionary to store the recognized components.

        Returns:
        dict: Updated tibetan_att with recognized components.
        """
        if self.match(tibetan_code[0], 'superscript_letters') and self.match(tibetan_code[1], 'root_letters_short') \
            and self.match_ori(short_to_tall(tibetan[1]), self.superscript_root_relation[tibetan[0]]):
            tibetan_att["上加字"] = self.match(tibetan_code[0], 'superscript_letters')
            tibetan_att["基字"] = self.match(tibetan_code[1], 'root_letters_short')
            
        elif self.match(tibetan_code[0], 'root_letters') and self.match(tibetan_code[1], 'subscript_letters') \
            and self.match_ori(tibetan[0], self.subscript_root_relation[tibetan[1]]):
            tibetan_att["基字"] = self.match(tibetan_code[0], 'root_letters')
            tibetan_att["下加字"] = self.match(tibetan_code[1], 'subscript_letters')
            
        elif self.match(tibetan_code[0], 'root_letters') and self.match(tibetan_code[1], 'suffix_letters'):
            tibetan_att["基字"] = self.match(tibetan_code[0], 'root_letters')
            tibetan_att["后加字"] = self.match(tibetan_code[1], 'suffix_letters')
            
        elif self.match(tibetan_code[0], 'root_letters') and self.match(tibetan_code[1], 'vowel'):
            tibetan_att["基字"] = self.match(tibetan_code[0], 'root_letters')
            tibetan_att["元音"] = self.match(tibetan_code[1], 'vowel')
            
        else:
            tibetan_att = tibetan_att
        return tibetan_att
    
    def recognize_three_components(self, tibetan, tibetan_code, tibetan_att):
        """
        Recognizes three-component Tibetan characters based on various rules and relations.

        Parameters:
        tibetan (list): List of three Tibetan letters to recognize.
        tibetan_code (list): Binary codes of the Tibetan letters.
        tibetan_att (dict): Dictionary to store the recognized components.

        Returns:
        dict: Updated tibetan_att with recognized components.
        """
        three_jhz = ['བགས', 'མབས', 'གགས', 'བངས', 'དངས', 'གངས', 'འངས',
                     'གམས', 'མམས', 'བབས', 'མངས', 'གབས', 'བམས', 'འམམ']
        
        if self.match(tibetan_code[0], 'prefix_letters') and self.match(tibetan_code[1], 'root_letters') \
            and self.match(tibetan_code[2], 'suffix_letters'):
            if tibetan not in three_jhz and self.match_ori(tibetan[1], self.prefix_root_relation[tibetan[0]]):
                tibetan_att["前加字"] = tibetan[0]
                tibetan_att["基字"] = tibetan[1]
                tibetan_att["后加字"] = tibetan[2]
                
            elif self.match_ori(tibetan[1], self.suffix_relation[tibetan[2]]):
                tibetan_att["基字"] = tibetan[0]
                tibetan_att["后加字"] = tibetan[1]
                tibetan_att["再后加字"] = tibetan[2]
                
            else:
                tibetan_att = tibetan_att
                
        elif self.match(tibetan_code[0], 'root_letters') and self.match(tibetan_code[1], 'suffix_letters') \
            and self.match(tibetan_code[2], 'farther_suffix_letters') \
            and self.match_ori(tibetan[1], self.suffix_relation[tibetan[2]]):
            tibetan_att["基字"] = tibetan[0]
            tibetan_att["后加字"] = tibetan[1]
            tibetan_att["再后加字"] = tibetan[2]
            
        elif self.match(tibetan_code[0], 'prefix_letters') and self.match(tibetan_code[1], 'root_letters') \
            and self.match(tibetan_code[2], 'vowel') \
            and self.match_ori(tibetan[1], self.prefix_root_relation[tibetan[0]]):
            tibetan_att["前加字"] = tibetan[0]
            tibetan_att["基字"] = tibetan[1]
            tibetan_att["元音"] = tibetan[2]
            
        elif self.match(tibetan_code[0], 'prefix_letters') and self.match(tibetan_code[1], 'superscript_letters') \
            and self.match(tibetan_code[2], 'root_letters_short') \
            and self.match_ori(short_to_tall(tibetan[2]), self.prefix_root_relation[tibetan[0]]) \
            and self.match_ori(tibetan[2], self.superscript_root_relation[tibetan[1]]):
            tibetan_att["前加字"] = tibetan[0]
            tibetan_att["上加字"] = tibetan[1]
            tibetan_att["基字"] = tibetan[2]
            
        elif self.match(tibetan_code[0], 'prefix_letters') and self.match(tibetan_code[1], 'root_letters') \
            and self.match(tibetan_code[2], 'subscript_letters') \
            and self.match_ori(tibetan[1], self.prefix_root_relation[tibetan[0]]) \
            and self.match_ori(tibetan[1], self.subscript_root_relation[tibetan[2]]):
            tibetan_att["前加字"] = tibetan[0]
            tibetan_att["基字"] = tibetan[1]
            tibetan_att["下加字"] = tibetan[2]
            
        elif self.match(tibetan_code[0], 'superscript_letters') and self.match(tibetan_code[1], 'root_letters_short') \
            and self.match(tibetan_code[2], 'vowel') \
            and self.match_ori(short_to_tall(tibetan[1]), self.superscript_root_relation[tibetan[0]]):
            tibetan_att["上加字"] = tibetan[0]
            tibetan_att["基字"] = tibetan[1]
            tibetan_att["元音"] = tibetan[2]
            
        elif self.match(tibetan_code[0], 'superscript_letters') and self.match(tibetan_code[1], 'root_letters_short') \
            and self.match(tibetan_code[2], 'subscript_letters') \
            and self.match_ori(short_to_tall(tibetan[1]), self.superscript_root_relation[tibetan[0]]) \
            and self.match_ori(tibetan[1], self.subscript_root_relation[tibetan[2]]):
            tibetan_att["上加字"] = tibetan[0]
            tibetan_att["基字"] = tibetan[1]
            tibetan_att["下加字"] = tibetan[2]
            
        elif self.match(tibetan_code[0], 'superscript_letters') and self.match(tibetan_code[1], 'root_letters_short') \
            and self.match(tibetan_code[2], 'suffix_letters') \
            and self.match_ori(short_to_tall(tibetan[1]), self.superscript_root_relation[tibetan[0]]):
            tibetan_att["上加字"] = tibetan[0]
            tibetan_att["基字"] = tibetan[1]
            tibetan_att["后加字"] = tibetan[2]
            
        elif self.match(tibetan_code[0], 'root_letters') and self.match(tibetan_code[1], 'subscript_letters') \
            and self.match(tibetan_code[2], 'vowel') \
            and self.match_ori(tibetan[0], self.subscript_root_relation[tibetan[1]]):
            tibetan_att["基字"] = tibetan[0]
            tibetan_att["下加字"] = tibetan[1]
            tibetan_att["元音"] = tibetan[2]
            
        elif self.match(tibetan_code[0], 'root_letters') and self.match(tibetan_code[1], 'subscript_letters') \
            and self.match(tibetan_code[2], 'suffix_letters') \
            and self.match_ori(tibetan[0], self.subscript_root_relation[tibetan[1]]):
            tibetan_att["基字"] = tibetan[0]
            tibetan_att["下加字"] = tibetan[1]
            tibetan_att["后加字"] = tibetan[2]
            
        elif self.match(tibetan_code[0], 'root_letters') and self.match(tibetan_code[1], 'vowel') \
            and self.match(tibetan_code[2], 'suffix_letters'):
            tibetan_att["基字"] = tibetan[0]
            tibetan_att["元音"] = tibetan[1]
            tibetan_att["后加字"] = tibetan[2]
            
        elif self.match(tibetan_code[0], 'root_letters') and self.match(tibetan_code[1], 'subscript_letters') \
            and self.match(tibetan_code[2], 'farther_subscript_letters') \
            and self.match_ori(tibetan[0], self.subscript_root_relation[tibetan[1]]) \
            and self.match_ori(tibetan[0], self.subscript_root_relation[tibetan[2]]):
            tibetan_att['基字'] = tibetan[0]
            tibetan_att['下加字'] = tibetan[1]
            tibetan_att['再下加字'] = tibetan[2]
            
        else:
            tibetan_att = tibetan_att
        return tibetan_att
    
    def recognize_four_components(self, tibetan, tibetan_code, tibetan_att):
        """
        Recognizes Tibetan words with four components (prefix, superscript, root, vowel or suffix).
        
        Parameters:
        tibetan (list): A list of Tibetan characters in the word.
        tibetan_code (list): A list of classifications for each Tibetan character (e.g., 'prefix_letters', 'root_letters', etc.).
        tibetan_att (dict): A dictionary that will hold the recognized components of the Tibetan word.
        
        Returns:
        dict: Updated `tibetan_att` with recognized Tibetan components (prefix, superscript, root, etc.) or remains unchanged.
        """
        if self.match(tibetan_code[0], 'prefix_letters') and self.match(tibetan_code[1], 'superscript_letters') \
            and self.match(tibetan_code[2], 'root_letters_short') and self.match(tibetan_code[3], 'vowel') \
            and self.match_ori(short_to_tall(tibetan[2]), self.prefix_root_relation[tibetan[0]]) \
            and self.match_ori(short_to_tall(tibetan[2]), self.superscript_root_relation[tibetan[1]]):
            tibetan_att["前加字"] = tibetan[0]
            tibetan_att["上加字"] = tibetan[1]
            tibetan_att["基字"] = tibetan[2]
            tibetan_att["元音"] = tibetan[3]
            
        elif self.match(tibetan_code[0], 'prefix_letters') and self.match(tibetan_code[1], 'root_letters') \
            and self.match(tibetan_code[2], 'subscript_letters') and self.match(tibetan_code[3], 'vowel') \
            and self.match_ori(tibetan[1], self.prefix_root_relation[tibetan[0]]) \
            and self.match_ori(tibetan[1], self.subscript_root_relation[tibetan[2]]):
            tibetan_att["前加字"] = tibetan[0]
            tibetan_att["基字"] = tibetan[1]
            tibetan_att["下加字"] = tibetan[2]
            tibetan_att["元音"] = tibetan[3]
            
        elif self.match(tibetan_code[0], 'prefix_letters') and self.match(tibetan_code[1], 'root_letters') \
            and self.match(tibetan_code[2], 'vowel') and self.match(tibetan_code[3], 'suffix_letters') \
            and self.match_ori(tibetan[1], self.prefix_root_relation[tibetan[0]]):
            tibetan_att["前加字"] = tibetan[0]
            tibetan_att["基字"] = tibetan[1]
            tibetan_att["元音"] = tibetan[2]
            tibetan_att["后加字"] = tibetan[3]
            
        elif self.match(tibetan_code[0], 'prefix_letters') and self.match(tibetan_code[1], 'superscript_letters') \
            and self.match(tibetan_code[2], 'root_letters_short') and self.match(tibetan_code[3], 'subscript_letters') \
            and self.match_ori(short_to_tall(tibetan[2]), self.prefix_root_relation[tibetan[0]]) \
            and self.match_ori(short_to_tall(tibetan[2]), self.superscript_root_relation[tibetan[1]]) \
            and self.match_ori(tibetan[2], self.subscript_root_relation[tibetan[3]]):
            tibetan_att["前加字"] = tibetan[0]
            tibetan_att["上加字"] = tibetan[1]
            tibetan_att["基字"] = tibetan[2]
            tibetan_att["下加字"] = tibetan[3]
            
        elif self.match(tibetan_code[0], 'prefix_letters') and self.match(tibetan_code[1], 'superscript_letters') \
            and self.match(tibetan_code[2], 'root_letters_short') and self.match(tibetan_code[3], 'suffix_letters') \
            and self.match_ori(short_to_tall(tibetan[2]), self.prefix_root_relation[tibetan[0]]) \
            and self.match_ori(short_to_tall(tibetan[2]), self.superscript_root_relation[tibetan[1]]):
            tibetan_att["前加字"] = tibetan[0]
            tibetan_att["上加字"] = tibetan[1]
            tibetan_att["基字"] = tibetan[2]
            tibetan_att["后加字"] = tibetan[3]
            
        elif self.match(tibetan_code[0], 'prefix_letters') and self.match(tibetan_code[1], 'root_letters') \
            and self.match(tibetan_code[2], 'subscript_letters') and self.match(tibetan_code[3], 'suffix_letters') \
            and self.match_ori(tibetan[1], self.prefix_root_relation[tibetan[0]]) \
            and self.match_ori(tibetan[1], self.subscript_root_relation[tibetan[2]]):
            tibetan_att["前加字"] = tibetan[0]
            tibetan_att["基字"] = tibetan[1]
            tibetan_att["下加字"] = tibetan[2]
            tibetan_att["后加字"] = tibetan[3]
            
        elif self.match(tibetan_code[0], 'prefix_letters') and self.match(tibetan_code[1], 'root_letters') \
            and self.match(tibetan_code[2], 'suffix_letters') and self.match(tibetan_code[3], 'farther_suffix_letters') \
            and self.match_ori(tibetan[1], self.prefix_root_relation[tibetan[0]]) \
            and self.match_ori(tibetan[2], self.suffix_relation[tibetan[3]]):
            tibetan_att["前加字"] = tibetan[0]
            tibetan_att["基字"] = tibetan[1]
            tibetan_att["后加字"] = tibetan[2]
            tibetan_att["再后加字"] = tibetan[3]
            
        elif self.match(tibetan_code[0], 'superscript_letters') and self.match(tibetan_code[1], 'root_letters_short') \
            and self.match(tibetan_code[2], 'subscript_letters') and self.match(tibetan_code[3], 'vowel') \
            and self.match_ori(short_to_tall(tibetan[1]), self.superscript_root_relation[tibetan[0]]) \
            and self.match_ori(short_to_tall(tibetan[1]), self.subscript_root_relation[tibetan[2]]):
            tibetan_att["上加字"] = tibetan[0]
            tibetan_att["基字"] = tibetan[1]
            tibetan_att["下加字"] = tibetan[2]
            tibetan_att["元音"] = tibetan[3]
            
        elif self.match(tibetan_code[0], 'superscript_letters') and self.match(tibetan_code[1], 'root_letters_short') \
            and self.match(tibetan_code[2], 'vowel') and self.match(tibetan_code[3], 'suffix_letters') \
            and self.match_ori(short_to_tall(tibetan[1]), self.superscript_root_relation[tibetan[0]]):
            tibetan_att["上加字"] = tibetan[0]
            tibetan_att["基字"] = tibetan[1]
            tibetan_att["元音"] = tibetan[2]
            tibetan_att["后加字"] = tibetan[3]
            
        elif self.match(tibetan_code[0], 'superscript_letters') and self.match(tibetan_code[1], 'root_letters_short') \
            and self.match(tibetan_code[2], 'subscript_letters') and self.match(tibetan_code[3], 'suffix_letters') \
            and self.match_ori(short_to_tall(tibetan[1]), self.superscript_root_relation[tibetan[0]]) \
            and self.match_ori(short_to_tall(tibetan[1]), self.subscript_root_relation[tibetan[2]]):
            tibetan_att["上加字"] = tibetan[0]
            tibetan_att["基字"] = tibetan[1]
            tibetan_att["下加字"] = tibetan[2]
            tibetan_att["后加字"] = tibetan[3]
            
        elif self.match(tibetan_code[0], 'superscript_letters') and self.match(tibetan_code[1], 'root_letters_short') \
            and self.match(tibetan_code[2], 'suffix_letters') and self.match(tibetan_code[3], 'farther_suffix_letters') \
            and self.match_ori(short_to_tall(tibetan[1]), self.superscript_root_relation[tibetan[0]]) \
            and self.match_ori(tibetan[2], self.suffix_relation[tibetan[3]]):
            tibetan_att["上加字"] = tibetan[0]
            tibetan_att["基字"] = tibetan[1]
            tibetan_att["后加字"] = tibetan[2]
            tibetan_att["再后加字"] = tibetan[3]
            
        elif self.match(tibetan_code[0], 'root_letters') and self.match(tibetan_code[1], 'vowel') \
            and self.match(tibetan_code[2], 'suffix_letters') and self.match(tibetan_code[3], 'farther_suffix_letters') \
            and self.match_ori(tibetan[2], self.suffix_relation[tibetan[3]]):
            tibetan_att["基字"] = tibetan[0]
            tibetan_att["元音"] = tibetan[1]
            tibetan_att["后加字"] = tibetan[2]
            tibetan_att["再后加字"] = tibetan[3]
            
        elif self.match(tibetan_code[0], 'root_letters') and self.match(tibetan_code[1], 'subscript_letters') \
            and self.match(tibetan_code[2], 'vowel') and self.match(tibetan_code[3], 'suffix_letters') \
            and self.match_ori(tibetan[0], self.subscript_root_relation[tibetan[1]]):
            tibetan_att["基字"] = tibetan[0]
            tibetan_att["下加字"] = tibetan[1]
            tibetan_att["元音"] = tibetan[2]
            tibetan_att["后加字"] = tibetan[3]
            
        elif self.match(tibetan_code[0], 'root_letters') and self.match(tibetan_code[1], 'subscript_letters') \
            and self.match(tibetan_code[2], 'suffix_letters') and self.match(tibetan_code[3], 'farther_suffix_letters') \
            and self.match_ori(tibetan[0], self.subscript_root_relation[tibetan[1]]) \
            and self.match_ori(tibetan[2], self.suffix_relation[tibetan[3]]):
            tibetan_att["基字"] = tibetan[0]
            tibetan_att["下加字"] = tibetan[1]
            tibetan_att["后加字"] = tibetan[2]
            tibetan_att["再后加字"] = tibetan[3]
            
        else:
            tibetan_att = tibetan_att
        return tibetan_att
    
    def recognize_five_components(self, tibetan, tibetan_code, tibetan_att):
        """
        Recognizes Tibetan words with five components (prefix, superscript, root, subscript, vowel or suffix).
        
        Parameters:
        tibetan (list): A list of Tibetan characters in the word.
        tibetan_code (list): A list of classifications for each Tibetan character (e.g., 'prefix_letters', 'root_letters', etc.).
        tibetan_att (dict): A dictionary that will hold the recognized components of the Tibetan word.
        
        Returns:
        dict: Updated `tibetan_att` with recognized Tibetan components (prefix, superscript, root, subscript, etc.) or remains unchanged.
        """
        if self.match(tibetan_code[0], 'prefix_letters') and self.match(tibetan_code[1], 'superscript_letters') \
            and self.match(tibetan_code[2], 'root_letters_short') and self.match(tibetan_code[3], 'subscript_letters') \
            and self.match(tibetan_code[4], 'vowel'):
            tibetan_att["前加字"] = tibetan[0]
            tibetan_att["上加字"] = tibetan[1]
            tibetan_att["基字"] = tibetan[2]
            tibetan_att["下加字"] = tibetan[3]
            tibetan_att["元音"] = tibetan[4]
            
        elif self.match(tibetan_code[0], 'prefix_letters') and self.match(tibetan_code[1], 'superscript_letters') \
            and self.match(tibetan_code[2], 'root_letters_short') and self.match(tibetan_code[3], 'subscript_letters') \
            and self.match(tibetan_code[4], 'suffix_letters'):
            tibetan_att["前加字"] = tibetan[0]
            tibetan_att["上加字"] = tibetan[1]
            tibetan_att["基字"] = tibetan[2]
            tibetan_att["下加字"] = tibetan[3]
            tibetan_att["后加字"] = tibetan[4]
            
        elif self.match(tibetan_code[0], 'prefix_letters') and self.match(tibetan_code[1], 'superscript_letters') \
            and self.match(tibetan_code[2], 'root_letters_short') and self.match(tibetan_code[3], 'vowel') \
            and self.match(tibetan_code[4], 'suffix_letters'):
            tibetan_att["前加字"] = tibetan[0]
            tibetan_att["上加字"] = tibetan[1]
            tibetan_att["基字"] = tibetan[2]
            tibetan_att["元音"] = tibetan[3]
            tibetan_att["后加字"] = tibetan[4]
            
        elif self.match(tibetan_code[0], 'prefix_letters') and self.match(tibetan_code[1], 'superscript_letters') \
            and self.match(tibetan_code[2], 'root_letters_short') and self.match(tibetan_code[3], 'suffix_letters') \
            and self.match(tibetan_code[4], 'farther_suffix_letters'):
            tibetan_att["前加字"] = tibetan[0]
            tibetan_att["上加字"] = tibetan[1]
            tibetan_att["基字"] = tibetan[2]
            tibetan_att["后加字"] = tibetan[3]
            tibetan_att["再后加字"] = tibetan[4]
                
        elif self.match(tibetan_code[0], 'prefix_letters') and self.match(tibetan_code[1], 'root_letters') \
            and self.match(tibetan_code[2], 'subscript_letters') and self.match(tibetan_code[3], 'vowel') \
            and self.match(tibetan_code[4], 'suffix_letters'):
            tibetan_att["前加字"] = tibetan[0]
            tibetan_att["基字"] = tibetan[1]
            tibetan_att["下加字"] = tibetan[2]
            tibetan_att["元音"] = tibetan[3]
            tibetan_att["后加字"] = tibetan[4]
            
        elif self.match(tibetan_code[0], 'prefix_letters') and self.match(tibetan_code[1], 'root_letters') \
            and self.match(tibetan_code[2], 'subscript_letters') and self.match(tibetan_code[3], 'suffix_letters') \
            and self.match(tibetan_code[4], 'farther_suffix_letters'):
            tibetan_att["前加字"] = tibetan[0]
            tibetan_att["基字"] = tibetan[1]
            tibetan_att["下加字"] = tibetan[2]
            tibetan_att["后加字"] = tibetan[3]
            tibetan_att["再后加字"] = tibetan[4]
            
        elif self.match(tibetan_code[0], 'prefix_letters') and self.match(tibetan_code[1], 'root_letters') \
            and self.match(tibetan_code[2], 'vowel') and self.match(tibetan_code[3], 'suffix_letters') \
            and self.match(tibetan_code[4], 'farther_suffix_letters'):
            tibetan_att["前加字"] = tibetan[0]
            tibetan_att["基字"] = tibetan[1]
            tibetan_att["元音"] = tibetan[2]
            tibetan_att["后加字"] = tibetan[3]
            tibetan_att["再后加字"] = tibetan[4]
            
        elif self.match(tibetan_code[0], 'superscript_letters') and self.match(tibetan_code[1], 'root_letters_short') \
            and self.match(tibetan_code[2], 'subscript_letters') and self.match(tibetan_code[3], 'vowel') \
            and self.match(tibetan_code[4], 'suffix_letters'):
            tibetan_att["上加字"] = tibetan[0]
            tibetan_att["基字"] = tibetan[1]
            tibetan_att["下加字"] = tibetan[2]
            tibetan_att["元音"] = tibetan[3]
            tibetan_att["后加字"] = tibetan[4]
            
        elif self.match(tibetan_code[0], 'superscript_letters') and self.match(tibetan_code[1], 'root_letters_short') \
            and self.match(tibetan_code[2], 'subscript_letters') and self.match(tibetan_code[3], 'suffix_letters') \
            and self.match(tibetan_code[4], 'farther_suffix_letters'):
            tibetan_att["上加字"] = tibetan[0]
            tibetan_att["基字"] = tibetan[1]
            tibetan_att["下加字"] = tibetan[2]
            tibetan_att["后加字"] = tibetan[3]
            tibetan_att["再后加字"] = tibetan[4]
            
        elif self.match(tibetan_code[0], 'superscript_letters') and self.match(tibetan_code[1], 'root_letters_short') \
            and self.match(tibetan_code[2], 'vowel') and self.match(tibetan_code[3], 'suffix_letters') \
            and self.match(tibetan_code[4], 'farther_suffix_letters'):
            tibetan_att["上加字"] = tibetan[0]
            tibetan_att["基字"] = tibetan[1]
            tibetan_att["元音"] = tibetan[2]
            tibetan_att["后加字"] = tibetan[3]
            tibetan_att["再后加字"] = tibetan[4]
            
        elif self.match(tibetan_code[0], 'root_letters') and self.match(tibetan_code[1], 'subscript_letters') \
            and self.match(tibetan_code[2], 'vowel') and self.match(tibetan_code[3], 'suffix_letters') \
            and self.match(tibetan_code[4], 'farther_suffix_letters'):
            tibetan_att["基字"] = tibetan[0]
            tibetan_att["下加字"] = tibetan[1]
            tibetan_att["元音"] = tibetan[2]
            tibetan_att["后加字"] = tibetan[3]
            tibetan_att["再后加字"] = tibetan[4]
            
        else:
            tibetan_att = tibetan_att
        return tibetan_att
    
    def recognize_six_components(self, tibetan, tibetan_code, tibetan_att):
        """
        Recognizes a Tibetan word composed of six components and updates tibetan_att accordingly.

        Parameters:
        tibetan (list): A list of Tibetan characters representing a word.
        tibetan_code (list): A list of codes representing the types of the corresponding Tibetan characters.
        tibetan_att (dict): A dictionary to store recognized components of the word, e.g., prefix, root letter, etc.

        Returns:
        dict: Updated tibetan_att with recognized components, such as 前加字 (prefix), 上加字 (superscript), 基字 (root letter),
        元音 (vowel), 后加字 (suffix), 下加字 (subscript), 再后加字 (farther suffix), depending on the word structure.
        """
        if self.match(tibetan_code[0], 'prefix_letters') and self.match(tibetan_code[1], 'superscript_letters') \
            and self.match(tibetan_code[2], 'root_letters_short') and self.match(tibetan_code[3], 'subscript_letters') \
            and self.match(tibetan_code[4], 'vowel') and self.match(tibetan_code[5], 'suffix_letters'):
            tibetan_att["前加字"] = tibetan[0]
            tibetan_att["上加字"] = tibetan[1]
            tibetan_att["基字"] = tibetan[2]
            tibetan_att["下加字"] = tibetan[3]
            tibetan_att["元音"] = tibetan[4]
            tibetan_att["后加字"] = tibetan[5]
            
        elif self.match(tibetan_code[0], 'prefix_letters') and self.match(tibetan_code[1], 'root_letters') \
            and self.match(tibetan_code[2], 'subscript_letters') and self.match(tibetan_code[3], 'vowel') \
            and self.match(tibetan_code[4], 'suffix_letters') and self.match(tibetan_code[5], 'farther_suffix_letters'):
            tibetan_att["前加字"] = tibetan[0]
            tibetan_att["基字"] = tibetan[1]
            tibetan_att["下加字"] = tibetan[2]
            tibetan_att["元音"] = tibetan[3]
            tibetan_att["后加字"] = tibetan[4]
            tibetan_att["再后加字"] = tibetan[5]
            
        elif self.match(tibetan_code[0], 'prefix_letters') and self.match(tibetan_code[1], 'superscript_letters') \
            and self.match(tibetan_code[2], 'root_letters_short') and self.match(tibetan_code[3], 'vowel') \
            and self.match(tibetan_code[4], 'suffix_letters') and self.match(tibetan_code[5], 'farther_suffix_letters'):
            tibetan_att["前加字"] = tibetan[0]
            tibetan_att["上加字"] = tibetan[1]
            tibetan_att["基字"] = tibetan[2]
            tibetan_att["元音"] = tibetan[3]
            tibetan_att["后加字"] = tibetan[4]
            tibetan_att["再后加字"] = tibetan[5]
            
        elif self.match(tibetan_code[0], 'prefix_letters') and self.match(tibetan_code[1], 'superscript_letters') \
            and self.match(tibetan_code[2], 'root_letters_short') and self.match(tibetan_code[3], 'subscript_letters') \
            and self.match(tibetan_code[4], 'suffix_letters') and self.match(tibetan_code[5], 'farther_suffix_letters'):
            tibetan_att["前加字"] = tibetan[0]
            tibetan_att["上加字"] = tibetan[1]
            tibetan_att["基字"] = tibetan[2]
            tibetan_att["下加字"] = tibetan[3]
            tibetan_att["后加字"] = tibetan[4]
            tibetan_att["再后加字"] = tibetan[5]
            
        elif self.match(tibetan_code[0], 'superscript_letters') and self.match(tibetan_code[1], 'root_letters_short') \
            and self.match(tibetan_code[2], 'subscript_letters') and self.match(tibetan_code[3], 'vowel') \
            and self.match(tibetan_code[4], 'suffix_letters') and self.match(tibetan_code[5], 'farther_suffix_letters'):
            tibetan_att["上加字"] = tibetan[0]
            tibetan_att["基字"] = tibetan[1]
            tibetan_att["下加字"] = tibetan[2]
            tibetan_att["元音"] = tibetan[3]
            tibetan_att["后加字"] = tibetan[4]
            tibetan_att["再后加字"] = tibetan[5]
            
        else:
            tibetan_att = tibetan_att
        return tibetan_att
    
    def recognize_seven_components(self, tibetan, tibetan_code, tibetan_att):
        """
        Recognizes a Tibetan word composed of seven components and updates tibetan_att accordingly.

        Parameters:
        tibetan (list): A list of Tibetan characters representing a word.
        tibetan_code (list): A list of codes representing the types of the corresponding Tibetan characters.
        tibetan_att (dict): A dictionary to store recognized components of the word, e.g., prefix, root letter, etc.

        Returns:
        dict: Updated tibetan_att with recognized components.
        """
        if self.match(tibetan_code[0], 'prefix_letters') and self.match(tibetan_code[1], 'superscript_letters') \
            and self.match(tibetan_code[2], 'root_letters_short') and self.match(tibetan_code[3], 'subscript_letters') \
            and self.match(tibetan_code[4], 'vowel') and self.match(tibetan_code[5], 'suffix_letters') \
            and self.match(tibetan_code[6], 'farther_suffix_letters'):
            tibetan_att["前加字"] = tibetan[0]
            tibetan_att["上加字"] = tibetan[1]
            tibetan_att["基字"] = tibetan[2]
            tibetan_att["下加字"] = tibetan[3]
            tibetan_att["元音"] = tibetan[4]
            tibetan_att["后加字"] = tibetan[5]
            tibetan_att["再后加字"] = tibetan[6]
            
        else:
            tibetan_att = tibetan_att
        return tibetan_att