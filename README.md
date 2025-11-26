# OCR-Searchable-PDF-Tool
Convert Any PDF Into a Fully Searchable, Highlightable and Selectable Text PDF — **100% Free & Offline**

[![Download EXE](https://img.shields.io/github/v/release/sunilprajapati832/OCR-Searchable-PDF-Tool?style=for-the-badge)](https://github.com/sunilprajapati832/OCR-Searchable-PDF-Tool/releases)

## Overview
OCR-Searchable-PDF-Tool is a powerful desktop application that converts non-searchable image-based PDFs into full searchable PDFs using Tesseract OCR — packed inside a sleek GUI & shareable as a Windows .exe.
This tool works completely offline, costs zero and produces highly accurate OCR text embedded into your original PDF.
<br>
link: https://github.com/sunilprajapati832/OCR-Searchable-PDF-Tool/releases/tag/v1.0.0/pdf_ocr_gui.exe 

## Inspiration Behind This Project
A real incident created this idea:

**“Someone gave me a PDF and asked me to search a name inside it.
But the PDF was made from images of a Word file — so Ctrl+F didn’t work.
I tried many tools online, but most were paid or added watermarks.
At that moment, I decided to build my own OCR software — free, accurate, and easy for everyone.
Now I’m sharing it publicly as a .exe tool so no one faces the problem I faced.”**

This mindset led to the creation of OCR-Searchable-PDF-Tool — a professional Python + Tesseract project that helps thousands of users convert any PDF into a searchable format.

## Features
- **Drag & Drop PDF**: Easily drop your PDF into the window.
- **Fast & Accurate OCR**: Uses Tesseract 5 OCR with optimized settings (--oem 3 --psm 1).
- **Searchable Output**: You get a perfectly searchable, highlightable, copy-able PDF.
- **Image + Text Layer**: 
- Final PDF contains:
  * your original high-quality image
  * hidden text layer for searchability
- **Progress Bar + Time Estimate**: Track progress page-by-page.
- **Auto-close After Completion**: After success, it opens folder → shows success → closes automatically.
- **Standalone Windows EXE**: No Python required. Just download & run.

## Tech Stack
| Component          | Purpose             |
| ------------------ | ------------------- |
| **Python 3.10+**   | Core logic          |
| **Tkinter**        | GUI                 |
| **TkinterDnD2**    | Drag & Drop support |
| **PyMuPDF (fitz)** | PDF handling        |
| **Pillow (PIL)**   | Image compression   |
| **Tesseract OCR**  | Text extraction     |
| **PyInstaller**    | EXE packaging       |

## Installation (For Developers)
**1. Clone the repository** <br>
git clone https://github.com/sunilprajapati832/OCR-Searchable-PDF-Tool.git <br>
cd OCR-Searchable-PDF-Tool <br>

**2. Install dependencies** <br>
pip install -r requirements.txt <br>

**3. Install Tesseract OCR** <br>
Download Windows installer: https://github.com/UB-Mannheim/tesseract/wiki <br>
Then set the path in code: TESSERACT_PATH = r"C:\Program Files\Tesseract-OCR\tesseract.exe" <br>

## How to Use the Software (For Users)
* **Method — Direct EXE**
  * Download OCR-Searchable-PDF-Tool.exe from GitHub Releases
  * Double-click to open
  * Drag your PDF
  * Click Start OCR
  * Done — your searchable PDF appears in the same folder

## Project Structure 
OCR-Searchable-PDF-Tool/
│
├── pdf_ocr_gui.py
├── requirements.txt
├── tesseract
├── build_instructions.txt
└── README.md

## Screenshots
<p align="center">
  <img src="AppScreenshot/SearchablePDFToolImage1.png" alt="App Screenshot 1" width="45%"/>
  &nbsp;&nbsp;&nbsp;
  <img src="AppScreenshot/SearchablePDFToolImage2.png" alt="App Screenshot 2" width="45%"/>
</p>







