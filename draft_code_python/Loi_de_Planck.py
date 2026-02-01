""" ====================================================================
Calcul du spectre d'un corps à partir de la loi de Planck
Donne également des éléments tel que le maximum, la constante de Stefan, etc

Pour modifier les températures à afficher, modifier la liste "temperature"

	Auteur: Grégoire Martouzet, gregoire.martouzet@ens-paris-saclay.fr

	24 septembre 2017
==================================================================== """

# Importation des bibliothèques
import numpy as np
import matplotlib.pyplot as plt
import scipy.integrate as integrate
from matplotlib.legend_handler import HandlerLine2D

# Liste des températures à traiter (en K)
temperature = [300,2000,6000]
	



""" ----- Physique ----- """
# Constantes physiques (unités SI)
h = 6.63e-34	# Constante de Planck
c = 3e8			# Vitesse de la lumière
kb = 1.38e-23	# Constante de Boltzmann

# Loi de Planck
u = lambda l, T: (8*np.pi*h*c)/(l**5) * 1/(np.exp((h*c)/(kb*l*T))-1)




""" ----- Paramètres de calcul ----- """
# Limite de la fenêtre en longueur d'onde (lambda) (en m)
lambda_max = 1e-3
lambda_min = 1e-7
n_points = 1000 # Nombre de points

# Limite de la fenêtre en densité spectrale (W/m^2)
u_min = 10e-10
u_max = 10e6

# Liste des longueurs d'onde pour le calcul de la loi de Planck 
lambd = np.logspace(np.log10(lambda_min), np.log10(lambda_max), num=n_points)



""" ----- Création de la fenetre ----- """
fig = plt.figure()
#fig.canvas.set_window_title('Loi de Planck')



""" ----- Fonctions utiles ----- """
# Fonction pour trouver le maximum dans une liste
# utilisée pour déterminer lambda_max, longueur d'onde telle que u_lambda soit maximal
def recherche_max(liste):
	m = 0 # maximum
	p_m = 0 # position du maximum
	
	for i, element in enumerate(liste):
		if element>m:
			m=element
			p_m=i
	return m, p_m
	
# Fonction pour trouver la position d'un element dans une liste (si il n'est pas present, retourne la position précédente)
# ne fonctionne que pour une liste triée ! (ce qui est le cas de la liste lambd)
# utilisée pour extraire la sous-liste [0.5l; 8l] 
def recherche_element(liste, element):
	
	for i in range(len(liste)-1):
		if (liste[i]<=element) and (liste[i+1]>element):
			return i
	return len(liste)-1
	
	

""" ----- Affichage du visible ----- """
# Bornes du visible et dessin des bornes sur le graphique
l_visible = [
	[380e-9, '#68228b'],
	[450e-9, 'b'],
	[525e-9, 'g'],
	[575e-9, 'y'],
	[650e-9, '#FF8000'],
	[780e-9, 'r']]

for l in l_visible:
	plt.axvline(l[0], linewidth=3, color=l[1], alpha=0.5)
plt.text(525e-9, 0.5*u_min, 'Visible', horizontalalignment='center', verticalalignment='top')



""" ----- Boucle sur toutes les temperatures ----- """
for T in temperature:
	
	# Calcul de u pour les lambdas considérés
	y = u(lambd, T)
	# Trace la densité
	l, = plt.loglog(lambd, y, linewidth = 1.5)
	
	# Recherche du maximum
	# m = valeur du maximum de la liste y
	# pm = position de ce maximum dans la liste
	m, p_m = recherche_max(y)
	l_max = lambd[p_m]
	
	# Integration numérique de la densité -> on obtient la puissance
	P = c/4 * integrate.simps(y, lambd)
	
	# Recherche des positions des points 0.5l_max et 8l_max dans la liste lambd
	i_int_min = recherche_element(lambd, l_max*0.5)
	i_int_max = recherche_element(lambd, l_max*8)
	
	# Dessin de ces bornes sur le graphique
	y_tmp = u(lambd[i_int_min: i_int_max], T)
	plt.loglog(lambd[i_int_min: i_int_max], y_tmp, linewidth = 3, color=l.get_color(), label = '$T = %i K$'%T)
	plt.plot((l_max*0.5, l_max*8), (y[i_int_min], y[i_int_max]), 'ko')
	
	# Integration numérique de la densité -> Puissance entre 0.5*Lambda et 8*Lambda
	P_partielle = c/4 * integrate.simps(y[i_int_min: i_int_max], lambd[i_int_min: i_int_max])
	
	# Sortie: quelque grandeurs importantes
	print('Temperature = %i K'%T) # Température de calcul
	
	print('    l_max = %.0f nm'%(lambd[p_m]*1e9)) # Lambda max
	print('    M = %.0f W/m2'%P) # Emittance
	
	print('    M[0.5L:8L] =  %.0f W/m^2'%P_partielle) # Emittance sur l'intervalle [0.5l: 8l]
	
	
	print('     ->  l_max*T = %.0f um*K'%(lambd[p_m]*T*1e6)) # Constante de Wien ~2900um*K
	print('     ->  M/T^4 = %.3fe-8 W/m^2/K^4'%(1e8*P/T**4)) # Constante de Stephan ~5.67e-8 W/m/K^-4
	print('     ->  M[0.5L:8L]/M = %.3f'%(P_partielle/P)) # Rapport (Emittance partielle)/(Emittance totale), toujours ~0.98
	print('')



""" ----- Mise en forme du graphique et affichage ----- """
# Labels et legende du graphique
line_temp, = plt.plot([], [] ,'ok', label = '98%') # Ajout à la legende la zone à 98%
plt.xlabel('$\lambda$ (m)', fontsize = 'x-large')
plt.ylabel('$u_\lambda(\lambda, T)$ (W m$^{-4}$)', fontsize = 'x-large')
plt.title('Loi de Planck')
plt.legend(fontsize = 'x-large', handler_map={line_temp: HandlerLine2D(numpoints=2)})
	
# Borne d'affichage
plt.axis([lambda_min, lambda_max, u_min, u_max])

# Affichage
plt.show()
