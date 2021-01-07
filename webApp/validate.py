import ipaddress


def validateIp(userIp):
    """Small function to determine if string looks like an IP address in order to avoid
    querying the API when user inputs a nonsensical string

    :userIp (str): IP address that user inputs
    :returns: tuple containing a cleaned-up version of the entered IP address (e.g
    converting '1.1.01.1' to '1.1.1.1') and bool of whether the entered IP address
    seems to be valid

    """
    if userIp is None:
        # return None and invalid if there is no search string
        return None, False
    try:
        # try to create IPv4Address or IPv6Address object from string, which is the
        # only way for function to return that IP address is valid
        return str(ipaddress.ip_address(userIp)), True
    except ValueError:
        # otherwise, return original string saying that it is invalid
        return userIp, False
