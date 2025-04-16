import PyPDF2
import docx
from PIL import Image
import re
from core.detc_obj import extract_text_easyocr

def process_file(uploaded_file):
    """Process different file types and extract text content."""
    file_type = uploaded_file.name.split('.')[-1].lower()
    
    if file_type == 'pdf':
        return process_pdf(uploaded_file)
    elif file_type == 'docx':
        return process_docx(uploaded_file)
    elif file_type in ['txt']:
        return uploaded_file.getvalue().decode('utf-8')
    elif file_type in ['png', 'jpg', 'jpeg']:
        return extract_text_easyocr(uploaded_file.getvalue())
    else:
        return "Unsupported file type"

def process_pdf(file):
    """Extract text from PDF file."""
    pdf_reader = PyPDF2.PdfReader(file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text

def process_docx(file):
    """Extract text from DOCX file."""
    doc = docx.Document(file)
    return "\n".join([paragraph.text for paragraph in doc.paragraphs])

def detect_doc_type(text):
    """Detect document type based on content patterns."""
    text = text.lower()
    
    # Simple pattern matching for demonstration
    if re.search(r'contrato|termo|cláusula', text):
        return "Contrato", "Analisar cláusulas e termos importantes"
    elif re.search(r'nota fiscal|nf|nfe', text):
        return "Nota Fiscal", "Extrair dados fiscais e valores"
    elif re.search(r'relatório|análise|conclusão', text):
        return "Relatório", "Sintetizar informações principais"
    else:
        return "Documento", None 