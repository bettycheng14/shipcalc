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
source venv/bin/activate
pip install -r requirements.txt
python run.py
```

Visit http://localhost:5000 in your browser.

## Run Tests

```bash
pytest tests/unit tests/integration --cov=app -v
```

## Run with Docker

```bash
docker build -t shipcalc .
docker run -p 5000:5000 shipcalc
```

## Selenium Tests

Selenium tests require the Flask app running separately on localhost:5000.

```bash
# Terminal 1
python run.py

# Terminal 2
pytest tests/selenium -v
```

## Testing Methodology

| Methodology      | Demonstrated In                                                                 |
|------------------|---------------------------------------------------------------------------------|
| BVA              | `test_validator.py` weight/price boundaries; `test_calculator.py` fee at 19.9/20.0/20.1 kg |
| ECT              | `test_validator.py` valid/invalid classes for region, price, weight, shipping type |
| Right-BICEP      | `test_calculator.py` cross-checks total - shipping - tax == item_price          |
| Decision Table   | `test_calculator.py` parametrised test covering all 6 region × shipping_type combos |
| TDD              | Tests written before implementation; each layer (validator → service → route) follows red-green cycle |
| Selenium         | `tests/selenium/test_selenium.py` full browser end-to-end form submission tests |
| CI/CD            | `cloudbuild.yaml` runs tests, builds Docker image, deploys to Cloud Run on GCP  |
