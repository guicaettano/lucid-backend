import os
from dotenv import load_dotenv
from together import Together

load_dotenv()

try:
    client = Together(api_key=os.getenv("TOGETHER_API_KEY", "tgp_v1_27_E4RHmsTzYm2Iz7Cvp8ZYWD3IRcnCMLlt9GML27Vs"))
except Exception as e:
    print(f"Error initializing Together client: {e}")
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
            model="meta-llama/Llama-4-Maverick-17B-128E-Instruct-FP8",
            messages=[{"role": "user", "content": prompt}]
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