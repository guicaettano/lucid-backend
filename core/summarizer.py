import os
from dotenv import load_dotenv
from together import Together

load_dotenv()
os.environ["TOGETHER_API_KEY"] = "bd403cf4cea85ed2304bb0e62881379af0fa2aba31b48947d02c86951d86a32c"

# Initialize the Together client
client = Together(api_key=os.environ["TOGETHER_API_KEY"])

def resumir_texto(texto, objetivo):
    if not client:
        return "Erro ao inicializar o cliente de IA. Por favor, tente novamente mais tarde."

    try:
        prompt = (
            f"Você é um assistente que leu um documento com o seguinte objetivo: '{objetivo}'.\n"
            f"Por favor, crie um resumo conciso e relevante do documento, focando nas informações mais importantes para atingir esse objetivo.\n\n"
            f"Documento:\n{texto[:8000]}"
        )

        # Using the correct API method based on Together AI's current SDK
        response = client.complete(
            model="meta-llama/Llama-4-Maverick-17B-128E-Instruct-FP8",
            prompt=prompt,
            temperature=0.7,
        )
        
        # Extract the generated text from the response
        return response["output"]["choices"][0]["text"]
    except Exception as e:
        import traceback
        traceback.print_exc()
        return (
            f"Desculpe, ocorreu um erro ao gerar o resumo: {e}"
        )

if __name__ == "__main__":
    texto_teste = "Este é um relatório contendo dados de desempenho trimestral, indicadores de vendas e análise de mercado."
    print(resumir_texto(texto_teste, "Resumir os principais pontos."))