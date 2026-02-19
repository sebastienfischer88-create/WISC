import streamlit as st
import matplotlib.pyplot as plt

st.set_page_config(page_title="Simulateur WISC-V Complet", layout="centered")

st.title("📊 Simulateur WISC-V : Profils Cliniques")
st.write("Analyse des zones de performance (Déficit, Normalité, HPI).")

# 1. Configuration Sidebar
st.sidebar.header("Réglages des scores")
conf_level = st.sidebar.radio("Niveau de confiance", ["90%", "95%"])
sem = 4  
z_score = 1.645 if conf_level == "90%" else 1.96
margin = round(z_score * sem)

icv = st.sidebar.slider("ICV (Verbal)", 45, 155, 100)
ivs = st.sidebar.slider("IVS (Visuospatial)", 45, 155, 100)
irf = st.sidebar.slider("IRF (Raisonnement)", 45, 155, 100)
imt = st.sidebar.slider("IMT (Mémoire)", 45, 155, 100)
ivt = st.sidebar.slider("IVT (Vitesse)", 45, 155, 100)

indices = ['ICV', 'IVS', 'IRF', 'IMT', 'IVT']
scores = [icv, ivs, irf, imt, ivt]
y_err = [margin] * 5

# 2. Graphique
fig, ax = plt.subplots(figsize=(10, 7))

# --- ZONES PÉDAGOGIQUES ---
# Zone Déficitaire (< 70)
ax.axhspan(40, 70, facecolor='#FF0000', alpha=0.1, label="Zone de déficit (< 70)")

# Zone Moyenne (85 - 115)
ax.axhspan(85, 115, facecolor='gray', alpha=0.1, label="Zone moyenne (85-115)")

# Zone HPI (> 130)
ax.axhspan(130, 160, facecolor='#2ECC71', alpha=0.1, label="Zone de Haut Potentiel (> 130)")

# Lignes de repère horizontales
ax.axhline(130, color='green', linestyle='--', linewidth=1, alpha=0.5)
ax.axhline(100, color='black', linestyle='-', linewidth=0.5, alpha=0.3)
ax.axhline(70, color='red', linestyle='--', linewidth=1, alpha=0.5)

# --- TRACÉ ---
ax.errorbar(indices, scores, yerr=y_err, fmt='o-', color='#1f77b4', 
            ecolor='#E67E22', elinewidth=3, capsize=6, markersize=10, 
            linewidth=2, label=f"Score et IC {conf_level}")

# Scores et Intervalles
for i, score in enumerate(scores):
    ax.text(i, score + margin + 3, f"{score}\n[{score-margin}-{score+margin}]", 
            ha='center', fontsize=9, fontweight='bold')

# Mise en forme
ax.set_ylim(40, 160)
ax.set_yticks([40, 70, 80, 90, 100, 110, 120, 130, 140, 150, 160])
ax.set_ylabel("Note Standard")
ax.set_title("Analyse du Profil WISC-V", fontsize=15)
ax.legend(loc='lower right', fontsize='small')
ax.grid(axis='y', linestyle=':', alpha=0.2)

st.pyplot(fig)

# --- ANALYSE DYNAMIQUE ---
st.subheader("Analyse rapide :")
col1, col2 = st.columns(2)

with col1:
    if max(scores) >= 130:
        st.success("✅ Point de force : Au moins un indice est dans la zone HPI.")
    if min(scores) <= 70:
        st.error("⚠️ Point de vigilance : Au moins un indice est dans la zone de déficit.")

with col2:
    dispersion = max(scores) - min(scores)
    if dispersion >= 23:
        st.warning(f"❗ Hétérogénéité forte : {dispersion} pts d'écart. Le CIT est à interpréter avec prudence.")
    else:
        st.info(f"📊 Profil homogène : {dispersion} pts d'écart.")
