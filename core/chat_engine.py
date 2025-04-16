import openai
from collections import deque

client = openai.OpenAI(
    api_key="109232856114214290025_3dedd8dadabfe8df", 
    base_url="https://chat.maritaca.ai/api",
)

historico_conversa = deque(maxlen=10)
def responder_com_maritaca(texto, objetivo, pergunta_usuario):
    prompt_base = (
        f"Você é um assistente inteligente. O objetivo do usuário é: '{objetivo}'. "
        f"Com base no documento abaixo, responda à pergunta de forma clara e completa.\n\n"
        f"Documento:\n{texto}\n\n"
        f"Pergunta: {pergunta_usuario}"
    )

    historico_conversa.append({"role": "user", "content": pergunta_usuario})

    mensagens = [{"role": "user", "content": prompt_base}]
    for mensagem in historico_conversa:
        mensagens.append(mensagem)

    texto_truncado = texto[:12000]

    response = client.chat.completions.create(
        model="sabia-3",
        messages=mensagens,
        max_tokens=8000
    )
    return response.choices[0].message.content

if __name__ == "__main__":
    texto_teste = "Este é um relatório contendo dados de desempenho trimestral, indicadores de vendas e análise de mercado."
    print(responder_com_maritaca(texto_teste, "Resumir os principais pontos."))