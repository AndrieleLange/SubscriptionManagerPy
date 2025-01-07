from sqlmodel import SQLModel, create_engine, Field
from .model import *

sqlite_file_name = 'database.db'
sqlite_url = f'sqlite:///{sqlite_file_name}'

# conexão com o banco de dados
engine = create_engine(sqlite_url, echo=False) # mudar para false quando acabar

if __name__ == '__main__':
    SQLModel.metadata.create_all(engine) # cria o banco de dados