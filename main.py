from typing import Optional

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.exceptions import HTTPException as StarletteHTTPException

from errors import ASNPrefixError, IPDetailsError
from utils import getAllInfo
from validate import validateIp

app = FastAPI()

# register javascript file in static directory
app.mount("/static", StaticFiles(directory="static"), name="static")

# register Jinja2 templates in templates directory
templates = Jinja2Templates(directory="templates")

# TODO: add docstrings/comments, would be cool if IP address field
# autopopulated to user's IP address,
# do some form of testing


@app.get("/", response_class=HTMLResponse)
async def home(request: Request, ip: Optional[str] = None):
    cleanIp, isIpValid = validateIp(ip)

    error = None
    ipDetails = None
    asnPrefixes = None

    try:
        ipDetails, asnPrefixes = await getAllInfo(cleanIp, isIpValid)
        print("got em")
    except IPDetailsError as ipError:
        error = str(ipError)
    except ASNPrefixError as asnError:
        error = str(asnError)
    except Exception:
        error = "There was an error querying the API."

    infoDict = {
        "request": request,
        "error": error,
        "ip": cleanIp,
        "isIpValid": isIpValid,
        "ipDetails": ipDetails,
        "asnPrefixes": asnPrefixes,
    }

    # import json

    # if isIpValid:
    #     # with open("ipDetails.json", "w") as f:
    #     with open("ipDetails.json") as f:
    #         # json.dump(ipDetails, f, indent=2)
    #         ipDetails = json.load(f)
    #     # with open("asnPrefixes.json", "w") as f:
    #     with open("asnPrefixes.json") as f:
    #         # json.dump(asnPrefixes, f, indent=2)
    #         asnPrefixes = json.load(f)

    # infoDict = {
    #     "request": request,
    #     "ip": cleanIp,
    #     "error": error,
    #     "isIpValid": isIpValid,
    #     "ipDetails": ipDetails,
    #     "asnPrefixes": asnPrefixes,
    # }

    return templates.TemplateResponse("home.html", infoDict)


@app.exception_handler(StarletteHTTPException)
async def test(request: Request, exc: StarletteHTTPException):
    return RedirectResponse("/")
