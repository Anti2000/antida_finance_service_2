from ..exceptions import ClientError


class OperationCategoryNotFound(ClientError):
    pass


class OperationShopNotFound(ClientError):
    pass
