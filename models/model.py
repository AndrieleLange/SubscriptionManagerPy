from sqlmodel import Field, SQLModel, Relationship
from typing import Optional # para ser opcional
from datetime import date # para data
from decimal import Decimal # para valores decimais

#tabela do banco de dados
class Subscription(SQLModel, table=True):
    id: int = Field(primary_key=True) # pk true para o banco criar e n a gente
    empresa: str  # nome da empresa
    site: Optional[str] = None # site da empresa, pode ser nulo
    data_assinatura: date
    valor: Decimal

class Payments(SQLModel, table=True):
    id: int = Field(primary_key=True)
    subscription_id: int = Field(foreign_key="subscription.id") # chave estrangeira
    subscription: Subscription = Relationship() # relacionamento com a tabela Subscription
    data: date
