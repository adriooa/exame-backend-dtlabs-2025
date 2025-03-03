# scripts/setup_timescaledb.py
import psycopg2
from app.core.config import configs

def setup_timescaledb():
    """Configura o TimescaleDB (cria a extensão)."""
    try:
        conn = psycopg2.connect(
            host="localhost",
            database=configs.POSTGRES_DB,
            user=configs.POSTGRES_USER,
            password=configs.POSTGRES_PASSWORD,
            port="5432" #Usar a porta para o caso de estar rodando local
        )
        conn.autocommit = True  # Importante para CREATE EXTENSION
        cursor = conn.cursor()

        # Cria a extensão TimescaleDB
        cursor.execute("CREATE EXTENSION IF NOT EXISTS timescaledb;")
        print("TimescaleDB extension created/enabled.")

        cursor.close()
        conn.close()

    except psycopg2.OperationalError as e:
        print(f"Error connecting to PostgreSQL: {e}")
        exit(1)
    except psycopg2.Error as e:
        print(f"Error creating TimescaleDB extension: {e}")
        exit(1)

if __name__ == "__main__":
    setup_timescaledb()