"""
Martouzet Grégoire - gregoire.martouzet@ens-paris-saclay.fr

----------------------------------------

Affichage de l'énergie libre dans le cas du model de Landau (pour différentes températures).

Energie libre de Landau:
F = alpha*(T/Tc-1)*m**2 + beta*m**4
"""

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.widgets import Slider

""" ----- Paramètres ----- """
N = 1000 # Nombre de point à calculer

# liste de température pour Landau
liste_t_landau = [0.001,0.01,0.1,1,10]

# Aimantation pour Landau
m_landau = np.linspace(-10,10,N)


""" ---------- """

# Energie libre de Landau
def F(m, T):
	
	alpha = 1
	beta = 1e-2
	Tc = 1
	
	return alpha*(T/Tc-1)*m**2 + beta*m**4	
	
# Calcul de F en fonction de l'aimantation pour chaque température
for T in liste_t_landau:
	f = F(m_landau, T)
	plt.plot(m_landau, f, label='$T=$'+str(T))
				
plt.axis([-10,10,-30,100])
plt.legend()

plt.show()
