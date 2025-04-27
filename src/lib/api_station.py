import requests
import json

link ="https://public-api.meteofrance.fr/public/DPClim/v1/liste-stations/horaire?id-departement=13&parametre=temperature"


token = "eyJ4NXQiOiJOelU0WTJJME9XRXhZVGt6WkdJM1kySTFaakZqWVRJeE4yUTNNalEyTkRRM09HRmtZalkzTURkbE9UZ3paakUxTURRNFltSTVPR1kyTURjMVkyWTBNdyIsImtpZCI6Ik56VTRZMkkwT1dFeFlUa3paR0kzWTJJMVpqRmpZVEl4TjJRM01qUTJORFEzT0dGa1lqWTNNRGRsT1RnelpqRTFNRFE0WW1JNU9HWTJNRGMxWTJZME13X1JTMjU2IiwidHlwIjoiYXQrand0IiwiYWxnIjoiUlMyNTYifQ.eyJzdWIiOiI0YzhkMTg0Ny01OTdhLTRhYWUtOGQ3ZS0wMTg5NzU1OTc2YmMiLCJhdXQiOiJBUFBMSUNBVElPTiIsImF1ZCI6InNabDR0eWFlSjl1N0FQWWQ4a2ZXZkhBcUJxOGEiLCJuYmYiOjE3NDU3NTcwMzIsImF6cCI6InNabDR0eWFlSjl1N0FQWWQ4a2ZXZkhBcUJxOGEiLCJzY29wZSI6ImRlZmF1bHQiLCJpc3MiOiJodHRwczpcL1wvcG9ydGFpbC1hcGkubWV0ZW9mcmFuY2UuZnJcL29hdXRoMlwvdG9rZW4iLCJleHAiOjE3NDU3NjA2MzIsImlhdCI6MTc0NTc1NzAzMiwianRpIjoiMjY1ZmUzYTAtZmYzMC00NjYzLTkwMzgtMzhkNDkzNjE4NmM0IiwiY2xpZW50X2lkIjoic1psNHR5YWVKOXU3QVBZZDhrZldmSEFxQnE4YSJ9.BTPyuw64bNEoB78Ykwbeeaw2_7d8rj5r29I1Qfz8OzOVt2WM81MT-tpM8pNnQht-NC0aJwdOgqR-3BPM3gvnpRX4IOCckl2txBbFYMh87wyyXzdERL7bXtum7K4EmIhl75LcqrTOkK6orfoY9tkNg1ei3vVrxEeJd-A-OrTR6Xp-dqzNYx6alDm5mf_wU4qWQLGc2XQzzJgaOmiLhkePaIWpYJPA_hnJ_QgSVJIseAzIlWgdPgij-Y0D9flMj2MCncj_zcBn728XR_eDr5O8UHTWY-CGvNs19VLpqxtlxYH6jCRnDfnRtbhluFaQTCkN6rDjJiRGoBTACAEz7qNnaA"




def fetch_api():
    headers = {
        'Authorization': 'Bearer ' + token,
        'Content-Type': 'application/json'
    }

    response = requests.get(link, headers=headers)

    if response.status_code == 200:
        print("API is reachable.")
        print("Response JSON:")
        return response.json()
    else:
        print(f"API returned an error: {response.status_code} - {response.text}")
        

def write_json_to_file(data, filename):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)
    print(f"Data written to {filename}")




def main():
    write_json_to_file(fetch_api(), "files/stations/13.json")
    
    
if __name__ == "__main__":
    main()
    