# 📦 ReturnSense: End-to-End AI E-commerce Return Mitigation

### 🚀 [Live Demo: View ReturnSense on Streamlit Cloud](https://returnsense-n2l74ghdjscawr45pivydt.streamlit.app/)

![ReturnSense Dashboard Hero](https://via.placeholder.com/1000x500.png?text=ReturnSense+Dashboard+Preview+Click+Live+Demo+Above)
*Above: High-level overview of the ReturnSense Intelligence Command Center.*

**ReturnSense** is a production-grade AI ecosystem designed to solve one of the most expensive problems in e-commerce: **Product Returns.** 

By fusing **Predictive Machine Learning**, **Explainable AI (XAI)**, and **Agentic Prescriptive Reasoning**, ReturnSense doesn't just predict a return—it explains the root cause and provides actionable strategies to prevent it.

---

## 🎯 The Business Value
- **Profit Recovery:** E-commerce returns cost retailers over **$760B** annually. ReturnSense identifies high-risk orders *before* shipment, allowing for pre-delivery intervention.
- **Sustainability (ESG):** Every return prevented saves ~2.5kg of CO2 and 0.5kg of packaging waste. Our dashboard tracks these metrics in real-time.
- **Customer Loyalty:** By identifying common "Sizing" or "Quality" complaints via AI, sellers can fix product listings, leading to higher customer satisfaction.

---

## 🏛️ The Three Pillars of Technology

### 1. The Predictive Brain (XGBoost)
A highly tuned Machine Learning model that analyzes historical patterns to assign a probability score to new orders.
- **Recall: 82.76%** – Optimized to catch the maximum number of potential returns.
- **Precision: 30.00%** – Balanced to provide high-sensitivity alerts for risk management.
- **ROC-AUC: 0.51** – Predictive baseline built on historical category and user behavior.
- **Leakage-Safe Engineering:** Advanced feature engineering computes historical rates *strictly* on training data to prevent "future-data" contamination.

### 2. The Explainability Layer (SHAP)
AI shouldn't be a black box. ReturnSense uses **SHAP (SHapley Additive exPlanations)** to break down every score.
- **Contextual Reasoning:** Instead of raw math, the system provides insights like *"High risk due to historical return rates for this category"* or *"Customer order quantity suggests size wardrobing."*

### 3. The Agentic Strategy Engine (Groq Llama 3.1)
The system transitions from **Predictive** (what will happen) to **Prescriptive** (what to do).
- **LLM Intelligence:** A Generative AI Agent (Llama 3.1) analyzes seller history and customer complaints to generate custom business strategies, such as adding specific size charts or updating product imagery.

---

## 📂 Project Anatomy & Technical Logic

```text
returnsense/
├── dashboard/
│   ├── app.py                     # Entry point (Home Page with Feature Guide)
│   └── pages/
│       ├── 1_Business_Overview.py # Macro-level financial & CO2 metrics
│       ├── 2_Product_Performance.py# SKU-level diagnostics & age demographics
│       ├── 3_Regional_Performance.py# City-level leaderboard & savings forecast
│       ├── 4_Order_Risk_Scorer.py  # Live AI Inference with SHAP explanations
│       └── 5_Get_Advice.py        # Groq-powered Agentic business insights
├── src/
│   ├── predictor/
│   │   ├── data_loader.py         # Stratified train/test splitting
│   │   ├── feature_builder.py     # Categorical encoding & historical mapping
│   │   ├── train.py               # XGBoost training pipeline (v1.5 Strict Params)
│   │   ├── evaluate.py            # Custom thresholding for High Recall
│   │   └── explain.py             # SHAP TreeExplainer integration
│   └── agent/
│       └── agent.py               # Generative AI Logic (Llama 3.1 via Groq)
├── data/
│   └── processed/                 # Refined datasets (Classified via LLM)
├── models/                        # Serialized ML artifacts (.pkl)
├── requirements.txt               # Project dependencies
└── build.sh                       # Automation script for cloud deployment
```

---

## 🛠️ Tech Stack
- **AI/ML:** XGBoost, SHAP, Scikit-Learn
- **GenAI:** Groq (Llama 3.1 8B), Prompt Engineering
- **Data:** Pandas, Plotly (Interactive Charts)
- **Deployment:** Streamlit, GitHub, python-dotenv
- **Security:** Streamlit Secrets & Environment Variables

---

## 🚀 How to Run locally

1. **Clone and Install:**
   ```bash
   pip install -r requirements.txt
   ```
2. **Set up Keys:**
   Create a `.env` file and add `GROQ_API_KEY=your_key`.
3. **Train and Run:**
   ```bash
   python -m src.predictor.train
   streamlit run dashboard/app.py
   ```
