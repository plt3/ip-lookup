from typing import Optional

from fastapi import Request
from fastapi.responses import HTMLResponse, RedirectResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

from webApp import app, templates
from webApp.errors import ASNPrefixError, IPDetailsError
from webApp.utils import getAllInfo
from webApp.validate import validateIp


@app.get("/", response_class=HTMLResponse)
async def home(request: Request, ip: Optional[str] = None):
    """Main view function housing all functionality of web app

    :request (fastapi.Request): Required to return any response template
    :ip (str): IPv4 or IPv6 address as a string to get information about. If not
    included, will show basica IP address search form
    :returns: fastapi.templating.Jinja2Templates.TemplateResponse for HTML page of
    web app

    """
    cleanIp, isIpValid = validateIp(ip)

    error = None
    ipDetails = None
    asnPrefixes = None

    try:
        ipDetails, asnPrefixes = await getAllInfo(cleanIp, isIpValid)
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
