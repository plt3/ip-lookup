from typing import Optional

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from utils import getAllInfo

app = FastAPI()

templates = Jinja2Templates(directory="templates")


# TODO: get functionality, add docstrings/comments, would be cool if IP address field
# autopopulated to user's IP address


@app.get("/", response_class=HTMLResponse)
async def home(request: Request, ip: Optional[str] = None):
    # ipDetails, asnPrefixes = await getAllInfo(ip)

    import json

    ipDetails = None
    asnPrefixes = None

    if ip is not None:
        with open("ipDetails.json") as f:
            ipDetails = json.load(f)
        with open("asnPrefixes.json") as f:
            asnPrefixes = json.load(f)

    infoDict = {
        "request": request,
        "ip": ip,
        "ipDetails": ipDetails,
        "asnPrefixes": asnPrefixes,
    }
    return templates.TemplateResponse("home.html", infoDict)
