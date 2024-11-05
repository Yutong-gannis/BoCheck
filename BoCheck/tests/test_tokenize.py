import pytest
from BoCheck.tokenize import punctuation_split_sentence, space_split_sentence, \
                          split_word, split_number, split_auxiliary, \
                          convert_sanskrit


example_text = '༄༅།།ཞི་ཅིན་ཕིང་གིས་ཏི་ས་ནཱ་ཡ་ཁེས་སི་རི་ལན་ཁའི་ཙུང་ཐུང་གི་འགན་བཞེས་པར་རྟེན་འབྲེལ་གློག་འཕྲིན་བཏང་གནང་བ།གསར་འགྱུར་སྤེལ་དུས།ལོའི་ཟླ་ཚེས་ཉིན།ཡོང་ཁུངས།མི་དམངས་ཉིན་རེའི་ཚགས་པར།རྩོམ་སྒྲིག་འགན་འཁུར་པ།མཁའ་འགྲོ།'


@pytest.fixture
def test_punctuation_split_sentence():
    sentences = punctuation_split_sentence(example_text)
    assert sentences == ['༄༅', 'ཞི་ཅིན་ཕིང་གིས་ཏི་ས་ནཱ་ཡ་ཁེས་སི་རི་ལན་ཁའི་ཙུང་ཐུང་གི་འགན་བཞེས་པར་རྟེན་འབྲེལ་གློག་འཕྲིན་བཏང་གནང་བ', 'གསར་འགྱུར་སྤེལ་དུས', 'ལོའི་ཟླ་ཚེས་ཉིན', 'ཡོང་ཁུངས', 'མི་དམངས་ཉིན་རེའི་ཚགས་པར', 'རྩོམ་སྒྲིག་འགན་འཁུར་པ', 'མཁའ་འགྲོ']
    
def test_space_split_sentence():
    sentence = space_split_sentence(example_text)
    assert sentence == ['༄༅།།ཞི་ཅིན་ཕིང་གིས་ཏི་ས་ནཱ་ཡ་ཁེས་སི་རི་ལན་ཁའི་ཙུང་ཐུང་གི་འགན་བཞེས་པར་རྟེན་འབྲེལ་གློག་འཕྲིན་བཏང་གནང་བ།གསར་འགྱུར་སྤེལ་དུས།ལོའི་ཟླ་ཚེས་ཉིན།ཡོང་ཁུངས།མི་དམངས་ཉིན་རེའི་ཚགས་པར།རྩོམ་སྒྲིག་འགན་འཁུར་པ།མཁའ་འགྲོ།']
    
def test_split_word():
    word_list = split_word(example_text)
    assert word_list == ['༄༅།།ཞི', 'ཅིན', 'ཕིང', 'གིས', 'ཏི', 'ས', 'ནཱ', 'ཡ', 'ཁེས', 'སི', 'རི', 'ལན', 'ཁའི', 'ཙུང', 'ཐུང', 'གི', 'འགན', 'བཞེས', 'པར', 'རྟེན', 'འབྲེལ', 'གློག', 'འཕྲིན', 'བཏང', 'གནང', 'བ།གསར', 'འགྱུར', 'སྤེལ', 'དུས།ལོའི', 'ཟླ', 'ཚེས', 'ཉིན།ཡོང', 'ཁུངས།མི', 'དམངས', 'ཉིན', 'རེའི', 'ཚགས', 'པར།རྩོམ', 'སྒྲིག', 'འགན', 'འཁུར', 'པ།མཁའ', 'འགྲོ།']
    
def test_split_number():
    word_list = split_number(split_word(example_text))
    assert word_list == ['༄༅།།ཞི', 'ཅིན', 'ཕིང', 'གིས', 'ཏི', 'ས', 'ནཱ', 'ཡ', 'ཁེས', 'སི', 'རི', 'ལན', 'ཁའི', 'ཙུང', 'ཐུང', 'གི', 'འགན', 'བཞེས', 'པར', 'རྟེན', 'འབྲེལ', 'གློག', 'འཕྲིན', 'བཏང', 'གནང', 'བ།གསར', 'འགྱུར', 'སྤེལ', 'དུས།ལོའི', 'ཟླ', 'ཚེས', 'ཉིན།ཡོང', 'ཁུངས།མི', 'དམངས', 'ཉིན', 'རེའི', 'ཚགས', 'པར།རྩོམ', 'སྒྲིག', 'འགན', 'འཁུར', 'པ།མཁའ', 'འགྲོ།']
    
def test_split_auxiliary():
    word_list = split_auxiliary(split_number(split_word(example_text)))
    assert word_list == ['༄༅།།ཞི', 'ཅིན', 'ཕིང', 'གིས', 'ཏི', 'ས', 'ནཱ', 'ཡ', 'ཁེས', 'སི', 'རི', 'ལན', 'ཁ', 'འི', 'ཙུང', 'ཐུང', 'གི', 'འགན', 'བཞེས', 'པར', 'རྟེན', 'འབྲེལ', 'གློག', 'འཕྲིན', 'བཏང', 'གནང', 'བ།གསར', 'འགྱུར', 'སྤེལ', 'དུས།ལོ', 'འི', 'ཟླ', 'ཚེས', 'ཉིན།ཡ', 'ོང', 'ཁུངས།', 'མི', 'དམངས', 'ཉིན', 'རེ', 'འི', 'ཚགས', 'པར།རྩོམ', 'སྒྲིག', 'འགན', 'འཁུར', 'པ།མཁ', 'འ', 'འགྲོ།']
    
def test_convert_sanskrit():
    word_list = convert_sanskrit(split_auxiliary(split_number(split_word(example_text))))
    assert word_list == ['༄༅།།ཞི', 'ཅིན', 'ཕིང', 'གིས', 'ཏི', 'ས', 'ནཱ', 'ཡ', 'ཁེས', 'སི', 'རི', 'ལན', 'ཁ', 'འི', 'ཙུང', 'ཐུང', 'གི', 'འགན', 'བཞེས', 'པར', 'རྟེན', 'འབྲེལ', 'གློག', 'འཕྲིན', 'བཏང', 'གནང', 'བ།གསར', 'འགྱུར', 'སྤེལ', 'དུས།ལོ', 'འི', 'ཟླ', 'ཚེས', 'ཉིན།ཡ', 'ོང', 'ཁུངས།', 'མི', 'དམངས', 'ཉིན', 'རེ', 'འི', 'ཚགས', 'པར།རྩོམ', 'སྒྲིག', 'འགན', 'འཁུར', 'པ།མཁ', 'འ', 'འགྲོ།']


def test_punctuation_split_sentence_errors():
    with pytest.raises(ValueError):
        punctuation_split_sentence(233)
        
def test_space_split_sentence_errors():
    with pytest.raises(ValueError):
        space_split_sentence(43)
        
def test_split_word_errors():
    with pytest.raises(ValueError):
        split_word(453)
        
def test_split_number_errors():
    with pytest.raises(ValueError):
        split_number(example_text)
        split_number([1, 2, 3])
        
def test_split_auxiliary_errors():
    with pytest.raises(ValueError):
        split_auxiliary(example_text)
        split_auxiliary([1, 2, 3])
        
def test_convert_sanskrit_errors():
    with pytest.raises(ValueError):
        convert_sanskrit(example_text)
        convert_sanskrit([1, 2, 3])
        
        
if __name__ == "__main__":
    pytest.main()