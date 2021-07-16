# Rate limiter (Traffic shaping)

We are solving (Partially) below mentioned problem:

Requirement:
      Create framework that can throttle client requests in distributed system.
      Throttling could be on multiple level i.e per client, per endpoint etc.
      In case client limit has breached the framework should reject the request with appropriate http status.
      This framework can be included in any service to throttle client requests accross all its instances.

Exmaple:
client: E-COM
limit:
     HOUR -> 100
     WEEK -> 900
     MONTH  -> 10000
specialization:
    type: METHOD
      - GET :
      limit:
        SEC -> 10
        MIN -> 50
        WEEK -> 700
      - POST :
      limit:
        SEC -> 20
        HOUR -> 40
        WEEK -> 900
        MONTH -> 1000

type: API
 - /status :
       limit:
         SEC -> 20
         HOUR -> 40
         WEEK -> 900
         MONTH -> 1000
 - /pay :
       limit:
         SEC -> 10
         MIN -> 50
         WEEK -> 700
