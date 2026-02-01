""" ====================================================================
Illustration du critère de Rayleigh.


Possibilité de modifier:
 - longueur d'onde (variable: lamb)
 - largeur de la fente (variable: a)
 - distance focale de la lentielle de sortie (variable: f)
 
On observe:
 - l'éclairement 2D, tel qu'on le voit sur un écran
 - l'éclairement 1D

	Auteur: Grégoire Martouzet, gregoire.martouzet@ens-paris-saclay.fr

	2 mai 2018
==================================================================== """

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.widgets import Slider, Button, RadioButtons
from scipy.special import jn

""" ----- Paramètres physiques (unité SI) ----- """
f = 1		# Focale de la lentille de sortie
a = 0.1e-3	# Taille de la fente (largeur ou diamètre)
lamb = 500e-9	# Longeur d'onde

# Coordonnées réduites
cr = a/lamb

""" ----- Paramètres de simulation ----- """
N = 200		# Nombre de point
N_mat = 100	# Nombre de point sur l'écran

# Borne pour l'angle
theta_min = -10e-3
theta_max = 10e-3

# Liste angle
theta = np.linspace(theta_min, theta_max, N)

# Position sur l'écran
x_mat = np.linspace(theta_min, theta_max, N_mat)
y_mat = np.linspace(theta_min/2, theta_max/2, N_mat//2)

X, Y = np.meshgrid(x_mat, y_mat)

""" ----- Paramèters initiaux ----- """
theta_ini = 0.0
# mode = 1 : fentes
# 		 2 : Ouverture circulaire
mode = 1

""" ----- Fonctions éclairment ----- """
# Sinc carré
def sinc2(theta, theta0):
	eta = (theta - theta0) * cr
	return np.sinc(eta)**2
	
# Bessel
def J1(theta, theta0):
	eta = np.pi * (theta - theta0) * cr
	return (jn(1,eta)/eta)**2
	
""" ----- Création fenêtre ----- """
fig = plt.figure()
#fig.canvas.set_window_title('Critère de Rayleigh')

""" ----- Creation des axes ----- """
# Axe principal (intensité)
axe_principal = plt.axes([0.12, 0.15, 0.78, 0.35])
axe_principal.set_title('Eclairement')

axe_principal.set_ylabel('$I(\Theta)/I_0$')
axe_principal.set_xlabel('$\Theta$ (mrad)')

axe_principal.axis([theta_min*1000, theta_max*1000, -0.1, 2.2])

# Image de l'écran
axe_ecran = plt.axes([0.12, 0.6, 0.78, 0.35])
axe_ecran.text(theta_min*f*1000, theta_max*f/2.5*1000,'Ecran',color='white')

#axe_ecran.axis('off')
axe_ecran.set_xlabel('x (mm)')
axe_ecran.set_ylabel('y (mm)')

# Axes des widgets 
axangle = plt.axes([0.12, 0.025, 0.78, 0.03])	# Slider angle
rayax = plt.axes([0.05, 0.65, 0.1, 0.1])		# Btn Rayleigh
rax = plt.axes([0.05, 0.8, 0.1, 0.1])			# Choix de la fente

""" ----- Calcul d'élairement ----- """
def eclairement(theta, d):
	
	if mode == 1: # Fentes
		y1 = sinc2(theta, 0)
		y2 = sinc2(theta, d)
	else:	# Ouverture circulaire
		y1 = J1(theta, 0)
		y2 = J1(theta, d)
	
	# Normalisation
	y1 /= max(y1)
	y2 /= max(y2)
	
	return y1, y2, y1+y2

def eclairement2D(x, y, d):
	
	if mode == 1: # Fentes
		y1 = sinc2(x, 0)
		y2 = sinc2(x, d)
	else:	# Ouverture circulaire
		R = np.sqrt(x**2+y**2)
		R2 = np.sqrt((x-d)**2+y**2)
		
		y1 = J1(R, 0)
		y2 = J1(R2, 0)
	
	# On normalise comme on veut, c'est juste pour l'affichage sur l'écran
	# Objectif: faire ressortir les détails ?
	y1 /= np.amax(y1)
	y2 /= np.amax(y2)
	
	Z = (y1 + y2)/2
	#Z /= np.amax(Z)
	
	Z = Z**(1/2)
	
	# Inversion du contraste
	Z = 1 - Z
	
	return Z

""" ----- Cacluls initiaux ----- """
y1, y2, y3 = eclairement(theta, theta_ini)

l1, = axe_principal.plot(theta*1000, y1, color = 'blue')
l2, = axe_principal.plot(theta*1000, y2, color = 'red')
l3, = axe_principal.plot(theta*1000, y3, lw=2, color = 'green')

Z = eclairement2D(X, Y, theta_ini)

img_ecran = axe_ecran.matshow(Z, interpolation='bessel',
                            extent = (theta_min*f*1000, theta_max*f*1000, f*theta_min/2*1000, f*theta_max/2*1000),
                            vmin=0,
                            vmax=1, 
                            cmap='Greys')

""" ----- Fonction de mise à jour ----- """
def change_angle(val):
	
	val = sangle.val/1000
	
	y1, y2, y3 = eclairement(theta, val)
	
	Z = eclairement2D(X, Y, val)
	
	l1.set_ydata( y1 )
	l2.set_ydata( y2 )
	l3.set_ydata( y3 )
	img_ecran.set_data( Z )
	
	plt.draw()

def get_rayleigh(event):
	
	if mode == 1:
		val = 1/cr		# Critère de Rayleigh pour une fente
	else:
		val = 1.22/cr	# Critère de Rayleigh pour un trou
	
	sangle.set_val(val*1000)
	
	change_angle(0)

def change_fente(label):
	global mode
	
	if label=='Fentes':
		mode = 1
	else:
		mode = 2
		
	change_angle(0)

""" ----- Création des widgets ----- """
# Slider angle	
sangle = Slider(axangle, '$\Delta\Theta$ (mrad)', theta_min*1000, theta_max*1000, valinit=theta_ini)
sangle.on_changed(change_angle)

# Btn Critère de Rayleigh	
button = Button(rayax, 'Rayleigh')
button.on_clicked(get_rayleigh)

# Choix fentes/trous	
radio = RadioButtons(rax, ('Fentes', 'Trous'), active=0)
radio.on_clicked(change_fente)

""" ----- Affichage fenêtre ----- """
plt.show()
