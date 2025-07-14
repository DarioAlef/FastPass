from pydantic import BaseModel, EmailStr
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime

Base = declarative_base()

class UserORM(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    
    # Relacionamento com senhas
    senhas = relationship("SenhaORM", back_populates="usuario")

class SenhaORM(Base):
    __tablename__ = "senhas"
    id = Column(Integer, primary_key=True, index=True)
    senha = Column(String, nullable=False)
    tempo_completado = Column(Integer, nullable=False)  # tempo em segundos
    data_criacao = Column(DateTime, default=datetime.utcnow)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # Relacionamento com usuário
    usuario = relationship("UserORM", back_populates="senhas")

class User(BaseModel):
    nome: str
    email: EmailStr

class Senha(BaseModel):
    senha: str
    tempo_completado: int
    user_id: int

class SenhaResponse(BaseModel):
    id: int
    senha: str
    tempo_completado: int
    data_criacao: datetime
    user_id: int
    
    class Config:
        from_attributes = True