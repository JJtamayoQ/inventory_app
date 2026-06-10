# Project Overview

## Purpose

Inventory App is a small internal web app for laboratory supply control. It
tracks supplies, package types, locations, workers, and the history of stock
changes.

## Technology

- Python 3.13
- Flask for HTTP routes and Jinja rendering
- Waitress for serving the app outside Flask debug mode
- SQLite for persistence
- Bootstrap, Bootstrap Icons, jQuery, and DataTables for the frontend
- Pandas, NumPy, and OpenPyXL for Excel-to-SQLite imports

## Runtime Entry Points

- `app.py`: starts Flask debug mode on port `5001` when run directly.
- `run.py`: serves the Flask app with Waitress on port `5050`.
- `data/excel_to_sqlite.py`: rebuilds the root `inventario.db` from Excel files.
- `data/pruebas.py`: read-only database smoke check.

## Main Routes

| Route | Methods | Purpose |
| --- | --- | --- |
| `/` | GET | Show active inventory items. |
| `/add_item` | POST | Add a new inventory item and history entry. |
| `/edit` | POST | Edit an inventory item and reset its initial quantity. |
| `/update_quantity` | POST | Register stock entry or exit and update status. |
| `/delete_item` | POST | Mark an inventory item inactive. |
| `/inactive` | GET | Show inactive inventory items. |
| `/activate_item` | POST | Reactivate an inventory item. |
| `/history` | GET | Show stock movement history. |
| `/workers` | GET | Show active workers. |
| `/add_worker` | POST | Add a worker. |
| `/edit_worker` | POST | Edit a worker. |
| `/delete_worker` | POST | Mark a worker inactive. |
| `/inactive_workers` | GET | Show inactive workers. |
| `/activate_worker` | POST | Reactivate a worker. |

## Data Model

### `insumos`

Inventory items.

- `Item_id`: primary key
- `Activo`: active/inactive flag
- `Nombre`: item name
- `Detalles`: item details
- `Cantidad`: current quantity
- `Cantidad_Inicial`: reference quantity used for status calculation
- `Estado_id`: foreign key to `estados`
- `Ubicacion_id`: foreign key to `ubicaciones`
- `Empaque_id`: foreign key to `empaques`

### `trabajadores`

Workers who can be responsible for inventory changes.

- `Trabajador_id`: primary key
- `Activo`: active/inactive flag
- `Nombre_Apellido`
- `Dependencia`
- `Cargo`
- `Correo`

### `historial`

Audit trail for inventory item changes.

- `Historial_id`: primary key
- `Tipo`: movement type, such as `Entrada`, `Salida`, `Editar`
- `Detalles`: comment or generated movement detail
- `Trabajador_id`: responsible worker
- `Fecha`: SQLite timestamp
- `Item_id`: inventory item

### Reference Tables

- `estados`: status values used for Bootstrap badges: `success`, `warning`, `danger`
- `empaques`: package names
- `ubicaciones`: location names

## Stock Status Logic

`getQuantityStatus(former_quantity, new_quantity)` compares the new quantity
against the initial quantity:

- `success`: at least 70 percent of initial quantity
- `warning`: at least 30 percent and below 70 percent
- `danger`: below 30 percent, or no initial quantity

When editing an item, the edited quantity becomes the new `Cantidad_Inicial`.

## Recent Hardening

- Database path now resolves relative to `app.py`.
- `SECRET_KEY` can be configured through the environment.
- Stock exits cannot reduce inventory below zero.
- Quantity validation allows valid zero current stock.
- Debug printing of submitted item data was removed.
- DataTables initialization now only targets tables present on the current page.
- Excel import no longer appends duplicate rows on every run.
- `data/pruebas.py` is read-only.

## Maintenance Notes

- Keep `requirements.txt` updated when adding Python imports.
- Avoid running `data/excel_to_sqlite.py` against important history unless a full
  rebuild is intended.
- Prefer adding database helper functions in `app.py` instead of repeating raw
  connection setup in every route.
- The frontend currently uses CDN assets, so browser access to those CDNs is
  required unless local copies are added.
