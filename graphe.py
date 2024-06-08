from tkiteasy import *
from console import *

def creationGraphique():
    '''
    Ouvre une fenetre graphique, puis crée la grille et fait apparaitre les flèches directionnelles 
    '''
    g=ouvrirFenetre(1000,1000)
    creationGrilleGraphique(g)
    direction(g)
    return g

def creationGrilleGraphique(GRAPHIQUE):
    '''
    Crée la grille
    '''
    nbrcase=21
    x=35
    x2=35
    for i in range (nbrcase+1):
        GRAPHIQUE.dessinerLigne(x,35,x2,770,'white')
        x+=35
        x2+=35
    y=35
    y2=35
    for i in range (nbrcase+1):
        GRAPHIQUE.dessinerLigne(770,y,35,y2,'white')
        y+=35
        y2+=35

def placement(graphique,x,y,name,c):
    '''
    Fait des carée de couleur dans la grille pour les missions et les joueurs.
    '''
    posx=((x+1)*35) + 1
    posy=((y+1)*35) + 1
    rect =graphique.dessinerRectangle(posx,posy,34,34,c)
    txt = graphique.afficherTexte(str(name), posx+17,posy+17, 'black', 20)
    return rect, txt
    

def GrilleGraphique(GRILLE, GRAPHIQUE, MISSIONS):
    '''
    frr je sais pas 
    '''
    listeObjets = []
    for ligne in range(len(GRILLE)):
        for colonne in range(len(GRILLE[ligne])):
            if isinstance(GRILLE[ligne][colonne],int):
                listeObjets.append(placement(GRAPHIQUE, colonne, ligne, GRILLE[ligne][colonne], 'blue'))
            if GRILLE[ligne][colonne] == 'X':
                listeObjets.append(placement(GRAPHIQUE, colonne, ligne, GRILLE[ligne][colonne], 'yellow'))
    for mission in MISSIONS:
        if mission.etat == 'Valide':
            listeObjets.append(placement(GRAPHIQUE, mission.x, mission.y, mission.ID, 'red'))
        else:
            listeObjets.append(placement(GRAPHIQUE, mission.x, mission.y, mission.ID, 'grey'))
    return listeObjets

def barre(g,stat_max,stat_actuelle,col,placementx,placementy,texte):
    '''
    Fait la barre d'energie
    '''
    barre_complete=100
    statut_stat = (barre_complete*stat_actuelle)/stat_max
    rect1 = g.dessinerRectangle(placementx,placementy,barre_complete,35,'white')
    rect2 = g.dessinerRectangle(placementx,placementy,statut_stat,35,col)
    txt1 = g.afficherTexte(texte,placementx+40,placementy-15,'white',15)
    txt2 = g.afficherTexte(stat_actuelle,placementx+35,placementy+20,'black',15)
    txt3 = g.afficherTexte('/',placementx+50,placementy+20,'black',15)
    txt4 = g.afficherTexte(stat_max,placementx+65,placementy+20,'black',15)
    return rect1, rect2, txt1, txt2, txt3, txt4

def barre_stat(g,stat_act,col,x,y,texte):
    '''
    fait la barre des stats
    '''
    rect1 = g.dessinerRectangle(x,y,100,35,col)
    txt1 = g.afficherTexte(texte,x+40,y-15,'white',15)
    txt2 = g.afficherTexte(stat_act,x+50,y+20,'black',15)
    return rect1, txt1, txt2

def direction(g):
    '''
    fait les flèches directionnelles
    '''
    #fleche du haut
    g.dessinerRectangle(665,800,25,30,'yellow')
    g.dessinerTriangle(665,830,689,830,678,850,'yellow')
    #fleche de gauche
    g.dessinerRectangle(620,843,30,25,'yellow')
    g.dessinerTriangle(650,843,650,867,670,855,'yellow')
    #fleche du bas
    g.dessinerRectangle(706,843,30,25,'yellow')
    g.dessinerTriangle(706,843,706,867,686,855,'yellow')
    #fleche de droite
    g.dessinerRectangle(665,880,25,30,'yellow')
    g.dessinerTriangle(665,880,689,880,678,860,'yellow')


def boutton(g, placex,placey,col,texte):
    '''
    fait les boutons
    '''
    bouton1 = g.dessinerDisque(placex,placey,50,col)
    texte1 = g.afficherTexte(texte,placex,placey,'black',15)   
    return bouton1, texte1

def info_demande(g,num_joueur,texte,x,y):
    '''
    affiche les infos demandées
    '''
    txt = g.afficherTexte(texte,x,y,'white',15) 
    txt2= g.afficherTexte(num_joueur,x+50,y,'white',15)  
    return  txt, txt2

def ecran_fin(g,num_joueur):
    '''
    fait un écran de victoire a la fin
    '''
    if num_joueur==False: 
        g.dessinerRectangle(0,0,1000,1000,'white')
        g.afficherTexte('Partie nulle',470,500,'black',15)
    else:
        g.dessinerRectangle(0,0,1000,1000,'white')
        g.afficherTexte('Victoire du J',470,500,'black',15)
        g.afficherTexte(num_joueur,530,500,'black',15)





if __name__ == "__main__":

    g = creationGraphique()
    MISSIONS = creationMissions('map1.txt')
    JOUEURS = creationJoueurs(2)
    GRILLE = actualiserGrille(MISSIONS, JOUEURS)
    direction()
    
    clic = g.attendreClic()
    

    while g.attendreTouche() == None:
        continue

    g.fermerFenetre()


