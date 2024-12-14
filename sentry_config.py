import sentry_sdk
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Function to initialize Sentry SDK for error tracking and performance monitoring


def initialize_sentry():
    sentry_dsn = os.getenv("SENTRY_DSN")
    if not sentry_dsn:
        raise ValueError("Sentry DSN not found. Please set it in your .env file.")

    sentry_sdk.init(
        dsn=sentry_dsn,
        # Set traces_sample_rate to 1.0 to capture 100% of transactions for tracing.
        traces_sample_rate=1.0,
    )

    # Optional: Example profiling usage
    def slow_function():
        import time
        time.sleep(0.1)
        return "done"

    def fast_function():
        import time
        time.sleep(0.05)
        return "done"

    # Manually call start_profiler and stop_profiler to profile the code in between
    sentry_sdk.profiler.start_profiler()
    for i in range(0, 10):
        slow_function()
        fast_function()

    # Calls to stop_profiler are optional
    sentry_sdk.profiler.stop_profiler()
