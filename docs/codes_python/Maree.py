""" ---------------------------------------------------------------- """
"""                                                                  """
""" Volte Antoine & Martouzet Grégoire                               """
"""                                                                  """
""" gregoire.martouzet@ens-paris-saclay.com							 """
""" ---------------------------------------------------------------- """

""" ----- Bibliothèques ----- """
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.widgets import CheckButtons, Slider, Button
from numpy import cos, sin, sqrt, arctan, linspace, pi, roll

""" ----- Paramètres d'affichage ----- """
Delta_index = 40	# Nombre de frame non affichées pendant l'annimation (permet d'accelerer l'animation)
N 			= 240	# Nombre de point de calcul (discretisation de l'angle)
N_aff		= 8	# Nombre de vecteur affichés = N/N_aff

""" ----- Constantes Physiques (SI) ----- """
G	=	6.67e-11	# Constante gravitationnelle

# Terre
R	=	6370		# Rayon
M0	=	6e24		# Masse

# Lune
Ml	=	7.35e22		# Masse
dl	=	384400		# Distance Terre-Lune
tl	=	0			# Angle Terre-Lune par rappport à l'axe Terre-Soleil

# Soleil
Ms	=	1.99e30		# Masse
ds	=	149.6e6		# Distance Terre-Soleil

# Masse d'un élément sur lequel le calcul est effectué
m = 100


""" ----- Initialisation des listes ----- """
# Liste d'angle
theta = linspace(0, 2*pi, N)
delta_theta = theta[1] - theta[0]

# Positions des vecteurs
x, y = R*cos(theta), R*sin(theta)

""" ----- Force exercée par les astres ----- """
def f(theta, M, d): 
	fx = 2*G*m*R*cos(theta)* M/d**3
	fy =  -G*m*R*sin(theta)* M/d**3
	return fx, fy 

# Lune
fx, fy = f(theta, Ml, dl)
fmaree_L_x, fmaree_L_y = fx, fy

# Soleil
fmaree_S_x, fmaree_S_y = f(theta, Ms, ds)

# Total
fmaree_T_x = fmaree_L_x + fmaree_S_x
fmaree_T_y = fmaree_L_y + fmaree_S_y

""" ----- Fonction de mise-à-jour des paramètres ----- """
def maj_slide(val):
	""" Modification de la postion de la Lune
		- On calcul les nouvelles directions et normes dans le repère de départ
		- On réalise une permutation circultaire pour placer les vecteur "où il faut"
		- Maj de l'affichage si il faut
		""" 
	global fmaree_L_x, fmaree_L_y, tl
	
	# Arrondi de la position de la lune au theta le plus proche
	tl = round(val/delta_theta)*delta_theta
	
	# nombre de circulation à faire pour tourner 
	n = int(round(val/delta_theta))
	
	# maj de la position graphique
	circle_Lune1.center = 8000*cos(tl), 8000*sin(tl)
	circle_Lune2.center = 8000*cos(tl), 8000*sin(tl)
	
	# On pivote les directions
	fmaree_L_x = ( cos(tl)*fx - sin(tl)*fy )
	fmaree_L_y = ( cos(tl)*fy + sin(tl)*fx )
	
	# On fait une permutation circulaire pour placer les vecteur "où il faut"
	fmaree_L_x = roll(fmaree_L_x, n)
	fmaree_L_y = roll(fmaree_L_y, n)
	
	# Maj du champ de la lune	
	vector_l.set_UVC(fmaree_L_x[::N_aff], fmaree_L_y[::N_aff])
	
	# Maj de la somme
	fmaree_T_x = fmaree_L_x + fmaree_S_x
	fmaree_T_y = fmaree_L_y + fmaree_S_y
		
	vector_t.set_UVC(fmaree_T_x[::N_aff], fmaree_T_y[::N_aff])
		
def maj_check(label):
	global is_check, vector_l, vector_s, vector_t
	
	is_check[label] = not is_check[label]
	vector_l.set_visible( is_check['Lune'] )
	vector_s.set_visible( is_check['Soleil'] )	
	vector_t.set_visible( is_check['Somme'] )
		
	plt.draw()

""" ----- Création de la fenetre ----- """
fig = plt.figure()
fig.canvas.set_window_title('Marée')

""" ----- Différents axes et configuration ----- """
ax_astre= plt.axes( [0.25, 0.30, 0.70, 0.65] ) # Zone de dessin des astres
ax_anim = plt.axes( [0.1 , 0.1 , 0.85, 0.15] ) # Secondaire (1D)

# Aspect ration equal pour avoir des cercles ronds
ax_astre.set_aspect('equal', 'datalim')

# Pas de ticks pour la zone de dessin
ax_astre.get_xaxis().set_visible(False)
ax_astre.get_yaxis().set_visible(False)

