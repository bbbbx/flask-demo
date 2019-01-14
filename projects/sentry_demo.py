from raven import Client

client = Client('Sentry 的 DSN')

try:
    1 / 0
except ZeroDivisionError:
    client.captureException()

