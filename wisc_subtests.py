import streamlit as st
import matplotlib.pyplot as plt

st.set_page_config(page_title="WISC-V Subtests par Indices", layout="wide")

st.markdown("""
    <style>
    .block-container {padding-top: 2rem; padding-bottom: 0rem;}
    header {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

st.sidebar.header("Notes des Subtests")

# Groupement par indices
groups = {
    "Compréhension Verbale": [("Similitudes", "Sim"), ("Vocabulaire", "Voc")],
    "Visuospatial": [("Cubes", "Cub"), ("Puzzles", "Puz")],
    "Raisonnement Fluide": [("Matrices", "Mat"), ("Balances", "Bal")],
    "Mémoire de Travail": [("Chiffres", "Chi"), ("Images", "Ima")],
    "Vitesse de Traitement": [("Code", "Cod"), ("Symboles", "Sym")]
}

all_scores = []
for group_name, subs in groups.items():
    st.sidebar.markdown(f"**{group_name}**")
    for full_name, short_name in subs:
        score = st.sidebar.slider(full_name, 1, 19, 10, key=full_name)
        all_scores.append(score)

st.subheader("🧩 Profil détaillé par paires d'Indices")

fig, ax = plt.subplots(figsize=(11, 4))

# Zones de performance
ax.axhspan(1, 7, facecolor='red', alpha=0.08)
ax.axhspan(7, 13, facecolor='gray', alpha=0.08)
ax.axhspan(13, 19, facecolor='green', alpha=0.08)

# Tracé par paires
short_labels = ["Sim", "Voc", "Cub", "Puz", "Mat", "Bal", "Chi", "Ima", "Cod", "Sym"]
colors = ['#1f77b4', '#d62728', '#2ca02c', '#9467bd', '#e377c2'] # Une couleur par indice
indices_names = ["ICV", "IVS", "IRF", "IMT", "IVT"]

for i in range(0, 10, 2):
    pair_scores = all_scores[i:i+2]
    pair_labels = short_labels[i:i+2]
    color = colors[i//2]
    
    # Tracer la ligne entre les deux subtests de la paire
    ax.plot(pair_labels, pair_scores, color=color, marker='o', linewidth=3, markersize=10)
    
    # Ajouter les barres d'erreur (Intervalle de confiance)
    ax.errorbar(pair_labels, pair_scores, yerr=1.2, fmt='none', ecolor='orange', elinewidth=2, capsize=4)
    
    # Afficher les scores
    for j, s in enumerate(pair_scores):
        ax.text(i+j, s + 1.5, str(s), ha='center', fontweight='bold', color=color)
        
    # Ajouter le nom de l'indice en bas
    ax.text(i + 0.5, -2.5, indices_names[i//2], ha='center', fontweight='bold', fontsize=11, color=color)

ax.set_ylim(-3, 21) # On descend un peu pour laisser de la place aux noms d'indices
ax.set_yticks([1, 7, 10, 13, 19])
ax.set_xticks(range(10))
ax.set_xticklabels(short_labels)
ax.grid(axis='y', linestyle=':', alpha=0.3)

st.pyplot(fig)

# Analyse d'hétérogénéité intra-indice
st.markdown("---")
hétéro = []
for i, name in enumerate(indices_names):
    diff = abs(all_scores[i*2] - all_scores[i*2+1])
    if diff >= 3: # Seuil clinique classique de significativité
        hétéro.append(f"{name} ({diff} pts)")

if hétéro:
    st.warning(f"⚠️ Dissociation significative dans : {', '.join(hétéro)}")
