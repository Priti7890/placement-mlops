# Student Placement Predictor – CI/CD + Monitoring (ML DevOps Lab ISE-2)

Flask ML web app that predicts whether a student will be placed, built and deployed
through **Git → GitHub → Jenkins → Docker**, and monitored with **Prometheus + Grafana**.

## Endpoints
| Endpoint | Purpose |
|---|---|
| `/` | Web form |
| `/predict` (POST) | JSON prediction |
| `/health` | Health check |
| `/metrics` | Prometheus metrics |

## Run locally
```bash
python3 -m venv venv && source venv/bin/activate
pip install -r requirements.txt
pytest -v
python app.py            # http://localhost:5000
```

## Docker
```bash
docker build -t placement-predictor .
docker run -d -p 5000:5000 --name placement-app placement-predictor
```

## Monitoring stack
```bash
docker compose up -d --build
# App: http://localhost:5001   Prometheus: http://localhost:9090   Grafana: http://localhost:3000 (admin/admin)
```
Grafana: add data source Prometheus with URL `http://prometheus:9090`.
