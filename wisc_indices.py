import streamlit as st
import matplotlib.pyplot as plt

# Configuration
st.set_page_config(page_title="WISC-V Indices", layout="wide")

# CSS pour supprimer le scroll et ajuster les marges
st.markdown("""
    <style>
    .block-container {padding-top: 2rem; padding-bottom: 0rem;}
    header {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# Barre latérale
st.sidebar.header("Saisie des Indices")
icv = st.sidebar.slider("ICV", 45, 155, 100)
ivs = st.sidebar.slider("IVS", 45, 155, 100)
irf = st.sidebar.slider("IRF", 45, 155, 100)
imt = st.sidebar.slider("IMT", 45, 155, 100)
ivt = st.sidebar.slider("IVT", 45, 155, 100)

st.subheader("📊 Profil des Indices Principaux")

# Graphique
fig, ax = plt.subplots(figsize=(10, 4))
blue_color = '#1f77b4'
red_alert = '#d62728'

# Zones de fond
ax.axhspan(40, 70, facecolor='red', alpha=0.05)
ax.axhspan(85, 115, facecolor='gray', alpha=0.05)
ax.axhspan(130, 160, facecolor='green', alpha=0.05)

labels = ['ICV', 'IVS', 'IRF', 'IMT', 'IVT']
scores = [icv, ivs, irf, imt, ivt]

# Ligne de liaison discrète
ax.plot(labels, scores, color=blue_color, linewidth=1, alpha=0.3, zorder=1)

# Points et moustaches dynamiques
for i, (label, score) in enumerate(zip(labels, scores)):
    color = red_alert if score < 70 else blue_color
    
    # Point affiné
    ax.plot(label, score, marker='o', color=color, markersize=7, zorder=3)
    # Moustache nette
    ax.errorbar(label, score, yerr=4, fmt='none', ecolor=color, 
                elinewidth=1.2, capsize=6, alpha=1.0, zorder=2)
    # Texte score
    ax.text(i, score + 7, str(score), ha='center', fontweight='bold', 
            color=color, fontsize=11)

ax.set_ylim(40, 165)
ax.set_yticks([40, 70, 85, 100, 115, 130, 160])
ax.grid(axis='y', linestyle=':', alpha=0.4)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

st.pyplot(fig)

# Analyse
st.markdown("---")
dispersion = max(scores) - min(scores)
if dispersion >= 23:
    st.warning(f"⚠️ Hétérogénéité : {dispersion} points d'écart.")
else:
    st.success(f"✅ Profil homogène : {dispersion} points d'écart.")
