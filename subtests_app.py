import streamlit as st
import matplotlib.pyplot as plt

st.set_page_config(page_title="WISC-V Subtests", layout="wide")

st.title("🧩 Analyse des 10 Subtests Principaux")
st.write("Échelle de 1 à 19 (Moyenne = 10)")

# 1. Configuration des subtests par blocs (Colonnes)
st.sidebar.header("Notes des Subtests")

sub_names = [
    "Similitudes", "Vocabulaire", "Cubes", "Puzzles", 
    "Matrices", "Balances", "Mém. Chiffres", "Mém. Images", 
    "Code", "Symboles"
]

scores_sub = []
for name in sub_names:
    scores_sub.append(st.sidebar.slider(name, 1, 19, 10))

# 2. Graphique
fig, ax = plt.subplots(figsize=(12, 6))

# Zones colorées
ax.axhspan(1, 7, facecolor='#FF0000', alpha=0.1, label="Zone de fragilité (< 7)")
ax.axhspan(7, 13, facecolor='gray', alpha=0.1, label="Zone moyenne (7-13)")
ax.axhspan(13, 19, facecolor='#2ECC71', alpha=0.1, label="Zone de force (> 13)")

ax.axhline(10, color='black', linestyle='-', linewidth=0.8, alpha=0.5)

# Tracé (Histogramme ou ligne)
ax.bar(sub_names, scores_sub, color='#3498DB', alpha=0.7, edgecolor='navy')
ax.plot(sub_names, scores_sub, color='navy', marker='o', linewidth=2)

# Affichage des scores
for i, s in enumerate(scores_sub):
    ax.text(i, s + 0.5, str(s), ha='center', fontweight='bold')

ax.set_ylim(0, 20)
ax.set_yticks(range(1, 20))
ax.set_ylabel("Note Standard (1-19)")
ax.set_title("Profil détaillé des Subtests", fontsize=15)
ax.legend(loc='upper right')

st.pyplot(fig)

# 3. Analyse pédagogique
st.subheader("Analyse clinique")
ecart = max(scores_sub) - min(scores_sub)
if ecart >= 5:
    st.warning(f"⚠️ **Hétérogénéité des subtests :** {ecart} points d'écart. Cela peut suggérer un profil 'dys' ou un trouble spécifique malgré un indice global correct.")
