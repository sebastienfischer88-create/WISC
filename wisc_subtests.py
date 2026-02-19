import streamlit as st
import matplotlib.pyplot as plt

# Configuration
st.set_page_config(page_title="WISC-V Subtests", layout="wide")

st.markdown("""
    <style>
    .block-container {padding-top: 2rem; padding-bottom: 0rem;}
    header {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

st.sidebar.header("Notes des Subtests")

groups = {
    "Compréhension Verbale": [("Similitudes", "Sim"), ("Vocabulaire", "Voc")],
    "Visuospatial": [("Cubes", "Cub"), ("Puzzles", "Puz")],
    "Raisonnement Fluide": [("Matrices", "Mat"), ("Balances", "Bal")],
    "Mémoire de Travail": [("Chiffres", "Chi"), ("Images", "Ima")],
    "Vitesse de Traitement": [("Code", "Cod"), ("Symboles", "Sym")]
}

all_scores = []
short_labels = []
for group_name, subs in groups.items():
    st.sidebar.markdown(f"**{group_name}**")
    for full_name, short_name in subs:
        score = st.sidebar.slider(full_name, 1, 19, 10, key=full_name)
        all_scores.append(score)
        short_labels.append(short_name)

st.subheader("🧩 Profil détaillé des Subtests (Analyse par paires)")

# Graphique
fig, ax = plt.subplots(figsize=(11, 4.2))
blue_color = '#1f77b4'
red_alert = '#d62728'

# Zones de fond
ax.axhspan(1, 7, facecolor='red', alpha=0.05)
ax.axhspan(7, 13, facecolor='gray', alpha=0.05)
ax.axhspan(13, 19, facecolor='green', alpha=0.05)

indices_names = ["ICV", "IVS", "IRF", "IMT", "IVT"]

# Tracé par paires uniformisé
for i in range(0, 10, 2):
    pair_scores = all_scores[i:i+2]
    
    # Ligne de liaison entre les deux subtests
    ax.plot([i, i+1], pair_scores, color=blue_color, linewidth=1.2, alpha=0.3, zorder=1)
    
    for j in range(2):
        idx = i + j
        score = pair_scores[j]
        color = red_alert if score < 7 else blue_color
        
        # Point affiné
        ax.plot(idx, score, marker='o', color=color, markersize=7, zorder=3)
        # Moustache nette
        ax.errorbar(idx, score, yerr=1.2, fmt='none', ecolor=color, 
                    elinewidth=1.2, capsize=4, alpha=1.0, zorder=2)
        # Texte score
        ax.text(idx, score + 1.4, str(score), ha='center', fontweight='bold', 
                color=color, fontsize=10)

    # Nom de l'indice
    ax.text(i + 0.5, -2, indices_names[i//2], ha='center', fontweight='bold', 
            fontsize=10, color='#555555')

ax.set_ylim(-3, 21)
ax.set_yticks([1, 7, 10, 13, 19])
ax.set_xticks(range(10))
ax.set_xticklabels(short_labels, fontsize=9)
ax.grid(axis='y', linestyle=':', alpha=0.4)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

st.pyplot(fig)

# Analyse
st.markdown("---")
hétéro = [indices_names[i] for i in range(5) if abs(all_scores[i*2] - all_scores[i*2+1]) >= 3]
if hétéro:
    st.warning(f"⚠️ Dissociation intra-indice : {', '.join(hétéro)}.")
else:
    st.success("✅ Profil intra-indice homogène.")
