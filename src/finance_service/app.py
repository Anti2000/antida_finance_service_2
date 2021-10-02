from fastapi import FastAPI

from . import accounts
from . import auth
from . import shops
from . import categories
from . import operations
from .middleware import QueryStringFlatteningMiddleware

app = FastAPI()
app.add_middleware(QueryStringFlatteningMiddleware)

accounts.initialize_app(app)
auth.initialize_app(app)
shops.initialize_app(app)
categories.initialize_app(app)
operations.initialize_app(app)

# уменьшить время жизни токена в settings.toml!!!!
