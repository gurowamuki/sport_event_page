# Sports Calendar
 
A Django web application for browsing and managing sports events. Users can view upcoming and past events across multiple sports (football, ice hockey, basketball), see event details including teams, venues, leagues, and results, and create new events via form.

## Features
 
- Home page with navigation to the events calendar
- Event list view showing all events with sport, teams, league, venue and status
- Event detail view with full information including match results for finished games
- Form-based event creation (`/events/create/`)
- PostgreSQL backend with a normalised schema covering countries, cities, venues, sports, leagues, teams, events, and results

---
 
## Tech Stack
 
| Layer      | Technology                        |
|------------|-----------------------------------|
| Framework  | Django 6.0.3                      |
| Database   | PostgreSQL (via psycopg2-binary)  |
| Config     | python-dotenv                     |
| Python     | 3.12+                             |
| Postman    | Optionaly                         |
 
---

## Project Structure
 
```
sports_calendar/
├── events/                  # Main Django app
│   ├── models.py            # ORM models (mapped to SQL schema)
│   ├── views.py             # Views: home, event_list, event_detail, event_create
│   ├── urls.py              # App-level URL routing
│   ├── forms.py             # EventForm with home/away team validation
│   ├── templates/events/    # HTML templates
│   └── static/events/       # CSS and images
├── sports_calendar/         # Project config
│   ├── settings.py
│   └── urls.py
├── db/
│   └── sports_calendar.sql  # Database schema + seed data
├── .env.example             # Environment variable template
├── manage.py
└── requirements.txt
```
 
---
 
## Setup & Installation
 
### Prerequisites
 
- Python 3.12+
- PostgreSQL 13+ running locally (or a remote instance)
 
---
 
### 1. Clone the repository
 
```bash
git clone <repository-url>
cd sports_calendar
```
 
### 2. Create and activate a virtual environment
 
```bash
python -m venv venv
 
# Windows
venv\Scripts\activate
 
# macOS / Linux
source venv/bin/activate
```
 
### 3. Install dependencies
 
```bash
pip install -r requirements.txt
```
 
### 4. Configure environment variables
 
Copy `.env.example` to `.env` and fill in your values:
 
```bash
cp .env.example .env
```
 
```ini
# .env
SECRET_KEY=your_secret_key_here
DB_NAME=sports_calendar
DB_USER=postgres
DB_PASSWORD=your_password_here
DB_HOST=localhost
DB_PORT=5432
```
 
### 5. Set up the database
 
Create a PostgreSQL database matching the name in your `.env`:
 
```sql
CREATE DATABASE sports_calendar;
```
 
#### Setup using SQL file:
 
Load the schema and seed data directly from the provided SQL file:
 
```bash
psql -U postgres -d sports_calendar -f db/sports_calendar.sql
```
 
This creates all tables and populates them with sample data (countries, cities, venues, sports, leagues, teams, and events).
 
---
 
### 6. Run the development server
 
```bash
python manage.py runserver
```

Open your browser at [http://127.0.0.1:8000](http://127.0.0.1:8000).
 
---

## URL Routes
 
| URL                     | View             | Description                            |
|-------------------------|------------------|----------------------------------------|
| `/`                     | `home`           | Home / landing page                    |
| `/events/`              | `event_list`     | List of all events                     |
| `/events/<id>/`         | `event_detail`   | Detail view for a single event         |
| `/events/create/`       | `event_create`   | Create a new event (GET form / POST)   |
 
## Creating an Event via Postman

### 1. Open Postman.com

Send a `GET` request to `http://127.0.0.1:8000/events/` and open the **Cookies** tab. Copy the `csrftoken` value.
 
### 2. Submit the form via POST
 
Send a `POST` request to `http://127.0.0.1:8000/events/create/`
 
Add a header:
- **Key:** `X-CSRFToken`
- **Value:** `<your csrftoken value>`
 
Example body (form-data or JSON):
```json
{
  "event_date": "2026-03-30",
  "event_time": "18:30:00",
  "sport_id": 1,
  "home_team_id": 1,
  "away_team_id": 2,
  "league_id": 1,
  "venue_id": 1,
  "event_status": "scheduled"
}
```

---
## Assumptions & Decisions
 
### Unmanaged Django models (`managed = False`)
All models are set to `managed = False`. This means Django does not own the database schema — the SQL file is the source of truth for table definitions. This approach was chosen to keep the SQL schema explicit and fully under developer control, and to allow the same schema to be used independently of Django (e.g. for direct SQL queries or other tools).
 
### SQL file as the primary setup method
Because models are unmanaged, the SQL file (`db/sports_calendar.sql`) must be run to create the tables. The file also includes sample seed data (teams, leagues, events) so the application is immediately usable after setup without manual data entry.
 
### `RESTRICT` on foreign key deletion
All `ForeignKey` fields in Django models use `on_delete=models.RESTRICT`. This mirrors the referential integrity intent of the SQL schema — for example, a country cannot be deleted if cities still reference it. This prevents accidental data loss through cascading deletes.
 
### CSRF handling
The `event_list` and `event_detail` views use the `@ensure_csrf_cookie` decorator to send the CSRF token to the client. The `event_create` POST endpoint uses `@csrf_exempt` since it is designed for API consumption (e.g. from a separate frontend or curl).
 
### Event status values
The `event_status` field is constrained to: `scheduled`, `live`, `finished`, `postponed`, `cancelled`. This is enforced both at the database level (a `CHECK` constraint in SQL) and at the application level (Django field validation).