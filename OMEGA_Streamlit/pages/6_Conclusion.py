import streamlit as st

st.set_page_config(page_title="Conclusion des prévisions", layout="centered")
st.title("📌 Conclusion du projet de prévision météo")

st.markdown("""
##  Objectif atteint

Le modèle **SARIMA** a permis de générer des **prévisions fiables** de la température pour les 24 prochaines heures à Aix-en-Provence. Grâce à l’analyse des données climatiques historiques, nous avons pu :

- Identifier une **saisonnalité claire** (journalière et annuelle).
- Ajuster le modèle aux spécificités locales (température stable, humidité variable, peu de précipitations).
- Évaluer les prédictions avec des **intervalles de confiance réalistes**.

---

##  Résultats du modèle SARIMA

- Modèle entraîné sur les températures des dernières semaines.
- Horizon de prévision : **24 heures**.
- Visualisation des données récentes et des prévisions avec incertitude.
- Précision satisfaisante pour un usage de court terme (±1 à 2°C).

Les courbes obtenues montrent que le modèle :
- **Suit bien la tendance de la température** sur 24h.
- Capte les variations de **cycle journalier**.
- Fournit une **estimation prudente** des écarts possibles (via l’intervalle de confiance).

---

##  Limites observées

Malgré les bons résultats, certaines limites subsistent :

- **Modèle univarié** : seule la température est prédite. D'autres variables (vent, pression, humidité) ne sont pas encore intégrées.
- **Pas de gestion d'événements rares** : les épisodes extrêmes (canicules, vents violents, orages) sont peu prédits.
- **Mise à jour du modèle manuelle** : un automatisme quotidien serait préférable.

---

##  Améliorations futures possibles

- Entraînement **multivarié** avec d'autres variables météo pertinentes.
- Intégration de **modèles avancés** : Prophet, LSTM, XGBoost.
- Déploiement web avec automatisation du traitement et des prédictions.
- Extension à d'autres villes pour comparer les dynamiques climatiques régionales.

---

## Conclusion

Le modèle SARIMA constitue une **base robuste** pour la prévision météo à court terme sur des données structurées. Il est particulièrement adapté pour des usages pédagogiques, exploratoires ou pour un prototype d'application météo localisée.

""")
