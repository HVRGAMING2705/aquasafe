from pptx import Presentation
from pptx.util import Inches, Pt
import sys
DOMAIN = sys.argv[1] if len(sys.argv) > 1 else "aquasafe-beta.vercel.app"
prs = Presentation(); prs.slide_width = Inches(13.33); prs.slide_height = Inches(7.5)
def add(i, title, lines):
    s = prs.slides.add_slide(prs.slide_layouts[1])
    s.shapes.title.text = title
    tf = s.placeholders[1].text_frame; tf.word_wrap = True
    for j, ln in enumerate(lines):
        p = tf.paragraphs[0] if j == 0 else tf.add_paragraph()
        p.text = ln; p.font.size = Pt(20); p.space_after = Pt(10)
add(0, "AquaSafe — Drinking Water Potability Checker", ["An AI/ML project by Vikranth Reddy", "B.Tech CSE (AI & ML), 2nd Year — Woxsen University", "A model that reads 9 water-test values and tells you whether the water is safe to drink"])
add(1, "The Problem", ["Unsafe drinking water causes disease — but lab tests are slow and costly", "People cannot tell by looking whether tap or borewell water is safe", "A quick first check from 9 simple readings would help households decide", "AquaSafe gives that instant, explainable first verdict"])
add(2, "The Solution — AquaSafe", ["Enter 9 readings: pH, hardness, TDS, chloramines, sulfate, conductivity, organic carbon, trihalomethanes, turbidity", "A trained model returns the probability the water is potable, with a clear verdict", "Try clean tap water or murky water with one click", "Runs fully in the browser — no backend, no waiting"])
add(3, "Tech Stack", ["Python + scikit-learn: dataset generation and model training", "Logistic regression (C = 1.0) on 9 standardised features", "HTML, CSS and vanilla JavaScript for the interactive demo", "GitHub for source control, Vercel for free hosting"])
add(4, "Architecture", ["Dataset: 1,000 synthetic water samples modelled on the classic water-potability data", "Readings -> standardisation -> logistic regression -> sigmoid -> potability probability", "model.json ships with the site; JavaScript applies the same formula", "Training script: train.py; site generator: gen_site.py"])
add(5, "Live Demo", ["Try it: enter your readings and press Check My Water", "Clean tap water: pH 7.0, TDS 15,000, turbidity 3.0 -> about 86.6% potable", "Murky water: pH 6.2, TDS 45,000, turbidity 6.2 -> about 0.3% potable — do not drink", f"Demo: https://{DOMAIN}"])
add(6, "Results", ["5-fold cross-validation accuracy: 68.2%, AUC: 0.74", "Baseline (always guessing the most common class): 54.8% — a clear lift", "Potable rate in the data: 45.2%; clean samples score above 95%, worst samples below 1%", "Browser demo matches Python probabilities exactly on all test samples"])
add(7, "Future Scope", ["Train on the real water-potability dataset with measured lab samples", "Add WHO guideline flags — highlight each reading that breaks a safe limit", "Add a photo-based turbidity estimate from a phone camera", "Support regional languages, starting with Telugu, for village health workers"])
add(8, "Thank You", ["AquaSafe — Drinking Water Potability Checker", "Vikranth Reddy, B.Tech CSE (AI & ML), Woxsen University", "Source: github.com/HVRGAMING2705/aquasafe", "Questions welcome!"])
prs.save("/home/hatch/workspace/goals/daily-ai-ml-project-factory/files/AIML_AquaSafe_2026-11-10.pptx")
print("slides:", len(prs.slides._sldIdLst))
