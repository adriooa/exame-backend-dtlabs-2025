import sys
from sqlalchemy import create_engine, text, exc
from app.core.config import configs
from app.core.database.db import Base  # Importe Base

def create_hypertable(engine):
    """Cria a hypertable para sensor_data."""
    try:
        with engine.connect() as connection:
            # Verifica se a tabela sensor_data já existe
            if not engine.dialect.has_table(connection, "sensor_data"):
                print("Error: Table 'sensor_data' does not exist.  Create it first.")
                exit(1)

            # Cria a hypertable
            print("Creating hypertable 'sensor_data'...")
            connection.execute(text(
                "SELECT create_hypertable('sensor_data', 'timestamp', if_not_exists => TRUE);"
            ))
            print("Hypertable 'sensor_data' created successfully.")
    except exc.SQLAlchemyError as e:
        print(f"ERROR: Could not create hypertable: {e}", file=sys.stderr)
        exit(1)
    except Exception as e:
        print(f"An unexpected error occurred: {e}", file=sys.stderr)
        exit(1)

if __name__ == "__main__":
    database_url = configs.DATABASE_URL
    engine = create_engine(database_url)
    create_hypertable(engine)