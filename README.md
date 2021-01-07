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

## Screenshots:
### Main page once server is running:
![web app home page](images/homePage.png)
### Form validation for search bar:
![web app form validation](images/formValidation.png)
### ASN prefix tables are collapsed by default when searching:
![web app IPv4 search](images/ipv4Search.png)
### Can search for IPv6 address as well as IPv4:
![web app IPv6 search](images/ipv6Search.png)
### Click on "Click to show" to display ASN prefix tables:
![web app IPv4 results](images/ipv4Results.png)
### Tables can have lots of results:
![web app IPv6 results](images/ipv6Results.png)
