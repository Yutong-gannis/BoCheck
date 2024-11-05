def unicode_to_text(unicode_list):
    """
    Convert a list of Unicode code points to the corresponding text.

    Parameters:
    unicode_list (list): A list of Unicode code points (integers).

    Returns:
    str: The corresponding text.
    """
    return ''.join([chr(code) for code in unicode_list])

print(unicode_to_text([0x0F42,0x0F7C,0x0F72]))
