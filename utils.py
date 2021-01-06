import asyncio

import aiohttp


async def getAllInfo(ipAddress):
    """TODO: Docstring for getAllInfo.

    :ipAddress: TODO
    :returns: TODO

    """
    if ipAddress is None:
        return None, None

    # THIS NEEDS A LOT OF ERROR HANDLING!!!!! (IF USER ENTERS RANDOM STRING, NOT IP)

    async with aiohttp.ClientSession() as mainSession:
        ipDetails, asns = await getIPDetails(ipAddress, mainSession)
        asnPrefixes = await getAsnPrefixes(asns, mainSession)

    return ipDetails, asnPrefixes


async def getIPDetails(ipAddress, session):
    """TODO: Docstring for getIPDetails.

    :ipAddress: TODO
    :session: TODO
    :returns: TODO

    """
    ipDetailEndpoint = f"https://api.bgpview.io/ip/{ipAddress}"

    ipDetailJson = await getJson(ipDetailEndpoint, session)

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

    # return {asn: prefixData["data"] for asn, prefixData in zip(asnList, asnPrefixes)}
    return asnInfoDict


async def getJson(url, session):
    """TODO: Docstring for getJson.

    :url: TODO
    :session: TODO
    :returns: TODO

    """

    # should probably have more error handling here

    async with session.get(url) as response:
        print(response.status)
        jsonResp = await response.json()

    return jsonResp


if __name__ == "__main__":
    asyncio.run(getAllInfo("73.143.190.5"))
    # asyncio.run(getAllInfo("2620:119:35::35"))
