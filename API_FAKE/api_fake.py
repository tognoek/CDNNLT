from fastapi import FastAPI # type: ignore
from fastapi.responses import JSONResponse # type: ignore
import json

app = FastAPI()

@app.get("/hot_destination")
async def read_json():
    with open("hot_destination.json", "r", encoding="utf-8") as file:
        data = json.load(file)
    return JSONResponse(content=data)
@app.get("/list_tour")
async def read_json():
    with open("list_tour.json", "r", encoding="utf-8") as file:
        data = json.load(file)
    return JSONResponse(content=data)
@app.get("/list_tour_all")
async def read_json():
    with open("list_tour_all.json", "r", encoding="utf-8") as file:
        data = json.load(file)
    return JSONResponse(content=data)

# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app, host="0.0.0.0", port=8000)
