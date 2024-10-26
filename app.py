from fastapi import FastAPI, HTTPException
from main import take_screenshot  # Import your selenium script functions here

app = FastAPI()

@app.get("/capture/{chart}/{timeframe}")
async def capture(chart: str, timeframe: str):
    try:
        screenshot_path = take_screenshot(chart, timeframe)
        return {"screenshot_path": screenshot_path}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

#uvicorn app:app --port=8000 --reload 