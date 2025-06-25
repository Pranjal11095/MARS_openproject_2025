# MARS_openproject_2025-Automated Metadata Generation System

This project is a Flask-based web application designed to automatically generate structured metadata from unstructured documents. Built for simplicity and compatibility, it supports `.pdf`, `.docx`, `.txt`, and common image formats like `.jpg` and `.png`, with integrated OCR for scanned documents. The system runs seamlessly in **Google Colab** using `flask-ngrok`, making it ideal for quick demos and public access.

---

##  Project Overview

With the rapid growth of unstructured data, metadata generation is essential for digital archiving, search, and classification. MARS_openproject_2025 automates this process by extracting and analyzing content from various document types and returning metadata in clean, structured JSON format.

---

##  Features

- **Automated Metadata Extraction**  
  Extracts metadata fields: title, word count, keywords, summary, language, file type, and creation time.

- **Multi-format File Support**  
  Accepts `.pdf`, `.docx`, `.txt`, `.png`, and `.jpg`. Performs OCR on image-based content.

- **Semantic Analysis**  
  Identifies key terms and generates concise summaries using lightweight text processing.

- **JSON Output**  
  Clean metadata output stored as `.json` for further processing or storage.

- **Web Interface**  
  Simple, pastel-themed HTML upload form powered by Flask and Bootstrap.

- **Colab-Compatible**  
  Fully operational in Google Colab using `flask-ngrok` for live, shareable links.


---

##  Folder Structure
metadata_generator/

├── outputs/

│   └── TheoryOfComputation.pdf_metadata.json   ← Sample metadata output

├── static/

│   └── style.css                               ← Custom styling for UI

├── templates/

│   └── index.html                              ← Upload form with pastel design

├── main.py                                     ← Flask backend (local run)

├── Marsproject.ipynb                           ← Executable Colab notebook

├── README.md                                   ← Project documentation

├── TheoryOfComputation.pdf                     ← Sample input document



##  How to Run (Google Colab )

1. Open `Marsproject.ipynb` in [Google Colab]
2. Run all cells sequentially.
3. A public `ngrok` URL will be displayed in the output.
4. Upload a supported document using the form.
5. View or download the generated metadata (`.json` file).

 ## Optional: Local Setup



git clone https://github.com/yourusername/MARS_2025.git

cd metadata_generator

pip install -r requirements.txt

python main.py

Then visit http://localhost:5000 in your browser.


## Sample metadata output

    "title": "Introduction to Theory of Computation Anil Maheshwari Michiel Smid School of Computer Science Carlet",
    "keywords": [
        "language",
        "string",
        "state",
        "regular",
        "turing"
    ],
    "summary": "Introduction to Theory of Computation Anil Maheshwari Michiel Smid School of Computer Science Carleton University Ottawa Canada {anil,michiel}@scs.carleton.ca August 29, 2024 ii Contents Contents Preface vi 1 Introduction 1 1.1 Purpose and motivation . . . . . . . . . . . . . . . . . . . . . 1 1.1.1 Complexity theory . . . . . . . . . . . . . . . . . . . . 2 1.1.2 Computability theory . . . . . . . . . . . . . . . . . ....",
    "language": "en",
    "filename": "TheoryOfComputation.pdf",
    "word_count": 70463,
    "created_time": "Wed Jun 25 21:25:42 2025",
    "file_type": "application/pdf"
## Deliverables
Marsproject.ipynb – Google Colab executable notebook

main.py – Local Flask server script

index.html, style.css – Web interface

TheoryOfComputation.pdf – Sample input document

TheoryOfComputation.pdf_metadata.json – Sample output

demo.mp4 – Demo video

README.md – Project documentation   
