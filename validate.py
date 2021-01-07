import ipaddress


def validateIp(userIp):
    """TODO: Docstring for validateIp.

    :userIp: TODO
    :returns: TODO

    """
    if userIp is None:
        return None, False
    try:
        return str(ipaddress.ip_address(userIp)), True
    except ValueError:
        return userIp, False
