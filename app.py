import os

import joblib
import pandas as pd
from flask import Flask, jsonify, render_template, request
from prometheus_client import Counter
from prometheus_flask_exporter import PrometheusMetrics

from train import FEATURES, train

MODEL_PATH = os.path.join(os.path.dirname(__file__), "model.pkl")
if not os.path.exists(MODEL_PATH):
    train(MODEL_PATH)
model = joblib.load(MODEL_PATH)

app = Flask(__name__)
metrics = PrometheusMetrics(app)  # exposes /metrics automatically
metrics.info("app_info", "Placement predictor", version="1.0.0")

PREDICTIONS = Counter(
    "placement_predictions_total", "Total predictions made", ["result"]
)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/health")
def health():
    return jsonify(status="ok")


@app.route("/predict", methods=["POST"])
def predict():
    data = request.get_json(silent=True) or request.form.to_dict()
    try:
        row = {f: float(data[f]) for f in FEATURES}
    except (KeyError, ValueError, TypeError):
        return jsonify(error=f"Provide numeric values for: {FEATURES}"), 400

    X = pd.DataFrame([row], columns=FEATURES)
    pred = int(model.predict(X)[0])
    prob = float(model.predict_proba(X)[0][1])
    label = "Placed" if pred == 1 else "Not Placed"
    PREDICTIONS.labels(result=label).inc()
    return jsonify(prediction=label, placement_probability=round(prob, 3))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
