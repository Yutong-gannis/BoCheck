import pytest
from BoCheck.clean import whitespace_clean, only_tibetan_clean, \
                          corpus_clean, punctuation_clean
                          

example_text = '༄༅།།ཞི་ཅིན་ཕིང་གིས་ཏི་ས་ནཱ་ཡ་ཁེས་སི་རི་ལན་ཁའི་ཙུང་ཐུང་གི་འགན་བཞེས་པར་རྟེན་འབྲེལ་གློག་འཕྲིན་བཏང་གནང་བ།གསར་འགྱུར་སྤེལ་དུས།ལོའི་ཟླ་ཚེས་ཉིན།ཡོང་ཁུངས།མི་དམངས་ཉིན་རེའི་ཚགས་པར།རྩོམ་སྒྲིག་འགན་འཁུར་པ།མཁའ་འགྲོ།'


@pytest.fixture
def test_clean_intergration():
    """
    Test fixture for the text cleaning process.
    """
    text = whitespace_clean(example_text)
    text = punctuation_clean(text)
    text = corpus_clean(text)
    text = only_tibetan_clean(text)
    assert text == '༄༅།།ཞི་ཅིན་ཕིང་གིས་ཏི་ས་ནཱ་ཡ་ཁེས་སི་རི་ལན་ཁའི་ཙུང་ཐུང་གི་འགན་བཞེས་པར་རྟེན་འབྲེལ་གློག་འཕྲིན་བཏང་གནང་བ།གསར་འགྱུར་སྤེལ་དུས།ལོའི་ཟླ་ཚེས་ཉིན།ཡོང་ཁུངས།མི་དམངས་ཉིན་རེའི་ཚགས་པར།རྩོམ་སྒྲིག་འགན་འཁུར་པ།མཁའ་འགྲོ།'
    

if __name__ == "__main__":
    pytest.main()