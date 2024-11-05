import pytest
import pandas as pd
from BoCheck.process import process_text, process_file, process_dir


example_text = '    \n    ༄༅།།ཞི་ཅིན་ཕིང་གིས་ཏི་ས་ནཱ་ཡ་ཁེས་སི་རི་ལན་ཁའི་ཙུང་ཐུང་གི་འགན་བཞེས་པར་རྟེན་འབྲེལ་གློག་འཕྲིན་བཏང་གནང་བ།\nགསར་འགྱུར་སྤེལ་དུས། \u3000【2024ལོའི་ཟླ་ 09ཚེས་25ཉིན། 14:21】  ཡོང་ཁུངས།：མི་དམངས་ཉིན་རེའི་ཚགས་པར། （རྩོམ་སྒྲིག་འགན་འཁུར་པ། མཁའ་འགྲོ།）\n\n      '
example_docx = "tests/examples/example.docx"
example_txt = "tests/examples/example.txt"
example_dir = "tests/examples"


@pytest.fixture
def test_process_text():
    """
    Test fixture for the process_text function.
    """
    result = process_text(example_text)
    assert type(result) == pd.DataFrame


def test_process_file():
    """
    Test case for the process_file function.
    """
    result = process_file(example_docx)
    assert type(result) == pd.DataFrame
    
    result = process_file(example_txt)
    assert type(result) == pd.DataFrame


def test_process_dir():
    """
    Test case for the process_dir function.
    """
    result = process_dir(example_dir, table_path=None)
    assert type(result) == dict
    
    if len(result):
        assert type(list(result.keys())[0]) == str
        assert type(list(result.values())[0]) == pd.DataFrame


def test_process_text_error():
    """
    Test case for error handling in the process_text function.
    """
    with pytest.raises(ValueError):
        process_text(example_docx)
        process_text(example_txt)


def test_process_file_error():
    """
    Test case for error handling in the process_file function.
    """
    with pytest.raises(ValueError):
        process_file(example_text)
        process_file(example_dir)


def test_process_dir_error():
    """
    Test case for error handling in the process_dir function.
    """
    with pytest.raises(ValueError):
        process_dir(example_text)
        process_dir(example_docx)
        process_dir(example_txt)


if __name__ == "__main__":
    pytest.main()
