import BoCheck
from BoCheck.process import process_text, process_file

recog = BoCheck.Checker()

text = "ཡང་དེབ་འདི་ནི་ལས་དབང་འཛོམས་པའི་སྐབས་འགན་འཁྲི་ཞིག་ལྡན་པའི་ཐོག་ནས་ཀློག་པ་པོས་ཤོག་ལྷེ་ཕྱེ་ཡི་ཡོད།"
result = recog.recognization_text(text)
print(result)
check_result = recog.check_text(text)
check_result.to_csv("demo.csv", encoding='utf-8-sig')
print(check_result)

process_text(text, table_path="demo.csv")
process_file("assets/text.txt", table_path="demo.xlsx", component_recognization=True, spelling_check=True)
process_file("assets/text.docx", table_path="demo.xlsx")
