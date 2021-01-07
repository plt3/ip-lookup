import asyncio

import aiohttp

from webApp.errors import ASNPrefixError, IPDetailsError


async def getAllInfo(ipAddress, isValid):
    """Main coroutine to obtain all info (IP address details and ASN prefixes) from
    given IP address

    :ipAddress (str): IP address to get information about
    :isValid (bool): whether IP address string looks anything like an IP address. This
    is determined by validateIp function in validate.py
    :returns: tuple containing list of IP prefixes associated with IP address and dict
    of each ASN prefix associated with IP address and IP prefixes associated with that
    ASN

    """
    # abort if IP address did not pass initial validation by isValid function
    if not isValid:
        return None, None

    # asynchronous context manager to make any sort of asynchronous HTTP requests
    async with aiohttp.ClientSession() as mainSession:
        # make both requests asking for IP details and IP prefixes associated to ASNs
        ipDetails, asns = await getIPDetails(ipAddress, mainSession)
        asnPrefixes = await getAsnPrefixes(asns, mainSession)

    # change any instance of None in nested objects to more meaningful string
    changeNone(ipDetails)
    changeNone(asnPrefixes)

    return ipDetails, asnPrefixes


async def getIPDetails(ipAddress, session):
    """Coroutine to get details about given IP address using "View IP Address
    Details" API endpoint

    :ipAddress (str): IP address to get details about
    :session (aiohttp.ClientSession): session object in order to perform asynchronous
    HTTP requests
    :returns: tuple containing list of IP prefixes associated to IP address and list
    of ASNs associated with IP address

    """
    ipDetailEndpoint = f"https://api.bgpview.io/ip/{ipAddress}"

    ipDetailJson = await getJson(ipDetailEndpoint, session)

    # raise IPDetailsError in case API responds unexpectedly
    if ipDetailJson["status"] == "error":
        raise IPDetailsError('"View IP Address Details" API endpoint raised an error.')

    # only need list of prefixes from returned JSON, the rest is unimportant
    prefixList = ipDetailJson["data"]["prefixes"]

    # create list of ASNs from list of IP prefixes
    asnList = [prefix["asn"]["asn"] for prefix in prefixList]

    return prefixList, asnList


async def getAsnPrefixes(asnList, session):
    """Coroutine to get all IP prefixes associated with each ASN in given list of ASNs

    :asnList (list): list of ASNs as integers, usually is second element of tuple
    returned by getIPDetails coroutine
    :session (aiohttp.ClientSession): session object in order to perform asynchronous
    HTTP requests
    :returns: dict with each ASN in asnList as keys and with list of IP prefixes as
    values

    """
    # create list of non-executed getJson coroutines for all ASNs to asynchronously
    # query the API
    asnTasks = [
        getJson(f"https://api.bgpview.io/asn/{asn}/prefixes", session)
        for asn in asnList
    ]

    # query the API and return the information in the order in which it was requested
    # (important because the IP prefix data would otherwise get mixed up)
    asnPrefixes = await asyncio.gather(*asnTasks)

    asnInfoDict = {}

    # loop through asnList and asnPrefixes (since they are the same length) to populate
    # dict
    for asn, prefixData in zip(asnList, asnPrefixes):
        # raise ASNPrefixError in case API response unexpectedly
        if prefixData["status"] == "error":
            raise ASNPrefixError('"View ASN Prefixes" API endpoint raised an error.')

        asnData = []

        # replace ugly API information about IP type with cleaner string
        for prefixType in prefixData["data"]:
            if prefixType == "ipv4_prefixes":
                shortPrefixType = "IPv4"
            else:
                shortPrefixType = "IPv6"
            for prefix in prefixData["data"][prefixType]:
                prefix["type"] = shortPrefixType
                # append individual prefix to prefix list associated with ASN
                asnData.append(prefix)

        # populate dictionary with ASNs and associated prefix lists
        asnInfoDict[asn] = asnData

    return asnInfoDict


async def getJson(url, session):
    """Simple coroutine to asynchronously retrieve JSON from specified API endpoint

    :url (str): API endpoint to query
    :session (aiohttp.ClientSession): session object in order to perform asynchronous
    HTTP GET request
    :returns: JSON response converted to a Python list or dict

    """

    async with session.get(url) as response:
        jsonResp = await response.json()

    return jsonResp


def changeNone(listOrDict):
    """Recursively walk through nested list or dict (obtained from API JSON response)
    and change any instances of None with specified replacement string to clean
    up appearance of rendered HTML tables

    :listOrDict (list or dict): list or dict with values to replace in it
    :returns: None, because this function alters the parameter in place

    """
    noneReplacement = "not specified"

    # iterate through each item in listOrDict depending on its type
    if isinstance(listOrDict, list):
        for element in listOrDict:
            changeNone(element)
    elif isinstance(listOrDict, dict):
        for key in listOrDict:
            if listOrDict[key] is None:
                listOrDict[key] = noneReplacement
            else:
                changeNone(listOrDict[key])
