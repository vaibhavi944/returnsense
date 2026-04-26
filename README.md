# ReturnSense

ReturnSense is a production-grade AI system designed to predict, classify, and mitigate e-commerce returns. By combining traditional machine learning (XGBoost) with state-of-the-art Generative AI agents, ReturnSense provides comprehensive visibility and actionable recommendations for businesses.

## Architecture

1. **Machine Learning Pipeline:** End-to-end data processing, feature engineering, and model training with XGBoost and MLflow integration.
2. **Explainability Layer:** SHAP TreeExplainer converts complex model predictions into human-readable insights.
3. **FastAPI Backend:** Production-ready REST and WebSocket APIs serving real-time predictions.
4. **Agentic Recommendation System:** Context-aware LLM agents that analyze seller metrics and product flaws to provide actionable remedies.
5. **Streamlit Dashboard:** Interactive, multi-page visualization tool for Executive Overview, Product/Seller Intelligence, and Live Scoring.

## Features
- **Zero Data Leakage:** Aggregated historical features map strictly to test data.
- **Class Imbalance Handling:** Tuned `scale_pos_weight` ensures high recall for potential returns.
- **Explainable AI:** Top three driving factors for each prediction provided directly to the dashboard.
- **Real-Time Scoring:** WebSocket integration allows instant risk assessment as users shop.
- **Containerized:** Fully Dockerized ecosystem via `docker-compose`.

## Setup Instructions

### Local Development
1. **Clone the repository.**
2. **Install requirements:**
   ```bash
   pip install -r requirements.txt
   ```
3. **Train the Model:**
   ```bash
   python -m src.predictor.train
   ```
   *This outputs models to `models/` and logs via MLflow.*
4. **Run the API:**
   ```bash
   uvicorn src.api.main:app --reload
   ```
5. **Run the Dashboard:**
   ```bash
   streamlit run dashboard/app.py
   ```

### Docker
To spin up both the API and the Dashboard:
```bash
docker-compose up --build
```
API will be on port `8000`, Dashboard on `8501`.

## API Documentation
Interactive docs available at `http://localhost:8000/docs`

### Endpoints
- `POST /predict-return-risk`: Send an order payload, receive risk score and top SHAP reasons.
- `POST /classify-return`: Predict category and confidence of unstructured return text.
- `GET /seller-intelligence/{seller_id}`: Retrieve seller-level aggregation statistics.
- `POST /generate-recommendations`: Generative AI agent providing strategic steps to reduce returns.
- `WS /realtime-scoring`: Stream order info via WebSockets for live alerts.

![Screenshots placeholders]
*(Screenshot 1: Executive Dashboard)*
*(Screenshot 2: Real-time Order Risk Scorer)*
