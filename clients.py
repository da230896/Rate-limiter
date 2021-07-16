from utility import HOUR, WEEK, MONTH
from ratelimiter import RateLimitDecorator, RateLimitException

@RateLimitDecorator(10000, MONTH)
@RateLimitDecorator(900, WEEK)
@RateLimitDecorator(100, HOUR)
def rate_limit_for_ecom():
    print("Rate limiting for E-Com client passed")

clientBasedRateLimiters = {
    'E-Com': rate_limit_for_ecom
}