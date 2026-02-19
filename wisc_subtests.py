import streamlit as st
import matplotlib.pyplot as plt

st.set_page_config(page_title="WISC-V Subtests", layout="wide")

st.markdown("""
    <style>
    .block-container {padding-top: 2rem; padding-bottom: 0rem;}
    </style>
    """, unsafe_allow_html=True)

st.sidebar.header("Notes des Subtests")
sub_names = ["Similitudes", "Vocabulaire", "Cubes", "Puzzles", "Matrices", 
             "Balances", "Chiffres", "Images", "Code", "Symboles"]

scores = [st.sidebar.slider(name, 1, 19, 10) for name in sub_names]
labels_short = ["Sim", "Voc", "Cub", "Puz", "Mat", "Bal", "Chi", "Ima", "Cod", "Sym"]

st.subheader("🧩 Profil des Subtests")

fig, ax = plt.subplots(figsize=(10, 3.8))

ax.axhspan(1, 7, facecolor='red', alpha=0.08)
ax.axhspan(7, 13, facecolor='gray', alpha=0.08)
ax.axhspan(13, 19, facecolor='green', alpha=0.08)

ax.errorbar(labels_short, scores, yerr=1.2, fmt='o-', color='#1f77b4', ecolor='orange', 
            elinewidth=2, capsize=4, markersize=8, linewidth=2)

for i, s in enumerate(scores):
    ax.text(i, s + 1.2, str(s), ha='center', fontweight='bold', fontsize=9)

ax.set_ylim(0, 21)
ax.set_yticks([1, 7, 10, 13, 19])
ax.grid(axis='y', linestyle=':', alpha=0.3)

st.pyplot(fig)

if max(scores) - min(scores) >= 5:
    st.info(f"💡 Écart : {max(scores) - min(scores)} pts.")
