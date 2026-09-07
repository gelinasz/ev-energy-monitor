# EV Energy Monitoring System

A portfolio-scale EV charging telemetry and energy management system built to demonstrate a production-oriented architecture using **Python, FastAPI, PostgreSQL, React, and cloud deployment**.

The system simulates EV charger telemetry, stores readings in PostgreSQL, monitors site-level electrical load, detects stale/offline chargers, and provides operator recommendations when site power exceeds a configured limit.

## Live Demo

**API:** https://ev-energy-monitor.onrender.com

**API Documentation:** https://ev-energy-monitor.onrender.com/docs

The React operator dashboard runs locally against the deployed API.

---

## Architecture

```text
┌─────────────────────┐
│  Simulated Chargers │
│                     │
│ Voltage             │
│ Current             │
│ Power               │
│ Temperature         │
│ Status              │
└──────────┬──────────┘
           │
           │ REST / JSON
           ▼
┌─────────────────────┐
│      FastAPI        │
│                     │
│ Telemetry API       │
│ Site Power Logic    │
│ Health Monitoring   │
│ Recommendations     │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│     PostgreSQL      │
│                     │
│ Historical readings │
└──────────┬──────────┘
           │
           │ REST API
           ▼
┌─────────────────────┐
│   React Dashboard   │
│                     │
│ Site power          │
│ Charger telemetry   │
│ Health status       │
│ Operator alerts     │
└─────────────────────┘
```

---

## Features

### Live Charger Telemetry

The simulator generates charger measurements including:

* Voltage
* Current
* Power
* Temperature
* Charging status
* Timestamp

Telemetry is sent to the deployed FastAPI service every five seconds.

### Site-Level Power Management

The system calculates aggregate site power and compares it against a configurable site limit.

Current configuration:

```text
Site power limit: 150 kW
```

When the site exceeds the limit, the API identifies the amount of power that needs to be reduced and recommends a charger based on charging priority.

Example:

```json
{
  "status": "over_limit",
  "action": "reduce_charging",
  "power_to_reduce_kw": 21.06,
  "target_charger": "Charger-02"
}
```

### Stale Data Detection

The system monitors when each charger last reported telemetry.

A charger becomes stale when its last reading exceeds the configured threshold.

```text
Fresh → normal operation
Stale → check connection
```

The simulator intentionally stops sending data for one charger to demonstrate an offline communication condition.

When telemetry resumes, the charger automatically returns to a fresh state.

### Operator Health Monitoring

The `/site/health` endpoint provides:

* Charger name
* Last-seen timestamp
* Reading age
* Fresh/stale state
* Recommended operator action

### REST API

The FastAPI backend exposes endpoints for:

```text
GET  /
GET  /health
GET  /db-test

GET  /sensors
POST /sensors

GET  /site/power
GET  /site/power/recommendation
GET  /site/health
```

Interactive API documentation is available through FastAPI's generated Swagger UI.

---

## Technology Stack

### Backend

* Python
* FastAPI
* SQLAlchemy
* Pydantic
* Uvicorn

### Database

* PostgreSQL
* Historical telemetry storage

### Frontend

* React
* Vite
* JavaScript
* REST API integration

### Infrastructure

* Git
* GitHub
* Render
* Environment-based database configuration

---

## Failure-State Simulation

A key goal of the project is to demonstrate that telemetry systems need to handle more than the normal operating state.

The simulator can demonstrate:

| Condition                   | System Behavior                            |
| --------------------------- | ------------------------------------------ |
| Normal telemetry            | Charger reported as fresh                  |
| Charger offline             | Reading becomes stale                      |
| Telemetry recovery          | Charger returns to fresh                   |
| High power demand           | Site approaches/exceeds power limit        |
| Site overload               | System recommends reducing charging        |
| Database connection failure | Health/diagnostic endpoint reports failure |

This provides a small-scale demonstration of the type of monitoring and operational reasoning required in distributed energy systems.

---

## Project Structure

```text
ev-energy-monitor/
│
├── main.py
├── models.py
├── database.py
├── simulator.py
├── requirements.txt
├── .gitignore
├── .env
│
└── frontend/
    ├── src/
    │   └── App.jsx
    ├── package.json
    └── vite.config.js
```

`.env` is intentionally excluded from version control.

---

## Running Locally

### Backend

Create and activate a Python virtual environment:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

Install dependencies:

```powershell
pip install -r requirements.txt
```

Set the PostgreSQL connection string in `.env`:

```text
DATABASE_URL=your_database_connection_string
```

Start FastAPI:

```powershell
python -m uvicorn main:app --reload
```

The API will be available at:

```text
http://127.0.0.1:8000
```

Swagger documentation:

```text
http://127.0.0.1:8000/docs
```

### Frontend

```powershell
cd frontend
npm install
npm run dev
```

The React dashboard will be available at:

```text
http://localhost:5173
```

### Simulator

From the project root:

```powershell
python simulator.py
```

The simulator sends charger telemetry to the deployed API.

---

## Engineering Decisions

### Latest Reading Per Charger

Site-level calculations use the latest telemetry reading for each charger rather than summing historical records.

This prevents historical measurements from being incorrectly interpreted as simultaneous electrical load.

### Environment-Based Configuration

Database credentials are supplied through environment variables rather than committed to source control.

### Dependency Injection

FastAPI database sessions use a dependency that guarantees the SQLAlchemy session is closed after each request.

### Explicit Failure States

The system treats stale telemetry as an operational condition rather than silently ignoring missing data.

---

## What This Project Demonstrates

This project was built as a focused portfolio implementation to demonstrate practical experience with:

* Designing a REST API
* Building a Python/FastAPI backend
* Working with PostgreSQL
* Modeling telemetry data
* Connecting a React frontend to a live API
* Processing real-time-style sensor data
* Implementing site-level control logic
* Detecting stale telemetry
* Designing failure and recovery scenarios
* Deploying a backend to the cloud
* Using Git and GitHub for version control
* Separating configuration and secrets from application code

It is intentionally smaller than a production energy-management platform, but the architecture is designed to provide a foundation for adding additional production capabilities such as automated testing, containerization, CI/CD, time-series optimization, authentication, alerting, and more advanced load-management strategies.

---

## Why I Built It

I built this project to explore the software architecture behind EV charging and energy-management systems and to turn the concepts into a working system rather than simply describing them.

The project focuses particularly on the connection between **physical systems, telemetry, software, and operational decision-making**.

---

## Future Development

Potential next steps include:

* Docker containerization
* GitHub Actions CI/CD
* Automated API and failure-state tests
* TimescaleDB optimization for high-frequency telemetry
* Authentication and role-based access
* Persistent alert history
* Historical power/temperature charts
* More sophisticated charger scheduling
* Dynamic site power allocation
* Production monitoring and logging
