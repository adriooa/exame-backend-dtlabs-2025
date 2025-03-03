# scripts/create_tables.py
import sys  # Adicione essa linha no topo do seu script

from sqlalchemy import create_engine, inspect, exc
from app.core.database.db import Base, DATABASE_URL  # Importe Base e a URL


def create_tables(engine):
    """
    Cria todas as tabelas definidas nos metadados da Base.
    """
    inspector = inspect(engine)
    if inspector.get_table_names():
        print("WARNING: Tables already exist.  They will NOT be recreated.")
        return  # Sai da função se as tabelas já existirem

    print("Creating all tables...")
    try:
        if not inspector.get_table_names():  # Se não houver tabelas, cria
            print("Creating all tables...")
            Base.metadata.create_all(bind=engine)
            print("Tables created successfully.")
        else:
            print("Tables already exist. Skipping creation.")
        print("Tables created successfully.")
    except exc.SQLAlchemyError as e:
        print(f"ERROR: Could not create tables: {e}", file=sys.stderr)
        exit(1)
    except Exception as e:
        print(f"An unexpected error occurred: {e}", file=sys.stderr)
        exit(1)


if __name__ == "__main__":
    print(f"Using DATABASE_URL: {DATABASE_URL}")  # Imprime a URL

    # Cria a engine do SQLAlchemy
    try:
        engine = create_engine(DATABASE_URL)
        # Testa a conexão *imediatamente*
        with engine.connect() as connection:
            print("Database connection successful.")
    except exc.SQLAlchemyError as e:
        print(
            f"ERROR: Could not connect to the database: {e}", file=sys.stderr)
        exit(1)
    except Exception as e:
        print(f"An unexpected error occurred: {e}", file=sys.stderr)
        exit(1)

    # Chame a função para criar as tabelas
    create_tables(engine)
