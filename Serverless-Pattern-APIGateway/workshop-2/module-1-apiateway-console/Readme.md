<!-- Module Goals -->
- Create your first API
- Transform Request / Response Payload
- Build validations for requests
- Create and Configure Authentication and Authorization with Cognito and IAM
- Deploy API
- Configure Cache
- Configure Usage Plans

<!-- Some of the commands used for the labs -->


$ aws cognito-idp admin-initiate-auth --user-pool-id us-east-1_2c9wzwK8p --client-id 2356r0k2a7k6hc8kfhtv14jgg6 --auth-flow ADMIN_NO_SRP_AUTH --auth-parameters 'USERNAME=testUser,PASSWORD="testUser123!"'



$ aws cognito-idp admin-respond-to-auth-challenge --user-pool-id us-east-1_2c9wzwK8p  --client-id 2356r0k2a7k6hc8kfhtv14jgg6 --challenge-name NEW_PASSWORD_REQUIRED --challenge-responses 'USERNAME=testUser,NEW_PASSWORD=Test1234!,userAttributes.email=test@user.com' --session 'AYABeE_z1cGvTdz2WH5W9fy4ZGwAHQABAAdTZXJ2aWNlABBDb2duaXRvVXNlclBvb2xzAAEAB2F3cy1rbXMAS2Fybjphd3M6a21zOnVzLWVhc3QtMTo3NDU2MjM0Njc1NTU6a2V5L2IxNTVhZmNhLWJmMjktNGVlZC1hZmQ4LWE5ZTA5MzY1M2RiZQC4AQIBAHhR9E4zNbI1ofi3Y01_Ljgh2wK-ZaC__bKufjbgmejy4gFwLUkO07XoCn5Eo8QRFrE-AAAAfjB8BgkqhkiG9w0BBwagbzBtAgEAMGgGCSqGSIb3DQEHATAeBglghkgBZQMEAS4wEQQMz_pF1b_nZN5Ch52sAgEQgDsGyRbfjKgWdkOsOsWnmFOmd2Y0ar1fJ82J3iPHehhHKuFHPpK5VhTleIMVM0OmbSTAOffH67DBS8HMzAIAAAAADAAAEAAAAAAAAAAAAAAAAAClFGivHL14ExQpLa-sP0cu_____wAAAAEAAAAAAAAAAAAAAAEAAADacf2N97ps3V0aagKVAzAqP8ZRI-h2SytzUXr6_WrXXSuTY2UvpM0HO8Y4spTfHp1S__GYOihDxxAx0ID60RCLyNZwg25FzF8W5qiCpsf4_lpI4MOley3r9VJrbFD2z-R9ClVgwsqvWLRQ3rUspOF2bv-l-Q-F4oY3GqOPDwFc3gdyLBUSYUAtJXKpmTTsrBevIRrQ6Pkip_UDlvE5FXIe0GfOgSiazpKymEk1qioR5lCT6hvA4YCER5RtW0-T1RCIYi0G9hFV3rSr1bSKc0e5rjQecfJ8DpZDs03gi5e7P9dmOtJp7UxmW8Vj'




$ curl --location 'https://3acigw0x3f.execute-api.us-east-1.amazonaws.com/dev/pricePerMeter' \
--header 'Content-Type: application/json' \
--header 'Authorization: 'eyJraWQiOiJLNGpBY3lnS05LaVVIZ0NWb1wvN1kydGtZSVdva2pYVFJyMHN4TzU4WEhqYz0iLCJhbGciOiJSUzI1NiJ9eyJzdWIiOiJjNDk4YzRhOC0wMDUxLTcwODYtYWM2Yy1mYTE0ZjUxYjhhOTEiLCJpc3MiOiJodHRwczpcL1wvY29nbml0by1pZHAudXMtZWFzdC0xLmFtYXpvbmF3cy5jb21cL3VzLWVhc3QtMV8yYzl3endLOHAiLCJjb2duaXRvOnVzZXJuYW1lIjoidGVzdHVzZXIiLCJvcmlnaW5fanRpIjoiMzEzZTViNjYtMGM4Ni00ZGUyLWI5ZGMtNTcyMjRhZWJjMTY3IiwiYXVkIjoiMjM1NnIwazJhN2s2aGM4a2ZodHYxNGpnZzYiLCJldmVudF9pZCI6IjNiNDBkMDdkLTUxMmItNDY1Yi04MzBhLWFlZWIwM2YzYTM4NSIsInRva2VuX3VzZSI6ImlkIiwiYXV0aF90aW1lIjoxNzQ2NDUzNjY0LCJleHAiOjE3NDY0NTcyNjQsImlhdCI6MTc0NjQ1MzY2NCwianRpIjoiNTRhODk4ZTctOWM3YS00OTYxLWJiNTAtMmZmODU3YWM1OGMwIiwiZW1haWwiOiJ0ZXN0QHVzZXIuY29tIn0.etq-n7Mflea_hVOnUZoZsuOuJdoIFjdyFcmiFJBpd4EzenY3bfjTtBCXJLbjKtRRzt2k1LMJr_fthWEMKAy6jGf9ZMnLqLkiSHY9QX2nsrBSOwsZznzDJjP-roDxMsd-e5hAjp0ZoPd9JsMk7D6H83NjEitedRtr-RthyjxzpyVPA5znxzpH14l4KKRugI0hX0GXFAKi2d1zXuSSq-dtd2PywzhtoMPgKYXxp6DIBu0UtQXLuBVGcFlN0M6ATll7P5F6WsxX2yuQUNSrtWdIa4H-WlRnNLAbP98IZ0uhz8dUE4PsJiGkv9aj6KvN1brIrLgecRHFzPR_hH6TLxDurA' \
--data '{"price": 400000,"size": 1600,"unit": "sqFt","downPayment" : 20}'




$ curl --location 'https://3acigw0x3f.execute-api.us-east-1.amazonaws.com/dev/medianPriceCalculator?region=US' --header 'Content-Type: application/json' --data '{}' -w '\n===\nTotal time: %{time_total}s\n'