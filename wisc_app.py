import streamlit as st
import matplotlib.pyplot as plt

st.set_page_config(page_title="Simulateur WISC-V", layout="centered")

st.title("📊 Simulateur de Profil WISC-V")
st.write("Visualisez les zones de performance et les dissociations.")

# 1. Barre latérale
st.sidebar.header("Scores des Indices")
icv = st.sidebar.slider("ICV (Verbal)", 45, 155, 100)
ivs = st.sidebar.slider("IVS (Visuospatial)", 45, 155, 100)
irf = st.sidebar.slider("IRF (Raisonnement)", 45, 155, 100)
imt = st.sidebar.slider("IMT (Mémoire)", 45, 155, 100)
ivt = st.sidebar.slider("IVT (Vitesse)", 45, 155, 100)

indices = ['ICV', 'IVS', 'IRF', 'IMT', 'IVT']
scores = [icv, ivs, irf, imt, ivt]

# 2. Création du graphique
fig, ax = plt.subplots(figsize=(10, 6))

# --- AJOUT DES ZONES VISUELLES ---
# Zone Déficitaire (inférieur à 70) en rouge très clair
ax.axhspan(40, 70, facecolor='#FF0000', alpha=0.1, label="Zone Déficitaire (< 70)")

# Zone de Normalité (85-115) en gris
ax.axhspan(85, 115, facecolor='gray', alpha=0.1, label="Zone Moyenne (85-115)")

# Ligne du score 70 (Seuil critique)
ax.axhline(70, color='red', linestyle='--', linewidth=1, alpha=0.6)
# Ligne de la moyenne 100
ax.axhline(100, color='black', linestyle='-', linewidth=0.5, alpha=0.5)

# --- TRACÉ DU PROFIL ---
ax.plot(indices, scores, marker='o', markersize=12, linestyle='-', color='#1f77b4', linewidth=3, zorder=5)

# Étiquettes de scores
for i, score in enumerate(scores):
    ax.text(i, score + 4, str(score), ha='center', fontweight='bold', fontsize=11)

# Paramètres des axes
ax.set_ylim(40, 160)
ax.set_yticks([40, 70, 85, 100, 115, 130, 145, 160]) # Repères psychométriques
ax.set_ylabel("Note Standard")
ax.set_title("Profil WISC-V : Analyse de la dispersion", fontsize=14)
ax.legend(loc='upper right', frameon=True)
ax.grid(axis='y', linestyle=':', alpha=0.3)

st.pyplot(fig)
