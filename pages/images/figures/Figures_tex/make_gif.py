from PIL import Image, ImageOps

with open('gif_figure_elec_continu.txt') as f:
	liste_nom = f.readlines()

img_liste = []
hm = 0
wm = 0
for nom in liste_nom:
	nom = nom.replace('\n', '')
	img = Image.open('../'+nom)
	if img.width>wm:
		wm = img.width
	if img.height>hm:
		hm = img.height
	img_liste.append( img )

image = Image.new('RGB', (wm, hm), (255, 255, 255))
img1 = img_liste[0]
img1 = ImageOps.contain( img1, (wm, hm) )
image.paste(img1, (0, 0))

# Enregistrer en format GIF animé
image.save(
    'Circuit_elec_continu.gif',
    save_all=True,
    disposal=2,
    append_images=[ ImageOps.contain( img, (wm, hm) ) for img in img_liste[1:]],
    duration=2000,  # Durée d'affichage de chaque image en millisecondes (ex: 500 ms)
    loop=0,  # 0 pour une boucle infinie, ou un nombre entier pour répéter N fois
)
