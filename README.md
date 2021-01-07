# ip-lookup
> FastAPI web app to view information about IP addresses

## Installation:
NOTE: tested for Mac, but installation on Linux or Windows should be similar.   
Requirements: Python 3.6+, Pip
- Clone repo with `git clone https://github.com/plt3/ip-lookup`
- Enter project directory with `cd ip-lookup`
- Recommended: create virtual environment: `python3 -m venv venv` and activate it: `source venv/bin/activate`
- Install dependencies with `pip install -r requirements.txt`

## Usage:
- In project home directory, run server with `uvicorn runApp:app`
- Navigate to http://localhost:8000 or http://127.0.0.1:8000 in browser
- When finished, kill the server with Ctrl + c
