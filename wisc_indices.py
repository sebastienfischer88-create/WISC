import streamlit as st
import matplotlib.pyplot as plt

# Configuration de la page
st.set_page_config(page_title="WISC-V Indices", layout="wide")

# HACK CSS pour supprimer les marges blanches en haut
st.markdown("""
    <style>
    .block-container {padding-top: 0.5rem; padding-bottom: 0rem;}
    header {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

st.sidebar.header("Saisie des Indices")
icv = st.sidebar.slider("ICV", 45, 155, 100)
ivs = st.sidebar.slider("IVS", 45, 155, 100)
irf = st.sidebar.slider("IRF", 45, 155, 100)
imt = st.sidebar.slider("IMT", 45, 155, 100)
ivt = st.sidebar.slider("IVT", 45, 155, 100)

st.subheader("📊 Profil des Indices")

# On réduit la hauteur à 3.8 pour que ça tienne sur un écran portable/projecteur
fig, ax = plt.subplots(figsize=(10, 3.8))

ax.axhspan(40, 70, facecolor='red', alpha=0.08)
ax.axhspan(85, 115, facecolor='gray', alpha=0.08)
ax.axhspan(130, 160, facecolor='green', alpha=0.08)

labels = ['ICV', 'IVS', 'IRF', 'IMT', 'IVT']
scores = [icv, ivs, irf, imt, ivt]

ax.errorbar(labels, scores, yerr=6, fmt='o-', color='#1f77b4', ecolor='orange', 
            elinewidth=2, capsize=4, markersize=8, linewidth=2)

for i, s in enumerate(scores):
    ax.text(i, s + 6, str(s), ha='center', fontweight='bold', fontsize=10)

ax.set_ylim(40, 165)
ax.set_yticks([40, 70, 85, 100, 115, 130, 160])
ax.grid(axis='y', linestyle=':', alpha=0.3)

st.pyplot(fig)

# Analyse sur une seule ligne courte
dispersion = max(scores) - min(scores)
if dispersion >= 23:
    st.warning(f"⚠️ Hétérogénéité : {dispersion} pts.")
