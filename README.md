# TempCheck

MVP demo built for **Muriel** to test a digital workflow for managing temperature-related risk during product transportation.

The idea came from a simple limitation: Muriel did not have IoT sensors or dataloggers available to automatically monitor temperature during deliveries.

Instead of simulating sensor readings, the prototype uses information that employees could actually enter themselves.

## What It Does

The workflow allows users to:

- Review active deliveries
    
- Check transportation conditions
    
- Assess operational risk
    
- Complete a checklist
    
- Register corrective actions
    
- Close a reception
    
- Review a final summary
    

## Risk Score

The prototype uses information such as:

- Product type
    
- Estimated transportation time
    
- Approximate time outside proper storage
    
- Vehicle condition
    
- Loading condition
    
- Storage conditions at the destination
    

These inputs are converted into a simple score:

```text
0–3  → Low Risk
4–6  → Medium Risk
7+   → High Risk
```

This is a rule-based score for the MVP, not a validated predictive model.

## Stack

- Python
    
- FastAPI
    
- Jinja2
    
- HTML
    
- CSS
    
- JavaScript
    
- Docker
    

## Data

The application currently stores:

- Deliveries
    
- Checklist responses
    
- Changes to deliveries
    
- Corrective actions
    
- Reception closures
    

in:

```text
app/data/shipments.json
```

The initial data is simulated.

## Run Locally

```bash
python3 -m venv .venv
source .venv/bin/activate

pip install -r requirements.txt

uvicorn app.main:app --reload
```

Then open:

```text
http://127.0.0.1:8000
```

## Docker

```bash
docker build -t tempcheck .
docker run -p 8000:8000 tempcheck
```

To keep local data after removing the container:

```bash
docker run \
  -p 8000:8000 \
  -v "$(pwd)/app/data:/app/app/data" \
  tempcheck
```

## GitHub Codespaces

The repository includes a dev-container configuration.

The application can be started with:

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## Render

The repository also includes:

```text
render.yaml
```

for deployment on Render.

## Current Limitations

- Uses simulated data
    
- No real temperature sensors
    
- No IoT or datalogger integration
    
- JSON persistence instead of a database
    
- No user authentication
    
- No role-based permissions
    
- Risk score is rule-based
    

## Next Steps

Possible improvements include:

- PostgreSQL
    
- User roles for factory, transport, and branches
    
- Historical delivery reports
    
- Sensor or datalogger integration
    
- PDF summaries
    
- Alerts for high-risk deliveries
    
- More detailed rules by product type
