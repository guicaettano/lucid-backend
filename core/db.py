import os
import logging
from sqlalchemy import Column, String, Text, DateTime, create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from datetime import datetime

# Configuração de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

Base = declarative_base()

class Documento(Base):
    __tablename__ = "documentos"

    id = Column(String, primary_key=True)
    nome_arquivo = Column(String, nullable=False)
    objetivo = Column(String, nullable=False)
    resumo = Column(Text, nullable=False)
    faq = Column(Text, nullable=True)
    chat = Column(Text, nullable=True)
    timestamp = Column(DateTime, default=datetime.now)

    def __repr__(self):
        return f"<Documento(id={self.id}, nome={self.nome_arquivo})>"

def init_db():
    """Inicializa o banco de dados"""
    try:
        # Recria o banco de dados
        if os.path.exists("lucid.db"):
            os.remove("lucid.db")
            logger.info("🗑️ Banco de dados existente excluído")
        
        # Cria novo banco
        engine = create_engine("sqlite:///lucid.db", echo=True)
        Base.metadata.create_all(engine)
        logger.info("✅ Novo banco de dados criado com sucesso")
        
        # Cria e retorna a Session
        Session = sessionmaker(bind=engine)
        return Session
        
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