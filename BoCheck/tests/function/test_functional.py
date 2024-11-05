import pytest
import pandas as pd
from BoCheck import Checker


checker = Checker()
example_syllable = 'འཕྲིན'
example_text = '    \n    ༄༅།།ཞི་ཅིན་ཕིང་གིས་ཏི་ས་ནཱ་ཡ་ཁེས་སི་རི་ལན་ཁའི་ཙུང་ཐུང་གི་འགན་བཞེས་པར་རྟེན་འབྲེལ་གློག་འཕྲིན་བཏང་གནང་བ།\nགསར་འགྱུར་སྤེལ་དུས། \u3000【2024ལོའི་ཟླ་ 09ཚེས་25ཉིན། 14:21】  ཡོང་ཁུངས།：མི་དམངས་ཉིན་རེའི་ཚགས་པར། （རྩོམ་སྒྲིག་འགན་འཁུར་པ། མཁའ་འགྲོ།）\n\n      '


@pytest.fixture
def test_recognization():
    """Test the syllable and text recognition functions."""
    result = checker.recognization_syllable(example_syllable)
    assert result == {'原字': 'འཕྲིན', '前加字': 'འ', '上加字': None, '基字': 'ཕ', '下加字': 'ྲ', '再下加字': None,
                      '元音': 'ི', '后加字': 'ན', '再后加字': None}
    result = checker.recognization_text(example_text)
    assert type(result) == pd.DataFrame
    
def test_check():
    """Test the syllable and text checking functions."""
    result = checker.check_syllable(example_syllable)
    assert result == True
    result = checker.check_text(example_text)
    assert type(result) == pd.DataFrame
    
    
def test_recognization_error():
    """Test error handling in recognition functions for invalid inputs."""
    with pytest.raises(ValueError):
        checker.recognization_syllable(4)
        checker.recognization_text(45)
        
def test_check_error():
    """Test error handling in checking functions for invalid inputs."""
    with pytest.raises(ValueError):
        checker.check_syllable(4)
        checker.check_text(45)
        
        
if __name__ == "__main__":
    pytest.main()