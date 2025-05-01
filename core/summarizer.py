import os
from dotenv import load_dotenv
# Make sure you have the latest version of the Together SDK
# pip install --upgrade together

# Import the Together client
from together import Together

load_dotenv()
# Set API key through environment variable
API_KEY = "bd403cf4cea85ed2304bb0e62881379af0fa2aba31b48947d02c86951d86a32c"
os.environ["TOGETHER_API_KEY"] = API_KEY

# Initialize client
client = Together()

def resumir_texto(texto, objetivo):
    if not client:
        return "Erro ao inicializar o cliente de IA. Por favor, tente novamente mais tarde."

    try:
        # Create a message following OpenAI-style format as recommended by Together
        prompt = (
            f"Você é um assistente que leu um documento com o seguinte objetivo: '{objetivo}'.\n"
            f"Por favor, crie um resumo conciso e relevante do documento, focando nas informações mais importantes para atingir esse objetivo.\n\n"
            f"Documento:\n{texto[:8000]}"
        )
        
        # Use the chat completions API as documented
        response = client.chat.completions.create(
            model="meta-llama/Llama-4-Maverick-17B-128E-Instruct-FP8",
            messages=[{"role": "user", "content": prompt}]
        )
        
        # Extract response content
        return response.choices[0].message.content
        
    except Exception as e:
        import traceback
        traceback.print_exc()
        return f"Desculpe, ocorreu um erro ao gerar o resumo: {e}"

if __name__ == "__main__":
    texto_teste = "Este é um relatório contendo dados de desempenho trimestral, indicadores de vendas e análise de mercado."
    print(resumir_texto(texto_teste, "Resumir os principais pontos."))