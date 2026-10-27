"""Train a simple Student Placement model on synthetic data and save it."""
import joblib
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split

FEATURES = ["cgpa", "internships", "projects", "backlogs", "communication"]


def make_data(n=1000, seed=42):
    rng = np.random.default_rng(seed)
    df = pd.DataFrame({
        "cgpa": rng.uniform(5.0, 10.0, n).round(2),
        "internships": rng.integers(0, 4, n),
        "projects": rng.integers(0, 6, n),
        "backlogs": rng.integers(0, 5, n),
        "communication": rng.integers(1, 11, n),
    })
    score = (
        1.2 * (df["cgpa"] - 6.5)
        + 0.6 * df["internships"]
        + 0.4 * df["projects"]
        - 0.9 * df["backlogs"]
        + 0.3 * (df["communication"] - 5)
        + rng.normal(0, 0.5, n)
    )
    df["placed"] = (score > 0.8).astype(int)
    return df


def train(path="model.pkl"):
    df = make_data()
    X_train, X_test, y_train, y_test = train_test_split(
        df[FEATURES], df["placed"], test_size=0.2, random_state=42
    )
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    acc = accuracy_score(y_test, model.predict(X_test))
    joblib.dump(model, path)
    print(f"Model saved to {path} | test accuracy = {acc:.3f}")
    return acc


if __name__ == "__main__":
    train()
