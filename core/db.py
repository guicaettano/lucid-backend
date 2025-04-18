import os
import logging
from sqlalchemy import Column, String, Text, DateTime, create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from datetime import datetime
import json

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

def init_db():
    """Inicializa o banco de dados"""
    try:
        logger.info("Iniciando criação do banco de dados...")
        
        # Recria o banco de dados
        if os.path.exists("lucid.db"):
            os.remove("lucid.db")
            logger.info("🗑️ Banco de dados existente excluído")
        
        # Cria novo banco
        engine = create_engine("sqlite:///lucid.db", echo=False)
        Base.metadata.create_all(engine)
        logger.info("✅ Novo banco de dados criado com sucesso")
        
        # Cria e retorna a Session
        return sessionmaker(bind=engine)
        
    except Exception as e:
        logger.error(f"❌ Erro ao criar banco de dados: {str(e)}")
        raise

# Inicializa o banco de dados
try:
    Session = init_db()
    logger.info("✅ Conexão com banco de dados estabelecida")
except Exception as e:
    logger.error(f"❌ Falha ao inicializar banco de dados: {str(e)}")
    raise