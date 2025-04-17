import openai
import os
from dotenv import load_dotenv
import httpx

load_dotenv()

try:
    client = openai.OpenAI(
        api_key=os.getenv("MARITACA_API_KEY", "109232856114214290025_3dedd8dadabfe8df"),
        base_url=os.getenv("MARITACA_BASE_URL", "https://chat.maritaca.ai/api"),
        http_client=httpx.Client(timeout=30.0),
    )
except Exception as e:
    print(f"Error initializing OpenAI client: {e}")
    client = None


def gerar_faq(texto, objetivo):
    if not client:
        return [
            "Erro ao inicializar o cliente de IA. Por favor, tente novamente mais tarde."
        ]

    try:
        prompt = (
            f"Você é um assistente que leu um documento com o seguinte objetivo: '{objetivo}'.\n"
            f"Crie de 3 a 4 perguntas relevantes que uma pessoa faria ao tentar entender o conteúdo do documento com esse objetivo.\n\n"
            f"Documento:\n{texto[:8000]}"
        )

        response = client.chat.completions.create(
            model="sabia-3",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=1000,
        )

        resposta = response.choices[0].message.content

        # Separar por linha ou ponto de interrogação
        faqs = [linha.strip("-• \n") for linha in resposta.split("\n") if linha.strip()]
        return faqs
    except Exception as e:
        print(f"Error generating FAQ: {e}")
        return [
            "Desculpe, ocorreu um erro ao gerar as perguntas frequentes. Por favor, tente novamente."
        ]
