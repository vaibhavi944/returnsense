# 📦 ReturnSense: The Intelligent E-commerce Return Mitigation Ecosystem

### 🚀 [Live Demo: View ReturnSense on Streamlit Cloud](https://returnsense-n2l74ghdjscawr45pivydt.streamlit.app/)

**ReturnSense** is a production-grade AI ecosystem designed to solve one of the most expensive problems in e-commerce: **Customer Returns.** 

By fusing **Predictive Machine Learning**, **Explainable AI (XAI)**, and **Agentic Prescriptive Reasoning**, ReturnSense doesn't just predict a return—it explains the root cause and provides actionable strategies to prevent it.

---

## 🎯 The Business Case: Why ReturnSense?
- **The Financial Drain:** E-commerce returns cost retailers over **$760 billion** annually in the US alone.
- **The Environmental Cost:** Returns generate **15 million tons of CO2** emissions and **5 billion pounds of landfill waste** every year.
- **The ReturnSense Solution:** By identifying high-risk orders *before* they are shipped, businesses can intervene (e.g., offering a discount for keeping the item, verifying size via chat) to save revenue and reduce their carbon footprint.

---

## 🏛️ The Three Pillars of the System

### 1. The Predictive Engine (XGBoost)
The "Brain" of the system. It analyzes historical patterns to assign a probability score to new orders.
- **Recall-Focused Tuning:** In returns mitigation, missing a return is more expensive than a false alarm. We tuned the model for **Recall > 80%**.
- **Leakage Prevention:** Features like `product_return_rate` are calculated strictly on training data to ensure the model doesn't "cheat" by seeing the future.

### 2. The Explainability Layer (SHAP)
AI shouldn't be a black box. ReturnSense uses **SHAP (SHapley Additive exPlanations)** to break down every prediction.
- **Human-Readable Insights:** Instead of showing raw math, the system translates SHAP values into insights like *"High risk due to historical return rates for this category"* or *"Customer age is a driving factor for this prediction."*

### 3. The Agentic Recommendation Engine (Llama 3.1 via Groq)
The system transitions from **Predictive** (what will happen) to **Prescriptive** (what to do).
- **LLM Reasoning:** A Generative AI Agent (Llama 3.1) analyzes the specific data and generates custom business strategies for the seller, such as updating size charts or improving product imagery.

---

## 🏗️ Technical Architecture & Workflow
1. **Data Ingestion:** Processed CSV data with structured return categories (Size, Damage, Defect).
2. **Feature Engineering:** Automated pipeline to compute customer/product return velocities and categorical encoding.
3. **Training & Logging:** Model training with **XGBoost**, using **MLflow** for experiment tracking.
4. **Smart Inference:** A Streamlit-based "In-App" engine that loads serialized models (`.pkl`) and runs live scoring.
5. **Agentic Loop:** Groq-powered LLM analyzes the context and provides a strategy JSON.

---

## 📂 Project Anatomy

```text
returnsense/
├── dashboard/
│   ├── app.py                     # Entry point for the Cloud Dashboard
│   └── pages/
│       ├── 1_Executive_Overview.py # Macro-level business metrics
│       ├── 3_Seller_Intelligence.py # Deep-dive into seller performance
│       ├── 4_Order_Risk_Scorer.py   # Live ML Inference with SHAP explanations
│       └── 5_Recommendation_Engine.py # Groq-powered Agentic insights
├── src/
│   ├── predictor/
│   │   ├── data_loader.py         # Leakage-safe train/test splitting
│   │   ├── feature_builder.py     # Advanced feature engineering & mapping
│   │   ├── train.py               # XGBoost training pipeline with class weighting
│   │   ├── evaluate.py            # Custom thresholding for High Recall
│   │   └── explain.py             # SHAP TreeExplainer integration
│   └── agent/
│       └── agent.py               # Generative AI Logic (Groq Llama 3.1)
├── data/
│   └── processed/                 # Refined datasets for model training
├── models/                        # Serialized model artifacts (.pkl files)
├── requirements.txt               # Project dependencies
└── build.sh                       # Automation script for cloud deployment
```

---

## 🛠️ Tech Stack
- **Languages:** Python 3.10+
- **Machine Learning:** XGBoost, Scikit-Learn
- **Explainability:** SHAP
- **Generative AI:** Groq (Llama 3.1 8B)
- **Dashboard:** Streamlit
- **MLOps:** MLflow
- **Containerization:** Docker (optional)

---

## 🚀 Deployment & Installation

### Local Setup
1. **Clone & Install:**
   ```bash
   pip install -r requirements.txt
   ```
2. **Train the AI:**
   ```bash
   python -m src.predictor.train
   ```
3. **Run the Dashboard:**
   ```bash
   streamlit run dashboard/app.py
   ```

### Cloud Deployment (Streamlit Cloud)
1. Push this repo to GitHub.
2. Connect the repo to **Streamlit Community Cloud**.
3. Add your **GROQ_API_KEY** in the "Secrets" setting.
4. Launch and click **"Initialize AI"** on the main page to build the models live!

---

## 🛡️ Security & Scalability
- **Secrets Management:** Sensitive keys are never hardcoded; they are managed via `.env` or Streamlit Secrets.
- **Fail-Safe Design:** The recommendation engine has a built-in "Fallback Mode" to ensure the app never crashes even if the LLM API is unavailable.
- **Modular Code:** The `src/` directory is decoupled from the UI, allowing the ML engine to be used in a mobile app or a different backend in the future.

---
*Developed as a Production-Grade AI Portfolio Project.*
