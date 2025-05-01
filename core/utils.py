from PyPDF2 import PdfReader
from docx import Document
import io
from core.detc_obj import extract_text_easyocr

from dotenv import load_dotenv
from together import Together

load_dotenv()

api_key="bd403cf4cea85ed2304bb0e62881379af0fa2aba31b48947d02c86951d86a32c"

client = Together(api_key=api_key)


def process_file(uploaded_file):
    file_type = uploaded_file.type

    if file_type == "application/pdf":
        reader = PdfReader(uploaded_file)
        text = "\n".join([page.extract_text() or "" for page in reader.pages])
        return text

    elif (
        file_type
        == "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    ):
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

    return feedback_questions.get(
        doc_type,
        "Este documento não foi identificado corretamente. Você gostaria de fornecer mais detalhes?",
    )


def sugerir_objetivo(texto):
    # Sugestões simples e diretas que funcionam bem com o click
    return [
        "Resumir o conteúdo principal",
        "Extrair pontos-chave",
        "Gerar perguntas frequentes",
    ]