from sqlalchemy import Column, String, Text, DateTime, create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from sqlalchemy.ext.declarative import declarative_base
import os

Base = declarative_base()

class Documento(Base):
    __tablename__ = "documentos"

    id = Column(String, primary_key=True)
    nome_arquivo = Column(String)
    objetivo = Column(String)
    resumo = Column(Text)
    faq = Column(Text, nullable=True)
    chat = Column(Text, nullable=True)
    conteudo = Column(Text)
    timestamp = Column(DateTime, default=datetime.now)

# Garantir que o diretório existe
db_dir = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(db_dir, "lucid.db")

# Criar engine com configurações adicionais
engine = create_engine(
    f"sqlite:///{db_path}",
    connect_args={"check_same_thread": False},  # Necessário para o Streamlit
    echo=False  # Desativa logs detalhados
)

# Criar tabelas se não existirem
try:
    Base.metadata.create_all(engine)
except Exception as e:
    print(f"Erro ao criar banco de dados: {e}")

# Criar session factory
Session = sessionmaker(bind=engine)
