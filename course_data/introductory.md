---
marp: true
theme: default
paginate: true
header: 'IPAM USL · Introduction to AI (Introductory)'
footer: 'SLPTA · Route R12 · Solomon Wilson MBCS'
---

<!-- _paginate: false -->
<!-- _header: '' -->
<!-- _footer: '' -->

# Introduction to Artificial Intelligence
## Building Intelligent Systems — *Introductory tier*

**IPAM USL** · 5 weeks · 3 days/week · Google Colab (zero-install)
**Facilitator:** Solomon Wilson MBCS

> Running scenario all course: **Route R12** (Wilberforce → CBD), operator **OP-104**, a **25-minute delay**.

---

## How this course works

- **Content** follows the IPAM syllabus faithfully: classical ML → neural networks → LLM apps.
- **Delivery** keeps strict Introductory-tier discipline: one concept per day, *predict-then-run*, fill-one-blank exercises.
- **Every example** uses synthetic **SLPTA** data — no campus, mobile-money, or generic demos.
- **Four graded deliverables:** problem statement (D5), ethics checklist (D12), project brief (D14), presentation (D15).

---

## The 15-day map

- **Week 1 — Module 1 starts:** What is AI? · Data prep · Classification
- **Week 2:** Regression · Unsupervised (+ Deliverable 1) · How neural nets learn
- **Week 3 — Module 2:** First Keras net · Transfer learning · First LLM call
- **Week 4 — Module 3 starts:** Prompt engineering · Gradio app · Responsible AI (+ Deliverable 2)
- **Week 5:** Capstone build · Refine + brief (Deliverable 3) · Presentations (Deliverable 4)

---

## One mental model per day (L1–L15)

- **L1–L5:** rules vs learning · data as fuel · classification · regression · clustering
- **L6–L8:** how a neuron learns · building a network · transfer learning
- **L9–L10:** calling an LLM · prompting as specification
- **L11–L12:** notebook → app · responsible AI
- **L13–L15:** capstone — build · refine · present

---

<!-- _backgroundColor: '#dbe4ff' -->
# Module 1 — Foundations & ML Essentials
### Days 1–5

> **R12 hook:** Dispatch got 40 angry calls about R12's delay. Can a computer learn to *triage* the complaints, *predict* the delay, and *group* operators — all from data?

---

## Day 1 — What Is AI? Rules → Learning · L1

- **Concept:** traditional code *follows* a rule we write; machine learning *finds* the rule from examples.
- **R12 demo:** hand-label 10 passenger complaints, then a keyword rule labels them (scores 9/10 — good but brittle).
- **Exercise:** add one keyword; see which labels change.
- **Remember:** *AI learns the rule from examples; code follows the rule we wrote.*

---

## Day 2 — Data Is the Fuel · L2

- **Concept:** clean before you model — missing values, duplicates, outliers, encoding, train/test split.
- **R12 demo:** clean the route log (impute weather, drop a 600-minute typo), then split.
- **Exercise:** change `test_size`; watch train/test counts move.
- **Remember:** *a model is only as good as the data you feed it.*

---

## Day 3 — Classification · L3

- **Concept:** predict a category — *badly delayed: yes/no*. Decision Tree + KNN; confusion matrix.
- **R12 demo:** flag badly-delayed trips — ~80% accuracy, but **recall only ~51%** (it misses half!).
- **Exercise:** tune `max_depth`; write the manager's memo.
- **Remember:** *accuracy hides which mistakes you make — a missed delay costs most.*

---

## Day 4 — Regression & Honest Evaluation · L4

- **Concept:** predict a *number* (minutes late). MAE, R², overfitting, cross-validation.
- **R12 demo:** the simple linear model (MAE ~4.7 min) beats an overfit forest (train 2.0 / test 5.3).
- **Exercise:** drop a feature — `cause_category` collapses R² from 0.58 to 0.18.
- **Remember:** *trust the test error, not the training error.*

---

## Day 5 — Unsupervised + Module 1 Wrap · L5

- **Concept:** find groups with **no labels** — k-means + PCA to see them.
- **R12 demo:** cluster 20 operators into reliable / average / needs-support.
- **Deliverable 1 (15%):** one-page problem statement for your capstone.
- **Remember:** *clustering finds the groups; you give them meaning.*

---

<!-- _backgroundColor: '#e5dbff' -->
# Module 2 — Neural Networks & Modern AI
### Days 6–10

> **R12 hook:** From flagging R12's delay to *drafting its passenger SMS* — we open up neural networks and language models.

