from typing import Optional

from fastapi import Request
from fastapi.responses import HTMLResponse, RedirectResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

from webApp import app, templates
from webApp.errors import ASNPrefixError, IPDetailsError
from webApp.queryApi import getAllInfo
from webApp.validate import validateIp


@app.get("/", response_class=HTMLResponse)
async def home(request: Request, ip: Optional[str] = None):
    """Main view function housing all functionality of web app

    :request (fastapi.Request): Required to return any response template
    :ip (str): IPv4 or IPv6 address as a string to get information about. If not
    included, will show basic IP address search form
    :returns: fastapi.templating.Jinja2Templates.TemplateResponse for HTML page of
    web app

    """
    # perform quick initial validation to avoid querying API for non-IP address string
    cleanIp, isIpValid = validateIp(ip)

    error = None
    ipDetails = None
    asnPrefixes = None

    # query API and handle any possible error that may arise from API
    try:
        ipDetails, asnPrefixes = await getAllInfo(cleanIp, isIpValid)
    except IPDetailsError as ipError:
        error = str(ipError)
    except ASNPrefixError as asnError:
        error = str(asnError)
    except Exception:
        # general handler for an sort of unexpected error
        error = "There was an error querying the API."

    # information to pass onto Jinja2 template to render in HTML
    infoDict = {
        "request": request,
        "error": error,
        "ip": cleanIp,
        "isIpValid": isIpValid,
        "ipDetails": ipDetails,
        "asnPrefixes": asnPrefixes,
    }

    return templates.TemplateResponse("home.html", infoDict)


@app.exception_handler(StarletteHTTPException)
async def test(request: Request, exc: StarletteHTTPException):
    """Small error handling route to redirect to main page if any page is not found

    :request (fastapi.Request): required parameter for starlette error handler
    :exc (starlette.exceptions.HTTPException): second required parameter for starlette
    error handler
    :returns: fastapi.responses.RedirectResponse to redirect user to home page

    """
    return RedirectResponse("/")
