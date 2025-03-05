# IoT Backend

Este projeto é o backend de uma aplicação IoT, desenvolvido com FastAPI e SQLAlchemy, utilizando TimescaleDB para otimização de séries temporais.

## Descrição

A aplicação coleta dados de sensores (temperatura, umidade, tensão e corrente) enviados por servidores on-premise. Cada servidor possui até 4 sensores (um de cada tipo). A aplicação permite:
- Registro de dados dos sensores (`POST /data`) sem autenticação;
- Autenticação e gerenciamento de usuários (`POST /auth/register`, `POST /auth/login`);
- Consulta de dados com filtros e agregações (`GET /data`);
- Monitoramento da saúde dos servidores (`GET /health/{server_id}`, `GET /health/all`);
- Registro de servidores (`POST /servers`).

## Pré-requisitos

- Docker e Docker Compose instalados.
- 
## Estrutura do Projeto

```
iot-backend/
├── app/
│   ├── main.py               # Configuração do FastAPI e definição das rotas
│   ├── core/
│   │   ├── container.py      # Configuração do container de DI
│   │   ├── config.py         # Leitura de variáveis de ambiente e configurações
│   │   └── database/
│   │       ├── db.py         # Engine, SessionLocal e Base
│   │       └── models.py     # Models: SensorDataModel, ServerModel, etc.
│   ├── adapters/
│   │   └── repositories/    # Repositories implementation
│   │       ├── sensor_data.py 
│   │       └── servers.py
│   ├── api/
│   │   └── routes/          # Controllers
│   │       └── sensor_data_controller.py
│   └── useCases/
│       └── sensor_data_service.py
│   ├── ports/
│   │   └── repositories/    # Repositories interface
│   │       └── sensor_data_repository.py
│   │       └── servers.py
│   ├── domain/
│   │   └── dto/
│   │       └── sensor_data_dto.py
│   │   └── entities/
│   │       └── SensorData.py
│   │       └── Server.py
├── tests/
│   ├── conftest.py
│   │   └── integration/
│   │       └── test_sensor_data_controller.py
├── scripts/
│   ├── setup_timescaledb.py   # Script para habilitar a extensão e criar a hypertable
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── README.md
```

## Configuração

As variáveis de ambiente necessárias estão definidas no docker-compose.yml. Caso necessário, ajuste os seguintes valores:
```
    POSTGRES_USER
    POSTGRES_PASSWORD
    POSTGRES_DB
    DATABASE_URL (no serviço app)
```

## Como Rodar

 1. Clone o repositório:

```
git clone https://github.com/seu_usuario/iot-backend.git
cd iot-backend
```

 2. Construa e suba os containers:

        docker compose up --build

  3. Acesse a aplicação:

A aplicação estará disponível em http://localhost:8000.
Os endpoints de documentação (Swagger e Redoc) estarão disponíveis em /docs e /redoc.

## Testes

Para rodar os testes, execute:

    docker-compose run --rm app pytest

## Dependências

As dependências do projeto estão listadas no arquivo requirements.txt.
