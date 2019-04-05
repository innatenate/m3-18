import sentry_sdk
from sentry_sdk import capture_exception


def error_report(error, name="None"):
	sentry_sdk.init("https://2ddb4d5c3837499fa686086f9e70fbc5@sentry.io/1429670", server_name=name)
	capture_exception(error)
	print("This error has been successfully reported.")
