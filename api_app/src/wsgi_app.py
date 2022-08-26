from sentry_sdk.integrations.wsgi import SentryWsgiMiddleware

from main import app

app = SentryWsgiMiddleware(app)
