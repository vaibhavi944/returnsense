from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from src.api.routes import router
import json
import asyncio

app = FastAPI(title="ReturnSense API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)

@app.websocket("/realtime-scoring")
async def realtime_scoring(websocket: WebSocket):
    await websocket.accept()
    from src.api.routes import predict_return_risk
    from src.api.schemas import OrderPredictRequest
    
    try:
        while True:
            data = await websocket.receive_text()
            order_data = json.loads(data)
            request = OrderPredictRequest(**order_data)
            
            result = await predict_return_risk(request)
            
            response = {
                "order_id": request.order_id,
                "risk_score": result.return_probability,
                "risk_level": result.risk_level,
                "top_reasons": result.top_reasons,
                "flag_alert": result.return_probability > 0.7
            }
            
            await websocket.send_json(response)
    except WebSocketDisconnect:
        print("Client disconnected")
    except Exception as e:
        await websocket.send_json({"error": str(e)})
