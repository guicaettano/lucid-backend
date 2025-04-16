import openai

client = openai.OpenAI(
    api_key="109232856114214290025_3dedd8dadabfe8df", 
    base_url="https://chat.maritaca.ai/api",
)

def gerar_faq(texto, objetivo):
    prompt = (
        f"Você é um assistente que leu um documento com o seguinte objetivo: '{objetivo}'.\n"
        f"Crie de 3 a 5 perguntas relevantes que uma pessoa faria ao tentar entender o conteúdo do documento com esse objetivo.\n\n"
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
