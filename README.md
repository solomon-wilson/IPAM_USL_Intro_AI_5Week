# IPAM USL — Introduction to Artificial Intelligence (5-Week Short Course)

**Tier:** Introductory · **Audience:** IPAM USL IT/IS Year 3 & 4 students
**Mode:** Google Colab (zero-install) · **Running scenario:** SLPTA dispatch desk, **Route R12** (Wilberforce → CBD), operator OP-104, 25-minute delay
**Facilitator:** Solomon Wilson MBCS

This repository delivers the IPAM *Introduction to Artificial Intelligence: Building Intelligent Systems* syllabus, rebuilt so that **every example uses synthetic SLPTA transit data** and every session follows CS50-style, first-principles pedagogy.

---

## The teaching contract (read this first)

This course reconciles two things that pull in different directions, exactly as agreed:

1. **Content = the IPAM syllabus, followed faithfully.** The arc is classical ML → neural networks → LLM applications, using the real toolchain (scikit-learn, Keras/TensorFlow, Gemini, Gradio). Nothing from the approved syllabus is dropped.
2. **Delivery = strict Introductory-tier discipline** (from the `malan-course-design` method):
 - **70 / 30 scaffold** — students *run, predict, and fill one blank*; no writing functions from scratch.
 - **Predict → then run** — a prediction checkpoint sits before every demo cell.
 - **One new concept per day** — a single mental-model layer per session.
 - **Jargon defined on first use**; short sentences; SLPTA analogies only.
 - **Submission checklist** closing every notebook.
 - **Route R12 thread throughout** — no campus, mobile-money, jollof, or generic "chat with AI" examples.

> **The one deliberate relaxation:** the Malan Introductory tier normally restricts packages to `google-genai` only. That is impossible for a syllabus whose first eight days *are* scikit-learn and Keras. So we relax **only** the package restriction — scikit-learn and Keras are allowed where the syllabus needs them — and keep every other intro-tier rule strict.

---

## Mental-model ladder (one layer per day)

The original Malan ladder (L1–L6) is LLM-centric. We extend it to L1–L15 so each classical-ML day also gets a single, named mental model. The notebook header always states its layer.

| Layer | Day | Concept |
|-------|-----|---------|
| L0 | 0 | Python is the toolbox |
| L1 | 1 | Rules vs. learning |
| L2 | 2 | Data as fuel (cleaning, encoding, splitting) |
| L3 | 3 | Supervised classification |
| L4 | 4 | Supervised regression & honest evaluation |
| L5 | 5 | Unsupervised learning (clustering, PCA) |
| L6 | 6 | How neural networks learn |
| L7 | 7 | Building a neural network |
| L8 | 8 | Transfer learning (pre-trained CNNs) |
| L9 | 9 | Calling an LLM through an API |
| L10 | 10 | Prompt engineering as specification |
| L11 | 11 | From notebook to application |
| L12 | 12 | Responsible AI & limits |
| L13–15| 13–15 | Capstone: build, refine, present |

---

## The 15-day plan (SLPTA reskin of the IPAM syllabus)

Cadence: **3 days/week × 5 weeks**. "Module" follows the IPAM syllabus; "Status" tracks the build batches.

| Day | Wk | Module | Session | SLPTA reskin (replaces the syllabus's generic example) | Status |
|----:|---:|:------:|---------|--------------------------------------------------------|--------|
| 1 | 1 | 1 | What Is AI? Rules → Learning | Hand-label R12 passenger complaints, then beat a keyword rule | ✅ built |
| 2 | 1 | 1 | Data Is the Fuel | Clean the synthetic `route_logs` (delays, weather, operators) | ✅ built |
| 3 | 1 | 1 | Classification | Predict *badly delayed* trips (Decision Tree + KNN) | ✅ built |
| 4 | 2 | 1 | Regression & Evaluation | Predict delay **minutes**; MAE, R², overfitting, cross-validation | ✅ built |
| 5 | 2 | 1 | Unsupervised + Module 1 wrap | Cluster operators/routes by performance; PCA; **Deliverable 1 due (15%)** | ✅ built |
| 6 | 2 | 2 | How Neural Networks Learn | TensorFlow Playground framed as a delay-risk separator | ✅ built |
| 7 | 3 | 2 | First Neural Network (Keras) | Delay-risk net on tabular `route_logs`; read training curves | ✅ built |
| 8 | 3 | 2 | Transfer Learning (CNNs) | Classify synthetic **fleet-condition / signage** images (MobileNetV2) | ✅ built |
| 9 | 3 | 2 | LLM APIs | Summarise R12 incident report, zero-shot classify, and extract fields using Gemini | ✅ built |
| 10 | 4 | 3 | Prompt Engineering | Optimize prompts with few-shot learning, system instructions, and JSON formatting | ✅ built |
| 11 | 4 | 3 | Notebook to App | Build and deploy a clickable dispatch interface using Gradio | ✅ built |
| 12 | 4 | 3 | Responsible AI & Limits | Analyze operational bias and complete Ethics Checklist; **Deliverable 2 due (10%)** | ✅ built |
| 13 | 5 | 3 | Capstone Build — Part 1 | Construct end-to-end data pipelines, predictive models, and UI interfaces | ✅ built |
| 14 | 5 | 3 | Capstone Build — Part 2 | Perform edge-case tests, peer checkups, and draft the project brief; **Deliverable 3 due** | ✅ built |
| 15 | 5 | 3 | Capstone Presentations | Present working SLPTA AI prototypes to evaluation panel; **Deliverable 4 due** | ✅ built |

---

## Graded Deliverables

Each of the four milestones counts toward the final course grade:

*   **Deliverable 1 (15%):** One-page Capstone Problem Statement (Submitted Day 5)
*   **Deliverable 2 (10%):** AI Ethics & Risk Mitigation Checklist (Submitted Day 12)
*   **Deliverable 3:** Technical Project Brief (Submitted Day 14)
*   **Deliverable 4:** Live Capstone Presentation & Self-Assessment (Assessed Day 15)