""" ----- Affichage des champs ----- """
vector_l = ax_astre.quiver(x[::N_aff], y[::N_aff], fmaree_L_x[::N_aff], fmaree_L_y[::N_aff], units='xy', color='gray', scale_units='x', scale=0.04)
vector_s = ax_astre.quiver(x[::N_aff], y[::N_aff], fmaree_S_x[::N_aff], fmaree_S_y[::N_aff], units='xy', color='red', scale_units='x', scale=0.04)
vector_t = ax_astre.quiver(x[::N_aff], y[::N_aff], fmaree_T_x[::N_aff], fmaree_T_y[::N_aff], units='xy', scale_units='x', scale=0.04)

vector_s.set_visible( False )
vector_t.set_visible( False )

""" ----- Dessin des Astres ----- """
# Terre
ax_astre.add_artist( plt.Circle((0.0, 0.0), R, color='blue', fill=False) )

# Lune
circle_Lune1 = plt.Circle((8000*cos(tl), 8000*sin(tl)), 500, color='gray')
circle_Lune2 = plt.Circle((8000*cos(tl), 8000*sin(tl)), 500, fill=False)
ax_astre.add_artist(circle_Lune1)
ax_astre.add_artist(circle_Lune2)

# Soleil
ax_astre.add_artist( plt.Circle((-10000, 0.0), 1000, color='yellow') )
ax_astre.add_artist( plt.Circle((-10000, 0.0), 1000, color='red', fill=False) )

# Point rouge d'observation 
humain, = ax_astre.plot(x[0], y[0], 'or')

""" ----- Fonctions et paramètres pour l'animation ----- """
index = 0
t_max = 1

amp_lune = [0]
time = [0]
pause = True

def animate(i):
	global pause, index, amp_lune, time
	
	for j in range(Delta_index):
		if not pause:
			index += 1
				
			# on fait tourner la lune aussi
			maj_slide( (index)*2*pi/(29.5*N) )
			sang.set_val( (index)*2*pi/(29.5*N) )
			
			amp = ((fmaree_L_x+fmaree_S_x)*cos(theta) + (fmaree_L_y+fmaree_S_y)*sin(theta))
			
			time.append(index/N)
			amp_lune.append(amp[index%N])
			
			if index == int(t_max*N):
				pause = True
	
	humain.set_data(x[index%N], y[index%N])
	h.set_data(time, amp_lune)
	ax_anim.axis([0, index/N, 1.1*min(amp_lune), 1.1*max(amp_lune)])
	
	fig.canvas.draw_idle()
		
	return

def begin_animation(t):
	global amp_lune, time, t_max, index, pause
	index = 0
	t_max = t
	amp_lune = [0]
	time = [0]
	pause = False

def btn_anim1(event):
	begin_animation(1)

def btn_anim29(event):
	begin_animation(29.5)

def btn_animInf(event):
	begin_animation(-1)
		
def btn_pause(event):
	global pause
	pause = not pause

""" ----- Widgets pour changer les paramètres ----- """

# Zones des Widgets
rax 	= plt.axes( [0.01, 0.75, 0.12, 0.15] ) # Checkbox
bax 	= plt.axes( [0.01, 0.65, 0.12, 0.08] ) # btn 1
bax2 	= plt.axes( [0.01, 0.55, 0.12, 0.08] ) # btn 2
bax3 	= plt.axes( [0.01, 0.45, 0.12, 0.08] ) # btn 3
bax4 	= plt.axes( [0.01, 0.35, 0.12, 0.08] ) # btn 4
axang 	= plt.axes( [0.25, 0.01, 0.65, 0.03] ) # Slider

# Checkbox pour choisir les champs à afficher
is_check = {'Lune':True, 'Soleil':False, 'Somme': False}
check = CheckButtons(rax, ('Lune', 'Soleil', 'Somme'), (True, False, False))
check.on_clicked(maj_check)

# 1 jour sur terre
bouton_jour_terre = Button(bax, '24h')
bouton_jour_terre.on_clicked(btn_anim1)

# 1j sur la Lune (=29.5j)
bouton_jour_lune = Button(bax2, '29.5j')
bouton_jour_lune.on_clicked(btn_anim29)

# infini
bouton_inf = Button(bax3, 'Infini')
bouton_inf.on_clicked(btn_animInf)

# Pause
bouton_pause = Button(bax4, 'Pause')
bouton_pause.on_clicked(btn_pause)

# Axe pour la valeur de la force
ax_anim.set_xlabel('jour')
h, = ax_anim.plot([],[])

# Slider pour modifier la position de la Lune
sang = Slider(axang, 'Angle Terre-Lune', 0, 2*pi, valinit=0.0)
sang.on_changed(maj_slide)

""" ----- Affichage et lancement ----- """
ani = animation.FuncAnimation(fig, animate, blit=False, interval=200, repeat=True)

plt.show()
