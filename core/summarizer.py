import openai

client = openai.OpenAI(
    api_key="109232856114214290025_3dedd8dadabfe8df",  
    base_url="https://chat.maritaca.ai/api",
)

def resumir_texto(texto, objetivo):
    prompt = (
        f"Você é um assistente inteligente. Seu objetivo é: '{objetivo}'.\n\n"
        f"Com base no documento abaixo, gere um resumo claro, conciso e útil, focado nesse objetivo.\n\n"
        f"Documento:\n{texto[:8000]}"
    )

    response = client.chat.completions.create(
        model="sabia-3",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=1000,
    )
    
    return response.choices[0].message.content


if __name__ == "__main__":
    texto_teste = "Este é um relatório contendo dados de desempenho trimestral, indicadores de vendas e análise de mercado."
    print(resumir_texto(texto_teste, "Resumir os principais pontos."))