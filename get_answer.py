import math
from fastapi import FastAPI
from fastapi.responses import PlainTextResponse

app = FastAPI()


@app.get("/4berkeates_gmail_com", response_class=PlainTextResponse)
def calculate_lcm(x: str = "", y: str = "") -> str:
    if not (x.isdecimal() and y.isdecimal()):
        return "NaN"

    num_x = int(x)
    num_y = int(y)

    if num_x == 0 or num_y == 0:
        return "NaN"

    result = math.lcm(num_x, num_y)
    return str(result)