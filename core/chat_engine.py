import openai
import os
from dotenv import load_dotenv
import httpx
from collections import deque
from typing import Dict, List, Any
from datetime import datetime

load_dotenv()

try:
    client = openai.OpenAI(
        api_key=os.getenv("MARITACA_API_KEY", "109232856114214290025_3dedd8dadabfe8df"),
        base_url=os.getenv("MARITACA_BASE_URL", "https://chat.maritaca.ai/api"),
        http_client=httpx.Client(timeout=30.0)
    )
except Exception as e:
    print(f"Error initializing OpenAI client: {e}")
    client = None

# Variável global para armazenar o documento atual
current_document = None

# Dicionário para armazenar históricos de conversas por documento
chat_memories: Dict[str, List[Dict[str, Any]]] = {}

def add_to_history(document_key: str, role: str, content: str):
    """
    Adiciona uma mensagem ao histórico de conversas de um documento específico
    """
    if document_key not in chat_memories:
        chat_memories[document_key] = []
        
    chat_memories[document_key].append({
        "role": role,
        "content": content,
        "timestamp": datetime.now().isoformat()
    })
    
    # Limitar tamanho do histórico para controlar uso de tokens
    if len(chat_memories[document_key]) > 10:  # Mantém as últimas 10 mensagens
        chat_memories[document_key].pop(0)

def get_document_key(texto, objetivo):
    """
    Gera uma chave única para o documento baseado no seu conteúdo e objetivo
    """
    # Versão simplificada: usa os primeiros caracteres do texto e o objetivo
    texto_key = texto[:100] if texto else ""
    return f"{texto_key}_{objetivo}"

def format_messages_with_context(texto: str, objetivo: str, pergunta: str):
    """
    Formata as mensagens para a API do OpenAI/Maritaca incluindo contexto e histórico
    """
    # Obtém a chave do documento
    document_key = get_document_key(texto, objetivo)
    
    # Mensagem de sistema que define o contexto
    system_message = {
        "role": "system", 
        "content": f"Você é um assistente que analisou um documento com o seguinte objetivo: '{objetivo}'. "\
                  f"O conteúdo do documento é o seguinte:\n\n{texto[:6000]}...\n\n"\
                  f"Responda às perguntas com base apenas neste documento e no histórico da conversa."
    }
    
    messages = [system_message]
    
    # Adiciona histórico de conversa, se houver
    if document_key in chat_memories and chat_memories[document_key]:
        for msg in chat_memories[document_key]:
            messages.append({"role": msg["role"], "content": msg["content"]})
    
    # Adiciona a pergunta atual
    messages.append({"role": "user", "content": pergunta})
    
    return messages, document_key

def responder_com_maritaca(texto, objetivo, pergunta):
    """
    Responde a perguntas usando contexto do documento e histórico de conversa
    Mantém a assinatura original da função para compatibilidade
    """
    if not client:
        return "Erro ao inicializar o cliente de IA. Por favor, tente novamente mais tarde."
    
    try:
        # Formata mensagens com contexto e histórico
        messages, document_key = format_messages_with_context(texto, objetivo, pergunta)
        
        # Faz chamada à API
        response = client.chat.completions.create(
            model="sabia-3",
            messages=messages,
            max_tokens=1000,
        )
        
        resposta = response.choices[0].message.content
        
        # Adiciona pergunta e resposta ao histórico
        add_to_history(document_key, "user", pergunta)
        add_to_history(document_key, "assistant", resposta)
        
        return resposta
        
    except Exception as e:
        print(f"Error generating response: {e}")
        return "Desculpe, ocorreu um erro ao gerar a resposta. Por favor, tente novamente."

def limpar_historico_chat():
    """Limpa todo o histórico de chat"""
    chat_memories.clear()

if __name__ == "__main__":
    texto_teste = "Este é um relatório contendo dados de desempenho trimestral, indicadores de vendas e análise de mercado."
    print(responder_com_maritaca(texto_teste, "Resumir os principais pontos.", "Qual foi o desempenho de vendas?"))