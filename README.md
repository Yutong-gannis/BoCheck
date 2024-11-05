# BoCheck

[![PyPI version](https://badge.fury.io/py/your-package-name.svg)](https://badge.fury.io/py/your-package-name)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)

## Description

`BoCheck` is a Python package for Tibetan syllable component recognization and spelling check based on memristor. It allows users to tokenize, recognize and check Tibetan syllable from string, .txt or .docx file.

## Features

- Feature 1: Tibetan syllable tokenization.
- Feature 2: Tibetan syllable component recognization.
- Feature 3: Tibetan syllable spelling check.

## Installation

You can install the latest release of `BoCheck` from PyPI:

```bash
pip install BoCheck
```
Alternatively, you can install it directly from the source:
```
git clone https://github.com/username/repo-name.git
cd repo-name
pip install .
```

## Usage
Here are some basic examples to help you get started with Project Name.

### Example 1
```python
import BoCheck

# Use the end-to-end processing
BoCheck.process_text(text, table_path="demo.csv")
BoCheck.process_file("assets/text.txt", table_path=None)
BoCheck.process_file("assets/text.docx", table_path="demo.xlsx",
                     component_recognization=True, spelling_check=True)
```

### Example 2
```python
from BoCheck import Checker

# Initialize the class
recog = Checker()

text = "ཡང་དེབ་འདི་ནི་ལས་དབང་འཛོམས་པའི་སྐབས་འགན་འཁྲི་ཞིག་ལྡན་པའི་ཐོག་ནས་ཀློག་པ་པོས་ཤོག་ལྷེ་ཕྱེ་ཡི་ཡོད།"

# Component recognization
recognization_result = recog.recognization_text(text)
print(recognization_result)

# Spelling check
check_result = recog.check_text(text)
check_result.to_csv("demo.csv", encoding='utf-8-sig')
print(check_result)
```

## Documentation
Full documentation is available at Read the Docs.

## Contributing
Contributions are welcome! If you would like to contribute to this project, please read our Contributing Guide. You can also open an issue or submit a pull request on our GitHub repository.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/YourFeature`)
3. Commit your changes (`git commit -am 'Add some feature'`)
4. Push to the branch (`git push origin feature/YourFeature`)
5. Open a Pull Request

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments
Thank anyone whose code was used or who provided inspiration
Mention any additional resources or libraries that your project relies on
markdown
