import streamlit as st
from utils import process_file
from core.faq_generator import gerar_faq
from core.summarizer import resumir_texto
from core.chat_engine import responder_com_maritaca

# from core.db import Documento, Session
from core.utils import sugerir_objetivo
import uuid
from PIL import Image
import logging

# Configure logger
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Configuração da página
st.set_page_config(page_title="Lucid", layout="centered")

# CSS para estilização
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600&family=Noto+Sans:wght@300;400;500;600&display=swap&text=abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789.,!@#$%^&*()');
    
    html, body, [class*="css"] {
        font-family: Inter, -apple-system, BlinkMacSystemFont, "Segoe UI", "Noto Sans", Helvetica, Arial, sans-serif;
        background-color: #ffffff;
        color: #000000;
        -webkit-font-smoothing: antialiased;
        -moz-osx-font-smoothing: grayscale;
        text-rendering: optimizeLegibility;
    }

    .hero-title {
        font-family: Inter, -apple-system, BlinkMacSystemFont, "Segoe UI", "Noto Sans", Helvetica, Arial, sans-serif;
        text-align: center;
        font-size: 4.5rem !important;
        font-weight: 300;
        letter-spacing: -0.03em;
        color: #1d1d1f;
    }

    .hero-subtitle {
        font-family: Inter, -apple-system, BlinkMacSystemFont, "Segoe UI", "Noto Sans", Helvetica, Arial, sans-serif;
        text-align: center;
        font-size: 1.5rem !important;
        font-weight: 300;
        letter-spacing: -0.02em;
        color: #1d1d1f;
        opacity: 0.9;
    }

    .hero-subtitle::after {
        content: '...';
        animation: loading 2s steps(4, end) infinite;
        display: inline-block;
        vertical-align: bottom;
        margin-left: 2px;
    }

    @keyframes loading {
        0% { content: ''; }
        25% { content: '.'; }
        50% { content: '..'; }
        75% { content: '...'; }
        100% { content: ''; }
    }

    .section-title {
        font-family: Inter, -apple-system, BlinkMacSystemFont, "Segoe UI", "Noto Sans", Helvetica, Arial, sans-serif;
        font-size: 1.6rem;
        font-weight: 500;
        margin-top: 2rem;
        margin-bottom: 1rem;
        color: #1d1d1f;
        text-align: center;
        animation: fadeIn 0.7s ease-in;
        letter-spacing: -0.02em;
    }

    .card {
        font-family: Inter, -apple-system, BlinkMacSystemFont, "Segoe UI", "Noto Sans", Helvetica, Arial, sans-serif;
        background: #ffffff;
        color: #1d1d1f;
        padding: 1.2rem;
        border-radius: 12px;
        margin-bottom: 1rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        animation: fadeIn 0.7s ease-in;
        line-height: 1.5;
        letter-spacing: -0.01em;
    }

    .option-card {
        background: #ffffff;
        color: #424245;
        padding: 2rem;
        border-radius: 10px;
        margin: 0.5rem;
        font-weight: 500;
        transition: transform 0.3s, box-shadow 0.3s;
        box-shadow: 0 2px 6px rgba(0,0,0,0.1);
        text-align: center;
        border: 2px solid #424245;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        height: 180px;
        cursor: pointer;
    }
    .option-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 6px 12px rgba(0,0,0,0.15);
        background-color: #f5f5f7;
    }
    .option-icon {
        font-size: 3rem;
        margin-bottom: 1rem;
        color: #424245;
    }
    .faq-box {
        display: inline-block;
        background: #424245;
        color: #fff;
        padding: 0.8rem 1.2rem;
        border-radius: 8px;
        margin: 0.5rem;
        cursor: pointer;
        font-weight: 500;
        transition: background 0.3s;
    }
    .faq-box:hover {
        background: #2d2d2f;
    }
    .footer {
        text-align: center;
        font-size: 0.9rem;
        color: #999;
        margin-top: 4rem;
    }
    .choice-title {
        font-family: Inter, -apple-system, BlinkMacSystemFont, "Segoe UI", "Noto Sans", Helvetica, Arial, sans-serif;
        font-size: 1.5rem !important;
        font-weight: 200;
        letter-spacing: -0.025em;
        color: #1d1d1f;
        text-align: center;
        margin-bottom: 2rem;
        opacity: 0.9;
    }
    .history-item {
        padding: 12px;
        border-bottom: 1px solid #f0f0f0;
        cursor: pointer;
        transition: background-color 0.2s;
    }
    .history-item:hover {
        background-color: #f7f9fc;
    }
    .history-timestamp {
        font-size: 0.8rem;
        color: #999;
        margin-top: 4px;
    }
    .history-objective {
        font-size: 0.9rem;
        color: #424245;
        margin-top: 4px;
    }
    .history-empty {
        padding: 30px 0;
        text-align: center;
        color: #999;
    }
    /* Esconder botão "Voltar ao início" quando estiver na seção de chat */
    #chat-section ~ div [data-testid="baseButton-secondary"]:has(div:contains("⬅️ Voltar ao início")) {
        display: none !important;
    }
    /* Esconder o botão em toda a seção após #chat-section */
    #chat-section ~ * [data-testid="baseButton-secondary"]:has(div:contains("⬅️")) {
        display: none !important;
    }
    /* Garantir que o botão não apareça em nenhum lugar após a seção de chat */
    .stButton > button:has(div:contains("⬅️")):has-ancestor(#chat-section ~ *) {
        display: none !important;
    }
    /* Estilo para texto de input */
    .stTextInput input, .stTextArea textarea {
        font-family: Inter, -apple-system, BlinkMacSystemFont, "Segoe UI", "Noto Sans", Helvetica, Arial, sans-serif !important;
        font-size: 1rem !important;
        letter-spacing: -0.01em !important;
    }
    /* Estilo para botões */
    .stButton button {
        font-family: Inter, -apple-system, BlinkMacSystemFont, "Segoe UI", "Noto Sans", Helvetica, Arial, sans-serif !important;
        font-weight: 500 !important;
        letter-spacing: -0.01em !important;
    }
    /* Estilo para texto do chat */
    .chat-message {
        font-family: Inter, -apple-system, BlinkMacSystemFont, "Segoe UI", "Noto Sans", Helvetica, Arial, sans-serif;
        line-height: 1.5;
        letter-spacing: -0.01em;
    }
    /* Estilo para placeholders */
    ::placeholder {
        font-family: Inter, -apple-system, BlinkMacSystemFont, "Segoe UI", "Noto Sans", Helvetica, Arial, sans-serif !important;
        font-weight: 300 !important;
        letter-spacing: -0.01em !important;
    }
    /* Estilo para o rodapé */
    .fixed-footer {
        font-family: Inter, -apple-system, BlinkMacSystemFont, "Segoe UI", "Noto Sans", Helvetica, Arial, sans-serif;
        font-weight: 300;
        letter-spacing: -0.01em;
    }
    /* Otimizações para dispositivos móveis */
    @media screen and (max-width: 768px) {
        html {
            font-size: 14px;
        }
        
        .hero-title {
            font-size: 3rem !important;
        }
        
        .hero-subtitle {
            font-size: 1.25rem !important;
        }
    }
    /* Otimizações de renderização */
    * {
        -webkit-font-smoothing: antialiased;
        -moz-osx-font-smoothing: grayscale;
        text-rendering: optimizeLegibility;
    }
    /* Font display swap para carregamento mais rápido */
    @font-face {
        font-family: 'Inter';
        font-display: swap;
    }
    @font-face {
        font-family: 'Noto Sans';
        font-display: swap;
    }
    </style>
