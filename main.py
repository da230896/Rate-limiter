from utility import SECOND, HOUR, WEEK, MONTH
from ratelimiter import RateLimitDecorator, RateLimitException
from flask import request
from clients import clientBasedRateLimiters
import flask

app = flask.Flask("Rate limiting checking app")

@app.errorhandler(RateLimitException)
def handle_rate_limit(error):
    return str(error)

@app.errorhandler(Exception)
def handle_rate_limit(error):
    return str(error)

@app.route('/status', methods=['GET'])
@RateLimitDecorator(1000, MONTH)
@RateLimitDecorator(900, WEEK)
@RateLimitDecorator(40, HOUR)
@RateLimitDecorator(20, SECOND)
def status():
    # this can be added as decorator as well but let it be
    if request.headers.get("client_id") == None or clientBasedRateLimiters[request.headers.get("client_id")] == None:
        raise Exception("Invalid Client Id")
    print("Client Id is ", request.headers.get("client_id"))
    clientBasedRateLimiters[request.headers.get("client_id")]()
    response = '''
                    <h1>Status fetching endpoint</h1>
                    <p>This endpoint is a prototype API for checking rate limit functionality.</p>
                '''
    
    return response

app.run()







