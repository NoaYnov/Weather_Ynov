import requests
import json

link ="https://public-api.meteofrance.fr/public/DPClim/v1/liste-stations/infrahoraire-6m?id-departement=10&parametre=temperature"

token = "eyJ4NXQiOiJOelU0WTJJME9XRXhZVGt6WkdJM1kySTFaakZqWVRJeE4yUTNNalEyTkRRM09HRmtZalkzTURkbE9UZ3paakUxTURRNFltSTVPR1kyTURjMVkyWTBNdyIsImtpZCI6Ik56VTRZMkkwT1dFeFlUa3paR0kzWTJJMVpqRmpZVEl4TjJRM01qUTJORFEzT0dGa1lqWTNNRGRsT1RnelpqRTFNRFE0WW1JNU9HWTJNRGMxWTJZME13X1JTMjU2IiwidHlwIjoiYXQrand0IiwiYWxnIjoiUlMyNTYifQ.eyJzdWIiOiI0YzhkMTg0Ny01OTdhLTRhYWUtOGQ3ZS0wMTg5NzU1OTc2YmMiLCJhdXQiOiJBUFBMSUNBVElPTiIsImF1ZCI6InNabDR0eWFlSjl1N0FQWWQ4a2ZXZkhBcUJxOGEiLCJuYmYiOjE3NDM3NDkwOTYsImF6cCI6InNabDR0eWFlSjl1N0FQWWQ4a2ZXZkhBcUJxOGEiLCJzY29wZSI6ImRlZmF1bHQiLCJpc3MiOiJodHRwczpcL1wvcG9ydGFpbC1hcGkubWV0ZW9mcmFuY2UuZnJcL29hdXRoMlwvdG9rZW4iLCJleHAiOjE3NDM3NTI2OTYsImlhdCI6MTc0Mzc0OTA5NiwianRpIjoiZWNkNTRlZWQtMzdhNC00MTUyLWI4YmEtNDljZGVhN2Q2ZjE3IiwiY2xpZW50X2lkIjoic1psNHR5YWVKOXU3QVBZZDhrZldmSEFxQnE4YSJ9.WU8geqIV1Zgv6dKK8lqzmDtMVNTXvNQhsa_SeC71VUh8yt4vwL1i68cxUC6UMhbeO6yikksFNssGj1tfJ-IC1DWPZIFp-spYyLf_a82sHM7iBptce2lOksnrA4j3F59RffEnuQzCNmZCW5YfIK6FiIEUZNDi1wf_vEhFV_cGzmlPKQXXkiWHNfeo9y5ByEqgwtQ-_Xh2Yt-A3QAD7JUVcHdtZn14AzQAWlSu9Eorba7eZAF_zlYurWllD_QAhhkThA_6zMm2GqTNiINC_ocSSQawJbaeo9PaZaquSWmsJKlsky05ZWHm5AXz-woxrn_0MnuphE6XFcbRg9SjFENcWg"




def test_api():
    headers = {
        'Authorization': 'Bearer ' + token,
        'Content-Type': 'application/json'
    }

    response = requests.get(link, headers=headers)

    if response.status_code == 200:
        print("API is reachable.")
        print("Response JSON:")
        print(json.dumps(response.json(), indent=4))
    else:
        print(f"API returned an error: {response.status_code} - {response.text}")
        
test_api()