<!-- Message Caching -->
(***https://spec.openapis.org/oas/latest.html***)
You can enable API caching in Amazon API Gateway to cache your endpoint's response. With caching, you can reduce the number of calls made to your backend and also improve the latency of the requests to your API. When you enable caching for a stage, API Gateway caches responses from your backend for a specified time-to-live (TTL) period, in seconds. API Gateway then responds to the request by looking up the endpoint response from the cache instead of making a request to your endpoint.

NOTE: Caching is best-effort. You can use the CacheHitCount and CacheMissCount metrics in Amazon CloudWatch  to monitor requests that API Gateway serves from the API cache.

API Gateway enables caching at the stage or method level. In this section, you will create a new resource called medianPriceCalculator. This service returns the median price of houses in US or Canada. Since these regional prices do not change often, you can cache the results.

<!-- Test the resource that has caching enabled -->
Now that we have created our second resource in the API, it's time to test it. Notice that the medianPriceCalculator service gives the median house price for three regions (US, CA and BR). Since we are caching based on the region parameter, the responses from ?region=US will be cached separately from the response from ?region=CA and ?region=BR.

Let's test the API request using curl .

Follow lab docs to testing the enabled caching on the method using the listed command below:

$ curl --request POST '[insert your invoke URL here]/medianpricecalculator?region=BR' | python -m json.tool

