# Inventory App

A Flask and SQLite web application for managing laboratory inventory items,
workers, stock movements, inactive records, and movement history.

## Features

- View active inventory items.
- Add, edit, deactivate, and reactivate inventory items.
- Register stock entries and exits.
- Track movement history with responsible workers.
- Manage active and inactive workers.
- Rebuild the SQLite database from the Excel files in `data/`.

## Project Structure

```txt
inventory_app/
  app.py                    Flask application and routes
  run.py                    Waitress production-style runner
  inventario.db             SQLite database used by the app
  requirements.txt          Python dependencies
  data/
    excel_to_sqlite.py      Rebuilds the database from Excel files
    pruebas.py              Read-only database smoke check
    INVENTARIO INSUMOS.xlsx Inventory source data
    USUARIOS_UD.xlsx        Worker source data
  static/                   CSS and JavaScript assets
  templates/                Jinja HTML templates
  docs/                     Project documentation
```

## Setup

Create and activate the virtual environment:

```powershell
py -3.13 -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Install dependencies:

```powershell
python -m pip install -r requirements.txt
```

Dependencies are already installed in the local `.venv` in this workspace.

## Run The App

Development mode:

```powershell
python app.py
```

Open:

```txt
http://localhost:5001
```

Waitress runner:

```powershell
python run.py
```

Open:

```txt
http://localhost:5050
```

## Configuration

The app reads `SECRET_KEY` from the environment. If it is not set, a development
fallback is used.

Example:

```powershell
$env:SECRET_KEY = "change-this-for-production"
python run.py
```

## Database

The app uses the root-level `inventario.db` file. `app.py` resolves the database
path relative to the project folder, so it does not depend on the shell's current
working directory.

To inspect the database without changing data:

```powershell
python data\pruebas.py
```

To rebuild the database from Excel:

```powershell
python data\excel_to_sqlite.py
```

Warning: the rebuild script clears and reloads imported tables, including
`historial`, from the Excel sources.

## More Documentation

See [docs/PROJECT_OVERVIEW.md](docs/PROJECT_OVERVIEW.md) for routes, data model,
logic notes, and maintenance guidance.
