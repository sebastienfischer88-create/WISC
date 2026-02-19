import streamlit as st
import matplotlib.pyplot as plt

st.set_page_config(page_title="Simulateur WISC-V", layout="centered")

st.title("📊 Simulateur de Profil WISC-V")
st.write("Utilisez les curseurs à gauche pour moduler les indices en temps réel.")

# 1. Configuration des scores via la barre latérale
st.sidebar.header("Configuration des Indices")
icv = st.sidebar.slider("ICV (Compréhension Verbale)", 45, 155, 100)
ivs = st.sidebar.slider("IVS (Visuospatial)", 45, 155, 100)
irf = st.sidebar.slider("IRF (Raisonnement Fluide)", 45, 155, 100)
imt = st.sidebar.slider("IMT (Mémoire de Travail)", 45, 155, 100)
ivt = st.sidebar.slider("IVT (Vitesse de Traitement)", 45, 155, 100)

indices = ['ICV', 'IVS', 'IRF', 'IMT', 'IVT']
scores = [icv, ivs, irf, imt, ivt]

# 2. Création de la figure et de l'axe (L'étape cruciale pour éviter l'erreur)
fig, ax = plt.subplots(figsize=(10, 6))

# Dessin de la zone de normalité (85 - 115)
ax.axhspan(85, 115, facecolor='gray', alpha=0.15, label="Zone Moyenne (85-115)")
ax.axhline(100, color='black', linestyle='--', linewidth=1, alpha=0.5)

# Tracé du profil
ax.plot(indices, scores, marker='o', markersize=10, linestyle='-', color='#2E86C1', linewidth=3)

# Ajout des étiquettes de score au-dessus de chaque point
for i, score in enumerate(scores):
    ax.text(i, score + 3, str(score), ha='center', fontweight='bold', color='#1B4F72')

# Paramétrage des axes
ax.set_ylim(40, 160)
ax.set_yticks(range(40, 170, 10))
ax.set_ylabel("Note Standard (M=100, ET=15)")
ax.grid(axis='y', linestyle=':', alpha=0.6)
ax.set_title("Profil Clinique de l'enfant", fontsize=14)
ax.legend(loc='upper right')

# 3. Affichage dans Streamlit
st.pyplot(fig)