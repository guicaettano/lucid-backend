import os
from sqlalchemy import Column, String, Text, DateTime, create_engine
from sqlalchemy.orm import sessionmaker, declarative_base  # Atualizado aqui
from datetime import datetime

Base = declarative_base()  # Agora usa a nova localização

class Documento(Base):
    __tablename__ = "documentos"

    id = Column(String, primary_key=True)
    nome_arquivo = Column(String)
    objetivo = Column(String)
    resumo = Column(Text)
    faq = Column(Text, nullable=True)
    chat = Column(Text, nullable=True)
    conteudo = Column(Text)  # ⬅️ Adicione essa linha
    timestamp = Column(DateTime, default=datetime.now)

# Recria o banco de dados
if os.path.exists("lucid.db"):
    os.remove("lucid.db")
    print("🗑️ Banco de dados excluído.")
engine = create_engine("sqlite:///lucid.db")
Base.metadata.create_all(engine)
print("✅ Novo banco de dados criado.")
Session = sessionmaker(bind=engine)