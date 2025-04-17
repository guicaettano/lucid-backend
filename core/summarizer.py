import openai
import os
from dotenv import load_dotenv
import httpx

load_dotenv()

try:
    client = openai.OpenAI(
        api_key=os.getenv("MARITACA_API_KEY"),
        base_url=os.getenv("MARITACA_BASE_URL"),
        http_client=httpx.Client(timeout=30.0),
    )
except Exception as e:
    print(f"Error initializing OpenAI client: {e}")
    client = None


def resumir_texto(texto, objetivo):
    if not client:
        return "Erro ao inicializar o cliente de IA. Por favor, tente novamente mais tarde."

    try:
        prompt = (
            f"Você é um assistente que leu um documento com o seguinte objetivo: '{objetivo}'.\n"
            f"Por favor, crie um resumo conciso e relevante do documento, focando nas informações mais importantes para atingir esse objetivo.\n\n"
            f"Documento:\n{texto[:8000]}"
        )

        response = client.chat.completions.create(
            model="sabia-3",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=1000,
        )

        return response.choices[0].message.content
    except Exception as e:
        print(f"Error generating summary: {e}")
        return (
            "Desculpe, ocorreu um erro ao gerar o resumo. Por favor, tente novamente."
        )


if __name__ == "__main__":
    texto_teste = "Este é um relatório contendo dados de desempenho trimestral, indicadores de vendas e análise de mercado."
    print(resumir_texto(texto_teste, "Resumir os principais pontos."))
