import streamlit as st
import matplotlib.pyplot as plt

# ... (Configuration et CSS identiques) ...

# --- CONFIGURATION GRAPHIQUE ---
fig, ax = plt.subplots(figsize=(10, 4))
blue_color = '#1f77b4' 
red_alert = '#d62728' # Rouge vif pour l'alerte

# Zones de fond
ax.axhspan(40, 70, facecolor='red', alpha=0.05)
ax.axhspan(85, 115, facecolor='gray', alpha=0.05)
ax.axhspan(130, 160, facecolor='green', alpha=0.05)

labels = ['ICV', 'IVS', 'IRF', 'IMT', 'IVT']
scores = [icv, ivs, irf, imt, ivt]

# Tracé de la ligne de fond (en bleu léger ou gris)
ax.plot(labels, scores, color=blue_color, linewidth=1, alpha=0.3, zorder=1)

# Tracé point par point pour la coloration dynamique
for i, (label, score) in enumerate(zip(labels, scores)):
    # Détermination de la couleur
    current_color = red_alert if score < 70 else blue_color
    
    # Point et Moustache
    ax.plot(label, score, marker='o', color=current_color, markersize=7, zorder=3)
    ax.errorbar(label, score, yerr=4, fmt='none', ecolor=current_color, 
                elinewidth=1.2, capsize=6, zorder=2)
    
    # Score texte
    ax.text(i, score + 7, str(score), ha='center', fontweight='bold', 
            color=current_color, fontsize=11)

# ... (Fin du code identique) ...
