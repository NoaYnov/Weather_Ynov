import requests
import json

link ="https://public-api.meteofrance.fr/public/DPClim/v1/liste-stations/infrahoraire-6m?id-departement=10&parametre=temperature"

token = "eyJ4NXQiOiJOelU0WTJJME9XRXhZVGt6WkdJM1kySTFaakZqWVRJeE4yUTNNalEyTkRRM09HRmtZalkzTURkbE9UZ3paakUxTURRNFltSTVPR1kyTURjMVkyWTBNdyIsImtpZCI6Ik56VTRZMkkwT1dFeFlUa3paR0kzWTJJMVpqRmpZVEl4TjJRM01qUTJORFEzT0dGa1lqWTNNRGRsT1RnelpqRTFNRFE0WW1JNU9HWTJNRGMxWTJZME13X1JTMjU2IiwidHlwIjoiYXQrand0IiwiYWxnIjoiUlMyNTYifQ.eyJzdWIiOiI0YzhkMTg0Ny01OTdhLTRhYWUtOGQ3ZS0wMTg5NzU1OTc2YmMiLCJhdXQiOiJBUFBMSUNBVElPTiIsImF1ZCI6InNabDR0eWFlSjl1N0FQWWQ4a2ZXZkhBcUJxOGEiLCJuYmYiOjE3NDM2ODE0MTIsImF6cCI6InNabDR0eWFlSjl1N0FQWWQ4a2ZXZkhBcUJxOGEiLCJzY29wZSI6ImRlZmF1bHQiLCJpc3MiOiJodHRwczpcL1wvcG9ydGFpbC1hcGkubWV0ZW9mcmFuY2UuZnJcL29hdXRoMlwvdG9rZW4iLCJleHAiOjE3NDM2ODUwMTIsImlhdCI6MTc0MzY4MTQxMiwianRpIjoiYzRlODgwYzYtMjAzMC00YmFkLWI4NzEtZDlkNTdiZTFlMWE0IiwiY2xpZW50X2lkIjoic1psNHR5YWVKOXU3QVBZZDhrZldmSEFxQnE4YSJ9.xAdxsFz_q0iTkVJHlF2C-yE_7ZJ3zl0CYY3_RLZMIz3DlDvhaNnQSurfRwmc0IbXd9elyxUiS2EKzjw57eh67sDah7A20NuKPspIOYMtcvqxv_z88pE8fV-us7HpEVwSENY1L01MwGSvmMfhs6pgrs5jcnSkaEuRKsd2n88__38F2E7rqgf1FhR8tkU9XUFIIReFGzjihaP3qkZ7LEnI2dgugTjv-xUA0EtBcICYlBoWCej0dcEUC_CRxbdF5x2rD2OEulKP80vW7RcklAZ_9NfM5zMFhDyCKqQFOSDqWjBZ0PZWfKcP9EyOEawvpnMvVb5iQo5vI9pHtiQcviK0yQ"




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