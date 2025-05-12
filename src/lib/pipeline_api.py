import time
import requests
import os

##### Clé Api a modifier si plus valide #####
API_KEY = "Bearer eyJ4NXQiOiJOelU0WTJJME9XRXhZVGt6WkdJM1kySTFaakZqWVRJeE4yUTNNalEyTkRRM09HRmtZalkzTURkbE9UZ3paakUxTURRNFltSTVPR1kyTURjMVkyWTBNdyIsImtpZCI6Ik56VTRZMkkwT1dFeFlUa3paR0kzWTJJMVpqRmpZVEl4TjJRM01qUTJORFEzT0dGa1lqWTNNRGRsT1RnelpqRTFNRFE0WW1JNU9HWTJNRGMxWTJZME13X1JTMjU2IiwidHlwIjoiYXQrand0IiwiYWxnIjoiUlMyNTYifQ.eyJzdWIiOiJhNjI5YTQyMC0yYTMwLTQxZDYtYjE0MC0wZDQzY2MzZDIzYWYiLCJhdXQiOiJBUFBMSUNBVElPTiIsImF1ZCI6InNhWmtURWR1Um50d0xocktVTmRHWWJKVXM3Y2EiLCJuYmYiOjE3NDcwMzg5NjcsImF6cCI6InNhWmtURWR1Um50d0xocktVTmRHWWJKVXM3Y2EiLCJzY29wZSI6ImRlZmF1bHQiLCJpc3MiOiJodHRwczpcL1wvcG9ydGFpbC1hcGkubWV0ZW9mcmFuY2UuZnJcL29hdXRoMlwvdG9rZW4iLCJleHAiOjE3NDcwNDI1NjcsImlhdCI6MTc0NzAzODk2NywianRpIjoiMDMxOTY4YTQtNWM0MC00MjVhLWE4ZjktYTIwZjFhMmMyYTAwIiwiY2xpZW50X2lkIjoic2Faa1RFZHVSbnR3TGhyS1VOZEdZYkpVczdjYSJ9.CxPSfBdTP5pXv-O1pfw7rINYCu3s4J6qEGpmCFhw_kAaU_lZNv-gCYNVM0LR8Jt51v5tUqVkE1NghBX-d0tmoNVOuH_tUtlbdxNxz4JRbXSQnt2tr9rQDTNsusmD3yvXcXlptrhjwKImPwMB_tKFROjW9Tn3z6nJqsu3CGPOENTiMT13JChTQyuTKNuF2oSyJT0h17zmT_61YXfSqk1k7MJg1kHk8uOzLe9XDN_tZiEKsvSGHL4OTcREa9CwV8a8e_pDD4rJJnz5GG4qWht93McqCoaPX2w3OxSuXlgycrvrEgx9aDEIYsKYPrPySHYaQuHwpyNv2wA7Lk6sOhLKFQ"
##### Id station a changer selon la région #####
id_station = "13001009"
nom_ville = "Aix_en_Provence" ## Remplacer les tirets du 6(-) par ceux du 8(_)
##### Dates juste l'année, elles sont traitées après #####
date_debut = 2020 #AAAA
date_fin = 2022 #AAAA
##### Urls & Headers #####
url_commande = 'https://public-api.meteofrance.fr/public/DPClim/v1/commande-station/quotidienne'
url_csv = 'https://public-api.meteofrance.fr/public/DPClim/v1/commande/fichier'

headers = {
    "accept": "*/*",
    "Authorization": API_KEY
}
##### Chemin Dossier #####
chemin_dossier = "data"
os.makedirs(chemin_dossier, exist_ok=True)

##### Boucle sur chaque année #####
for annee in range(date_debut, date_fin + 1):
    print(f"\n📅 Traitement année : {annee}")

    date_debut_param = f"{annee}-01-01T00:00:00Z"
    date_fin_param = f"{annee}-12-31T23:59:59Z"

    params_commande_station = {
        "id-station": id_station,
        "date-deb-periode": date_debut_param,
        "date-fin-periode": date_fin_param
    }

    # Étape 1 : Demande de la commande
    response_cmd = requests.get(url_commande, headers=headers, params=params_commande_station)

    if response_cmd.status_code == 202:
        response_command = response_cmd.json()
        id_commande = response_command["elaboreProduitAvecDemandeResponse"]["return"]
        print("✅ Requête commande réussie - ID:", id_commande)
        time.sleep(5)

        # Étape 2 : Récupération du CSV
        params_csv = {"id-cmde": id_commande}
        response_csv = requests.get(url_csv, headers=headers, params=params_csv)
        time.sleep(5)
        if response_csv.status_code == 201:
            print("✅ Réception du CSV réussie")
            nom_fichier = f"{annee}_{nom_ville}_data_brut.csv"
            chemin_complet = os.path.join(chemin_dossier, nom_fichier)
            with open(chemin_complet, "w", encoding="utf-8") as f:
                f.write(response_csv.text)
            print(f"📁 Fichier sauvegardé sous : {chemin_complet}")
        else:
            print(f"❌ Erreur récupération CSV ({annee}) : {response_csv.status_code} - {response_csv.text}")
        time.sleep(5)
    else:
        print(f"❌ Erreur commande ({annee}) : {response_cmd.status_code} - {response_cmd.text}")