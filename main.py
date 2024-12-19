from fastapi import FastAPI, Request, HTTPException
from src.webhook_utils import get_response

app = FastAPI()

@app.post("/webhook")
async def receive_webhook(request: Request):
    try:
        payload = await request.json()
        # print("Received webhook payload:", payload)
        result = get_response(payload)
        return {"status": "success"}
    except Exception as e:
        print(e)
        raise HTTPException(status_code=400, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
