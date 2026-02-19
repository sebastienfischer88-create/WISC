import streamlit as st
import matplotlib.pyplot as plt

st.set_page_config(page_title="WISC-V Subtests - Analyse Clinique", layout="wide")

st.markdown("""
    <style>
    .block-container {padding-top: 1.5rem; padding-bottom: 0rem;}
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
for group_name, subs in groups.items():
    st.sidebar.markdown(f"**{group_name}**")
    for full_name, short_name in subs:
        score = st.sidebar.slider(full_name, 1, 19, 10, key=full_name)
        all_scores.append(score)

st.subheader("🧩 Profil détaillé des Subtests (Analyse par paires)")

# --- CONFIGURATION GRAPHIQUE ---
fig, ax = plt.subplots(figsize=(11, 4.2))
blue_color = '#1f77b4'  # Bleu professionnel uniforme pour tout

# Zones de performance discrètes
ax.axhspan(1, 7, facecolor='red', alpha=0.05)
ax.axhspan(7, 13, facecolor='gray', alpha=0.05)
ax.axhspan(13, 19, facecolor='green', alpha=0.05)

short_labels = ["Sim", "Voc", "Cub", "Puz", "Mat", "Bal", "Chi", "Ima", "Cod", "Sym"]
indices_names = ["ICV", "IVS", "IRF", "IMT", "IVT"]

# Tracé par paires uniformisé en bleu
for i in range(0, 10, 2):
    pair_scores = all_scores[i:i+2]
    
    # Ligne et points bleus
    ax.plot([i, i+1], pair_scores, color=blue_color, marker='o', 
            linewidth=2.5, markersize=9)
    
    # Barres d'erreur (moustaches) désormais en bleu également
    ax.errorbar([i, i+1], pair_scores, yerr=1.2, fmt='none', 
                ecolor=blue_color, elinewidth=1.5, capsize=4, alpha=0.6)
    
    # Affichage des notes
    for j, s in enumerate(pair_scores):
        ax.text(i+j, s + 1.4, str(s), ha='center', fontweight='bold', color=blue_color, fontsize=10)
        
    # Nom de l'indice sous chaque paire
    ax.text(i + 0.5, -2, indices_names[i//2], ha='center', 
            fontweight='bold', fontsize=10, color='#555555')

ax.set_ylim(-3, 21)
ax.set_yticks([1, 7, 10, 13, 19])
ax.set_xticks(range(10))
ax.set_xticklabels(short_labels, fontsize=9)
ax.grid(axis='y', linestyle=':', alpha=0.4)

ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

st.pyplot(fig)

# --- ANALYSE DYNAMIQUE ---
st.markdown("---")
hétéro = []
for i, name in enumerate(indices_names):
    diff = abs(all_scores[i*2] - all_scores[i*2+1])
    if diff >= 3: 
        hétéro.append(f"**{name}**")

if hétéro:
    st.warning(f"⚠️ **Hétérogénéité intra-indice :** {', '.join(hétéro)}. La dispersion suggère un fonctionnement irrégulier au sein de ces domaines.")
else:
    st.success("✅ **Profil homogène :** Les capacités mesurées au sein de chaque indice sont cohérentes.")
