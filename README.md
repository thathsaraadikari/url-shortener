# URL Shortener API

A fast and lightweight URL shortener built with FastAPI, SQLAlchemy, and MySQL.

## Project Structure

```
url-shortener/
├── app/
│   ├── __init__.py       # Package initializer
│   ├── main.py           # FastAPI entrypoint & routes
│   ├── database.py       # Database connection & session
│   ├── models.py         # SQLAlchemy database models
│   ├── schemas.py        # Pydantic schemas / DTOs
│   └── utils.py          # Helper functions & short code generation
├── tests/
│   └── test_api.py       # API integration tests
├── .env                  # Local environment configuration
├── .env.example          # Sample environment variables
├── .gitignore            # Git ignore rules
├── requirements.txt      # Project dependencies
└── README.md             # Project documentation
```

## Getting Started

### 1. Activate Virtual Environment
```bash
.\venv\Scripts\activate
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Run Development Server
```bash
uvicorn app.main:app --reload
```
