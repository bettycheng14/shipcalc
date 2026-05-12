# ShipCalc

## Overview

ShipCalc is a simple international shipping cost estimator built with Python Flask. It calculates shipping fees, taxes, and final totals for orders shipped to Australia, USA, and Europe. The project is intentionally simple and testing-focused, built to demonstrate BVA, ECT, Right-BICEP, Decision Table Testing, TDD, Selenium automation, and CI/CD on Google Cloud Platform as part of SIT707.

## Tech Stack

- Python Flask 3.x
- Pytest + pytest-cov
- Decimal module (all money calculations)
- Bootstrap 5 via CDN
- Jinja2 templates
- Selenium + webdriver-manager
- Gunicorn
- Docker
- Google Cloud Build + Cloud Run

## Run Locally

```bash
python3 -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
python run.py
```

Visit http://localhost:5000 in your browser.

## Run Tests

**Always activate the virtual environment first** — pytest and all test dependencies are installed inside `venv/`, not system-wide.

```bash
source venv/bin/activate        # Windows: venv\Scripts\activate
pytest tests/unit tests/integration --cov=app -v
```

> **Why can't I run pytest?**  
> Running `pytest` or `python -m pytest` without activating the venv uses the system Python, which doesn't have pytest installed. The fix is `source venv/bin/activate` before running any pytest command.

## Run with Docker

```bash
docker build -t shipcalc .
docker run -p 5000:5000 shipcalc
```

## Selenium Tests

Selenium tests require the Flask app running separately on localhost:5000.

```bash
# Terminal 1
source venv/bin/activate
python run.py

# Terminal 2
source venv/bin/activate
pytest tests/selenium -v
```

## CI/CD

`cloudbuild.yaml` runs the full pipeline on every push:

1. Install dependencies and run unit + integration tests with coverage
2. Install Chromium, start Flask, run Selenium end-to-end tests
3. Build Docker image
4. Push image to Google Container Registry
5. Deploy to Cloud Run (`australia-southeast1`)

## Testing Methodology

| Methodology    | Demonstrated In                                                                       |
|----------------|---------------------------------------------------------------------------------------|
| BVA            | `test_validator.py` weight/price boundaries; `test_calculator.py` fee at 19.9/20.0/20.1 kg |
| ECT            | `test_validator.py` valid/invalid classes for region, price, weight, shipping type    |
| Right-BICEP    | `test_calculator.py` cross-checks total - shipping - tax == item_price                |
| Decision Table | `test_calculator.py` parametrised test covering all 6 region × shipping_type combos  |
| TDD            | Tests written before implementation; each layer (validator → service → route) follows red-green cycle |
| Selenium       | `tests/selenium/test_selenium.py` full browser end-to-end form submission tests       |
| CI/CD          | `cloudbuild.yaml` runs tests, builds Docker image, deploys to Cloud Run on GCP        |
