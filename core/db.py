import os
import logging
from sqlalchemy import Column, String, Text, DateTime, create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from datetime import datetime
import json
import uuid

# Configuração de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

Base = declarative_base()

class Documento(Base):
    __tablename__ = "documentos"

    id = Column(String, primary_key=True)
    nome_arquivo = Column(String, nullable=False)
    objetivo = Column(String, nullable=False)
    resumo = Column(Text, nullable=False)
    faq = Column(Text, nullable=True)  # Will store JSON string
    chat = Column(Text, nullable=True)
    timestamp = Column(DateTime, default=datetime.now)

    @property
    def faq_list(self):
        """Convert JSON string to list"""
        return json.loads(self.faq) if self.faq else []

    @faq_list.setter
    def faq_list(self, value):
        """Convert list to JSON string"""
        self.faq = json.dumps(value) if value else None

    def __repr__(self):
        return f"<Documento(id={self.id}, nome={self.nome_arquivo})>"

def recriar_banco():
    """Exclui e recria o banco de dados"""
    if os.path.exists("lucid.db"):
        os.remove("lucid.db")
        print("🗑️ Banco de dados excluído.")
    engine = create_engine("sqlite:///lucid.db")
    Base.metadata.create_all(engine)
    print("✅ Novo banco de dados criado.")
    return sessionmaker(bind=engine)

def salvar_documento(nome_arquivo, objetivo, resumo, faq=None):
    session = Session()
    try:
        print(f"📄 Dados a serem salvos: nome_arquivo={nome_arquivo}, objetivo={objetivo}, resumo={resumo[:100]}, faq={faq[:100] if faq else None}")
        doc = Documento(
            id=str(uuid.uuid4()),
            nome_arquivo=nome_arquivo,
            objetivo=objetivo,
            resumo=resumo[:5000],  # Limita o tamanho do resumo
            faq=faq[:5000] if faq else None,
        )
        session.add(doc)
        session.commit()
        print("✅ Documento salvo com sucesso!")
    except Exception as e:
        print(f"❌ Erro ao salvar documento: {e}")
        session.rollback()
    finally:
        session.close()

# Inicializa o banco de dados
Session = recriar_banco()