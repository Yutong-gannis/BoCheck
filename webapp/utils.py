import os
import sys
import BoCheck as bc


def process_text(text, component_recognization=True, spelling_check=True):
    """
    Process text by performing component recognition and spelling check.

    This function takes a string of text and performs two optional tasks: 
    component recognition and spelling check. Both tasks are executed 
    by the Checker class. If both tasks are selected, the results 
    are combined and returned as a single dictionary.

    Parameters:
    text (str): The input text to be processed.
    component_recognization (bool): If True, performs component recognition on the text.
    spelling_check (bool): If True, performs a spelling check on the text.

    Returns:
    dict or None: A dictionary containing the results of the component recognition 
    and/or spelling check, depending on the options selected. Returns None if no tasks are performed.
    """
    checker = bc.Checker()
    # Perform component recognition if enabled
    recognization_result = checker.recognization_text(text) if component_recognization else None
    # Perform spelling check if enabled
    check_result = checker.check_text(text) if spelling_check else None

    # Combine results based on which tasks were performed
    if recognization_result is not None and check_result is not None:
        result = recognization_result
        result['拼写检查'] = check_result['拼写检查']
    elif recognization_result is None and check_result is not None:
        result = check_result
    elif recognization_result is not None and check_result is None:
        result = recognization_result
    else:
        result = None

    return result