#
#	Grégoire Martouzet
#	gregoire.martouzet@ens-paris-saclay.fr
#

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.widgets import Slider

N 	= 20
a = 1e-6
b = 0.5e-7
alpha = 0.0

Nb = 100000

# longeur d'onde (m)
lambda_bleu = 480e-9
lambda_vert = 630e-9
lambda_rouge = 700e-9

""" ----- paramètres d'affichage ----- """
# 0/1 = pas affiché / affiché
blaze = 1		# réseau blazé
structure = 1	# prise en compte de la largeur des fentes
rouge = 1		# affichage du rouge
vert = 1		# affichage du vert

def I(theta, lamb):
	
	if structure:
		amp = np.sinc(np.pi*b*np.sin(theta-alpha)/lamb) **2
	else:
		amp = np.ones(Nb)
	
	i = np.sin(N*a*np.pi*np.sin(theta)/lamb)**2 / np.sin(a*np.pi*np.sin(theta)/lamb)**2
	
	i /= max(i)
	
	return amp*i, amp

# Mise à jour des widgets
def maj_slider(val):
	global b, N, a, alpha
	
	N = int(sN.val)
	a = 10**sa.val
	
	if structure:
		b = 10**sb.val
	
	if blaze:
		alpha = salpha.val
	
	sN.valtext.set_text('{}'.format(N))
	
	I_b, A_b = I(theta, lambda_bleu)
	l_bleu.set_ydata(I_b)
	if structure:
		a_bleu.set_ydata(A_b)
		
	if rouge:
		I_r, A_r = I(theta, lambda_rouge)
		l_rouge.set_ydata(I_r)
		if structure:
			a_rouge.set_ydata(A_r)
	if vert:
		I_v, A_v = I(theta, lambda_vert)
		l_vert.set_ydata(I_v)
		if structure:
			a_vert.set_ydata(A_v)

""" ----- Création de la fenetre ----- """
fig = plt.figure()
#fig.canvas.set_window_title('Diffraction par structure périodique')	

theta_min = -np.pi/2
theta_max = np.pi/2

decalage = 3

ax1 = plt.axes([0.1, 0.05, 0.8, 0.05])
sN = Slider(ax1, '$N$', 1, 100, valinit=N)
sN.valtext.set_text('{}'.format(N))

ax2 = plt.axes([0.1, 0.12, 0.8, 0.05])
sa = Slider(ax2, '$a$ (m) $10^x$', -7, -4, valinit=np.log10(a))

if structure:
	decalage += 1
	ax3 = plt.axes([0.1, 0.19, 0.8, 0.05])
	sb = Slider(ax3, '$b$ (m) $10^x$', -8, -5, valinit=np.log10(b))
	sb.on_changed(maj_slider)

if blaze:
	decalage += 1
	ax4 = plt.axes([0.1, 0.26, 0.8, 0.05])
	salpha = Slider(ax4, '$\\alpha$ (rad)', 0, theta_max, valinit=alpha)
	salpha.on_changed(maj_slider)
	

bottom = 0.05 + 0.07*(decalage+0)	

ax = plt.axes([0.1, bottom, 0.8, 0.9-bottom])
	
sN.on_changed(maj_slider)
sa.on_changed(maj_slider)

theta = np.linspace(theta_min, theta_max, Nb)

if rouge:
	I_r, A_r = I(theta, lambda_rouge)
	l_rouge, = ax.plot(theta, I_r, 'r')
	if structure:
		a_rouge, = ax.plot(theta, A_r, 'r', alpha=0.5)
	
if vert:
	I_v, A_v = I(theta, lambda_vert)
	l_vert, = ax.plot(theta, I_v, 'g')
	if structure:
		a_vert, = ax.plot(theta, A_v, 'g', alpha=0.5)

I_b, A_b = I(theta, lambda_bleu)	
l_bleu, = ax.plot(theta, I_b, 'b')
if structure:
	a_bleu, = ax.plot(theta, A_b, 'b', alpha=0.5)		
		
	
ax.set_xlabel('$\\theta$ (rad)')

ax.set_ylabel('$I(\\theta)/I_0$')
ax.axis([theta_min, theta_max, -0.1, 1.1])

plt.show()

