"""
Martouzet Grégoire - gregoire.martouzet@ens-paris-saclay.fr

----------------------------------------

Résolution de l'équation auto-cohérente en champ moyen pour différentes températures et différents champs magnétiques
 
Equation auto-cohérente (cf DIU - Physique statistique):
tanh(x) = T/Tc*x - B/B0

  avec:
	x = M/M_inf
	M_inf = N*g*nu_b/(2*V)
	Tc = température critique
	B0 = -g*mu_b/(2*k*Tc)

"""

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.widgets import Slider

""" ----- Paramètres ----- """
N = 1000 # Nombre de point à calculer

temperature = np.linspace(0.25,1.75, 100)

x = np.linspace(-20, 20, N)

""" ---------- """

# Fonction pour le champ moyen
def fct1(x):
	return np.tanh(x)
	
def fct2(x, t, b):
	return t*x - b

# Fonction cohérente par défaut
y1= fct1(x)

# recherche des solutions de l'équation auto-cohérente
def search_and_append(y1, y2, t, T, M, X):
	y = y1-y2
	
	y3 = np.roll(y, 1)
	y3[0] = y[0]
	
	y3 *= y
	
	for i in range(len(y2)-1):
		if y3[i]<0:
			A = abs(y[i-1]/y[i])
			x_p = (A*x[i]+x[i-1])/(1+A)
			
			M.append( fct1(x_p) )
			T.append( t )
			X.append( x_p )
	
""" ----- fonctions de mise à jour des graphiques (uniquement dans le cas de champ moyen)----- """		

# MAJ lors d'une modification de B ou T
def update_graph(val):
	param_t = sT.val
	param_B = sB.val
	
	# détermination de la nouvelle fonction auto-cohérente
	y2 = fct2(x, param_t, param_B)
	
	l.set_ydata( y2 )
	
	T = []
	M = []
	X = []
	
	# recherche des solutions
	search_and_append(y1, y2, param_t, T, M, X)
	
	l2.set_data(X, M)
	
	
""" Résolution graphique de l'équation (avec Slider) """ 
plt.gcf().canvas.set_window_title('Equation auto-cohérente')

axG = plt.axes([0.1, 0.3, 0.8, 0.65])

axG.axis([-7.5,7.5,-1.2,1.2])
	
y1 = fct1(x)
y2 = fct2(x, 0.5, 0.0)
	
# Tracer des deux fonctions à égaliser
axG.plot(x, y1)
l, = axG.plot(x, y2)
	
# Recherche de solutions
T = []
M = []
X = []
search_and_append(y1, y2, 0.5, T, M, X)
	
# Petit ronds rouges au niveau des solutions
l2, = axG.plot(X, M, 'or')

# Slider pour T et B
axT = plt.axes([0.1, 0.2, 0.8, 0.03])
sT = Slider(axT, '$T/T_c$', 0.25, 1.5, valinit=0.5)
sT.on_changed(update_graph)

axB = plt.axes([0.1, 0.1, 0.8, 0.03])
sB = Slider(axB, '$B/B_0$', 0, 0.05, valinit=0)
sB.on_changed(update_graph)

plt.show()
