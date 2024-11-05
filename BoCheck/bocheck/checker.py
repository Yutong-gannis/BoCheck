import numpy as np
import pandas as pd
import re
from ..memristor.memristor import memristor
from ..utils.utils import get_bin_list, short_to_tall
from ..utils.clean import *
from ..utils.tokenize import *
from ..letters import *
from .recognizor import Recognizer


class Checker(Recognizer):
    """
    A class for recognizing Tibetan syllable components based on a memristive network.
    """
    def __init__(self):
        """
        Initializes the class with predefined Tibetan characters, punctuation, and memristor settings.
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
    
    def convert_sanskrit(self, text):
        """
        Converts specific characters that resemble Sanskrit letters in the Tibetan script.

        Parameters:
        text (list): List of words to process.

        Returns:
        list: Modified list with converted Sanskrit characters.
        """
        for i in range(len(text)):
            if text[i] == 'སིཊ':
                text[i] = 'སིགས'
        return text
    
    def recognization_text(self, text):
        """
        Performs Tibetan syllable recognition on input text.

        Parameters:
        text (str): Input text containing Tibetan syllables.

        Returns:
        pd.DataFrame: DataFrame containing recognized syllable components.
        """
        if type(text) != str: 
            raise ValueError("\"text\" is not a string, please input a string.")
        text = only_tibetan_clean(text)
        text = punctuation_clean(text)
        sentences = punctuation_split_sentence(text)
        tibetan_components = []
        
        for sentence in sentences:
            word_list = split_word(sentence)
            word_list = split_number(word_list)
            #word_list = split_auxiliary(word_list)
            for word in word_list:
                if len(word):
                    tibetan_att = self.recognization_syllable(word)
                    tibetan_components.append(list(tibetan_att.values()))
        tibetan_components = pd.DataFrame(tibetan_components, columns=tibetan_att.keys())
        return tibetan_components
    
    def recognization_syllable(self, tibetan):
        """
        Recognizes and categorizes the components of a Tibetan syllable based on specific character relationships.
        
        Parameters:
        tibetan (str): A Tibetan syllable as input to be analyzed and categorized into components.
        
        Returns:
        dict: A dictionary with the following keys:
            - "原字": Original input Tibetan syllable.
            - "前加字": Preposed character.
            - "上加字": Superscript character.
            - "基字": Root character.
            - "下加字": Subscript character.
            - "再下加字": Second-level subscript character.
            - "元音": Vowel.
            - "后加字": Suffix character.
            - "再后加字": Further suffix character.
        """
        if type(tibetan) != str: 
            raise ValueError("\"tibetan\" is not a string, please input a string.")
        
        three_jhz = ['བགས', 'མབས', 'གགས', 'བངས', 'དངས', 'གངས', 'འངས',
                     'གམས', 'མམས', 'བབས', 'མངས', 'གབས', 'བམས', 'འམམ']
        tibetan_att = {"原字": tibetan, "前加字": None, "上加字": None, "基字": None, "下加字": None,
                       "再下加字": None, "元音": None, "后加字": None, "再后加字": None}
        tibetan_code = get_bin_list(tibetan)
        
        # component recognization
        for tibetan in re.split(r"[་།\n]", tibetan):
            # 1 component
            if len(tibetan_code) == 1:
                tibetan_att["基字"] = self.match(tibetan_code[0], 'root_letters')
            
            # 2 components
            elif len(tibetan_code) == 2:
                tibetan_att = self.recognize_two_components(tibetan, tibetan_code, tibetan_att)
                
            # 3 components
            elif len(tibetan) == 3:
                tibetan_att = self.recognize_three_components(tibetan, tibetan_code, tibetan_att)
                        
            # 4 components
            elif len(tibetan) == 4:
                tibetan_att = self.recognize_four_components(tibetan, tibetan_code, tibetan_att)
            
            # 5 components
            elif len(tibetan) == 5:
                tibetan_att = self.recognize_five_components(tibetan, tibetan_code, tibetan_att)
                
            # 6 components
            elif len(tibetan) == 6:
                tibetan_att = self.recognize_six_components(tibetan, tibetan_code, tibetan_att)
                    
            # 7 components
            elif len(tibetan) == 7:
                tibetan_att = self.recognize_seven_components(tibetan, tibetan_code, tibetan_att)
                
            # over 7 components
            else:
                continue
        
        if tibetan_att["基字"] in self.root_letters_short:
            tibetan_att["基字"] = short_to_tall(tibetan_att["基字"])
        return tibetan_att
    
    def check_text(self, text):
        """
        Processes a given Tibetan text, checking each sentence and word for Tibetan language-specific 
        syllable structure and returns the results in a pandas DataFrame.

        Parameters:
        text (str): The input Tibetan text to be checked.

        Returns:
        DataFrame: A DataFrame containing the attributes of each syllable and a spelling check result 
                for each word.
        """
        if type(text) != str: 
            raise ValueError("\"text\" is not a string, please input a string.")
        text = only_tibetan_clean(text)
        text = punctuation_clean(text)
        sentences = punctuation_split_sentence(text)
        check_result = []
        for sentence in sentences:
            word_list = split_word(sentence)
            word_list = split_number(word_list)
            #word_list = split_auxiliary(word_list)
            #word_list = self.convert_sanskrit(word_list)
            for word in word_list:
                if len(word):
                    tibetan_att = self.recognization_syllable(word)
                    if_true = self.check_syllable(word)
                    check_result.append([tibetan_att["原字"], if_true])
        check_result = pd.DataFrame(check_result, columns=["原字", "拼写检查"])
        return check_result
    
    def check_syllable(self, tibetan):
        """
        Checks if a given Tibetan syllable conforms to grammatical rules regarding prefixes, 
        superscripts, subscripts, and suffixes.

        Parameters:
        tibetan (str): A Tibetan syllable to be checked.

        Returns:
        bool: True if the syllable conforms to the rules, False otherwise.
        """
        if type(tibetan) != str: 
            raise ValueError("\"text\" is not a string, please input a string.")
        tibetan_att = self.recognization_syllable(tibetan)
        if tibetan_att['基字'] is None:
            return False
        if tibetan_att['前加字'] is not None:
            if not self.match_ori(tibetan_att['基字'], self.prefix_root_relation[tibetan_att['前加字']]):
                return False
        if tibetan_att['上加字'] is not None:
            if not self.match_ori(tibetan_att['基字'], self.superscript_root_relation[tibetan_att['上加字']]):
                return False
        if tibetan_att['下加字'] is not None:
            if not self.match_ori(tibetan_att['基字'], self.subscript_root_relation[tibetan_att['下加字']]):
                return False
        if tibetan_att['再下加字'] is not None:
            if not self.match_ori(tibetan_att['基字'], self.subscript_root_relation[tibetan_att['再下加字']]):
                return False
        if tibetan_att['后加字'] is not None and tibetan_att['再后加字'] is not None:
            if not self.match_ori(tibetan_att['后加字'], self.suffix_relation[tibetan_att['再后加字']]):
                return False
        return True
            
        
    def vectorization(self, tibetan_att):
        """
        Converts a dictionary of Tibetan syllable attributes into a fixed-length numerical vector 
        for machine learning applications.

        Parameters:
        tibetan_att (dict): A dictionary containing syllable attributes such as prefixes, roots, 
                            superscripts, subscripts, suffixes, and vowels.

        Returns:
        numpy.ndarray: A numpy array representing the syllable in vector form, where each position 
                    corresponds to a syllable component (e.g., root, prefix, etc.).
        """
        vector = np.array([-1, -1, -1, -1, -1, -1, -1]) # 基字，前加字，上加字，下加字，元音，后加字，再后加字
        if tibetan_att['前加字'] is not None:
            try:
                vector[0] = self.prefix_letters.index(tibetan_att['前加字'])
            except:
                vector[0] = -1
        if tibetan_att['上加字'] is not None:
            try:
                vector[1] = self.superscript_letters.index(tibetan_att['上加字'])
            except:
                vector[0] = -1
        if tibetan_att['基字'] is not None:
            try:
                vector[2] = self.root_letters.index(tibetan_att['基字'])
            except:
                vector[0] = -1
        if tibetan_att['下加字'] is not None:
            try:
                vector[3] = self.subscript_letters.index(tibetan_att['下加字'])
            except:
                vector[0] = -1
        if tibetan_att['后加字'] is not None:
            try:
                vector[4] = self.suffix_letters.index(tibetan_att['后加字'])
            except:
                vector[0] = -1
        if tibetan_att['再后加字'] is not None:
            try:
                vector[5] = self.farther_suffix_letters.index(tibetan_att['再后加字'])
            except:
                vector[0] = -1
        if tibetan_att['元音'] is not None:
            try:
                vector[6] = self.vowel.index(tibetan_att['元音'])
            except:
                vector[0] = -1
        return vector