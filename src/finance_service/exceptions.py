class BaseServiceError(Exception):
    pass


class ClientError(BaseServiceError):
    pass


class ServerError(BaseServiceError):
    pass
