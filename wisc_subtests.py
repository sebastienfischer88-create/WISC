import streamlit as st
import matplotlib.pyplot as plt

st.set_page_config(page_title="WISC-V Subtests - Analyse Clinique", layout="wide")

# CSS pour compacter et épurer le rendu
st.markdown("""
    <style>
    .block-container {padding-top: 1.5rem; padding-bottom: 0rem;}
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

st.subheader("🧩 Profil détaillé des Subtests (Analyse par paires)")

# --- CONFIGURATION GRAPHIQUE ---
fig, ax = plt.subplots(figsize=(11, 4.2))
blue_color = '#1f77b4'  # Bleu professionnel uniforme
orange_color = '#E67E22' # Orange pour les IC (contraste doux)

# Zones de performance discrètes
ax.axhspan(1, 7, facecolor='red', alpha=0.05)
ax.axhspan(7, 13, facecolor='gray', alpha=0.05)
ax.axhspan(13, 19, facecolor='green', alpha=0.05)

short_labels = ["Sim", "Voc", "Cub", "Puz", "Mat", "Bal", "Chi", "Ima", "Cod", "Sym"]
indices_names = ["ICV", "IVS", "IRF", "IMT", "IVT"]

# Tracé par paires uniformisé
for i in range(0, 10, 2):
    pair_scores = all_scores[i:i+2]
    pair_labels = short_labels[i:i+2]
    
    # Ligne et points bleus
    ax.plot([i, i+1], pair_scores, color=blue_color, marker='o', 
            linewidth=2.5, markersize=9, label=indices_names[i//2] if i==0 else "")
    
    # Intervalles de confiance orange (pour la rigueur)
    ax.errorbar([i, i+1], pair_scores, yerr=1.2, fmt='none', 
                ecolor=orange_color, elinewidth=2, capsize=4, alpha=0.8)
    
    # Affichage des notes au-dessus
    for j, s in enumerate(pair_scores):
        ax.text(i+j, s + 1.4, str(s), ha='center', fontweight='bold', color=blue_color, fontsize=10)
        
    # Nom de l'indice sous chaque paire
    ax.text(i + 0.5, -2, indices_names[i//2], ha='center', 
            fontweight='bold', fontsize=10, color='#555555')

# Finalisation des axes
ax.set_ylim(-3, 21)
ax.set_yticks([1, 7, 10, 13, 19])
ax.set_xticks(range(10))
ax.set_xticklabels(short_labels, fontsize=9)
ax.grid(axis='y', linestyle=':', alpha=0.4)

# Suppression des bordures inutiles pour plus de clarté
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

st.pyplot(fig)

# --- ANALYSE DYNAMIQUE ---
st.markdown("---")
hétéro = []
for i, name in enumerate(indices_names):
    diff = abs(all_scores[i*2] - all_scores[i*2+1])
    if diff >= 3: 
        hétéro.append(f"**{name}** ({diff} pts)")

if hétéro:
    st.warning(f"⚠️ **Dissociation intra-indice détectée :** {', '.join(hétéro)}. "
               "L'indice global correspondant peut manquer de cohérence.")
else:
    st.success("✅ **Profil homogène :** Les subtests au sein de chaque indice sont cohérents entre eux.")
