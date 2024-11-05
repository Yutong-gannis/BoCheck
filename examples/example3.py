from BoCheck import Checker


recog = Checker()
text = "ཡང་དེབ་འདི་ནི་ལས་དབང་འཛོམས་པའི་སྐབས་འགན་འཁྲི་ཞིག་ལྡན་པའི་ཐོག་ནས་ཀློག་པ་པོས་ཤོག་ལྷེ་ཕྱེ་ཡི་ཡོད།"

if __name__ == '__main__':
    result = recog.recognization_text(text)
    check_result = recog.check_text(text)
    check_result.to_csv("demo.csv", encoding='utf-8-sig')
    print(result)
    print(check_result)
    