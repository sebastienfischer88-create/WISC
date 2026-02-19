import streamlit as st
import matplotlib.pyplot as plt

st.set_page_config(page_title="WISC-V Subtests", layout="wide")

st.markdown("<style>.block-container {padding-top: 1rem;}</style>", unsafe_allow_html=True)
st.subheader("🧩 Profil Détallé des Subtests (M=10)")

sub_names = ["Sim", "Voc", "Cub", "Puz", "Mat", "Bal", "Chi", "Ima", "Cod", "Sym"]
cols = st.columns(10)
scores = []
for i, name in enumerate(sub_names):
    with cols[i]:
        scores.append(st.slider(name, 1, 19, 10))

fig, ax = plt.subplots(figsize=(12, 4.5))
ax.axhspan(1, 7, facecolor='red', alpha=0.08, label="Faiblesse")
ax.axhspan(7, 13, facecolor='gray', alpha=0.08, label="Moyenne")
ax.axhspan(13, 19, facecolor='green', alpha=0.08, label="Force")

ax.errorbar(sub_names, scores, yerr=1.5, fmt='o-', color='#1f77b4', ecolor='orange', elinewidth=3, capsize=6, markersize=10, linewidth=3)

for i, s in enumerate(scores):
    ax.text(i, s + 1.2, str(s), ha='center', fontweight='bold')

ax.set_ylim(0, 20)
ax.set_yticks([1, 7, 10, 13, 19])
ax.grid(axis='y', linestyle=':', alpha=0.3)
ax.legend(loc='lower right', fontsize='small')

st.pyplot(fig)
