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
    if not client:
        return ["Erro ao inicializar o cliente de IA. Por favor, tente novamente mais tarde."]
        
    try:
        prompt = (
            f"Você é um assistente que leu um documento. "
            f"Com base no conteúdo, sugira 3 objetivos possíveis que uma pessoa poderia ter ao ler este documento.\n\n"
            f"Documento:\n{texto[:8000]}"
        )

        response = client.chat.completions.create(
            model="sabia-3",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=1000,
        )

        resposta = response.choices[0].message.content
        sugestoes = [linha.strip("-• \n") for linha in resposta.split("\n") if linha.strip()]
        return sugestoes[:3]  # Retorna apenas as 3 primeiras sugestões
    except Exception as e:
        print(f"Error generating suggestions: {e}")
        return ["Desculpe, ocorreu um erro ao gerar as sugestões. Por favor, tente novamente."]