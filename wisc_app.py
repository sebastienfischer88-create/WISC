import streamlit as st
import matplotlib.pyplot as plt

# 1. Mode LARGE et CSS pour compacter l'affichage
st.set_page_config(page_title="WISC-V Compact", layout="wide")

st.markdown("""
    <style>
    .block-container {padding-top: 0.5rem; padding-bottom: 0rem; padding-left: 2rem; padding-right: 2rem;}
    .stSlider {margin-bottom: -1.5rem;}
    p {margin-bottom: 0.2rem;}
    </style>
    """, unsafe_allow_html=True)

# --- ENTÊTE SUR UNE LIGNE ---
col_t1, col_t2, col_t3 = st.columns([3, 2, 2])
with col_t1:
    st.subheader("📊 Analyseur WISC-V")
with col_t2:
    mode = st.selectbox("", ["Indices Principaux", "Subtests (Détails)"], label_visibility="collapsed")
with col_t3:
    conf_level = st.radio("", ["90%", "95%"], horizontal=True, label_visibility="collapsed")

# --- LOGIQUE ---
sem = 4 if mode == "Indices Principaux" else 0.8
z_score = 1.645 if conf_level == "90%" else 1.96
margin = round(z_score * sem, 1)

if mode == "Indices Principaux":
    labels = ['ICV', 'IVS', 'IRF', 'IMT', 'IVT']
    y_min, y_max, y_ticks = 40, 160, [40, 70, 85, 100, 115, 130, 160]
    default_val = 100
else:
    labels = ["Sim", "Voc", "Cub", "Puz", "Mat", "Bal", "Chi", "Ima", "Cod", "Sym"]
    y_min, y_max, y_ticks = 0, 20, [1, 7, 10, 13, 19]
    default_val = 10

# --- GRAPHIQUE ---
fig, ax = plt.subplots(figsize=(11, 3.8)) # Hauteur ajustée pour écran standard
scores = []

# Zones de performance
ax.axhspan(y_min, y_ticks[1], facecolor='red', alpha=0.07)
ax.axhspan(y_ticks[2]-15 if mode=="Indices Principaux" else 7, 
           y_ticks[4] if mode=="Indices Principaux" else 13, facecolor='gray', alpha=0.07)
ax.axhspan(y_ticks[5] if mode=="Indices Principaux" else 13, y_max, facecolor='green', alpha=0.07)

# --- GRILLE DE CURSEURS (Placés avant le graphique pour le scroll) ---
cols = st.columns(len(labels))
for i, label in enumerate(labels):
    with cols[i]:
        val = st.slider(label, y_min, y_max, default_val, key=label)
        scores.append(val)

# Tracé du profil
ax.errorbar(labels, scores, yerr=margin, fmt='o-', color='#1f77b4', ecolor='orange', 
            elinewidth=2, capsize=4, markersize=8, linewidth=2)

for i, s in enumerate(scores):
    ax.text(i, s + (margin + 0.5), str(s), ha='center', fontweight='bold', fontsize=9)

ax.set_ylim(y_min, y_max)
ax.set_yticks(y_ticks)
ax.tick_params(axis='both', which='major', labelsize=8)
ax.grid(axis='y', linestyle=':', alpha=0.3)

st.pyplot(fig)

# --- ANALYSE COURTE ---
dispersion = max(scores) - min(scores)
seuil = 23 if mode == "Indices Principaux" else 5
if dispersion >= seuil:
    st.warning(f"⚠️ Hétérogénéité : Écart de {dispersion} pts.")
else:
    st.success(f"✅ Profil homogène.")
