# TempCheck

> MVP demo developed for **Muriel** to explore temperature-risk controls during product transportation.

TempCheck is an internal web prototype designed to help operational teams review deliveries, assess temperature-related risk, document preventive actions, and close product receptions using a structured digital workflow.

## Problem

Some products can lose quality during transportation because of factors such as:

- Prolonged exposure outside appropriate storage
    
- Weak cold-chain controls
    
- Vehicle condition
    
- Product handling
    
- Delays
    
- Loading conditions
    
- Storage readiness at the destination
    

Muriel did not have automatic IoT temperature sensors or dataloggers available for this prototype.

Instead of inventing measurements that do not exist, TempCheck focuses on information that employees can realistically record during an operational process.

## Objective

The MVP explores whether a lightweight digital workflow can help employees:

1. Review active deliveries.
    
2. Identify operational temperature risk.
    
3. Complete preventive checklists.
    
4. Document corrective actions.
    
5. Close product reception.
    
6. Maintain a simple record of the process.
    

## How It Works

Each delivery includes operational information used to evaluate its potential temperature risk.

The prototype considers factors including:

- Product storage requirement
    
- Estimated transportation time
    
- Approximate exposure time
    
- Vehicle condition
    
- Loading condition
    
- Destination storage condition
    

These variables are converted into a simple risk score.

## Temperature Risk Index

The current prototype uses an explainable rule-based score.

```text
0–3 points  → Low Risk
4–6 points  → Medium Risk
7+ points   → High Risk
```

The goal is not to claim scientific temperature prediction.

The score is used to demonstrate how operational information could be structured into an easy-to-understand decision-support tool.

## Workflow

```text
Active Delivery
      │
      ▼
Review Conditions
      │
      ▼
Risk Assessment
      │
      ▼
Operational Checklist
      │
      ▼
Corrective Actions
      │
      ▼
Reception Closure
      │
      ▼
Final Summary
```

## Tech Stack

- Python
    
- FastAPI
    
- Jinja2
    
- HTML
    
- CSS
    
- JavaScript
    
- Docker
    
- JSON-based persistence
    
- Render deployment configuration
    

## Data Persistence

The current MVP stores:

- Deliveries
    
- Delivery edits
    
- Checklist responses
    
- Corrective actions
    
- Reception closures
    

inside:

```text
app/data/shipments.json
```

If the file does not exist, the application can create it using initial demo data.

## Important Data Limitation

TempCheck currently uses **simulated data**.

It does not:

- Read real temperature sensors
    
- Connect to IoT devices
    
- Connect to dataloggers
    
- Automatically measure cold-chain conditions
    

This is intentional.

The MVP was built to validate the workflow and product concept before investing in additional hardware or infrastructure.

## Run Locally

Create a Python environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Start the application:

```bash
uvicorn app.main:app --reload
```

Open:

```text
http://127.0.0.1:8000
```

## Docker

Build the image:

```bash
docker build -t tempcheck .
```

Run the container:

```bash
docker run -p 8000:8000 tempcheck
```

To persist local application data:

```bash
docker run \
  -p 8000:8000 \
  -v "$(pwd)/app/data:/app/app/data" \
  tempcheck
```

## GitHub Codespaces

The repository includes a development-container configuration.

A Codespace can run the application using:

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## Deployment

The repository includes:

```text
render.yaml
```

for deployment through Render.

The application can be started in a hosted environment with:

```bash
uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

## Current Limitations

TempCheck is an MVP designed for concept validation.

Current limitations include:

- Simulated operational data
    
- No real temperature measurements
    
- No IoT integration
    
- No production database
    
- JSON-based persistence
    
- No authentication or role-based access
    
- Rule-based risk score rather than a validated predictive model
    

## Possible Next Steps

Future versions could include:

- PostgreSQL persistence
    
- Factory, transportation, and branch user roles
    
- Historical delivery reporting
    
- Real sensor or datalogger integration
    
- Delivery analytics
    
- PDF summary exports
    
- Product-specific temperature requirements
    
- More advanced risk validation
    
- Alerts for high-risk deliveries
    

## Project Context

TempCheck was built as a **demo MVP for Muriel**.

Its purpose is to demonstrate a possible operational workflow and test the usefulness of the concept before building a production system.
