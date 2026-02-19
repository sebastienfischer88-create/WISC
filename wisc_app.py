import streamlit as st
import matplotlib.pyplot as plt

# Configuration de la page
st.set_page_config(page_title="Expert WISC-V", layout="wide")

st.title("🧠 Analyseur Professionnel WISC-V")

# --- MENU DE SÉLECTION ---
mode = st.sidebar.selectbox("Choisir le niveau d'analyse :", ["1. Indices Principaux", "2. Subtests (Détails)"])

# Paramètres communs (Intervalle de confiance)
st.sidebar.markdown("---")
conf_level = st.sidebar.radio("Niveau de confiance", ["90%", "95%"])
sem = 4 if mode == "1. Indices Principaux" else 0.8 # SEM réduit pour les subtests
z_score = 1.645 if conf_level == "90%" else 1.96
margin = round(z_score * sem, 1)

# --- MODE 1 : INDICES ---
if mode == "1. Indices Principaux":
    st.sidebar.subheader("Notes d'Indices")
    icv = st.sidebar.slider("ICV", 45, 155, 100)
    ivs = st.sidebar.slider("IVS", 45, 155, 100)
    irf = st.sidebar.slider("IRF", 45, 155, 100)
    imt = st.sidebar.slider("IMT", 45, 155, 100)
    ivt = st.sidebar.slider("IVT", 45, 155, 100)

    labels = ['ICV', 'IVS', 'IRF', 'IMT', 'IVT']
    scores = [icv, ivs, irf, imt, ivt]
    
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.axhspan(40, 70, facecolor='red', alpha=0.1, label="Déficit (<70)")
    ax.axhspan(85, 115, facecolor='gray', alpha=0.1, label="Moyenne (85-115)")
    ax.axhspan(130, 160, facecolor='green', alpha=0.1, label="HPI (>130)")
    
    ax.errorbar(labels, scores, yerr=margin, fmt='o-', color='#1f77b4', ecolor='orange', elinewidth=3, capsize=5)
    ax.set_ylim(40, 160)
    ax.set_yticks([40, 70, 85, 100, 115, 130, 160])
    ax.set_title("Profil des Indices (M=100)")

# --- MODE 2 : SUBTESTS ---
else:
    st.sidebar.subheader("Notes Standard")
    sub_names = ["Similitudes", "Vocabulaire", "Cubes", "Puzzles", "Matrices", "Balances", "Mém. Chiffres", "Mém. Images", "Code", "Symboles"]
    scores = []
    for name in sub_names:
        scores.append(st.sidebar.slider(name, 1, 19, 10))
    
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.axhspan(1, 7, facecolor='red', alpha=0.1, label="Faiblesse (<7)")
    ax.axhspan(7, 13, facecolor='gray', alpha=0.1, label="Moyenne (7-13)")
    ax.axhspan(13, 19, facecolor='green', alpha=0.1, label="Force (>13)")
    
    ax.bar(sub_names, scores, color='#3498DB', alpha=0.6)
    ax.errorbar(sub_names, scores, yerr=margin, fmt='o', color='navy', ecolor='orange', capsize=3)
    ax.set_ylim(0, 20)
    ax.set_yticks(range(1, 21))
    ax.set_title("Profil des Subtests (M=10)")
    plt.xticks(rotation=45)

# --- AFFICHAGE COMMUN ---
for i, s in enumerate(scores):
    ax.text(i, s + (margin if mode=="2. Subtests (Détails)" else margin+2), str(s), ha='center', fontweight='bold')

ax.legend(loc='upper right', fontsize='small')
st.pyplot(fig)

# Analyseur de dispersion
dispersion = max(scores) - min(scores)
seuil_critique = 23 if mode == "1. Indices Principaux" else 5
if dispersion >= seuil_critique:
    st.warning(f"⚠️ Hétérogénéité détectée : Écart de {dispersion} points. L'analyse du score global est compromise.")
else:
    st.success(f"✅ Profil homogène (Écart de {dispersion} points).")
