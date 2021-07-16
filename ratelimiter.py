import time
import sys
from math import floor
from functools import wraps
import threading

def now():
    if hasattr(time, 'monotonic'):
        return time.monotonic
    return time.time

class RateLimitException(Exception):
    def __init__(self, message, period_remaining):
        super(RateLimitException, self).__init__(message)
        self.period_remaining = period_remaining

class RateLimitDecorator:
    def __init__(self, calls, period, clock=now(), raise_on_limit=True):
        self.allowed_calls = calls
        self.period = period
        self.clock = clock
        self.raise_on_limit = raise_on_limit

        # Initialise the decorator state.
        self.last_reset = clock()
        self.num_calls = 0

        # Add thread safety.
        self.lock = threading.RLock()

    def __call__(self, func):

        wraps(func)
        def wrapper(*args, **kwargs):
            with self.lock:
                period_remaining = self.__period_remaining()

                # If the time window has elapsed then reset.
                if period_remaining <= 0:
                    self.num_calls = 0
                    self.last_reset = self.clock()

                # Increase the number of attempts to call the function.
                self.num_calls += 1

                # If the number of attempts to call the function exceeds the
                # maximum then raise an exception.
                if self.num_calls > self.allowed_calls:
                    if self.raise_on_limit:
                        raise RateLimitException('too many calls', period_remaining)
                    return
            return func(*args, **kwargs)
        return wrapper

    def __period_remaining(self):
        elapsed = self.clock() - self.last_reset
        return self.period - elapsed