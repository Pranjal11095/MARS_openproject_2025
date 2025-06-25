import os
import re
import fitz
import pytesseract
from pdf2image import convert_from_path
from docx import Document
from langdetect import detect
from collections import Counter
import json
import mimetypes
import time

# ========== Text Extraction ==========
def extract_text(path):
    ext = os.path.splitext(path)[-1].lower()
    if ext == ".pdf": return extract_text_from_pdf(path)
    elif ext == ".docx": return extract_text_from_docx(path)
    elif ext == ".txt": return extract_text_from_txt(path)
    else: raise ValueError("Unsupported file format")

def extract_text_from_pdf(path):
    doc = fitz.open(path)
    text = ""
    for page in doc:
        t = page.get_text()
        if not t.strip(): t = ocr_pdf_page(path, page.number + 1)
        text += t + "\n"
    return text

def ocr_pdf_page(path, page_num):
    images = convert_from_path(path, first_page=page_num, last_page=page_num)
    return pytesseract.image_to_string(images[0])

def extract_text_from_docx(path):
    return "\n".join([p.text for p in Document(path).paragraphs])

def extract_text_from_txt(path):
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()

# ========== Metadata Generation ==========
def preprocess_text(text):
    return re.sub(r"\s+", " ", text).strip()

def extract_title(text):
    lines = text.split('\n')
    clean_lines = [line.strip() for line in lines if line.strip()]
    title = clean_lines[0] if clean_lines else "Untitled"
    return title

def extract_keywords(text, num=5):
    words = re.findall(r'\b[a-zA-Z]{5,}\b', text.lower())
    common = Counter(words).most_common(num)
    return [w for w, _ in common]

def summarize_text(text):
    return " ".join(text.split()[:100]) + "..." if len(text.split()) > 100 else text

def detect_language(text):
    try: return detect(text)
    except: return "unknown"

def generate_metadata(text, filename):
    clean = preprocess_text(text)
    stat_info = os.stat(filename)
    return {
        "title": extract_title(clean)[:100],
        "keywords": extract_keywords(clean),
        "summary": summarize_text(clean),
        "language": detect_language(clean),
        "filename": os.path.basename(filename),
        "word_count": len(clean.split()),
        "created_time": time.ctime(stat_info.st_ctime),
        "file_type": mimetypes.guess_type(filename)[0] or "unknown"
    }

# ========== VS Code Flask UI ==========
if __name__ == "__main__":
    from flask import Flask, request, render_template, jsonify, send_file
    from werkzeug.utils import secure_filename

    app = Flask(__name__)
    app.config['UPLOAD_FOLDER'] = "uploads"
    app.config['OUTPUT_FOLDER'] = "outputs"
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    os.makedirs(app.config['OUTPUT_FOLDER'], exist_ok=True)

    @app.route('/', methods=['GET'])
    def home():
        return render_template('index.html')

    @app.route('/', methods=['POST'])
    def upload_file():
        file = request.files['file']
        if file:
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)

            ext = filename.lower().split('.')[-1]
            if ext == 'pdf':
                text = extract_text_from_pdf(file_path)
            elif ext == 'docx':
                text = extract_text_from_docx(file_path)
            elif ext == 'txt':
                text = extract_text_from_txt(file_path)
            else:
                return "Unsupported file type."

            metadata = generate_metadata(text, file_path)
            save_metadata(filename, metadata)
            return jsonify(metadata)

    def save_metadata(filename, metadata):
        output_path = os.path.join(app.config['OUTPUT_FOLDER'], filename + '_metadata.json')
        with open(output_path, 'w', encoding='utf-8') as out_file:
            json.dump(metadata, out_file, indent=4)

    @app.route('/download/<filename>')
    def download_metadata(filename):
        filepath = os.path.join(app.config['OUTPUT_FOLDER'], filename + '_metadata.json')
        return send_file(filepath, as_attachment=True)

    app.run(debug=True)