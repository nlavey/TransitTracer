# Transit Tracer

A backend API for analyzing public transit data using **GTFS**, **FastAPI**, and **PostgreSQL**. The project extracts and transforms GTFS data, loads it into Supabase PostgreSQL, and provides REST endpoints for accessing transit information and running SQL-based analytics.

## Features

* GTFS data extraction and transformation
* PostgreSQL database hosted with Supabase
* REST API built with FastAPI
* Pydantic response validation
* SQL-based transit analytics
* Parameterized SQL queries
* Error handling and 404 responses
* Automated API tests with pytest
* Dockerized application

## Tech Stack

* **Python**
* **FastAPI**
* **Pydantic**
* **PostgreSQL**
* **Supabase**
* **Pandas**
* **psycopg2**
* **pytest**
* **Docker**
* **Uvicorn**

## API Endpoints

### Health

| Method | Endpoint     | Description                 |
| ------ | ------------ | --------------------------- |
| GET    | `/health/db` | Check database connectivity |

### Transit Data

| Method | Endpoint      | Description                     |
| ------ | ------------- | ------------------------------- |
| GET    | `/agencies`   | Get transit agencies            |
| GET    | `/routes`     | Get transit routes              |
| GET    | `/stops`      | Get transit stops               |
| GET    | `/trips`      | Get transit trips               |
| GET    | `/stop-times` | Get stop arrival/departure data |

### Analytics

| Method | Endpoint                       | Description                                    |
| ------ | ------------------------------ | ---------------------------------------------- |
| GET    | `/analytics/trips-per-route`   | Count trips by route                           |
| GET    | `/analytics/busiest-stops`     | Identify stops with the most scheduled service |
| GET    | `/analytics/trips-by-hour`     | Analyze trips by hour of the day               |
| GET    | `/analytics/routes/{route_id}` | Get statistics for a specific route            |

Example:

```text
GET /analytics/routes/77119
```

Example response:

```json
{
  "route_id": "77119",
  "total_trips": 153,
  "stops_served": 48,
  "average_stops_per_trip": 22.5
}
```

## Project Structure

```text
transit-api/
├── src/
│   ├── database/
│   │   └── connection.py
│   └── etl/
│       ├── extract.py
│       ├── transform.py
│       └── load.py
├── tests/
│   └── test_api.py
├── data/
│   └── raw/
├── main.py
├── requirements.txt
├── Dockerfile
├── .dockerignore
├── .gitignore
└── README.md
```

## Data Pipeline

The project uses a simple ETL pipeline to prepare GTFS data for the API:

```text
GTFS Feed
   ↓
Extract
   ↓
Transform / Clean
   ↓
Load
   ↓
Supabase PostgreSQL
   ↓
FastAPI
   ↓
REST API / Analytics
```

The current implementation uses **Caltrain GTFS data**.

## Running Locally

### 1. Clone the repository

```bash
git clone https://github.com/nlavey/TransitTracer.git
cd TransitTracer
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

Activate it on Windows:

```powershell
.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file in the project root:

```text
DATABASE_URL=your_supabase_database_url
```

Do not commit `.env` or database credentials to GitHub.

### 5. Start the API

```bash
uvicorn main:app --reload
```

The API will be available at:

```text
http://localhost:8000
```

Interactive API documentation:

```text
http://localhost:8000/docs
```

## Running with Docker

Build the Docker image:

```bash
docker build -t transit-tracer .
```

Run the container:

```bash
docker run --env-file .env -p 8000:8000 transit-tracer
```

The API will then be available at:

```text
http://localhost:8000
```

Swagger documentation:

```text
http://localhost:8000/docs
```

## Testing

The project uses **pytest** for automated API testing.

Run the test suite with:

```bash
pytest
```

Current test suite:

```text
12 passed
```

Tests cover:

* API endpoint availability
* Response structure
* Database health
* Analytics endpoints
* Route statistics
* Invalid route handling
* Valid hour ranges
* Non-negative analytics values

## Database

Transit data is stored in **PostgreSQL through Supabase**.

The database contains GTFS-related tables including:

* `agency`
* `calendar`
* `routes`
* `shapes`
* `stops`
* `stop_times`
* `trips`

The API uses parameterized SQL queries when interacting with the database.

## Future Improvements

* Deploy the API to a cloud platform
* Add additional transit agencies such as BART or VTA
* Add more advanced service and schedule analytics
* Add a frontend dashboard for visualizing transit data
* Expand automated test coverage
* Add CI/CD with GitHub Actions

## License

This project is for educational and portfolio purposes.
