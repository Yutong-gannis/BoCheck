import pytest
from BoCheck.tokenize import punctuation_split_sentence, space_split_sentence, \
                          split_word, split_number, split_auxiliary, \
                          convert_sanskrit
                          

example_text = '༄༅།།ཞི་ཅིན་ཕིང་གིས་ཏི་ས་ནཱ་ཡ་ཁེས་སི་རི་ལན་ཁའི་ཙུང་ཐུང་གི་འགན་བཞེས་པར་རྟེན་འབྲེལ་གློག་འཕྲིན་བཏང་གནང་བ།གསར་འགྱུར་སྤེལ་དུས།ལོའི་ཟླ་ཚེས་ཉིན།ཡོང་ཁུངས།མི་དམངས་ཉིན་རེའི་ཚགས་པར།རྩོམ་སྒྲིག་འགན་འཁུར་པ།མཁའ་འགྲོ།'


@pytest.fixture
def test_clean_intergration():
    """
    Test fixture for the integration of text cleaning and splitting processes.
    """
    sentences = punctuation_split_sentence(example_text)
    sentence = space_split_sentence(example_text)
    word_list = split_word(sentences[1])
    word_list = split_number(word_list)
    word_list = split_auxiliary(word_list)
    word_list = convert_sanskrit(word_list)
    assert sentence
    assert word_list == ['ཞི', 'ཅིན', 'ཕིང', 'གིས', 'ཏི', 'ས', 'ནཱ', 'ཡ', 'ཁེས', 'སི', 'རི', 'ལན', 'ཁ', 'འི', 'ཙུང', 'ཐུང', 'གི', 'འགན', 'བཞེས', 'པར', 'རྟེན', 'འབྲེལ', 'གློག', 'འཕྲིན', 'བཏང', 'གནང', 'བ']
    
    
if __name__ == "__main__":
    pytest.main()
    