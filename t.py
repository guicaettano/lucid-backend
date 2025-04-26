import streamlit as st
from PIL import Image





# Teste com um arquivo local
try:
    image = Image.open("lucid_logo.jpg")  # Substitua pelo caminho correto
    st.image(image, use_column_width=True)
except FileNotFoundError:
    st.error("Arquivo 'lucid_logo.png' não encontrado no caminho especificado.")
except Exception as e:
    st.error(f"Erro ao carregar a imagem: {e}")