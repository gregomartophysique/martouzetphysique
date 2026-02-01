"""
Trajectoire d'un point autour d'un centre et affichage de la zone d'énergie potentielle accessible.

Martouzet Grégoire - gregoire.martouzet@ens-paris-saclay.fr
"""

import matplotlib.pyplot as plt
from matplotlib.widgets import Slider
import numpy as np

# Paramètres
N = 100 # Nombre de point

# Liste des angles theta (paramétrisation en polaire
theta = np.linspace(0.0, 2*np.pi, N)

# Fonction r(theta)
def r(theta, e, p):
	return p/(1-e*np.cos(theta))
	
# Création de la fenêtre et des axes

# Graph 2D
ax1 = plt.axes([0.05, 0.55, 0.9, 0.4])
ax1.get_xaxis().set_visible(False)
ax1.get_yaxis().set_visible(False)
ax1.set_aspect('equal', 'datalim')

# Graph de l'énergie
axEN = plt.axes([0.05, 0.15, 0.9, 0.35])
axEN.axis([0.0, 15, -1.2, 0.1])

# Slider pour modifier l'excentricité
ax_slider = plt.axes([0.1, 0.03, 0.85, 0.04])

# Fonction mise à jour des axes
def maj_e(event):
	
	e = se.val
	p = 0.5
	
	# Calul de la nouvelle trajectoire
	R = r(theta, e, p)
	
	rmin = min(R)/p
	rmax = max(R)/p
	
	# Calul de l'énergie accessible
	rayon_accessible = np.linspace(max([rmin,0.5]), min([15, rmax]), N)
	EM = -2/rayon_accessible+1/rayon_accessible**2
	
	EM_bornes = -2/rmin+1/rmin**2
	
	# Mise à jour graphique
	l1.set_data(R*np.cos(theta), R*np.sin(theta)) # Trajectoire
	l3.set_data(rayon_accessible, EM) # Energie
	l4.set_data([rmin, rmax], [EM_bornes,EM_bornes]) # bornes des rayons accessibles

# Slider
se = Slider(ax_slider, '$e=$', 0, 1.5, valinit=0.0)
se.on_changed(maj_e)


""" ----- Premiers calculs et affichage ----- """
# trajectoire
R = r(theta, 0.0, 1.0)
l1, = ax1.plot(R*np.cos(theta), R*np.sin(theta))

# Image de la planète
ax1.plot(0,0, 'ro')

# Calcul de l'énergie mécanique
rayon = np.linspace(0.5, 15, N)
EM = -2/rayon+1/rayon**2 # energie


# Energie mécanique 
l2, = axEN.plot(rayon, EM, 'k', lw=0.5)

# Energie mécanique accessible
rmin = min(R)
rmax = max(R)

EM_bornes = -2/rmin+1/rmin**2 # bornes de l'energie	

rayon_accessible = np.linspace(max([rmin,0.5]), min([15, rmax]), N)

l3, = axEN.plot(rayon_accessible, EM, 'b')
l4, = axEN.plot([rmin, rmax], [EM_bornes,EM_bornes], 'bo')

# Affichage
plt.show()
