# scripts/drop_tables.py (Execute este script SEPARADAMENTE)
from app.core.database.db import engine, Base  # Importe engine e Base

# Apaga TODAS as tabelas definidas nos seus modelos:
if __name__ == "__main__":
    print("Dropping all tables...")
    Base.metadata.drop_all(bind=engine)  # CUIDADO!!! Apaga TODAS as tabelas
    print("Tables dropped.")

# Para executar:
# python scripts/drop_tables.py