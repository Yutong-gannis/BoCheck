from flask import Flask, request, render_template, redirect, url_for, flash, send_file
import os
from BoCheck.load import read_txt, read_docx, get_file_extension
from werkzeug.utils import secure_filename
from utils import process_text

# Initialize the Flask app
app = Flask(__name__)
app.secret_key = "supersecretkey"  # for session management

# Set allowed extensions
ALLOWED_EXTENSIONS = {'txt', 'docx'}
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Make sure the upload folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


def allowed_file(filename):
    """
    Check if the filename has an allowed extension.
    This function checks whether a given filename includes a file extension that is 
    listed in the allowed extensions defined by ALLOWED_EXTENSIONS.

    Parameters:
    filename (str): The name of the file to be checked.

    Returns:
    bool: True if the file has an allowed extension, False otherwise.
    """
    if '.' in filename:
        extension = filename.rsplit('.', 1)[1].lower()
        if extension in ALLOWED_EXTENSIONS:
            return True
    return False


@app.route('/', methods=['GET', 'POST'])
def index():
    """
    Handle the main page and process text or file inputs on form submission.

    This function responds to both GET and POST requests for the index route.
    For a POST request, it handles text input or file upload from the user.
    If a file is uploaded, it verifies the file type, saves it, and reads its content.
    It then processes the text for component recognition and/or spelling checks.
    The result is displayed as an HTML table, if available.

    Returns:
    For GET requests, renders the main page with a blank form.
    For POST requests:
      If successful, renders the result as an HTML table on the main page.
      If the input is invalid, redirects to the main page with an error message.
    """
    if request.method == 'POST':
        text = request.form.get('text')  # Text input
        file = request.files.get('file')  # File input

        if file and allowed_file(file.filename):  # Handle file upload
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            
            # Process the file
            extension = get_file_extension(file_path)
            if extension == '.txt':
                text = read_txt(file_path)
            elif extension == '.docx':
                text = read_docx(file_path)
            else:
                flash("Invalid file format. Please upload .txt or .docx files.")
                return redirect(request.url)
        elif not text:
            flash("Please provide text input or upload a file.")
            return redirect(request.url)

        # Process the text
        result = process_text(text)

        # Convert result to HTML table if available
        if result is not None:
            table_html = result.to_html(classes='table table-striped', index=False)
        else:
            table_html = "<p>No results available.</p>"

        return render_template('index.html', table=table_html)

    return render_template('index.html')


@app.route('/download/<filename>')
def download_file(filename):
    """
    Serve a file download request.

    This function checks if a requested file exists in the configured download folder.
    If the file exists, it is sent as an attachment for download.
    If the file does not exist, the user is redirected to the index page with an error message.

    Parameters:
    filename (str): The name of the file requested for download.

    Returns:
    If the file is found: A file download response.
    If the file is not found: Redirects to the index page with a flash error message.
    """
    path = os.path.join(app.config['DOWNLOAD_FOLDER'], filename)
    if os.path.exists(path):
        return send_file(path, as_attachment=True)
    else:
        flash("File not found.")
        return redirect(url_for('index'))


if __name__ == "__main__":
    app.run(debug=True)
