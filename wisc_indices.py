import streamlit as st
import matplotlib.pyplot as plt

st.set_page_config(page_title="WISC-V Indices", layout="wide")

st.markdown("<style>.block-container {padding-top: 1rem;}</style>", unsafe_allow_html=True)
st.subheader("📊 Profil des Indices Principaux (M=100)")

labels = ['ICV', 'IVS', 'IRF', 'IMT', 'IVT']
cols = st.columns(5)
scores = []
for i, l in enumerate(labels):
    with cols[i]:
        scores.append(st.slider(l, 45, 155, 100))

fig, ax = plt.subplots(figsize=(12, 4.5))
ax.axhspan(40, 70, facecolor='red', alpha=0.08, label="Déficit")
ax.axhspan(85, 115, facecolor='gray', alpha=0.08, label="Moyenne")
ax.axhspan(130, 160, facecolor='green', alpha=0.08, label="HPI")

ax.errorbar(labels, scores, yerr=6, fmt='o-', color='#1f77b4', ecolor='orange', elinewidth=3, capsize=6, markersize=10, linewidth=3)

for i, s in enumerate(scores):
    ax.text(i, s + 8, str(s), ha='center', fontweight='bold')

ax.set_ylim(40, 160)
ax.set_yticks([40, 70, 85, 100, 115, 130, 160])
ax.grid(axis='y', linestyle=':', alpha=0.3)
ax.legend(loc='lower right', fontsize='small')

st.pyplot(fig)