---

## Day 6 — How a Neuron Learns · L6

- **Concept:** a neuron = inputs × weights + bias → activation; it learns by lowering a loss.
- **R12 demo:** train one neuron by hand — accuracy climbs 72% → 81%; *mechanical fault* earns the biggest weight.
- **Exercise:** change the learning rate; watch the loss curve.
- **Remember:** *learning = small downhill steps that lower the loss.*

---

## Day 7 — Building a Neural Network (Keras) · L7

- **Concept:** stack `Dense` layers; compile (optimizer + loss); read training vs validation curves.
- **R12 demo:** a 16→8→1 network hits ~82% — and the curves show overfitting begin.
- **Exercise:** change the hidden-layer size; watch the gap widen.
- **Remember:** *the validation curve tells you when it stops learning and starts memorising.*

---

## Day 8 — Transfer Learning · L8

- **Concept:** reuse a model pre-trained on millions of images; freeze it, train only a small head.
- **R12 demo:** classify synthetic fleet cards (roadworthy / minor / grounded) with MobileNetV2.
- **Exercise:** train for more epochs; a frozen base converges fast.
- **Remember:** *reuse the giant model's eyes; teach only the last layer.*

---

## Day 9 — Calling an LLM through an API · L9

- **Concept:** an LLM predicts the next token; an API sends a prompt and returns text.
- **R12 demo:** summarise the incident report, classify a complaint, extract fields with Gemini.
- **Exercise:** write your own grounded instruction about R12.
- **Remember:** *give it the facts in the prompt — and verify before acting.*

---

## Day 10 — Prompting as Specification · L10

- **Concept:** zero-shot vs few-shot; system instructions; structured (JSON) output.
- **R12 demo:** few-shot complaint routing, a JSON incident record, a Krio passenger SMS.
- **Exercise:** change the tone of the SMS.
- **Remember:** *a prompt is a specification — be explicit and show examples.*

---

<!-- _backgroundColor: '#d3f9d8' -->
# Module 3 — Build & Present
### Days 11–15

> **R12 hook:** Turn the R12 delay-risk model into a tool a dispatcher can *click* — then stand up and present it.

---

## Day 11 — From Notebook to App · L11

- **Concept:** an app = model + UI + input/output handling. Gradio builds it in a few lines.
- **R12 demo:** wrap the complaint classifier so a dispatcher uses it with zero code.
- **Exercise:** change the app title and examples.
- **Remember:** *an app is a model plus a door users can open.*

---

## Day 12 — Responsible AI · L12

- **Concept:** an *accurate* model can still be *unfair* or wrong; grounding guards hallucination.
- **R12 demo:** the delay model flags Heavy Rain 84% vs Sunny 15% — fair to pre-warn, unfair to rank operators.
- **Deliverable 2 (10%):** AI Ethics Checklist (≥2 risks + mitigations).
- **Remember:** *check who it affects and where it's weakest before you deploy.*

---

## Day 13 — Capstone Build, Session 1 · L13

- **Goal:** a first working version — data pipeline, model/API, initial UI.
- **Reference:** TIA Lite (delay-risk + Gradio) as a template to adapt to *your* Deliverable 1 problem.
- **Two paths:** classical ML (no key) or LLM (needs key).
- **Check-in:** show the three blocks running; note one fix for tomorrow.

---

## Day 14 — Capstone Build, Session 2 · L14

- **Goal:** test with edge cases, refine one weakness, document.
- **Loop:** build → test → fix → repeat; stress-test like a real dispatcher.
- **Deliverable 3:** one-page project brief (problem, data, model, results, limits, deployment).
- **Remember:** *a demo that works once is not yet a tool people can trust.*

---

## Day 15 — Presentations & Closing · L15

- **Format:** 8-minute demo + 4-minute Q&A; arc = problem → data → demo → limits → next.
- **Deliverable 4 (30%):** the live presentation, scored on the four-level rubric.
- **Self-check:** Correctness · Grounding · Clarity · Safety (pass = Proficient+ on each).
- **Close:** keep your notebooks as a portfolio; find real SLPTA problems a small honest model helps.

---

<!-- _backgroundColor: '#dbe4ff' -->
<!-- _paginate: false -->

# From R12 to a working AI tool

- In 15 days: *"can a computer learn the rule?"* → a deployed delay-risk app.
- Difficulty scaled through **capability**, not story — one R12 thread throughout.
- Honest about limits at every step: when **not** to trust the model.

**Thank you — questions?**
