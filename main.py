from fastapi import FastAPI, Request, HTTPException

app = FastAPI()

@app.post("/webhook")
async def receive_webhook(request: Request):
    try:
        payload = await request.json()
        print("Received webhook payload:", payload)
        return {"status": "success"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
