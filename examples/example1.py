from BoCheck.process import process_file

if __name__ == '__main__':
    process_file("assets/text.txt", table_path="demo.xlsx", component_recognization=True, spelling_check=True)
    process_file("assets/text.docx", table_path="demo.xlsx")