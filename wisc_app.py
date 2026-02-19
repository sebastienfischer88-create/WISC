import streamlit as st
import matplotlib.pyplot as plt

# Configuration en mode large pour utiliser tout l'écran
st.set_page_config(page_title="WISC-V Dashboard", layout="wide")

# CSS pour supprimer les marges inutiles
st.markdown("""<style>.block-container {padding-top: 1rem;}</style>""", unsafe_allow_html=True)

st.title("📊 Analyseur WISC-V Professionnel")

# --- BANDEAU SUPÉRIEUR (Réglages rapides) ---
col_menu1, col_menu2, col_menu3 = st.columns([2, 2, 2])
with col_menu1:
    mode = st.selectbox("Niveau d'analyse :", ["Indices Principaux", "Subtests (Détails)"])
with col_menu2:
    conf_level = st.radio("Confiance :", ["90%", "95%"], horizontal=True)
with col_menu3:
    st.write(f"**Précision :** +/- {4 if mode == 'Indices Principaux' else 0.8} pts")

# --- LOGIQUE DES DONNÉES ---
sem = 4 if mode == "Indices Principaux" else 0.8
z_score = 1.645 if conf_level == "90%" else 1.96
margin = round(z_score * sem, 1)

if mode == "Indices Principaux":
    labels = ['ICV', 'IVS', 'IRF', 'IMT', 'IVT']
    y_min, y_max, y_ticks = 40, 160, [40, 70, 85, 100, 115, 130, 160]
else:
    labels = ["Sim", "Voc", "Cub", "Puz", "Mat", "Bal", "Chi", "Ima", "Cod", "Sym"]
    y_min, y_max, y_ticks = 0, 20, [1, 7, 10, 13, 19]

# --- ZONE DU GRAPHIQUE (Plus grande) ---
scores = []
# On crée le graphique d'abord avec des colonnes vides pour les curseurs en dessous
fig, ax = plt.subplots(figsize=(12, 5)) # Format large

# --- CURSEURS EN DESSOUS (Rééquilibrage) ---
st.markdown("---")
# On crée dynamiquement le nombre de colonnes nécessaires (5 ou 10)
cols = st.columns(len(labels))
for i, label in enumerate(labels):
    with cols[i]:
        # On place les curseurs à la verticale sous chaque point du graphique
        val = st.slider(label, y_min, y_max, 10 if mode == "Subtests (Détails)" else 100, key=label)
        scores.append(val)

# --- DESSIN DU GRAPHIQUE ---
# Zones
ax.axhspan(y_min, y_ticks[1], facecolor='red', alpha=0.08)
ax.axhspan(y_ticks[2]-15 if mode=="Indices Principaux" else 7, 
           y_ticks[4] if mode=="Indices Principaux" else 13, facecolor='gray', alpha=0.08)
ax.axhspan(y_ticks[5] if mode=="Indices Principaux" else 13, y_max, facecolor='green', alpha=0.08)

# Profil
ax.errorbar(labels, scores, yerr=margin, fmt='o-', color='#1f77b4', ecolor='orange', 
            elinewidth=3, capsize=5, markersize=10, linewidth=3)

# Valeurs
for i, s in enumerate(scores):
    ax.text(i, s + (margin + 1), str(s), ha='center', fontweight='bold')

ax.set_ylim(y_min, y_max)
ax.set_yticks(y_ticks)
ax.grid(axis='y', linestyle=':', alpha=0.4)

# Affichage du graphique au-dessus des curseurs
st.container().pyplot(fig)

# --- ALERTE DISPERSION ---
dispersion = max(scores) - min(scores)
seuil = 23 if mode == "Indices Principaux" else 5
if dispersion >= seuil:
    st.warning(f"⚠️ Hétérogénéité : Écart de {dispersion} points.")
