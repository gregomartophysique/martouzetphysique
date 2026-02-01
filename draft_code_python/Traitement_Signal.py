""" ====================================================================


Possibilité d'ajouter des filtres:
 - définir une fonction sur le modele de celles existantes
 - modifier le dictionnaire "liste_fonctions_transfert" en ajoutant le nom du filtre et le nom de la fonction correspondante
 
 
 
	Auteur: Grégoire Martouzet, gregoire.martouzet@ens-paris-saclay.fr

	7 janvier 2018
==================================================================== """

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import RadioButtons, Slider, Button, CheckButtons

""" ----- paramètres ----- """
H0 = 1
f0 = 1
Q = 1

# interface graphique ? (0/1) avec slider (1) ou pas (0)
graph = 1

# nombre de point dans le domaine temporel
N = 1000
# liste de temps
t = np.linspace(0.0, 4*np.pi, N)

# bornes d'affichage pour le bode (en puissance de 10)
f_min = -2
f_max = 2
f_bode = np.logspace(f_min, f_max, N)

# Nombre d'harmonique à calculer
nb_harmonique_carre = 200
nb_harmonique_triangle = 100

""" -----------------------
    Création fenêtre et axes
    ----------------------- """
fig = plt.figure()
#fig.canvas.set_window_title('Traitement du signal')

""" ----- Fonctions pour les signaux ----- """
def sinus():
	f = [1]
	amp = [1]
	phase = [0]
	s = gene_signal(f, amp, phase)
	return s, np.array(f), np.array(amp)
	
def triangle(n):
	# n: nombre d'harmonique
	f = [(2*i+1) for i in range(n)]
	amp = [(-1)**i * 1/(2*i+1)**2 for i in range(n)]
	phase = np.zeros(n)
	s = gene_signal(f, amp, phase)
	return s, np.array(f), np.array(amp)
	
def carre(n):
	# n: nombre d'harmonique
	f = [(2*i+1) for i in range(n)]
	amp = [1/(2*i+1) for i in range(n)]
	phase = np.zeros(n)
	s = gene_signal(f, amp, phase)
	return s, np.array(f), np.array(amp)


""" ----- Fonctions de transfert des filtres ----- """
def pb1(x):
	H = H0/(1+1j*x)
	return H
	
def ph1(x):
	H = H0*1j*x/(1+1j*x)
	return H
	
def pb2(x):
	H = H0/(1+(1j*x)**2+1j*x/Q)
	return H
	
def ph2(x):
	H = (H0*(1j*x)**2)/(1+(1j*x)**2+1j*x/Q)
	return H
	
def pbande2(x):
	H = H0/(1+1j*Q*(x-1/x))
	return H

def rej(x):
	H = H0*(1+(1j*x)**2)/(1+1j*x/Q+(1j*x)**2)
	return H

liste_fonctions_transfert = {
	'PB1' : pb1,
	'PH1' : ph1,
	'PB2' : pb2,
	'PH2' : ph2,
	'P Bande 2' : pbande2,
	'Rejecteur' : rej }

""" ----- ----- """
def gene_signal(frequence, amplitude, phase ):
	# signal
	s = np.zeros(N)
	
	# Somme sur tout les harmoniques voulues
	for i in range(len(frequence)):
		s += amplitude[i] * np.sin(frequence[i]*t + phase[i])
	return s

def signal_filtre(frequence, amplitude):
	H = fct_filtre(frequence/f0)
	
	G = np.abs(H)
	P = np.angle(H)
	
	s = gene_signal(frequence, G*amplitude, P)
	
	return s, G*amplitude

""" ----- Premiers calculs ----- """

# fonction de transfert par défaut
fct_filtre = pb1

H = fct_filtre(f_bode/f0)

G = np.absolute(H)
P = np.angle(H)

# Calcul signal entrant et filtré
se, fe, ampe = sinus()
ss, amps = signal_filtre(fe, ampe)


""" ----- Création de la fenêtre ----- """ 

if graph:
	ax1 = plt.axes([0.25, 0.6, 0.70, 0.3])
	ax_gain = plt.axes([0.25, 0.55-0.3, 0.7, 0.3])
else:
	f, axarr =plt.subplots(2)
	
	ax1 = axarr[0]
	ax_gain = axarr[1]

ax1.axis([0.0, 4*np.pi, -1.5, 1.5])
ax_gain.axis([0.5, 10**f_max, 1e-2, 2e1])

ax_gain.set_yscale('log')
ax_gain.set_xscale('log')
	
# Axe de la phase
ax_phase = ax_gain.twinx()
ax_phase.set_ylim(1.1*min(P), 1.1*max(P))
ax_phase.set_ylabel("$\Phi$ (rad)")
ax_phase.yaxis.label.set_color('m')

for phase_label in ax_phase.yaxis.get_ticklabels():
	phase_label.set_color('m')

# Labels
ax_gain.set_xlabel('$f/f_0$')
ax_gain.set_ylabel('$G_{dB}$')

