from pydantic import BaseModel


class IMUReading(BaseModel):
    ts: int
    ax: float
    ay: float
    az: float
    gx: float
    gy: float
    gz: float
    fsr: int
