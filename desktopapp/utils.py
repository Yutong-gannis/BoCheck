import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter.scrolledtext import ScrolledText
import pandas as pd
from BoCheck import Checker  # Assuming the checker module is defined elsewhere
from BoCheck.load import get_file_extension, read_txt, read_docx  # Helper functions

class BoCheckApp:
    """
    A GUI application for Tibetan text processing, including spelling checks and component recognition.
    
    Attributes:
    - root (tk.Tk): The main Tkinter root window.
    - current_language (str): The currently selected language for the UI.
    - text_box (ScrolledText): Text box for user text input.
    - upload_btn (tk.Button): Button for file upload.
    - process_btn (tk.Button): Button to process text input.
    - save_btn (tk.Button): Button to save results to a CSV file.
    - result_text (ScrolledText): Text box to display processing results.
    """
    
    def __init__(self, root):
        """
        Initializes the BoCheckApp class by setting up the main UI components.
        
        Parameters:
        - root (tk.Tk): The main Tkinter root window.
        """
        self.root = root
        self.root.title("BoCheck - Tibetan Spelling Check")
        self.root.geometry("800x600")
        self.root.config(bg="#f7f7f7")

        self.current_language = 'en'

        # Adding a header label
        self.header_label = tk.Label(root, text="BoCheck - Tibetan Spelling Check", font=("Helvetica", 18), bg="#f7f7f7")
        self.header_label.pack(pady=20)

        # Create Text Box for Input
        self.text_box = ScrolledText(root, wrap='word', height=8, font=("Arial", 12), bg="#fff", bd=1, relief="solid")
        self.text_box.pack(padx=10, pady=10, fill="x")

        # Adding Language Selection Buttons
        self.create_language_buttons()

        # Upload Button
        self.upload_btn = tk.Button(root, text="Upload File", command=self.upload_file, bg="#4CAF50", fg="white", font=("Arial", 12), relief="flat")
        self.upload_btn.pack(pady=10)

        # Process Button
        self.process_btn = tk.Button(root, text="Process", command=self.process_input, bg="#2196F3", fg="white", font=("Arial", 12), relief="flat")
        self.process_btn.pack(pady=10)
        
        # Save Button
        self.save_btn = tk.Button(root, text="Save to CSV", command=self.save_to_csv, bg="#FF5722", fg="white", font=("Arial", 12), relief="flat")
        self.save_btn.pack(pady=10)

        # Result Text Box for Output
        self.result_text = ScrolledText(root, wrap='word', height=8, font=("Arial", 12), bg="#f1f1f1", bd=1, relief="solid")
        self.result_text.pack(padx=10, pady=10, fill="x")

    def create_language_buttons(self):
        """
        Creates and packs language selection buttons for English, Chinese, and Tibetan.
        """
        frame = tk.Frame(self.root, bg="#f7f7f7")
        frame.pack(pady=10)
        
        en_button = tk.Button(frame, text="English", command=lambda: self.set_language('en'), bg="#e0e0e0", font=("Arial", 10), relief="flat")
        zh_button = tk.Button(frame, text="中文", command=lambda: self.set_language('zh'), bg="#e0e0e0", font=("Arial", 10), relief="flat")
        bo_button = tk.Button(frame, text="བོད་སྐད་", command=lambda: self.set_language('bo'), bg="#e0e0e0", font=("Arial", 10), relief="flat")
        
        en_button.pack(side=tk.LEFT, padx=5)
        zh_button.pack(side=tk.LEFT, padx=5)
        bo_button.pack(side=tk.LEFT, padx=5)

    def set_language(self, language):
        """
        Sets the current language of the application and updates the UI text.
        
        Parameters:
        - language (str): Language code to set ('en', 'zh', or 'bo').
        """
        self.current_language = language
        self.update_text()

    def update_text(self):
        """
        Updates the UI text based on the selected language.
        """
        if self.current_language == 'en':
            self.root.title("BoCheck - Tibetan Spelling Check")
            self.upload_btn.config(text="Upload File")
            self.process_btn.config(text="Process")
            self.save_btn.config(text="Save to CSV")
        elif self.current_language == 'zh':
            self.root.title("BoCheck - 藏文拼写检查")
            self.upload_btn.config(text="上传文件")
            self.process_btn.config(text="处理")
            self.save_btn.config(text="保存为CSV")
        else:
            self.root.title("BoCheck - བོད་ཡིག་ཚེག་རྡར་བྱས་ནས་འབྲི་བ་ལ་ཞིབ་བཤེར།")
            self.upload_btn.config(text="ཡིག་ཆ་ཕབ་ལེན།")
            self.process_btn.config(text="བཀག་བཏང་")
            self.save_btn.config(text="CSV རིགས་སྲུང་བཞག")

    def upload_file(self):
        """
        Opens a file dialog to select and upload a file, displaying its content in the text box.
        """
        file_path = filedialog.askopenfilename()
        if file_path:
            extension = get_file_extension(file_path)
            if extension == '.txt':
                text = read_txt(file_path)
            elif extension == '.docx':
                text = read_docx(file_path)
            else:
                messagebox.showerror("Error", "Invalid file format. Please upload .txt or .docx files.")
                return
            
            self.text_box.delete(1.0, tk.END)
            self.text_box.insert(tk.END, text)

    def process_input(self):
        """
        Processes the text input by calling methods for Tibetan component recognition and spelling checks.
        Displays the results in the result text box.
        """
        text = self.text_box.get("1.0", tk.END).strip()
        if not text:
            messagebox.showerror("Error", "Please provide text input or upload a file.")
            return

        checker = Checker()
        recognization_result = checker.recognization_text(text)
        check_result = checker.check_text(text)

        if recognization_result is not None and check_result is not None:
            result = recognization_result
            result['拼写检查'] = check_result['拼写检查']
            table_result = pd.DataFrame(result)
        elif recognization_result is None and check_result is not None:
            table_result = pd.DataFrame(check_result)
        elif recognization_result is not None and check_result is None:
            table_result = pd.DataFrame(recognization_result)
        else:
            table_result = pd.DataFrame(["No results available."])
        
        self.result_text.delete(1.0, tk.END)
        self.result_text.insert(tk.END, table_result.to_string(index=False))
        self.table_result = table_result

    def save_to_csv(self):
        """
        Opens a file dialog to save the results as a CSV file.
        """
        if hasattr(self, 'table_result') and self.table_result is not None:
            file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
            if file_path:
                self.table_result.to_csv(file_path, index=False)
                messagebox.showinfo("Saved", f"Results saved to {file_path}")
        else:
            messagebox.showwarning("No Data", "Please process some text first.")