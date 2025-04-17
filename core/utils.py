from PyPDF2 import PdfReader
from docx import Document
from PIL import Image
import io
import re
from core.detc_obj import extract_text_easyocr
import openai
import os
from dotenv import load_dotenv
import httpx

load_dotenv()

try:
    client = openai.OpenAI(
        api_key=os.getenv("MARITACA_API_KEY", "109232856114214290025_3dedd8dadabfe8df"),
        base_url=os.getenv("MARITACA_BASE_URL", "https://chat.maritaca.ai/api"),
        http_client=httpx.Client(timeout=30.0)
    )
except Exception as e:
    print(f"Error initializing OpenAI client: {e}")
    client = None


def process_file(uploaded_file):
    file_type = uploaded_file.type

    if file_type == "application/pdf":
        reader = PdfReader(uploaded_file)
        text = "\n".join([page.extract_text() or "" for page in reader.pages])
        return text

    elif file_type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
        doc = Document(uploaded_file)
        return "\n".join([para.text for para in doc.paragraphs])

    elif file_type.startswith("image/"):
        return extract_text_easyocr(uploaded_file.getvalue())

    elif file_type == "text/plain":
        stringio = io.StringIO(uploaded_file.getvalue().decode("utf-8"))
        return stringio.read()

    else:
        return "Formato de arquivo não suportado."


def detect_doc_type(text):
    text = text.lower()

    # Simples heurística de detecção por palavras-chave
    if "contrato" in text or "cláusula" in text:
        return "Contrato", "Analisar riscos e obrigações legais"
    elif "resumo" in text or "pesquisa" in text:
        return "Artigo científico ou acadêmico", "Resumir para apresentação ou estudo"
    elif "faturamento" in text or "kpi" in text:
        return "Relatório empresarial", "Extrair insights para decisão de negócios"
    elif "aluno" in text or "ensino" in text:
        return "Material educacional", "Simplificar para fins didáticos"
    else:
        return "Desconhecido", None


def feedback_suggestion(doc_type):
    feedback_questions = {
        "Contrato": "Este documento parece ser um contrato. Você confirmaria isso?",
        "Artigo científico ou acadêmico": "Este documento parece ser um artigo científico ou acadêmico. Está correto?",
        "Relatório empresarial": "Este parece ser um relatório de negócios. Você confirmaria isso?",
        "Material educacional": "Este documento parece ser material educacional. Você confirmaria isso?",
    }

    return feedback_questions.get(doc_type, "Este documento não foi identificado corretamente. Você gostaria de fornecer mais detalhes?")


def sugerir_objetivo(texto):
    # Analisa o texto para gerar sugestões mais relevantes
    doc_type, _ = detect_doc_type(texto)
    
    if doc_type == "Contrato":
        return [
            "Analisar cláusulas principais",
            "Identificar obrigações e direitos",
            "Extrair pontos críticos"
        ]
    elif doc_type == "Artigo científico ou acadêmico":
        return [
            "Resumir metodologia e resultados",
            "Extrair conclusões principais",
            "Identificar contribuições"
        ]
    elif doc_type == "Relatório empresarial":
        return [
            "Analisar indicadores de desempenho",
            "Extrair insights estratégicos",
            "Identificar tendências"
        ]
    elif doc_type == "Material educacional":
        return [
            "Simplificar conceitos principais",
            "Extrair pontos de aprendizado",
            "Gerar exercícios práticos"
        ]
    else:
        # Sugestões genéricas para documentos não identificados
        return [
            "Resumir o conteúdo principal",
            "Extrair pontos-chave",
            "Gerar perguntas frequentes"
        ]