import streamlit as st
import matplotlib.pyplot as plt

# Configuration pour éviter le scroll
st.set_page_config(page_title="WISC-V Pro", layout="centered")

# CSS personnalisé pour réduire les marges du haut
st.markdown("""<style>.block-container {padding-top: 1rem; padding-bottom: 0rem;}</style>""", unsafe_allow_html=True)

st.title("📊 Analyseur WISC-V")

# --- MENU ---
mode = st.sidebar.selectbox("Analyse :", ["Indices Principaux", "Subtests (Détails)"])

st.sidebar.markdown("---")
conf_level = st.sidebar.radio("Confiance", ["90%", "95%"], horizontal=True)
sem = 4 if mode == "Indices Principaux" else 0.8
z_score = 1.645 if conf_level == "90%" else 1.96
margin = round(z_score * sem, 1)

# --- DONNÉES ---
if mode == "Indices Principaux":
    labels = ['ICV', 'IVS', 'IRF', 'IMT', 'IVT']
    scores = [st.sidebar.slider(l, 45, 155, 100) for l in labels]
    y_min, y_max = 40, 160
    y_ticks = [40, 70, 85, 100, 115, 130, 160]
    zone_labels = ["Déficit", "Moyenne", "HPI"]
else:
    labels = ["Sim", "Voc", "Cub", "Puz", "Mat", "Bal", "Chi", "Ima", "Cod", "Sym"]
    scores = [st.sidebar.slider(l, 1, 19, 10) for l in labels]
    y_min, y_max = 0, 20
    y_ticks = [1, 7, 10, 13, 19]
    zone_labels = ["Fragilité", "Moyenne", "Force"]

# --- GRAPHIQUE COMPACT ---
fig, ax = plt.subplots(figsize=(9, 4.5)) # Taille réduite pour éviter le scroll

# Zones colorées uniformes
ax.axhspan(y_min, y_ticks[1], facecolor='red', alpha=0.08, label=zone_labels[0])
ax.axhspan(y_ticks[2]-15 if mode=="Indices Principaux" else 7, 
           y_ticks[4] if mode=="Indices Principaux" else 13, 
           facecolor='gray', alpha=0.08, label=zone_labels[1])
ax.axhspan(y_ticks[5] if mode=="Indices Principaux" else 13, y_max, facecolor='green', alpha=0.08, label=zone_labels[2])

# Tracé type profil (Ligne)
ax.errorbar(labels, scores, yerr=margin, fmt='o-', color='#1f77b4', ecolor='orange', 
            elinewidth=2, capsize=4, markersize=8, linewidth=2)

# Étiquettes
for i, s in enumerate(scores):
    ax.text(i, s + (margin + 1), str(s), ha='center', fontsize=9, fontweight='bold')

ax.set_ylim(y_min, y_max)
ax.set_yticks(y_ticks)
ax.grid(axis='y', linestyle=':', alpha=0.4)
ax.legend(loc='lower right', fontsize='x-small', ncol=3)

st.pyplot(fig)

# --- ANALYSE DYNAMIQUE COURTE ---
dispersion = max(scores) - min(scores)
seuil = 23 if mode == "Indices Principaux" else 5
if dispersion >= seuil:
    st.warning(f"⚠️ Hétérogénéité : Écart de {dispersion} points.")
else:
    st.success(f"✅ Profil homogène (Écart : {dispersion}).")
