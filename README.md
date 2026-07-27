# 🚀 FastAPI Microservice Architecture

![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-00a393.svg)
![Docker](https://img.shields.io/badge/Docker-Ready-2496ED.svg)

A scalable backend microservice template built with FastAPI, implementing clean architecture, dependency injection, and comprehensive testing suites.

## 🚀 Key Features
- **Clean Microservice Design**: Separated routing, business logic, and data access layers.
- **Dependency Injection**: Modular and testable code structure using FastAPI's native DI framework.
- **Dockerized Environment**: Production-ready Docker containerization.

## 🛠️ Quickstart & Local Setup

1. **Clone the repository**:
   ```bash
   git clone https://github.com/Sxmxxrth/fastApi-project-2.git
   cd fastApi-project-2
   ```
2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
3. **Run the microservice**:
   ```bash
   uvicorn app.main:app --reload
   ```



## 📁 Production Directory Structure

```text
📁 fastApi-project-2/
├── 📄 README.md
├── 📄 __init__.py
├── 📁 alembic/
│   ├── 📄 README
│   ├── 📄 env.py
│   ├── 📄 script.py.mako
│   └── 📁 versions/
├── 📄 alembic.ini
├── 📁 app/
│   ├── 📄 __init__.py
│   ├── 📁 core/
│   ├── 📁 models/
│   ├── 📁 router/
│   ├── 📁 schema/
│   ├── 📁 sevices/
│   ├── 📁 templates/
│   └── 📁 utils/
├── 📁 config/
│   └── 📄 settings.yaml
├── 📄 main.py
├── 📄 requirements.txt
├── 📄 router_integration_record.txt
├── 📄 suggested_endpoints.txt
└── 📁 tests/
    └── 📄 test_auth.py
```

## 🧪 Running Automated Tests

To run the automated production test suite, execute:

```bash
pytest tests/  # or python -m unittest discover -s tests
```
## 📝 License
MIT License
