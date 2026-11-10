import json
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import cross_val_predict, StratifiedKFold
from sklearn.metrics import accuracy_score, roc_auc_score, classification_report

rng = np.random.default_rng(42)
N = 1000

# Realistic ranges modelled on the classic water-potability dataset
ph = np.clip(rng.normal(7.0, 1.2, N), 0, 14)
hardness = np.clip(rng.normal(196, 32, N), 50, 300)
solids = np.clip(rng.normal(22000, 8500, N), 300, 60000)
chloramines = np.clip(rng.normal(7.1, 1.5, N), 0, 14)
sulfate = np.clip(rng.normal(333, 41, N), 150, 500)
conductivity = np.clip(rng.normal(426, 80, N), 100, 750)
organic = np.clip(rng.normal(14.3, 3.3, N), 2, 30)
trihalo = np.clip(rng.normal(66, 16, N), 0, 130)
turbidity = np.clip(rng.normal(3.97, 0.8, N), 0, 7)

X_raw = np.column_stack([ph, hardness, solids, chloramines, sulfate,
                         conductivity, organic, trihalo, turbidity])
FEATURES = ["ph", "hardness", "solids", "chloramines", "sulfate",
            "conductivity", "organic_carbon", "trihalomethanes", "turbidity"]

# Generative logit: safe water has pH near 7, low turbidity / trihalomethanes /
# solids, moderate chloramines; hard water and high sulfate push the other way.
z = (0.6
     - 0.8 * np.abs(ph - 7.0)
     - 0.004 * (hardness - 196)
     - 0.00003 * (solids - 22000)
     - 0.12 * np.abs(chloramines - 7.0)
     - 0.004 * (sulfate - 333)
     - 0.002 * (conductivity - 426)
     - 0.08 * (organic - 14.3)
     - 0.03 * (trihalo - 66)
     - 1.3 * (turbidity - 3.97))
p = 1 / (1 + np.exp(-z))
y = (rng.random(N) < p).astype(int)

# Standardize (store mean/std for the JS demo)
mean = X_raw.mean(axis=0)
std = X_raw.std(axis=0)
X = (X_raw - mean) / std

model = LogisticRegression(C=1.0, max_iter=2000).fit(X, y)
skf = StratifiedKFold(5, shuffle=True, random_state=42)
pred_cv = cross_val_predict(LogisticRegression(C=1.0, max_iter=2000), X, y, cv=skf)
proba_cv = cross_val_predict(LogisticRegression(C=1.0, max_iter=2000), X, y, cv=skf, method="predict_proba")[:, 1]
acc = float(accuracy_score(y, pred_cv))
auc = float(roc_auc_score(y, proba_cv))
base = float(max(np.bincount(y)) / len(y))
print(f"n={N} potable_rate={y.mean():.3f}")
print(f"CV accuracy={acc:.3f} AUC={auc:.3f} baseline={base:.3f}")
print(classification_report(y, pred_cv, target_names=["not potable", "potable"], digits=3))

mj = {"features": FEATURES, "mean": mean.tolist(), "std": std.tolist(),
      "coef": model.coef_[0].tolist(), "intercept": float(model.intercept_[0]),
      "metrics": {"cv_accuracy": acc, "auc": auc, "baseline_accuracy": base,
                  "potable_rate": float(y.mean()), "n": N}}
with open("model.json", "w") as f:
    json.dump(mj, f, indent=1)

def py_prob(row):
    xs = (np.array(row) - mean) / std
    return float(model.predict_proba([xs])[0][1] * 100)

samples = [
    [7.0, 180, 15000, 7.0, 300, 400, 12, 50, 3.0],    # clean tap water
    [6.2, 260, 45000, 9.5, 420, 620, 22, 110, 6.2],   # murky, contaminated
    [7.4, 200, 20000, 7.5, 330, 430, 14, 65, 4.0],    # typical city supply
    [8.9, 290, 55000, 12.0, 480, 720, 28, 125, 6.8],  # worst case
    [6.8, 150, 8000, 6.0, 250, 300, 8, 30, 2.0],      # very clean
]
for s in samples:
    print(s, "->", round(py_prob(s), 2), "% potable")
with open("parity_samples.json", "w") as f:
    json.dump([{"row": s, "prob": py_prob(s)} for s in samples], f, indent=1)
