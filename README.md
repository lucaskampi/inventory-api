# Inventory API (Django + Django Ninja)

A RESTful backend for managing entities, implemented in Python using Django and Django Ninja.

Key features
- CRUD for the `Entity` model (fields: `type`, `name`, `description`, `created_at`).
- OpenAPI/Swagger documentation provided by Django Ninja (`/api/docs`).

Entity model
- `id`: int (auto)
- `type`: string, required, max 100 characters
- `name`: string, optional, max 255 characters
- `description`: text, optional
- `created_at`: automatic creation timestamp

Planned endpoints
- GET  /api/entities         — list all entities
- GET  /api/entities/{id}    — retrieve entity by id
- POST /api/entities         — create a new entity
- PUT  /api/entities/{id}    — update an existing entity
- DELETE /api/entities/{id}  — delete an entity

Prerequisites
- Python 3.11+ (or compatible)
- Virtual environment (`venv`) recommended

Development installation
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

Running the project

Unix / macOS
```bash
# create and activate virtual environment
python -m venv .venv
source .venv/bin/activate

# install dependencies (first time)
pip install -r requirements.txt

# apply migrations and run the development server
python manage.py migrate
python manage.py runserver
```

Windows (PowerShell)
```powershell
# create and activate virtual environment
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# install dependencies (first time)
pip install -r requirements.txt

# apply migrations and run the development server
python manage.py migrate
python manage.py runserver
```

Run with ASGI server (uvicorn)
```bash
# hot-reload ASGI server (useful for Django Ninja/OpenAPI during development)
uvicorn inventory_api.asgi:application --reload
```

API documentation
- After starting the server, interactive API docs will be available at: `http://127.0.0.1:8000/api/docs`

Tests
- Tests use `pytest`/`pytest-django`.
```bash
pytest --cov=.
```

Docker (optional)
- You can dockerize the application and use a Postgres service for production. Add `Dockerfile` and `docker-compose.yml` for orchestration.

Security notes
- Do not commit secrets to the repository. Use environment variables or a secrets manager for production credentials.

Suggested next steps
- Implement the API with Django Ninja (`entities/api.py`) and expose routes in `inventory_api/urls.py`.
- Write tests for the endpoints and add CI/coverage.

Files edited: `entities/models.py`, `entities/migrations/0001_initial.py`, `inventory_api/settings.py` (registered `entities` app).
