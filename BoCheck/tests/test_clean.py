import pytest
from BoCheck.clean import whitespace_clean, only_tibetan_clean, \
                          corpus_clean, punctuation_clean


example_text = '    \n    ༄༅།།ཞི་ཅིན་ཕིང་གིས་ཏི་ས་ནཱ་ཡ་ཁེས་སི་རི་ལན་ཁའི་ཙུང་ཐུང་གི་འགན་བཞེས་པར་རྟེན་འབྲེལ་གློག་འཕྲིན་བཏང་གནང་བ།\nགསར་འགྱུར་སྤེལ་དུས། \u3000【2024ལོའི་ཟླ་ 09ཚེས་25ཉིན། 14:21】  ཡོང་ཁུངས།：མི་དམངས་ཉིན་རེའི་ཚགས་པར། （རྩོམ་སྒྲིག་འགན་འཁུར་པ། མཁའ་འགྲོ།）\n\n      '
non_tibetan_text = '一二三四五'
empty_text = ''
special_characters_text = '!@#$%^&*()_+1234567890'


@pytest.fixture
def test_whitespace_clean():
    """Test whitespace cleaning function."""
    text = whitespace_clean(example_text)
    assert text == '༄༅།།ཞི་ཅིན་ཕིང་གིས་ཏི་ས་ནཱ་ཡ་ཁེས་སི་རི་ལན་ཁའི་ཙུང་ཐུང་གི་འགན་བཞེས་པར་རྟེན་འབྲེལ་གློག་འཕྲིན་བཏང་གནང་བ། གསར་འགྱུར་སྤེལ་དུས། 【2024ལོའི་ཟླ་ 09ཚེས་25ཉིན། 14:21】 ཡོང་ཁུངས།：མི་དམངས་ཉིན་རེའི་ཚགས་པར། （རྩོམ་སྒྲིག་འགན་འཁུར་པ། མཁའ་འགྲོ།）'
    
    # Test with non-Tibetan text
    text = whitespace_clean(non_tibetan_text)
    assert text == non_tibetan_text
    
    # Test with special characters
    text = whitespace_clean(special_characters_text)
    assert text == special_characters_text
    
    # Test with empty string
    text = whitespace_clean(empty_text)
    assert text == ''


def test_only_tibetan_clean():
    """Test only Tibetan character cleaning function."""
    test = only_tibetan_clean(example_text)
    assert test == '༄༅།།ཞི་ཅིན་ཕིང་གིས་ཏི་ས་ནཱ་ཡ་ཁེས་སི་རི་ལན་ཁའི་ཙུང་ཐུང་གི་འགན་བཞེས་པར་རྟེན་འབྲེལ་གློག་འཕྲིན་བཏང་གནང་བ།གསར་འགྱུར་སྤེལ་དུས།ལོའི་ཟླ་ཚེས་ཉིན།ཡོང་ཁུངས།མི་དམངས་ཉིན་རེའི་ཚགས་པར།རྩོམ་སྒྲིག་འགན་འཁུར་པ།མཁའ་འགྲོ།'
    
    # Test with non-Tibetan text
    test = only_tibetan_clean(non_tibetan_text)
    assert test == ''
    
    # Test with special characters
    test = only_tibetan_clean(special_characters_text)
    assert test == ''
    
    # Test with empty string
    test = only_tibetan_clean(empty_text)
    assert test == ''


def test_corpus_clean():
    """Test corpus cleaning function."""
    test = corpus_clean(example_text)
    assert test == ' ༄༅།།ཞི་ཅིན་ཕིང་གིས་ཏི་ས་ནཱ་ཡ་ཁེས་སི་རི་ལན་ཁའི་ཙུང་ཐུང་གི་འགན་བཞེས་པར་རྟེན་འབྲེལ་གློག་འཕྲིན་བཏང་གནང་བ། གསར་འགྱུར་སྤེལ་དུས། ལོའི་ཟླ་ ཚེས་ ཉིན། ཡོང་ཁུངས། མི་དམངས་ཉིན་རེའི་ཚགས་པར། རྩོམ་སྒྲིག་འགན་འཁུར་པ། མཁའ་འགྲོ། '
    
    # Test with non-Tibetan text
    test = corpus_clean(non_tibetan_text)
    assert test == non_tibetan_text
    
    # Test with special characters
    test = corpus_clean(special_characters_text)
    assert test == ' '
    
    # Test with empty string
    test = corpus_clean(empty_text)
    assert test == ''


def test_punctuation_clean():
    """Test punctuation cleaning function."""
    test = punctuation_clean(example_text)
    assert test == '\n༄༅།།ཞི་ཅིན་ཕིང་གིས་ཏི་ས་ནཱ་ཡ་ཁེས་སི་རི་ལན་ཁའི་ཙུང་ཐུང་གི་འགན་བཞེས་པར་རྟེན་འབྲེལ་གློག་འཕྲིན་བཏང་གནང་བ།\nགསར་འགྱུར་སྤེལ་དུས།\u30002024ལོའི་ཟླ་09ཚེས་25ཉིན།1421ཡོང་ཁུངས།མི་དམངས་ཉིན་རེའི་ཚགས་པར།རྩོམ་སྒྲིག་འགན་འཁུར་པ།མཁའ་འགྲོ།\n\n'
    
    # Test with non-Tibetan text
    test = punctuation_clean(non_tibetan_text)
    assert test == non_tibetan_text
    
    # Test with special characters
    test = punctuation_clean(special_characters_text)
    assert test == '1234567890'
    
    # Test with empty string
    test = punctuation_clean(empty_text)
    assert test == ''


def test_whitespace_clean_errors():
    """Test error handling in whitespace_clean function."""
    with pytest.raises(ValueError):
        whitespace_clean(1)
        
def test_only_tibetan_clean_errors():
    """Test error handling in only_tibetan_clean function."""
    with pytest.raises(ValueError):
        only_tibetan_clean(2)
        
def test_corpus_clean_errors():
    """Test error handling in corpus_clean function."""
    with pytest.raises(ValueError):
        corpus_clean(3)
        
def test_punctuation_clean_errors():
    """Test error handling in punctuation_clean function."""
    with pytest.raises(ValueError):
        punctuation_clean(4)
        

if __name__ == "__main__":
    pytest.main()