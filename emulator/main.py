from dataclasses import dataclass
from io import BytesIO
from typing import Annotated, Dict

import cv2
from fastapi import FastAPI, Form, Depends
from starlette.responses import StreamingResponse

from emulator import Emulator
from model.canvas import Canvas
from model.catapult import Catapult

app = FastAPI()
emulator = Emulator(Catapult, Canvas(300, 300))


@app.get("/")
async def root():
    return {"message": "Hello World"}


@dataclass
class ShootForm:
    angleHorizontal: float = Form(...)
    angleVertical: float = Form(...)
    power: float = Form(...)
    colors: Dict[str, int] = Form(...)


@app.post("/art/ballista/shoot")
async def shoot(data: ShootForm = Depends()):
    emulator.shoot(data.angleHorizontal, data.angleVertical, data.power, data.colors)
    return {"status": "success"}


@app.get("/canvas")
def get_canvas():
    canvas = emulator.canvas
    buffer = BytesIO()
    canvas.to_pil().save(buffer, format="PNG")
    buffer.seek(0)
    return StreamingResponse(buffer, media_type="image/png")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
