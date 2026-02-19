import streamlit as st
import matplotlib.pyplot as plt

st.set_page_config(page_title="WISC-V Indices - Analyse Globale", layout="wide")

st.markdown("""
    <style>
    .block-container {padding-top: 2rem; padding-bottom: 0rem;}
    header {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

st.sidebar.header("Saisie des Indices")
icv = st.sidebar.slider("ICV", 45, 155, 100)
ivs = st.sidebar.slider("IVS", 45, 155, 100)
irf = st.sidebar.slider("IRF", 45, 155, 100)
imt = st.sidebar.slider("IMT", 45, 155, 100)
ivt = st.sidebar.slider("IVT", 45, 155, 100)

st.subheader("📊 Profil des Indices Principaux")

# --- CONFIGURATION GRAPHIQUE ---
fig, ax = plt.subplots(figsize=(10, 4))
blue_color = '#1f77b4' 

# Zones de performance discrètes
ax.axhspan(40, 70, facecolor='red', alpha=0.05)
ax.axhspan(85, 115, facecolor='gray', alpha=0.05)
ax.axhspan(130, 160, facecolor='green', alpha=0.05)

labels = ['ICV', 'IVS', 'IRF', 'IMT', 'IVT']
scores = [icv, ivs, irf, imt, ivt]

# --- TRACÉ AFFINÉ ---
# On réduit le trait à 1.5 et les points à 7
ax.plot(labels, scores, color=blue_color, marker='o', 
        linewidth=1.5, markersize=7, alpha=0.9, zorder=3)

# On rend les moustaches plus nettes (alpha=1.0) mais plus fines
ax.errorbar(labels, scores, yerr=4, fmt='none', ecolor=blue_color, 
            elinewidth=1.2, capsize=6, alpha=1.0, zorder=2)

# Affichage des scores
for i, s in enumerate(scores):
    ax.text(i, s + 7, str(s), ha='center', fontweight='bold', color=blue_color, fontsize=11)

ax.set_ylim(40, 165)
ax.set_yticks([40, 70, 85, 100, 115, 130, 160])
ax.grid(axis='y', linestyle=':', alpha=0.4)

ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

st.pyplot(fig)

# --- ANALYSE ---
st.markdown("---")
dispersion = max(scores) - min(scores)
if dispersion >= 23:
    st.warning(f"⚠️ **Hétérogénéité :** {dispersion} points d'écart.")
else:
    st.success(f"✅ **Profil homogène :** {dispersion} points d'écart.")
