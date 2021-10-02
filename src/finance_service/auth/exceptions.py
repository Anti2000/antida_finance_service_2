from ..exceptions import ClientError


class AccountNotFound(ClientError):
    pass


class InvalidCredentialsError(ClientError):
    pass
