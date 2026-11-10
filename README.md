# AquaSafe — Drinking Water Potability Checker

A 2nd-year B.Tech AI/ML project by Vikranth Reddy (Woxsen University).

Logistic regression (C=1.0) on standardized features — pH, hardness, solids (TDS), chloramines, sulfate, conductivity, organic carbon, trihalomethanes, turbidity — trained on 1,000 synthetic water samples (seed 42).

- 5-fold CV accuracy: 68.2%, AUC: 0.74 (majority-class baseline: 54.8%)
- Live demo: https://aquasafe.vercel.app (runs fully in the browser — no backend)
- `train.py` trains the model and writes `model.json`; `index.html` applies the same weights in JavaScript.
