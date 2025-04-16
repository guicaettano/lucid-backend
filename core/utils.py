from PyPDF2 import PdfReader
from docx import Document
from PIL import Image
import io
import re
from core.detc_obj import extract_text_easyocr
import openai

client = openai.OpenAI(
    api_key="109232856114214290025_3dedd8dadabfe8df", 
    base_url="https://chat.maritaca.ai/api",
)


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
    """Sugere objetivos com base em análise de IA do conteúdo do documento."""
    prompt = (
        f"Analise o seguinte documento e sugira 3 objetivos específicos e relevantes para trabalhar com este conteúdo. "
        f"Os objetivos devem ser práticos e focados em extrair valor do documento. "
        f"Retorne apenas os objetivos, um por linha, sem numeração ou formatação adicional.\n\n"
        f"Documento:\n{texto[:8000]}"
    )

    response = client.chat.completions.create(
        model="sabia-3",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=500,
    )
    
    # Processar a resposta para extrair as sugestões
    sugestoes = [s.strip() for s in response.choices[0].message.content.split("\n") if s.strip()]
    
    # Garantir que temos pelo menos 3 sugestões
    while len(sugestoes) < 3:
        sugestoes.append("Resumir conteúdo principal")
    
    return sugestoes[:3]  # Retornar apenas as 3 primeiras sugestões