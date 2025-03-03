import os
from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()


class Configs(BaseSettings):
    PROJECT_NAME: str = "IoT Backend"

    # POSTGRES_SERVER: str = os.getenv("POSTGRES_SERVER", "localhost")
    # POSTGRES_USER: str = os.getenv("POSTGRES_USER", "user")
    # POSTGRES_PASSWORD: str = os.getenv("POSTGRES_PASSWORD", "password")
    # POSTGRES_DB: str = os.getenv("POSTGRES_DB", "mydb")
    # POSTGRES_TEST_DB: str = os.getenv("POSTGRES_TEST_DB", "mydb_test")

    # DATABASE_URL: str = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER}/{POSTGRES_DB}"
    # TEST_DATABASE_URL: str = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER}/{POSTGRES_TEST_DB}"
    
    POSTGRES_SERVER: str = os.getenv("POSTGRES_SERVER", "localhost") #pode ser localhost ou db
    POSTGRES_USER: str = os.getenv("POSTGRES_USER", "myuser")
    POSTGRES_PASSWORD: str = os.getenv("POSTGRES_PASSWORD", "mypassword")
    POSTGRES_DB: str = os.getenv("POSTGRES_DB", "mydb")
    POSTGRES_TEST_DB: str = os.getenv("POSTGRES_TEST_DB", "mydb_test") #usado para testes

    # URL de conexão para o banco de dados de DESENVOLVIMENTO/PRODUÇÃO
    DATABASE_URL: str = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER}/{POSTGRES_DB}"

    TEST_DATABASE_URL: str = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER}/{POSTGRES_TEST_DB}"



configs = Configs()
