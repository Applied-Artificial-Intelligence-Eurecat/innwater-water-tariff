# Fast Backend for Water Tariff Application

This is a FastAPI-based backend for the Water Tariff application, providing a more modular and structured approach.

## Project Structure

```
fast_backend/
├── main.py                  # Main application entry point
├── requirements.txt         # Project dependencies
└── src/                     # Source code
    ├── core/                # Core modules (dependencies, ORM)
    │   ├── database.py      # Database connection and session management
    │   └── models.py        # SQLAlchemy ORM models
    └── affordability/       # Affordability module
        ├── router/          # API routes
        │   └── affordability.py  # Affordability endpoints
        └── services/        # Business logic
            └── affordability_indicator_bw.py  # Affordability indicator service
```

## Setup

1. Create a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Set environment variables (optional):
   ```
   export DATABASE_PATH=path/to/your/database.db  # Default: default_database.db
   export PORT=8000  # Default: 8000
   ```

## Running the Application

Run the application with:

```
python main.py
```

Or with uvicorn directly:

```
uvicorn main:app --reload
```

The API will be available at http://localhost:8000

## API Documentation

Once the application is running, you can access the auto-generated API documentation at:

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Available Endpoints

- `GET /health` - Health check endpoint
- `GET /api/affordability/indicators/{project_id}` - Get affordability indicators for a project
- `POST /api/affordability/indicators/{project_id}/generate` - Generate affordability indicators for a project