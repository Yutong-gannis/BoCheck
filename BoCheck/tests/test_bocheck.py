import pytest
import pandas as pd
import numpy as np
from BoCheck import Checker
from BoCheck.letters import *
from BoCheck.utils.utils import get_bin


checker = Checker()
example_syllable = 'འཕྲིན'
example_text = '    \n    ༄༅།།ཞི་ཅིན་ཕིང་གིས་ཏི་ས་ནཱ་ཡ་ཁེས་སི་རི་ལན་ཁའི་ཙུང་ཐུང་གི་འགན་བཞེས་པར་རྟེན་འབྲེལ་གློག་འཕྲིན་བཏང་གནང་བ།\nགསར་འགྱུར་སྤེལ་དུས། \u3000【2024ལོའི་ཟླ་ 09ཚེས་25ཉིན། 14:21】  ཡོང་ཁུངས།：མི་དམངས་ཉིན་རེའི་ཚགས་པར། （རྩོམ་སྒྲིག་འགན་འཁུར་པ། མཁའ་འགྲོ།）\n\n      '


@pytest.fixture
def test_match():
    """
    Test the match functionality of the checker.
    """
    result = checker.match(get_bin('ཕ'), 'root_letters')
    assert result == 'ཕ'
    result = checker.match_ori('ཕ', ROOT_LETTER)
    assert result == 'ཕ'
    
def test_vectorization():
    result = checker.vectorization({'原字': 'འཕྲིན', '前加字': 'འ', '上加字': None, '基字': 'ཕ', '下加字': 'ྲ', '再下加字': None, '元音': 'ི', '后加字': 'ན', '再后加字': None})
    assert (result == np.array([ 4, -1, 13,  1,  3, -1,  0])).all()

def test_recognization():
    result = checker.recognization_syllable(example_syllable)
    assert result == {'原字': 'འཕྲིན', '前加字': 'འ', '上加字': None, '基字': 'ཕ', '下加字': 'ྲ', '再下加字': None, '元音': 'ི', '后加字': 'ན', '再后加字': None}
    result = checker.recognization_text(example_text)
    assert type(result) == pd.DataFrame
    
def test_check():
    result = checker.check_syllable(example_syllable)
    assert result == True
    result = checker.check_text(example_text)
    assert type(result) == pd.DataFrame

def test_convert_sanskrit():
    """
    Test the convert_sanskrit function to ensure specific characters are converted.
    """
    input_text = ['སིཊ', 'སིགས']
    expected_output = ['སིགས', 'སིགས']
    result = checker.convert_sanskrit(input_text)
    assert result == expected_output

def test_recognization_text():
    """
    Test the recognization_text function to ensure correct syllable recognition.
    """
    text = "ཀ་ཁ་ག་ང་"
    
    # Convert result to DataFrame for column checking
    result = checker.recognization_text(text)
    assert isinstance(result, pd.DataFrame)
    assert len(result) > 0  # Ensure that the DataFrame has rows


def test_recognization_error():
    with pytest.raises(ValueError):
        checker.recognization_syllable(4)
        checker.recognization_text(45)
        
def test_check_error():
    with pytest.raises(ValueError):
        checker.check_syllable(4)
        checker.check_text(45)
        
        
if __name__ == "__main__":
    pytest.main()