""",
    unsafe_allow_html=True,
)

# Inicialização das variáveis de estado
if "app_state" not in st.session_state:
    st.session_state.app_state = (
        "inicio"  # estados: inicio, upload, type, objective, resumo, chat
    )
if "texto_extraido" not in st.session_state:
    st.session_state.texto_extraido = None
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "objetivo_selecionado" not in st.session_state:
    st.session_state.objetivo_selecionado = None
if "objetivo_final" not in st.session_state:
    st.session_state.objetivo_final = None
if "deve_gerar_resumo" not in st.session_state:
    st.session_state.deve_gerar_resumo = False
if "history_items" not in st.session_state:
    st.session_state.history_items = []
if "selected_history_id" not in st.session_state:
    st.session_state.selected_history_id = None
if "file_name" not in st.session_state:
    st.session_state.file_name = None
if "resumo_gerado" not in st.session_state:
    st.session_state.resumo_gerado = None
if "faqs_gerados" not in st.session_state:
    st.session_state.faqs_gerados = None


# Função para navegar entre estados
def change_state(new_state):
    st.session_state.app_state = new_state
    st.rerun()


# Função para definir o método de entrada
def handle_upload_click():
    change_state("upload")


def handle_type_click():
    change_state("type")


# Função para processar arquivo
def handle_file_upload(uploaded_file):
    with st.spinner("📖 Extraindo conteúdo..."):
        st.session_state.texto_extraido = process_file(uploaded_file)
        st.session_state.file_name = uploaded_file.name
        st.session_state.app_state = "objective"
        st.rerun()


# Função para processar texto digitado
def handle_text_input(texto_digitado):
    if texto_digitado:
        st.session_state.texto_extraido = texto_digitado
        st.session_state.file_name = "texto_digitado.txt"
        st.session_state.app_state = "objective"
        st.rerun()
    else:
        st.error("Por favor, digite algum texto antes de continuar.")


# Função para adicionar ao histórico
def add_to_history(file_name, objetivo, timestamp):
    history_id = str(uuid.uuid4())
    history_item = {
        "id": history_id,
        "file_name": file_name,
        "objetivo": objetivo,
        "timestamp": timestamp,
    }
    if "history_items" not in st.session_state:
        st.session_state.history_items = []
    st.session_state.history_items.insert(0, history_item)
    return history_id


# Função para lidar com o clique na sugestão
def handle_sugestao_click(sugestao):
    st.session_state.objetivo_selecionado = sugestao
    st.session_state.objetivo_final = sugestao
    gerar_resumo_e_faq(st.session_state.texto_extraido, sugestao)
    change_state("resumo")


# Função para gerar resumo e FAQ
def gerar_resumo_e_faq(texto, objetivo):
    # Gerar resumo
    with st.spinner("🧠 Resumindo com inteligência..."):
        resumo = resumir_texto(texto, objetivo)
        st.session_state.resumo_gerado = resumo

    # Generate FAQ
    with st.spinner("❓ Gerando perguntas frequentes..."):
        faqs = gerar_faq(texto, objetivo)
        st.session_state.faqs_gerados = faqs

    # Salvar no banco
    # session = Session()
    # try:
    #     # Create document
    #     doc = Documento(
    #         id=str(uuid.uuid4()),
    #         nome_arquivo=st.session_state.file_name,
    #         objetivo=objetivo,
    #         resumo=resumo[:5000] if resumo else "",
    #         faq=None,  # Will be updated later
    #     )
    #
    #     # Save initial document
    #     session.add(doc)
    #     session.commit()
    #     logger.info("✅ Documento inicial salvo com sucesso")
    #
    #
    #         # Convert FAQ list to JSON string before saving
    #         doc.faq_list = faqs  # This will automatically convert to JSON
    #         try:
    #             session.commit()
    #             print("✅ Documento salvo com sucesso!")
    #         except Exception as e:
    #             print(f"❌ Erro ao salvar no banco: {e}")
    #             session.rollback()
    #         finally:
    #             session.close()
    #         logger.info("✅ FAQs atualizadas com sucesso")
    #
    # except Exception as e:
    #     logger.error(f"❌ Erro ao salvar no banco: {str(e)}")
    #     session.rollback()
    #     st.error(f"Erro ao salvar no banco de dados. Por favor, tente novamente.")
    # finally:
    #     session.close()


# Função para processar objetivo digitado
def handle_objetivo_input(objetivo_usuario):
    if objetivo_usuario:
        st.session_state.objetivo_final = objetivo_usuario
        gerar_resumo_e_faq(st.session_state.texto_extraido, objetivo_usuario)
        st.session_state.app_state = "resumo"
        st.rerun()


# Função para processar nova mensagem no chat
def handle_new_message(message):
    if message:
        with st.spinner("💡 Gerando resposta..."):
            # Criar um ID de sessão baseado no nome do arquivo atual
            session_id = f"doc_{st.session_state.file_name}"

            resposta = responder_com_maritaca(
                st.session_state.texto_extraido,
                st.session_state.objetivo_final,
                message,
                session_id,  # Adicione este parâmetro
            )
            st.session_state.chat_history.append(
                {"pergunta": message, "resposta": resposta}
            )
        st.session_state.app_state = "chat"
        st.rerun()


def salvar_documento(nome_arquivo, objetivo, resumo, faq=None):
    print("Salvar documento")
    # session = Session()
    # try:
    #     print(
    #         f"📄 Dados a serem salvos: nome_arquivo={nome_arquivo}, objetivo={objetivo}, resumo={resumo[:100]}, faq={faq[:100] if faq else None}"
    #     )
    #     doc = Documento(
    #         id=str(uuid.uuid4()),
    #         nome_arquivo=nome_arquivo,
    #         objetivo=objetivo,
    #         resumo=resumo[:5000],  # Limita o tamanho do resumo
    #         faq=faq[:5000] if faq else None,
    #     )
    #     session.add(doc)
    #     session.commit()
    #     print("✅ Documento salvo com sucesso!")
    # except Exception as e:
    #     print(f"❌ Erro ao salvar documento: {e}")
    #     session.rollback()
    # finally:
    #     session.close()


try:
    image = Image.open("lucid_logo.jpg")
    st.image(image, width=100, use_container_width=True)
except FileNotFoundError:
    st.error("Arquivo 'lucid_logo.jpg' não encontrado no caminho especificado.")
except Exception as e:
    st.error(f"Erro ao carregar a imagem: {e}")



st.markdown(
    """
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600&display=swap" rel="stylesheet">
    <div class="hero-subtitle" style="font-family: 'Inter', sans-serif;">
        Uma tela. Um comando. Insights infinitos
    </div>
    """,
    unsafe_allow_html=True,
)

# Lógica principal baseada no estado atual
if st.session_state.app_state == "inicio":
    st.markdown(
    """
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600&display=swap" rel="stylesheet">
    <div class="choice-title" style="font-family: 'Inter', sans-serif;">
        Como você deseja inserir seu conteúdo?
    </div>
    """,
    unsafe_allow_html=True,
)


    col1, col2 = st.columns(2)

    with col1:
        if st.button(
            "📁 Upload de arquivo", key="upload_btn", use_container_width=True
        ):
            handle_upload_click()

        st.markdown(
            """
        <style>
        [data-testid="baseButton-secondary"]:has(div:contains("📁")) {
            height: 180px !important;
            background-color: white !important;
            color: #424245 !important;
            border: 2px solid #424245 !important;
            border-radius: 10px !important;
            font-size: 1.2rem !important;
            font-weight: 500 !important;
            display: flex !important;
            flex-direction: column !important;
            align-items: center !important;
            justify-content: center !important;
            padding: 2rem !important;
            transition: transform 0.3s, box-shadow 0.3s !important;
        }
        
        [data-testid="baseButton-secondary"]:has(div:contains("📁")):hover {
            transform: translateY(-5px) !important;
            box-shadow: 0 6px 12px rgba(0,0,0,0.15) !important;
            background-color: #f5f5f7 !important;
        }
        
        [data-testid="baseButton-secondary"]:has(div:contains("📁")) div {
            display: flex !important;
            flex-direction: column !important;
            align-items: center !important;
        }
        
        [data-testid="baseButton-secondary"]:has(div:contains("📁")) div::before {
            content: "📁" !important;
            font-size: 3rem !important;
            margin-bottom: 1rem !important;
        }
        </style>
        """,
            unsafe_allow_html=True,
        )

    with col2:
        if st.button("✏️ Digitar texto", key="text_btn", use_container_width=True):
            handle_type_click()

        st.markdown(
            """
        <style>
        [data-testid="baseButton-secondary"]:has(div:contains("✏️")) {
            height: 180px !important;
            background-color: white !important;
            color: #424245 !important;
            border: 2px solid #424245 !important;
            border-radius: 10px !important;
            font-size: 1.2rem !important;
            font-weight: 500 !important;
            display: flex !important;
            flex-direction: column !important;
            align-items: center !important;
            justify-content: center !important;
            padding: 2rem !important;
            transition: transform 0.3s, box-shadow 0.3s !important;
        }
        
        [data-testid="baseButton-secondary"]:has(div:contains("✏️")):hover {
            transform: translateY(-5px) !important;
            box-shadow: 0 6px 12px rgba(0,0,0,0.15) !important;
            background-color: #f5f5f7 !important;
        }
        
        [data-testid="baseButton-secondary"]:has(div:contains("✏️")) div {
            display: flex !important;
            flex-direction: column !important;
            align-items: center !important;
        }
        
        [data-testid="baseButton-secondary"]:has(div:contains("✏️")) div::before {
            content: "✏️" !important;
            font-size: 3rem !important;
            margin-bottom: 1rem !important;
        }
        </style>
        """,
            unsafe_allow_html=True,
        )

elif st.session_state.app_state == "upload":
    st.markdown(
        "<div class='section-title'>📁 Envie seu arquivo</div>", unsafe_allow_html=True
    )
    uploaded_file = st.file_uploader(
        "",
        type=["pdf", "docx", "txt", "png", "jpg", "jpeg"],
        label_visibility="collapsed",
    )

    if uploaded_file:
        handle_file_upload(uploaded_file)

    if st.button("⬅️ Voltar ao início", use_container_width=True):
        change_state("inicio")

elif st.session_state.app_state == "type":
    st.markdown(
        "<div class='section-title'>✏️ Digite seu texto</div>", unsafe_allow_html=True
    )
    texto_digitado = st.text_area(
        "",
        height=200,
        placeholder="Cole ou digite seu texto aqui...",
        label_visibility="collapsed",
    )

    if st.button("Processar texto", use_container_width=True):
        handle_text_input(texto_digitado)

    if st.button("⬅️ Voltar ao início", use_container_width=True):
        change_state("inicio")

elif st.session_state.app_state == "objective":
    st.markdown(
        "<div class='section-title'>🧭 Qual o seu objetivo com este conteúdo?</div>",
        unsafe_allow_html=True,
    )

    # Gerar sugestões de objetivo
    sugestoes = sugerir_objetivo(st.session_state.texto_extraido)

    # Mostrar sugestões como botões
    st.markdown(
        "<div style='margin-bottom: 1rem;'>Sugestões de objetivo:</div>",
        unsafe_allow_html=True,
    )
    col1, col2, col3 = st.columns(3)

    for i, sugestao in enumerate(sugestoes):
        col = col1 if i % 3 == 0 else col2 if i % 3 == 1 else col3
        if col.button(sugestao, key=f"sugestao_{i}", use_container_width=True):
            handle_sugestao_click(sugestao)

    objetivo_usuario = st.text_input(
        "Ou descreva seu objetivo: ",
        key="objetivo_input",
        placeholder="Ex: quero um resumo executivo",
    )

    if objetivo_usuario:
        handle_objetivo_input(objetivo_usuario)

    if st.button("⬅️ Voltar ao início", use_container_width=True):
        change_state("inicio")

elif st.session_state.app_state == "resumo" or st.session_state.app_state == "chat":
    # Se temos um resumo gerado, exibir
    if st.session_state.resumo_gerado:
        st.markdown(
            "<div class='section-title'>📄 Resumo Inteligente</div>",
            unsafe_allow_html=True,
        )
        st.markdown(
            f"<div class='card'>{st.session_state.resumo_gerado}</div>",
            unsafe_allow_html=True,
        )

    # Se temos FAQs gerados, exibir
    if st.session_state.faqs_gerados:
        st.markdown(
            "<div class='section-title'>❓ Perguntas Frequentes</div>",
            unsafe_allow_html=True,
        )
        for i, faq in enumerate(st.session_state.faqs_gerados, 1):
            st.markdown(
                f"<div class='card'><b>{i}. {faq}</b></div>", unsafe_allow_html=True
            )

    # Seção de chat
    st.markdown(
        "<div id='chat-section' class='section-title'>💬 Pergunte ao Lucid</div>",
        unsafe_allow_html=True,
    )

    # Mostrar histórico do chat
    for chat in st.session_state.chat_history:
        st.markdown(
            f"<div class='card'><b>Você:</b> {chat['pergunta']}</div>",
            unsafe_allow_html=True,
        )
        st.markdown(
            f"<div class='card'><b>Lucid:</b> {chat['resposta']}</div>",
            unsafe_allow_html=True,
        )

    # Input de chat com form para evitar loop
    with st.form("chat_form", clear_on_submit=True):
        message = st.text_input(
            "",
            placeholder="Escreva sua pergunta sobre o conteúdo...",
            label_visibility="collapsed",
            key="message_input",
        )
        submitted = st.form_submit_button("", type="primary")
        if submitted and message:
            # Criar um ID de sessão baseado no nome do arquivo atual
            session_id = f"doc_{st.session_state.file_name}"
            with st.spinner("💡 Gerando resposta..."):
                resposta = responder_com_maritaca(
                    st.session_state.texto_extraido,
                    st.session_state.objetivo_final,
                    message,
                    session_id,
                )
                st.session_state.chat_history.append(
                    {"pergunta": message, "resposta": resposta}
                )
                st.rerun()

    # Mostrar botão de feedback apenas após o uso do chat
    if st.session_state.chat_history:
        st.success("✅ Obrigado por usar o Lucid!")
        st.write("Quer nos ajudar a melhorar? Leva menos de 1 minuto!")

        # Botão para abrir o Forms
        if st.button("Dar Feedback"):
            st.markdown(
                "[Clique aqui para abrir o formulário de feedback 🚀](https://docs.google.com/forms/d/e/1FAIpQLSed-Pc0evoX5aYlh2PwNoNQuuMy8R3hL00vvK9MmPxm1NkbNQ/viewform)",
                unsafe_allow_html=True,
            )

    if st.button("⬅️ Voltar ao início", use_container_width=True):
        change_state("inicio")

# Rodapé fixo
st.markdown(
    """
    <style>
    .fixed-footer {
        position: fixed;
        left: 0;
        bottom: 0;
        width: 100%;
        background-color: white;
        text-align: center;
        padding: 10px 0;
        border-top: 1px solid #eee;
        color: #666;
        font-size: 0.8rem;
    }
    </style>
    
    <div class='fixed-footer'>
        © 2025 Lucid - Todos os direitos reservados
    </div>
""",
    unsafe_allow_html=True,
)
