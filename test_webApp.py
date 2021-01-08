import pytest
from fastapi.testclient import TestClient

from webApp import app

client = TestClient(app)

# obviously invalid IP addresses
invalidIps = ["random_string", "not an ip!", "Hello World", "1.256.98.34"]

# I know that these IPs have these associated ASNs
ipAsnPairs = [("73.143.190.5", 7922), ("2a05:dfc7:60::", 50546)]


def test_home():
    """home page should give 200 status code and give user instructions"""

    response = client.get("/")

    assert response.status_code == 200, "home returned non-200 response"
    assert (
        "Enter an IP address above" in response.text
    ), "home did not give instructions"


@pytest.mark.parametrize("invalidIp", invalidIps)
def test_invalid_ips(invalidIp):
    """home page should provide error information when entering an invalid IP address"""

    params = {"ip": invalidIp}
    response = client.get("/", params=params)

    assert response.status_code == 200, "home returned non-200 response"
    assert (
        f'"{invalidIp}" is not a valid IP address' in response.text
    ), "home did not inform user about invalid IP address"
    assert (
        "Enter an IP address above" in response.text
    ), "home did not give instructions"


@pytest.mark.parametrize("validIp, associatedAsn", ipAsnPairs)
def test_valid_ips(validIp, associatedAsn):
    """home page should return tables with information for valid IP address"""

    params = {"ip": validIp}
    response = client.get("/", params=params)

    assert response.status_code == 200, "home returned non-200 response"
    assert (
        f"Detailed information for {validIp}" in response.text
    ), "no details about IP address"
    assert (
        f"IP Prefixes for AS{associatedAsn}" in response.text
    ), "no ASN prefixes for IP address"
    assert (
        "Click to show" in response.text
    ), "no click to show button for ASN prefixes table"
    assert "Back to top" in response.text, "no back to top button in response"

    # there should be at least 2 tables created (4 instances of "table" because of
    # opening and closing HTML tags)
    assert (
        response.text.count("table") >= 4
    ), "home did not make at least 2 tables for a valid IP address"


def test_redirect():
    """any request for a resource that doesn't exist should redirect to home"""

    response = client.get("/does_not_exist")

    assert response.status_code == 200, "home returned non-200 response"
    assert (
        "Enter an IP address above" in response.text
    ), "home did not give instructions"
