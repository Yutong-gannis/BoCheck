import os
from tqdm import tqdm
import pandas as pd
from .bocheck.checker import Checker
from .utils.file import to_table
from .load import load_file, load_dir


def process_text(text, component_recognization=True, spelling_check=True, 
            return_result=True, table_path=None, print_result=True):
    if type(text) != str:
        raise ValueError("\"text\" is not string, please input a string.")
    if os.path.isfile(text):  
        raise ValueError("\"{}\" is a file, please use functrion 'process_file'.".format(text))
    if os.path.isdir(text):  
        raise ValueError("\"{}\" is a folder, please use functrion 'process_dir'.".format(text))
    checker = Checker()
    
    if component_recognization:
        recognization_result = checker.recognization_text(text)
    else:
        recognization_result = None
    if spelling_check:
        check_result = checker.check_text(text)
    else:
        check_result = None
    
    if recognization_result is not None and check_result is not None:
        result = recognization_result
        result['拼写检查'] = check_result['拼写检查']
    elif recognization_result is None and check_result is not None:
        result = check_result
    elif recognization_result is not None and check_result is None:
        result = recognization_result
    else:
        result = None
        
    if print_result:
        print(result)
    
    if table_path is not None:
        to_table(result, table_path)
        
    if return_result:
        return result
    
    
def process_file(file_path, component_recognization=True, spelling_check=True, 
            return_result=True, table_path=None, print_result=True):
    if type(file_path) != str:
        raise ValueError("\"{}\" is not a file, please input a file path or file path.".format(file_path))
    if not os.path.isfile(file_path):  
        raise ValueError("\"{}\" is not a file, please input a file path.".format(file_path))
    if os.path.isdir(file_path):  
        raise ValueError("\"{}\" is a folder, please use functrion 'process_dir'.".format(file_path))
    checker = Checker()
    text = load_file(file_path)
    
    if component_recognization:
        recognization_result = checker.recognization_text(text)
    else:
        recognization_result = None
    if spelling_check:
        check_result = checker.check_text(text)
    else:
        check_result = None
    
    if recognization_result is not None and check_result is not None:
        result = recognization_result
        result['拼写检查'] = check_result['拼写检查']
    elif recognization_result is None and check_result is not None:
        result = check_result
    elif recognization_result is not None and check_result is None:
        result = recognization_result
    else:
        result = None
        
    if print_result:
        print(result)
    
    if table_path is not None:
        to_table(result, table_path)
        
    if return_result:
        return result
    
    
def process_dir(dir_path, component_recognization=True, spelling_check=True, 
            return_result=True, table_path=None, print_result=True):
    if type(dir_path) != str:
        raise ValueError("\"{}\" is not a folder, lease input a folder path or folder path.".format(dir_path))
    if not os.path.isdir(dir_path):  
        raise ValueError("\"{}\" is not a folder, lease input a folder path or folder path.".format(dir_path))
    if os.path.isfile(dir_path):  
        raise ValueError("\"{}\" is a file, please use functrion 'process_file'.".format(dir_path))
    checker = Checker()
    texts = load_dir(dir_path)
    results = {}
    
    for file_path, text in tqdm(texts.items()):
        if component_recognization:
            recognization_result = checker.recognization_text(text)
        else:
            recognization_result = None
        if spelling_check:
            check_result = checker.check_text(text)
        else:
            check_result = None
        
        if recognization_result is not None and check_result is not None:
            result = recognization_result
            result['拼写检查'] = check_result['拼写检查']
        elif recognization_result is None and check_result is not None:
            result = check_result
        elif recognization_result is not None and check_result is None:
            result = recognization_result
        else:
            result = None
        
        results[os.path.basename(file_path)] = result
        
        if print_result:
            print(file_path)
            print(result)
        
        if table_path is not None:
            with pd.ExcelWriter(table_path, engine='xlsxwriter') as writer:
                for filename, result in results.items():
                    result.to_excel(writer, sheet_name=filename, index=False, engine='openpyxl')
            
    if return_result:
        return results
        