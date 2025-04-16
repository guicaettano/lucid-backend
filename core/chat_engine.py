import openai
import os
from dotenv import load_dotenv
import httpx
from collections import deque

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

historico_conversa = deque(maxlen=10)
def responder_com_maritaca(texto, objetivo, pergunta):
    if not client:
        return "Erro ao inicializar o cliente de IA. Por favor, tente novamente mais tarde."
        
    try:
        prompt = (
            f"Você é um assistente que leu um documento com o seguinte objetivo: '{objetivo}'.\n"
            f"Com base no documento e no objetivo, responda à seguinte pergunta de forma clara e concisa:\n\n"
            f"Documento:\n{texto[:8000]}\n\n"
            f"Pergunta: {pergunta}"
        )

        response = client.chat.completions.create(
            model="sabia-3",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=1000,
        )

        return response.choices[0].message.content
    except Exception as e:
        print(f"Error generating response: {e}")
        return "Desculpe, ocorreu um erro ao gerar a resposta. Por favor, tente novamente."

if __name__ == "__main__":
    texto_teste = "Este é um relatório contendo dados de desempenho trimestral, indicadores de vendas e análise de mercado."
    print(responder_com_maritaca(texto_teste, "Resumir os principais pontos."))