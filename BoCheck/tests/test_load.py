import pytest
from BoCheck.load import load_file, load_dir, read_docx, read_txt

# File paths for test documents and directories
docx_example = "tests/examples/example.docx"
txt_example = "tests/examples/example.txt"
dir_example = "tests/examples"


@pytest.fixture
def test_read_docx():
    """Test reading content from a DOCX file."""
    text = read_docx(docx_example)
    assert text == (
        '              ༄༅།།ཞི་ཅིན་ཕིང་གིས་ཏི་ས་ནཱ་ཡ་ཁེས་སི་རི་ལན་ཁའི་ཙུང་ཐུང་གི་འགན་བཞེས་པར་རྟེན་འབྲེལ་གློག་འཕྲིན་བཏང་གནང་བ།གསར་འགྱུར་སྤེལ་དུས། \u3000【2024ལོའི་ཟླ་ 09ཚེས་25ཉིན། 14:21】\xa0\xa0ཡོང་ཁུངས།：མི་དམངས་ཉིན་རེའི་ཚགས་པར།\xa0（རྩོམ་སྒྲིག་འགན་འཁུར་པ། མཁའ་འགྲོ།）\xa0'
    )

def test_read_txt():
    """Test reading content from a TXT file."""
    text = read_txt(txt_example)
    assert text == (
        '    \n    ༄༅།།ཞི་ཅིན་ཕིང་གིས་ཏི་ས་ནཱ་ཡ་ཁེས་སི་རི་ལན་ཁའི་ཙུང་ཐུང་གི་འགན་བཞེས་པར་རྟེན་འབྲེལ་གློག་འཕྲིན་བཏང་གནང་བ།\nགསར་འགྱུར་སྤེལ་དུས། \u3000【2024ལོའི་ཟླ་ 09ཚེས་25ཉིན། 14:21】  ཡོང་ཁུངས།：མི་དམངས་ཉིན་རེའི་ཚགས་པར། （རྩོམ་སྒྲིག་འགན་འཁུར་པ། མཁའ་འགྲོ།）\n\n      '
    )

def test_load_file():
    """Test loading content from files using load_file function (supports both DOCX and TXT formats)."""
    # Test DOCX file loading
    text = load_file(docx_example)
    assert text == (
        '              ༄༅།།ཞི་ཅིན་ཕིང་གིས་ཏི་ས་ནཱ་ཡ་ཁེས་སི་རི་ལན་ཁའི་ཙུང་ཐུང་གི་འགན་བཞེས་པར་རྟེན་འབྲེལ་གློག་འཕྲིན་བཏང་གནང་བ།གསར་འགྱུར་སྤེལ་དུས། \u3000【2024ལོའི་ཟླ་ 09ཚེས་25ཉིན། 14:21】\xa0\xa0ཡོང་ཁུངས།：མི་དམངས་ཉིན་རེའི་ཚགས་པར།\xa0（རྩོམ་སྒྲིག་འགན་འཁུར་པ། མཁའ་འགྲོ།）\xa0'
    )
    # Test TXT file loading
    text = load_file(txt_example)
    assert text == (
        '    \n    ༄༅།།ཞི་ཅིན་ཕིང་གིས་ཏི་ས་ནཱ་ཡ་ཁེས་སི་རི་ལན་ཁའི་ཙུང་ཐུང་གི་འགན་བཞེས་པར་རྟེན་འབྲེལ་གློག་འཕྲིན་བཏང་གནང་བ།\nགསར་འགྱུར་སྤེལ་དུས། \u3000【2024ལོའི་ཟླ་ 09ཚེས་25ཉིན། 14:21】  ཡོང་ཁུངས།：མི་དམངས་ཉིན་རེའི་ཚགས་པར། （རྩོམ་སྒྲིག་འགན་འཁུར་པ། མཁའ་འགྲོ།）\n\n      '
    )

def test_load_dir():
    """Test loading multiple files from a directory using load_dir function."""
    texts = load_dir(dir_example)
    assert texts
    assert isinstance(texts, dict)
    assert len(texts) > 0

def test_read_docx_errors():
    """Test error handling for read_docx with invalid input types."""
    with pytest.raises(ValueError):
        read_docx(2)
        read_docx('a')

def test_read_txt_errors():
    """Test error handling for read_txt with invalid input types."""
    with pytest.raises(ValueError):
        read_txt(0)
        read_txt("abc")

def test_load_file_errors():
    """Test error handling for load_file with invalid input types."""
    with pytest.raises(ValueError):
        load_file(4)
        load_file("abc")

def test_load_dir_errors():
    """Test error handling for load_dir with invalid input types."""
    with pytest.raises(ValueError):
        load_dir(txt_example)
        load_dir(docx_example)
        load_dir("abc")

        
if __name__ == "__main__":
    pytest.main()
