import os
import pandas as pd
from docx import Document


def get_file_extension(filename: str) -> str:
    """
    Get the file extension.
    
    Parameters:
    - filename: str, the file name or file path.
    
    Returns:
    - str, the file extension (including the "."), e.g., ".txt".
    """
    if type(filename) != str:
        raise ValueError("\"{}\" is not a file, please input a file path or file path.".format(filename))
    if not is_file_path(filename):  
        raise ValueError("\"{}\" is not a file, please input a file path or file path.".format(filename))
    _, extension = os.path.splitext(filename)
    return extension


def read_txt(file_path: str) -> str:
    """
    Reads the contents of a text file and returns it as a string.

    Parameters:
        file_path (str): The path to the text file to be read.

    Returns:
        str: The contents of the text file.
    """
    if type(file_path) != str:
        raise ValueError("\"{}\" is not a file, please input a file path or file path.".format(file_path))
    if not os.path.isfile(file_path):  
        raise ValueError("\"{}\" is not a file, please input a file path.".format(file_path))
    with open(file_path, 'r', encoding='utf-8') as file:
        text = file.read()
    return text


def read_docx(file_path: str) -> str:
    """
    Reads the contents of a text file and returns it as a string.

    Parameters:
        file_path (str): The path to the text file to be read.

    Returns:
        str: The contents of the text file.
    """
    if type(file_path) != str:
        raise ValueError("\"{}\" is not a file, please input a file path or file path.".format(file_path))
    if not os.path.isfile(file_path):  
        raise ValueError("\"{}\" is not a file, please input a file path.".format(file_path))
    doc = Document(file_path)
     
    text = []
    for paragraph in doc.paragraphs:
        text.append(paragraph.text)
    text = ''.join(text)
    return text


def to_table(df: pd.DataFrame, file_path: str, sheet_name="Sheet1") -> None:
    """
    Saves a Pandas DataFrame to a specified file format (CSV or Excel).

    Parameters:
        df (pd.DataFrame): The DataFrame to be saved.
        file_path (str): The path where the file will be saved (include file extension).
        file_format (str): The format to save the file in. Choose 'csv' or 'excel'. Defaults to 'csv'.

    Returns:
        None
    """
    if type(df) != pd.DataFrame:
        raise ValueError("\"df\" is not a pd.Dataframe, please input a pd.Dataframe form data.")
    if type(file_path) != str:
        raise ValueError("\"{}\" is not a file, please input a file path or file path.".format(file_path))
    if not is_file_path(file_path):  
        raise ValueError("\"{}\" is not a file, please input a file path.".format(file_path))
    file_format = get_file_extension(file_path)
    
    if file_format == '.csv':
        if sheet_name == "Sheet1":
            df.to_csv(file_path, index=False, encoding='utf-8-sig')
            return True
        else:
            file_path = file_path[:-4] + 'xlsx'
            df.to_excel(file_path, sheet_name=sheet_name, index=False, engine='openpyxl')
            return True
    elif file_format == '.xlsx':
        df.to_excel(file_path, sheet_name=sheet_name, index=False, engine='openpyxl')
        return True
    else:
        raise ValueError("Invalid file format. Please choose 'csv' or 'excel'.")
        return False
    
    
def is_file_path(path):
    has_extension = '.' in path and path.rsplit('.', 1)[-1].isalpha()
    return has_extension