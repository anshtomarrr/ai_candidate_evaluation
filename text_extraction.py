import PyPDF2
from pdfminer.high_level import extract_text as pdfminer_extract_text
from docx import Document


def extract_text_from_pdf(file_path):
    """
    Extract text from a PDF file using PyPDF2 and pdfminer.
    """
    try:
        # Try PyPDF2 first
        with open(file_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            text = ''
            for page in reader.pages:
                text += page.extract_text()
            if text.strip():
                return text
    except Exception as e:
        print(f"PyPDF2 extraction failed: {e}")

    try:
        # Fallback to pdfminer
        text = pdfminer_extract_text(file_path)
        return text
    except Exception as e:
        print(f"pdfminer extraction failed: {e}")
        return ""


def extract_text_from_docx(file_path):
    """
    Extract text from a DOCX file using python-docx.
    """
    try:
        doc = Document(file_path)
        text = '\n'.join([paragraph.text for paragraph in doc.paragraphs])
        return text
    except Exception as e:
        print(f"DOCX extraction failed: {e}")
        return "" 