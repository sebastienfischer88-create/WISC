import streamlit as st
import matplotlib.pyplot as plt

st.set_page_config(page_title="WISC-V Indices - Analyse Globale", layout="wide")

# CSS pour la netteté et la suppression du scroll
st.markdown("""
    <style>
    .block-container {padding-top: 2rem; padding-bottom: 0rem;}
    header {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

st.sidebar.header("Saisie des Indices")
icv = st.sidebar.slider("ICV (Verbal)", 45, 155, 100)
ivs = st.sidebar.slider("IVS (Visuospatial)", 45, 155, 100)
irf = st.sidebar.slider("IRF (Raisonnement)", 45, 155, 100)
imt = st.sidebar.slider("IMT (Mémoire)", 45, 155, 100)
ivt = st.sidebar.slider("IVT (Vitesse)", 45, 155, 100)

st.subheader("📊 Profil des Indices Principaux")

# --- CONFIGURATION GRAPHIQUE ---
fig, ax = plt.subplots(figsize=(10, 4))
blue_color = '#1f77b4' # Le même bleu que pour les subtests

# Zones de performance très discrètes
ax.axhspan(40, 70, facecolor='red', alpha=0.05)
ax.axhspan(85, 115, facecolor='gray', alpha=0.05)
ax.axhspan(130, 160, facecolor='green', alpha=0.05)

labels = ['ICV', 'IVS', 'IRF', 'IMT', 'IVT']
scores = [icv, ivs, irf, imt, ivt]

# Tracé uniformisé
ax.plot(labels, scores, color=blue_color, marker='o', linewidth=2.5, markersize=10)

# Barres d'erreur (moustaches) en bleu (SEM de l'indice environ 3-4 pts)
# On utilise yerr=4 pour une représentation visuelle standard du SEM
ax.errorbar(labels, scores, yerr=4, fmt='none', ecolor=blue_color, 
            elinewidth=1.5, capsize=5, alpha=0.6)

# Affichage des scores
for i, s in enumerate(scores):
    ax.text(i, s + 7, str(s), ha='center', fontweight='bold', color=blue_color, fontsize=11)

# Esthétique des axes
ax.set_ylim(40, 165)
ax.set_yticks([40, 70, 85, 100, 115, 130, 160])
ax.grid(axis='y', linestyle=':', alpha=0.4)

# Épurer le cadre
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

st.pyplot(fig)

# --- ANALYSE D'HÉTÉROGÉNÉITÉ ---
st.markdown("---")
dispersion = max(scores) - min(scores)
if dispersion >= 23:
    st.warning(f"⚠️ **Hétérogénéité inter-indices :** {dispersion} points d'écart. "
               "L'interprétation du CIT (QI Total) doit être menée avec prudence.")
else:
    st.success(f"✅ **Profil homogène :** L'écart entre les indices ({dispersion} pts) est cliniquement acceptable.")
