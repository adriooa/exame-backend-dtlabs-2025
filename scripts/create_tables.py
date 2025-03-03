# setup_timescaledb.py
import os
from sqlalchemy import create_engine, text
from app.core.database.db import Base  # Certifique-se de que seu Base contém o modelo SensorDataModel

# Obtenha a URL do banco a partir de uma variável de ambiente
DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL)

def enable_timescaledb_extension(engine):
    with engine.connect() as conn:
        print("Habilitando a extensão timescaledb...")
        conn.execute(text("CREATE EXTENSION IF NOT EXISTS timescaledb;"))
        print("Extensão habilitada.")

def create_hypertable(engine):
    with engine.connect() as conn:
        print("Convertendo a tabela sensor_data em hypertable...")
        conn.execute(
            text("SELECT create_hypertable('sensor_data', 'timestamp', if_not_exists => TRUE);")
        )
        print("Tabela convertida para hypertable.")

def main():
    print("Criando tabelas (se necessário)...")
    Base.metadata.create_all(bind=engine)
    
    enable_timescaledb_extension(engine)
    create_hypertable(engine)

if __name__ == "__main__":
    main()
