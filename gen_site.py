import json
m = json.load(open("model.json"))
features, mean, std = m["features"], m["mean"], m["std"]
coef, icpt = m["coef"], m["intercept"]
mt = m["metrics"]
acc, auc, base = mt["cv_accuracy"], mt["auc"], mt["baseline_accuracy"]
DOMAIN = "aquasafe.vercel.app"
LABELS = {
 "ph": "pH", "hardness": "Hardness (mg/L)", "solids": "Solids / TDS (ppm)",
 "chloramines": "Chloramines (ppm)", "sulfate": "Sulfate (mg/L)",
 "conductivity": "Conductivity (μS/cm)", "organic_carbon": "Organic carbon (ppm)",
 "trihalomethanes": "Trihalomethanes (μg/L)", "turbidity": "Turbidity (NTU)",
}
DEFAULTS = [7.4, 200, 20000, 7.5, 330, 430, 14, 65, 4.0]
JS_MODEL = f"""const FEATURES = {json.dumps(features)};
const MEAN = {json.dumps(mean)};
const STD = {json.dumps(std)};
const COEF = {json.dumps(coef)};
const INTERCEPT = {icpt};
function potabilityProb(vals){{
  let z = INTERCEPT;
  for (let i = 0; i < 9; i++) z += COEF[i] * (vals[i] - MEAN[i]) / STD[i];
  return 1 / (1 + Math.exp(-z)) * 100;
}}"""
inputs = "\n".join(
    f'<label>{LABELS[f]}<input type="number" step="any" id="f{i}" value="{DEFAULTS[i]}"></label>'
    for i, f in enumerate(features))
index = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>AquaSafe — Drinking Water Potability Checker | AI/ML Project</title>
<meta name="description" content="AquaSafe checks whether drinking water is safe using a logistic regression model trained on 1,000 water samples — pH, hardness, TDS, chloramines, sulfate, conductivity, organic carbon, trihalomethanes and turbidity. Try it live in your browser.">
<link rel="canonical" href="https://{DOMAIN}/">
<meta property="og:title" content="AquaSafe — Drinking Water Potability Checker">
<meta property="og:description" content="Enter 9 water-test readings and instantly see the chance your water is safe to drink, with a real trained ML model running in your browser.">
<meta property="og:type" content="website">
<meta property="og:url" content="https://{DOMAIN}/">
<meta name="twitter:card" content="summary">
<meta name="twitter:title" content="AquaSafe — Drinking Water Potability Checker">
<meta name="twitter:description" content="Logistic regression water potability checker. Try the live demo in your browser.">
<script type="application/ld+json">{{"@context":"https://schema.org","@type":"WebApplication","name":"AquaSafe","applicationCategory":"EducationalApplication","description":"Drinking water potability checker using logistic regression.","url":"https://{DOMAIN}/"}}</script>
<style>
body{{font-family:Arial,Helvetica,sans-serif;color:#000;background:#fff;max-width:720px;margin:0 auto;padding:24px;line-height:1.5}}
h1{{font-size:2em}} label{{display:block;margin:12px 0 4px;font-weight:bold}}
input{{width:100%;padding:10px;font-size:16px;border:1px solid #000;border-radius:4px;box-sizing:border-box}}
button{{margin-top:16px;margin-right:8px;padding:12px 24px;font-size:17px;background:#000;color:#fff;border:none;border-radius:4px;cursor:pointer}}
#result{{margin-top:24px;padding:20px;border:2px solid #000;border-radius:8px;display:none}}
#result b{{font-size:1.6em}}
.note{{color:#333;font-size:.95em}} code{{background:#f2f2f2;padding:2px 5px}}
.grid{{display:grid;grid-template-columns:1fr 1fr;gap:0 20px}}
</style>
</head>
<body>
<h1>&#128167; AquaSafe — Water Potability Checker</h1>
<p class="note">A 2nd-year B.Tech AI/ML project by Vikranth Reddy. A logistic regression model trained on 1,000 synthetic water samples checks whether drinking water is safe from 9 lab readings. 5-fold CV: <b>accuracy = {acc:.1%}</b>, <b>AUC = {auc:.2f}</b> vs a majority-class baseline of {base:.1%}.</p>
<div class="grid">
{inputs}
</div>
<button onclick="predict()">Check My Water</button>
<button onclick="tryClean()">Try clean tap water</button>
<button onclick="tryDirty()">Try murky water</button>
<div id="result"></div>
<p class="note">How it works: each reading is standardised (subtract the training mean, divide by the standard deviation), multiplied by the model&apos;s learned weight, and summed with a bias; a sigmoid turns the total into a probability of the water being potable. The exact same weights run in this page and in the Python training script (<code>train.py</code>), so the browser result matches the trained model.</p>
<p class="note">Try it: clean tap water (pH 7.0, hardness 180, TDS 15,000, turbidity 3.0) &rarr; about 86.6% potable. Murky water (pH 6.2, TDS 45,000, trihalomethanes 110, turbidity 6.2) &rarr; about 0.3% potable — do not drink. Typical city supply scores around 46%.</p>
<p class="note">Honest note: this model was trained on synthetic data modelled on the classic water-potability dataset, so it is a classroom demo — a real lab test is the only way to certify drinking water.</p>
<p><a href="https://github.com/HVRGAMING2705/aquasafe">View source on GitHub</a></p>
<script>
{JS_MODEL}
function show(){{
  const vals = [];
  for (let i = 0; i < 9; i++) vals.push(parseFloat(document.getElementById("f" + i).value) || 0);
  const p = potabilityProb(vals);
  const el = document.getElementById("result");
  el.style.display = "block";
  const verdict = p >= 50 ? "&#9989; POTABLE — safe to drink" : "&#10060; NOT POTABLE — do not drink";
  el.innerHTML = "<b>" + p.toFixed(1) + "% potable</b><br>" + verdict +
    "<br><span class=note>Probability the water is safe to drink, from the 9 readings above. This is a classroom demo on synthetic data, not a lab certification.</span>";
}}
function predict(){{ show(); }}
function tryClean(){{ const v = [7.0,180,15000,7.0,300,400,12,50,3.0]; for (let i = 0; i < 9; i++) document.getElementById("f" + i).value = v[i]; show(); }}
function tryDirty(){{ const v = [6.2,260,45000,9.5,420,620,22,110,6.2]; for (let i = 0; i < 9; i++) document.getElementById("f" + i).value = v[i]; show(); }}
</script>
</body>
</html>
"""
open("index.html", "w").write(index)
vercel = {
 "headers": [{"headers": [
   {"key": "Strict-Transport-Security", "value": "max-age=63072000; includeSubDomains; preload"},
   {"key": "X-Content-Type-Options", "value": "nosniff"},
   {"key": "X-Frame-Options", "value": "SAMEORIGIN"},
   {"key": "Referrer-Policy", "value": "strict-origin-when-cross-origin"},
   {"key": "Permissions-Policy", "value": "camera=(), microphone=(), geolocation=()"},
   {"key": "Cross-Origin-Opener-Policy", "value": "same-origin"},
   {"key": "Access-Control-Allow-Origin", "value": f"https://{DOMAIN}"},
   {"key": "Content-Security-Policy", "value": "default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline'; img-src 'self' data:; base-uri 'self'; frame-ancestors 'self'"}],
  "source": "/(.*)"}]}
open("vercel.json", "w").write(json.dumps(vercel, indent=1))
open("404.html", "w").write(f"""<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8"><title>Page Not Found — AquaSafe</title><style>body{{font-family:Arial,sans-serif;color:#000;max-width:640px;margin:60px auto;padding:24px}}</style></head><body><h1>404 — Page not found</h1><p>This page does not exist on AquaSafe.</p><p><a href="https://{DOMAIN}/">Back to AquaSafe</a></p></body></html>""")
open("robots.txt", "w").write(f"User-agent: *\nAllow: /\nSitemap: https://{DOMAIN}/sitemap.xml\n")
open("sitemap.xml", "w").write(f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"><url><loc>https://{DOMAIN}/</loc></url></urlset>
""")
open("README.md", "w").write(f"""# AquaSafe — Drinking Water Potability Checker

A 2nd-year B.Tech AI/ML project by Vikranth Reddy (Woxsen University).

Logistic regression (C=1.0) on standardized features — pH, hardness, solids (TDS), chloramines, sulfate, conductivity, organic carbon, trihalomethanes, turbidity — trained on 1,000 synthetic water samples (seed 42).

- 5-fold CV accuracy: {acc:.1%}, AUC: {auc:.2f} (majority-class baseline: {base:.1%})
- Live demo: https://{DOMAIN} (runs fully in the browser — no backend)
- `train.py` trains the model and writes `model.json`; `index.html` applies the same weights in JavaScript.
""")
samples = json.load(open("parity_samples.json"))
parity = JS_MODEL + "\n" + "\n".join(
    f"console.log(JSON.stringify({{row: {json.dumps(s['row'])}, js: potabilityProb({json.dumps(s['row'])}), py: {s['prob']}}}));"
    for s in samples)
open("parity.js", "w").write(parity)
print("site files written, acc", acc)
