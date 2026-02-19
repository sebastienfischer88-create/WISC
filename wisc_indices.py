import streamlit as st
import matplotlib.pyplot as plt

st.set_page_config(page_title="WISC-V Indices", layout="wide")

# Sidebar pour les curseurs
st.sidebar.header("Saisie des Indices")
icv = st.sidebar.slider("ICV (Verbal)", 45, 155, 100)
ivs = st.sidebar.slider("IVS (Visuospatial)", 45, 155, 100)
irf = st.sidebar.slider("IRF (Raisonnement)", 45, 155, 100)
imt = st.sidebar.slider("IMT (Mémoire)", 45, 155, 100)
ivt = st.sidebar.slider("IVT (Vitesse)", 45, 155, 100)

labels = ['ICV', 'IVS', 'IRF', 'IMT', 'IVT']
scores = [icv, ivs, irf, imt, ivt]

st.title("📊 Profil des Indices Principaux")

# Graphique central
fig, ax = plt.subplots(figsize=(10, 5))
ax.axhspan(40, 70, facecolor='red', alpha=0.1, label="Déficit (<70)")
ax.axhspan(85, 115, facecolor='gray', alpha=0.1, label="Zone Moyenne (85-115)")
ax.axhspan(130, 160, facecolor='green', alpha=0.1, label="HPI (>130)")

# Tracé
ax.errorbar(labels, scores, yerr=6, fmt='o-', color='#1f77b4', ecolor='orange', 
            elinewidth=3, capsize=6, markersize=10, linewidth=3)

for i, s in enumerate(scores):
    ax.text(i, s + 7, str(s), ha='center', fontweight='bold', fontsize=12)

ax.set_ylim(40, 160)
ax.set_yticks([40, 70, 85, 100, 115, 130, 160])
ax.grid(axis='y', linestyle=':', alpha=0.3)
ax.legend(loc='upper right')

st.pyplot(fig)

# Analyse rapide en bas
dispersion = max(scores) - min(scores)
if dispersion >= 23:
    st.warning(f"⚠️ Hétérogénéité : {dispersion} pts d'écart. Prudence sur le CIT.")
2. Code pour subtests.py (Moyenne 10)
Ici, les 10 curseurs sont rangés dans la barre latérale. C'est beaucoup plus propre car 10 curseurs alignés horizontalement rendaient les étiquettes illisibles.

Python
import streamlit as st
import matplotlib.pyplot as plt

st.set_page_config(page_title="WISC-V Subtests", layout="wide")

st.sidebar.header("Notes des Subtests")
sub_names = ["Similitudes", "Vocabulaire", "Cubes", "Puzzles", "Matrices", 
             "Balances", "Mémoire Chiffres", "Mémoire Images", "Code", "Symboles"]

scores = []
for name in sub_names:
    scores.append(st.sidebar.slider(name, 1, 19, 10))

# On utilise des abréviations pour l'axe X du graphique
labels_short = ["Sim", "Voc", "Cub", "Puz", "Mat", "Bal", "Chi", "Ima", "Cod", "Sym"]

st.title("🧩 Profil détaillé des Subtests")

fig, ax = plt.subplots(figsize=(10, 5))
ax.axhspan(1, 7, facecolor='red', alpha=0.1, label="Faiblesse (<7)")
ax.axhspan(7, 13, facecolor='gray', alpha=0.1, label="Zone Moyenne (7-13)")
ax.axhspan(13, 19, facecolor='green', alpha=0.1, label="Force (>13)")

ax.errorbar(labels_short, scores, yerr=1.2, fmt='o-', color='#1f77b4', ecolor='orange', 
            elinewidth=3, capsize=6, markersize=10, linewidth=3)

for i, s in enumerate(scores):
    ax.text(i, s + 1.2, str(s), ha='center', fontweight='bold', fontsize=10)

ax.set_ylim(0, 20)
ax.set_yticks([1, 7, 10, 13, 19])
ax.grid(axis='y', linestyle=':', alpha=0.3)
ax.legend(loc='upper right')

st.pyplot(fig)

dispersion = max(scores) - min(scores)
if dispersion >= 5:
    st.info(f"💡 Écart inter-subtests : {dispersion} points.")
