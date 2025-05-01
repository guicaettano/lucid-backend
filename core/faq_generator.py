import os
from dotenv import load_dotenv
from together import Together

load_dotenv()

try:
    client = Together(api_key=os.getenv("TOGETHER_API_KEY", "tgp_v1_27_E4RHmsTzYm2Iz7Cvp8ZYWD3IRcnCMLlt9GML27Vs"))
except Exception as e:
    print(f"Error initializing Together client: {e}")
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
            model="meta-llama/Llama-4-Maverick-17B-128E-Instruct-FP8",
            messages=[{"role": "user", "content": prompt}]
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