from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app = FastAPI()

# register javascript file in static directory
app.mount("/static", StaticFiles(directory="webApp/static"), name="static")

# register Jinja2 templates in templates directory
templates = Jinja2Templates(directory="webApp/templates")

# must import app routes after creating FastAPI instance to avoid circular import
from webApp import routes
