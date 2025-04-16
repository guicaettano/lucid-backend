import openai
import os
from dotenv import load_dotenv

load_dotenv()

client = openai.OpenAI(
    api_key=os.getenv("MARITACA_API_KEY", "109232856114214290025_3dedd8dadabfe8df"),
    base_url=os.getenv("MARITACA_BASE_URL", "https://chat.maritaca.ai/api"),
)

def gerar_faq(texto, objetivo):
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
