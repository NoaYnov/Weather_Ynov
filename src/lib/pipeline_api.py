import time
import requests
import os

##### Clé Api a modifier si plus valide #####
API_KEY = "Bearer eyJ4NXQiOiJOelU0WTJJME9XRXhZVGt6WkdJM1kySTFaakZqWVRJeE4yUTNNalEyTkRRM09HRmtZalkzTURkbE9UZ3paakUxTURRNFltSTVPR1kyTURjMVkyWTBNdyIsImtpZCI6Ik56VTRZMkkwT1dFeFlUa3paR0kzWTJJMVpqRmpZVEl4TjJRM01qUTJORFEzT0dGa1lqWTNNRGRsT1RnelpqRTFNRFE0WW1JNU9HWTJNRGMxWTJZME13X1JTMjU2IiwidHlwIjoiYXQrand0IiwiYWxnIjoiUlMyNTYifQ.eyJzdWIiOiJhNjI5YTQyMC0yYTMwLTQxZDYtYjE0MC0wZDQzY2MzZDIzYWYiLCJhdXQiOiJBUFBMSUNBVElPTiIsImF1ZCI6InNhWmtURWR1Um50d0xocktVTmRHWWJKVXM3Y2EiLCJuYmYiOjE3NDg4NTk1MTYsImF6cCI6InNhWmtURWR1Um50d0xocktVTmRHWWJKVXM3Y2EiLCJzY29wZSI6ImRlZmF1bHQiLCJpc3MiOiJodHRwczpcL1wvcG9ydGFpbC1hcGkubWV0ZW9mcmFuY2UuZnJcL29hdXRoMlwvdG9rZW4iLCJleHAiOjE3NDg4NjMxMTYsImlhdCI6MTc0ODg1OTUxNiwianRpIjoiYjFiMzVmMDUtYzA5MS00YzkyLWI1M2UtYzQ3ZjZjMDZkNjBiIiwiY2xpZW50X2lkIjoic2Faa1RFZHVSbnR3TGhyS1VOZEdZYkpVczdjYSJ9.w7WrcH75bnPcHotVYm0cl8uS4D5vPzEIPH9lDggq8bzD1jyANvhKE2qhZxmFaPmiJ8_aZCcsvdUgef7K2T46MDibA62SqEVBYZL6TmFFLli-293zN-VdWMl7mjBzLK9nFgeXHbdSZooVX7ib9BUwKPKOHqPgGy3uhebrmqhMCQHHc3DQsDLL-FWg7RA3jLLEiDqt3Wl-JtIdkwVIPtA1WZ4lvfXE-3OJ8zH4u0JONxhozflJIuXvxJ5i9WVC04C_lES_odlleAFfLeV7dG4L3IXTyEdVqzPK_76Zt7G3abp4lKzo3jZXmy84nGzRUz8hLPWCOd1Pad9I3zSPaN6MdQ"
##### Id station a changer selon la région #####
id_station = "13001009"
nom_ville = "Aix_en_Provence" ## Remplacer les tirets du 6(-) par ceux du 8(_)
##### Dates juste l'année, elles sont traitées après #####
date_debut = 2002 #AAAA
date_fin = 2024 #AAAA
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