ax1.set_xlabel('$t$')
ax1.set_ylabel('$U$')

# Plot des fonctions calculées au départ
signal_E, = ax1.plot(t, se, label='$U_e$', color = 'b')
signal_S, = ax1.plot(t, ss, label='$U_s$', color = 'r')

fourierE_line = ax_gain.vlines(x=fe, ymin=1e-2, ymax=ampe, colors = 'b', lw=5)
fourierS_line = ax_gain.vlines(x=fe, ymin=1e-2, ymax=amps, colors = 'r', lw=2)

line_gain, = ax_gain.plot(f_bode, G, color='k')
line_phase, = ax_phase.plot(f_bode, P, color='m')

# Legendes
ax1.legend()
ax_gain.legend((line_gain, line_phase, fourierE_line, fourierS_line), ('$G_{dB}$', '$\Phi$', '$TF(U_e)$', '$TF(U_s)$' ))

# Limites axes
ax1.set_ylim(1.1*min(min(ss), min(se)), 1.1*max(max(ss), max(se)))

""" ----- Fonctions de mise à jour du graphique ----- """

# MAJ du graphique lors d'un changement
def maj_graph():
	global ss, amps, segs
	
	# calcul du signal filtré
	ss, amps = signal_filtre(fe, ampe)
	
	# MAJ graph temporel
	signal_E.set_ydata(se)
	signal_S.set_ydata(ss)
	
	
	# MAJ décomposition spectrale
	segs = np.zeros((len(fe), 2, 2)) # pour vline
	for i in range(len(fe)):
		segs[i,:,0] = fe[i]
		segs[i,0,1] = 0.01
		segs[i,1,1] = np.abs(ampe)[i]
		
	fourierE_line.set_paths(segs)
	
	segs = np.zeros((len(fe), 2, 2)) # pour vline
	for i in range(len(fe)):
		segs[i,:,0] = fe[i]
		segs[i,0,1] = 0.01
		segs[i,1,1] = np.abs(amps)[i]
		
	fourierS_line.set_paths(segs)
	
	# Diagramme de Bode
	H = fct_filtre(f_bode/f0)
	G = np.abs(H)
	P = np.angle(H)
	
	line_gain.set_ydata(G)
	line_phase.set_ydata(P)
	
	# Ajustement des échelles
	ax_phase.set_ylim( 1.1*min(P), 1.1*max(P) )
	ax1.set_ylim(1.1*min(min(ss), min(se)), 1.1*max(max(ss), max(se)))
	
	text.set_text('\n$H_0=${:4.2f}\n$f_0=${:4.2f}\n$Q=${:4.2f}'.format(H0,f0,Q))
	
	plt.draw()

# Modification du signal
def on_click(label):
	global se, fe, ampe
	
	if label == 'Sinus':
		se, fe, ampe = sinus()
	elif label == 'Triangle':
		se, fe, ampe = triangle(nb_harmonique_triangle) # fixer le nombre d'harmoniques voulues
	else:
		se, fe, ampe = carre(nb_harmonique_carre)
	
	maj_graph()


# Selection d'un filtre 
def on_click_filtre(label):
	global fct_filtre
	
	fct_filtre = liste_fonctions_transfert[label]
	
	maj_graph()
		
# MAJ des sliders
def maj_slide(val):
	global H0, f0, Q
	
	H0 = slider1.val
	f0 = 10**slider3.val
	Q = 10**slider2.val
	
	maj_graph()
	
""" ----- affichage des slider si interface graphique ----- """
if graph:
	# Widgets
	rax = plt.axes([0.02, 0.75, 0.15, 0.15])
	radio2 = RadioButtons(rax, ('Sinus', 'Triangle', 'Carré'))
	radio2.on_clicked(on_click)

	rax2 = plt.axes([0.02, 0.45, 0.15, 0.25])
	radio3 = RadioButtons(rax2, liste_fonctions_transfert.keys())
	radio3.on_clicked(on_click_filtre)

	ax_s1= plt.axes([0.25, 0.01, 0.65, 0.03])
	ax_s2= plt.axes([0.25, 0.05, 0.65, 0.03])
	ax_s3= plt.axes([0.25, 0.09, 0.65, 0.03])

	slider1 = Slider(ax_s1, '$H_0$', 0.1, 2, valinit=1)
	slider1.on_changed(maj_slide)
	slider2 = Slider(ax_s2, 'Q', -1, 1, valinit=0)
	slider2.on_changed(maj_slide)
	slider3 = Slider(ax_s3, '$f_0$', -2, 2, valinit=0)
	slider3.on_changed(maj_slide)

	ax_text = plt.axes([0.01, 0.0, 0.15, 0.05])
	ax_text.axis('off')
	text = ax_text.annotate('', (0,0.5))
	text.set_text('\n$H_0=${:4.2f}\n$f_0=${:4.2f}\n$Q=${:4.2f}'.format(H0,f0,Q))

# Affichage final
plt.show()
