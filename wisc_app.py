import streamlit as st
import matplotlib.pyplot as plt

# 1. Configuration de la page
st.set_page_config(page_title="WISC-V Pro", layout="wide")

# CSS pour compacter au maximum et éviter le scroll
st.markdown("""
    <style>
    .block-container {padding-top: 0.5rem; padding-bottom: 0rem;}
    div[data-testid="stVerticalBlock"] > div {margin-top: -1rem;}
    .stSlider {margin-bottom: -1rem;}
    </style>
    """, unsafe_allow_html=True)

# --- ENTÊTE ---
col_t1, col_t2, col_t3 = st.columns([3, 2, 2])
with col_t1:
    st.subheader("📊 Analyseur WISC-V")
with col_t2:
    # Changement de mode avec une clé unique pour forcer le rafraîchissement
    mode = st.selectbox("Niveau :", ["Indices Principaux", "Subtests (Détails)"], key="main_mode")
with col_t3:
    conf_level = st.radio("Confiance :", ["90%", "95%"], horizontal=True)

# --- CONFIGURATION DES DONNÉES ---
if mode == "Indices Principaux":
    labels = ['ICV', 'IVS', 'IRF', 'IMT', 'IVT']
    y_min, y_max, y_ticks = 40, 160, [40, 70, 85, 100, 115, 130, 160]
    default_val = 100
    sem = 4
else:
    labels = ["Sim", "Voc", "Cub", "Puz", "Mat", "Bal", "Chi", "Ima", "Cod", "Sym"]
    y_min, y_max, y_ticks = 0, 20, [1, 7, 10, 13, 19]
    default_val = 10
    sem = 0.8

z_score = 1.645 if conf_level == "90%" else 1.96
margin = round(z_score * sem, 1)

# --- GRILLE DE CURSEURS (Placés en haut pour l'ergonomie) ---
scores = []
cols = st.columns(len(labels))
for i, label in enumerate(labels):
    with cols[i]:
        # L'utilisation de key=f"{mode}_{label}" règle le bug de basculement
        val = st.slider(label, y_min, y_max, default_val, key=f"{mode}_{label}")
        scores.append(val)

# --- GRAPHIQUE ---
# On réduit la hauteur (figsize) pour que tout tienne sans scroll
fig, ax = plt.subplots(figsize=(12, 4))

# Zones de performance
ax.axhspan(y_min, y_ticks[1], facecolor='red', alpha=0.08, label="Fragilité")
ax.axhspan(y_ticks[2]-15 if mode=="Indices Principaux" else 7, 
           y_ticks[4] if mode=="Indices Principaux" else 13, facecolor='gray', alpha=0.08, label="Moyenne")
ax.axhspan(y_ticks[5] if mode=="Indices Principaux" else 13, y_max, facecolor='green', alpha=0.08, label="Force")

# Tracé du profil
ax.errorbar(labels, scores, yerr=margin, fmt='o-', color='#1f77b4', ecolor='orange', 
            elinewidth=3, capsize=6, markersize=10, linewidth=3)

# Chiffres au-dessus des points
for i, s in enumerate(scores):
    ax.text(i, s + (margin + (0.5 if mode=="Subtests (Détails)" else 3)), 
            str(s), ha='center', fontweight='bold', fontsize=10)

ax.set_ylim(y_min, y_max)
ax.set_yticks(y_ticks)
ax.grid(axis='y', linestyle=':', alpha=0.3)
ax.legend(loc='lower right', fontsize='x-small')

st.pyplot(fig)

# --- ANALYSE ---
dispersion = max(scores) - min(scores)
seuil = 23 if mode == "Indices Principaux" else 5
if dispersion >= seuil:
    st.warning(f"⚠️ Hétérogénéité détectée : Écart de {dispersion} points.")
else:
    st.success(f"✅ Profil homogène (Écart : {dispersion}).")
