import os
from .utils.file import read_txt, read_docx, get_file_extension


def load_file(file_path):
    if type(file_path) != str:
        raise ValueError("\"{}\" is not a file, lease input a file path or file path.")
    if not os.path.isfile(file_path):  
        raise ValueError("\"{}\" is not a file, lease input a file path or file path.")
    file_format = get_file_extension(file_path)
    if file_format == '.txt':
        text = read_txt(file_path)
    elif file_format == '.docx':
        text = read_docx(file_path)
    else:
        raise ValueError("Invalid file format. Please choose .txt or .docx file.")
    return text


def load_dir(dir_path):
    if type(dir_path) != str:
        raise ValueError("\"{}\" is not a folder, lease input a folder path or folder path.".format(dir_path))
    if not os.path.isdir(dir_path):  
        raise ValueError("\"{}\" is not a folder, lease input a folder path or folder path.".format(dir_path))
    
    files = []
    for filename in os.listdir(dir_path):
        file_path = os.path.join(dir_path, filename)
        files.append(file_path)
    
    texts = {}
    for file_path in files:
        text = load_file(file_path)
        texts[file_path] = text
    return texts