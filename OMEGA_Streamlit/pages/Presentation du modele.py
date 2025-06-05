import streamlit as st

st.title("Modèles ARIMA & SARIMA")

st.markdown("""
Les modèles **ARIMA** et **SARIMA** sont des méthodes statistiques puissantes utilisées pour la prévision de séries temporelles.

---

## 🔹 ARIMA (AutoRegressive Integrated Moving Average)

Le modèle **ARIMA** est composé de trois éléments :

- **AR (Auto-Régressif)** : la valeur actuelle dépend linéairement de ses valeurs passées.
- **I (Integrated)** : différenciation des données pour les rendre stationnaires.
- **MA (Moving Average)** : prend en compte les erreurs passées du modèle.

**Notation : ARIMA(p, d, q)**

- `p` : ordre de l’auto-régression
- `d` : degré de différenciation
- `q` : ordre de la moyenne mobile

**ARIMA** est bien adapté aux séries temporelles **non saisonnières**.

---

## 🔹 SARIMA (Seasonal ARIMA)

**SARIMA** est une extension du modèle ARIMA qui intègre la **saisonnalité**. Il est utilisé lorsque la série présente des schémas récurrents (quotidiens, hebdomadaires, annuels...).

**Notation : SARIMA(p, d, q)(P, D, Q, s)**

- `(p, d, q)` : composantes non saisonnières (comme ARIMA)
- `(P, D, Q)` : composantes saisonnières
- `s` : période saisonnière (ex : `s=12` pour des données mensuelles)

SARIMA est plus adapté lorsque des **variations cycliques** apparaissent régulièrement dans la série de données.

---

##  Exemple d'application

Dans notre projet, nous utilisons **SARIMA** pour modéliser la température à Aix-en-Provence, car les données présentent une **saisonnalité annuelle** marquée.

---

##  Pourquoi pas un modèle plus complexe ?

SARIMA reste :
- Interprétable
- Robuste pour des séries temporelles classiques
- Adapté à notre jeu de données relativement structuré

Des modèles plus complexes comme les **RNN** ou **Prophet** peuvent être envisagés pour des cas plus dynamiques ou multi-variables.

---

""")
