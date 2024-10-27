from fastapi import FastAPI, HTTPException
from main import take_screenshot, take_screenshots  # Ensure these functions exist in main.py

app = FastAPI()

@app.get("/capture/{chart}/{timeframe}")
async def capture(chart: str, timeframe: str):
    try:
        screenshot_path = take_screenshot(chart, timeframe)
        return {"screenshot_path": screenshot_path}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/capture/{timeframe}")
async def capture_all_charts(timeframe: str):
    try:
        screenshot_paths = take_screenshots(timeframe)  # Call function to capture all charts for a timeframe
        return {"screenshot_paths": screenshot_paths}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Run with: uvicorn app:app --port=8000 --reload
