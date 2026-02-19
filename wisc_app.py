import streamlit as st
import matplotlib.pyplot as plt

st.set_page_config(page_title="Simulateur WISC-V Confiance", layout="centered")

st.title("📊 WISC-V : Notes & Intervalles de Confiance")
st.write("Le score n'est pas un point, c'est une zone.")

# 1. Configuration des scores et de la confiance
st.sidebar.header("Réglages")
conf_level = st.sidebar.radio("Niveau de confiance", ["90%", "95%"])
sem = 4  # Erreur type de mesure moyenne (Standard Error of Measurement)
z_score = 1.645 if conf_level == "90%" else 1.96
margin = round(z_score * sem)

icv = st.sidebar.slider("ICV (Verbal)", 45, 155, 100)
ivs = st.sidebar.slider("IVS (Visuospatial)", 45, 155, 100)
irf = st.sidebar.slider("IRF (Raisonnement)", 45, 155, 100)
imt = st.sidebar.slider("IMT (Mémoire)", 45, 155, 100)
ivt = st.sidebar.slider("IVT (Vitesse)", 45, 155, 100)

indices = ['ICV', 'IVS', 'IRF', 'IMT', 'IVT']
scores = [icv, ivs, irf, imt, ivt]
y_err = [margin] * 5  # La barre s'étend de +/- margin autour du score

# 2. Graphique
fig, ax = plt.subplots(figsize=(10, 6))

# Zones de couleur
ax.axhspan(40, 70, facecolor='#FF0000', alpha=0.1, label="Déficit (< 70)")
ax.axhspan(85, 115, facecolor='gray', alpha=0.1, label="Zone Moyenne")
ax.axhline(100, color='black', linewidth=0.8, alpha=0.4)

# Tracé avec barres d'erreur (Intervalles de confiance)
ax.errorbar(indices, scores, yerr=y_err, fmt='o', color='#1f77b4', 
            ecolor='orange', elinewidth=3, capsize=8, markersize=10, 
            label=f"Intervalle de confiance ({conf_level})")

# Affichage des valeurs (Score [Borne Inf - Borne Sup])
for i, score in enumerate(scores):
    ax.text(i, score + margin + 4, f"{score}\n[{score-margin}-{score+margin}]", 
            ha='center', fontsize=9, fontweight='bold', color='#1B4F72')

ax.set_ylim(40, 160)
ax.set_yticks([40, 70, 85, 100, 115, 130, 145, 160])
ax.set_title(f"Profil WISC-V avec IC à {conf_level} (+/- {margin} points)", fontsize=14)
ax.legend(loc='upper right')
ax.grid(axis='y', linestyle=':', alpha=0.3)

st.pyplot(fig)

st.info(f"💡 **Note pédagogique :** L'intervalle de confiance montre que si l'enfant passait le test 100 fois, son score se situerait dans cette zone orange {conf_level.replace('%','')} fois.")
