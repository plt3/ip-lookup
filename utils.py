import asyncio

import aiohttp

from errors import ASNPrefixError, IPDetailsError


async def getAllInfo(ipAddress, isValid):
    """TODO: Docstring for getAllInfo.

    :ipAddress: TODO
    :isValid: TODO
    :returns: TODO

    """
    if not isValid:
        return None, None

    async with aiohttp.ClientSession() as mainSession:
        ipDetails, asns = await getIPDetails(ipAddress, mainSession)
        asnPrefixes = await getAsnPrefixes(asns, mainSession)

    changeNone(ipDetails)
    changeNone(asnPrefixes)

    return ipDetails, asnPrefixes


async def getIPDetails(ipAddress, session):
    """TODO: Docstring for getIPDetails.

    :ipAddress: TODO
    :session: TODO
    :returns: TODO

    """
    ipDetailEndpoint = f"https://api.bgpview.io/ip/{ipAddress}"

    ipDetailJson = await getJson(ipDetailEndpoint, session)

    if ipDetailJson["status"] == "error":
        raise IPDetailsError('"View IP Address Details" API endpoint raised an error.')

    prefixList = ipDetailJson["data"]["prefixes"]
    asnList = [prefix["asn"]["asn"] for prefix in prefixList]

    return prefixList, asnList


async def getAsnPrefixes(asnList, session):
    """TODO: Docstring for getAsnPrefixes.

    :asnList: TODO
    :session: TODO
    :returns: TODO

    """
    asnTasks = [
        getJson(f"https://api.bgpview.io/asn/{asn}/prefixes", session)
        for asn in asnList
    ]
    asnPrefixes = await asyncio.gather(*asnTasks)

    asnInfoDict = {}

    for asn, prefixData in zip(asnList, asnPrefixes):
        if prefixData["status"] == "error":
            raise ASNPrefixError('"View ASN Prefixes" API endpoint raised an error.')

        asnData = []

        for prefixType in prefixData["data"]:
            if prefixType == "ipv4_prefixes":
                shortPrefixType = "IPv4"
            else:
                shortPrefixType = "IPv6"
            for prefix in prefixData["data"][prefixType]:
                prefix["type"] = shortPrefixType
                asnData.append(prefix)

        asnInfoDict[asn] = asnData

    return asnInfoDict


async def getJson(url, session):
    """TODO: Docstring for getJson.

    :url: TODO
    :session: TODO
    :returns: TODO

    """

    async with session.get(url) as response:
        jsonResp = await response.json()

    return jsonResp


def changeNone(listOrDict):
    """TODO: Docstring for removeNone.

    :listOrDict: TODO
    :returns: TODO

    """
    noneReplacement = "not specified"

    if isinstance(listOrDict, list):
        for element in listOrDict:
            changeNone(element)
    elif isinstance(listOrDict, dict):
        for key in listOrDict:
            if listOrDict[key] is None:
                listOrDict[key] = noneReplacement
            else:
                changeNone(listOrDict[key])
