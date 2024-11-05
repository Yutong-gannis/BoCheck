from BoCheck.process import process_dir

if __name__ == '__main__':
    process_dir("assets", table_path="demo.xlsx", component_recognization=True, spelling_check=True)