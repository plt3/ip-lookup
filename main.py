from typing import Optional

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

app = FastAPI()

templates = Jinja2Templates(directory="templates")


# TODO: get functionality, add docstrings/comments, would be cool if IP address field
# autopopulated to user's IP address


@app.get("/", response_class=HTMLResponse)
async def home(request: Request, ip: Optional[str] = None):
    return templates.TemplateResponse("home.html", {"request": request, "ip": ip})
