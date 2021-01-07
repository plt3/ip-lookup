class IPDetailsError(BaseException):
    """Error class for when BGPView API "View IP Address Details" endpoint returns an
    error in JSON body.

    """

    pass


class ASNPrefixError(BaseException):
    """Error class for when BGPView API "View ASN Prefixes" endpoint returns an error
    in JSON body.

    """

    pass
