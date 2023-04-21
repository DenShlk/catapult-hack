from dataclasses import dataclass
from io import BytesIO
from typing import Dict

from fastapi import FastAPI, Depends, Body
from starlette.responses import StreamingResponse

from emulator import Emulator
from simple_catapult import SimpleCatapult
from model.canvas import Canvas

app = FastAPI()
emulator = Emulator(SimpleCatapult, Canvas(250, 250))


@app.get("/")
async def root():
    return {"message": "Hello World"}


@dataclass
class ShootBody:
    angleHorizontal: float = Body(...)
    angleVertical: float = Body(...)
    power: float = Body(...)
    colors: Dict[str, int] = Body(...)


@app.post("/art/ballista/shoot")
async def shoot(data: ShootBody = Depends()):
    colors = {int(k): v for k, v in data.colors.items()}
    emulator.shoot(data.power, data.angleHorizontal, data.angleVertical, colors)
    return {"status": "success"}


@dataclass
class AimBody:
    x: int = Body(...)
    y: int = Body(...)
    amount: int = Body(...)
    color: int = Body(...)


@app.post("cheat/auto-aim")
async def auto_aim(data: AimBody = Depends()):
    emulator.auto_aim(data.x, data.y, data.amount, data.color)
    return {"status": "success"}


@app.post("/art/ballista/shoot-aim")
async def shoot_aim(data: AimBody = Depends()):
    emulator.shoot_aim(data.x, data.y, data.amount, data.color)
    return {"status": "success"}

@app.get("/canvas")
def get_canvas():
    canvas = emulator.canvas
    buffer = BytesIO()
    canvas.to_pil().save(buffer, format="BMP")
    buffer.seek(0)
    return StreamingResponse(buffer, media_type="image/png")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
