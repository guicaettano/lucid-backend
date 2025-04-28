import openai
import os
from dotenv import load_dotenv
import httpx
from collections import deque

load_dotenv()

try:
    client = openai.OpenAI(
        api_key=os.getenv("MARITACA_API_KEY"),
        base_url=os.getenv("MARITACA_BASE_URL", "https://chat.maritaca.ai/api"),
        http_client=httpx.Client(timeout=30.0),
    )
except Exception as e:
    print(f"Error initializing OpenAI client: {e}")
    client = None

# Dicionário para armazenar históricos para diferentes documentos
# Chave: hash do documento, Valor: histórico de conversa
doc_historicos = {}


def responder_com_maritaca(texto, objetivo, pergunta, session_id=None):
    if not client:
        return "Erro ao inicializar o cliente de IA. Por favor, tente novamente mais tarde."

    try:
        # Usar o session_id fornecido ou criar um baseado no texto e objetivo
        doc_id = session_id if session_id else hash(texto[:500] + objetivo)

        # Inicializar histórico para este documento se não existir
        if doc_id not in doc_historicos:
            doc_historicos[doc_id] = deque(maxlen=10)

        # Obter o histórico para este documento
        historico_conversa = doc_historicos[doc_id]

        # Formar o histórico formatado para o contexto
        historico_texto = ""
        if historico_conversa:
            historico_texto = "Histórico de conversa:\n"
            for item in historico_conversa:
                historico_texto += f"Pergunta: {item['pergunta']}\n"
                historico_texto += f"Resposta: {item['resposta']}\n\n"

        # Construir o prompt com contexto e histórico
        prompt = (
            f"Você é um assistente que leu um documento com o seguinte objetivo: '{objetivo}'.\n"
            f"Com base no documento, objetivo e histórico da conversa, responda de forma clara e detalhada:\n\n"
            f"Documento:\n{texto[:6000]}\n\n"
            f"{historico_texto}\n"
            f"Pergunta atual: {pergunta}"
        )

        response = client.chat.completions.create(
            model="sabia-3",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=1000,
        )

        resposta = response.choices[0].message.content

        # Adicionar ao histórico
        historico_conversa.append({"pergunta": pergunta, "resposta": resposta})

        return resposta
    except Exception as e:
        print(f"Error generating response: {e}")
        return (
            "Desculpe, ocorreu um erro ao gerar a resposta. Por favor, tente novamente."
        )


if __name__ == "__main__":
    texto_teste = "Este é um relatório contendo dados de desempenho trimestral, indicadores de vendas e análise de mercado."
    print(
        responder_com_maritaca(
            texto_teste,
            "Resumir os principais pontos.",
            "Qual foi o desempenho de vendas?",
        )
    )
