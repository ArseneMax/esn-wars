from console import *
from graphe import *
from tkiteasy import *



def objetCliqué(x1,y1,MISSIONS,JOUEURS):
    '''
    
    '''
    for mission in MISSIONS:
        coinX = (mission.x+1)*35
        coinY = (mission.y+1)*35
        if (x1,y1) in [(x,y) for x in range(coinX,coinX+36) for y in range(coinY,coinY+36)]:
            return 3, mission
    for joueur in JOUEURS:
        coinX = (joueur.x+1)*35
        coinY = (joueur.y+1)*35
        if (x1,y1) in [(x,y) for x in range(coinX,coinX+36) for y in range(coinY,coinY+36)]:
            return (2, joueur)
    return (-1,'') 


def boutonCliqué(x,y, MISSIONS, JOUEURS):
    '''
    Regarde où est ce que le joueur clique et renvois un truc??? correspondant a l'endroit où il a cliqué et si ça correspond a rien ca 
    retourne la fonction 'objetCliqué'
    Sortie: ???
    '''
    if 665<x<690 and 800<y<850:
        return (1,'haut')
    elif 620<x<670 and 843<y<867:
        return (1, 'gauche')
    elif 680<x<736 and 843<y<886:
        return (1, 'droite')
    elif 665<x<689 and 880<y<910:
        return (1, 'bas')
    elif 100<x<200 and 800<y<900:
        return (4, ' ')
    elif 250<x<350 and 800<y<900:
        return (5, '')
    elif 400<x<500 and 800<y<900:
        return (0,'')
    else:
        return objetCliqué(x,y, MISSIONS, JOUEURS)



def actualiser_interface(g,joueur):
    '''
    Actualise l'interface.
    Regarde si l'upgrade est possible pour l'EM si oui ça affiche le bouton en couleur et sinon ça l'affiche en gris , pareil pour le CL
    '''
    if joueur.upgradePossible('EM'):
        boutonEM = boutton(g,150,850,'red','Upgrade\n Energie\n max')
    else:
        boutonEM = boutton(g,150,850,'grey','Upgrade\n Energie\n max')
    if joueur.upgradePossible('CL'):
        boutonCL = boutton(g,300,850,'pink','Upgrade\n Coding\n Level')
    else:
        boutonCL =boutton(g,300,850,'grey','Upgrade\n Coding\n Level')

    flechex = g.dessinerTriangle((joueur.x+1)*35, 5, (joueur.x+2)*35, 5, (joueur.x+1)*35 + 18, 25, "green")
    flechey = g.dessinerTriangle(5, (joueur.y+1)*35,  5, (joueur.y+2)*35, 25, (joueur.y+1)*35 + 18, "green")
    boutonPT = boutton(g,450,850,'orange','Passer\n Tour')
    barreE = barre(g,joueur.EM,joueur.E,'yellow',800,130,'Energie')
    barreCL = barre_stat(g,joueur.CL,'blue',800,200,'Coding Level')
    barreR = barre_stat(g,joueur.R,'purple',800,270,'Revenu')

    tour = info_demande(g,joueur.ID,'Tour du J',825,70)
    return boutonCL, boutonEM, barreE, tour, barreCL, barreR, boutonPT, flechex, flechey


def interface_mission(g,mission):
    '''
    Permet d'actualiser l'interface des missions.
    '''
    nom_mission = info_demande(g,mission.ID,'Mission',825,400)
    missionx = info_demande(g,mission.x,'positionx  ',825,460)
    missiony = info_demande(g,mission.y,'positiony  ',825,520)
    missionRW = barre(g,mission.SW,mission.RW,'green',800,600,'RW')
    missionD = barre_stat(g,mission.D,'orange',800,670,'Difficulté')
    print(mission.etat)
    return nom_mission, missionx, missiony, missionRW, missionD


def supprimerObjets(g,listeObjets):
    '''
    Supprime ce qu'il y a sur l'interface graphique pour éviter que le jeu crash. 
    '''
    for elt in listeObjets:
        if isinstance(elt,tuple):
            for elt2 in elt:
                g.supprimer(elt2)
        else:
            g.supprimer(elt)

def supprimerInterface(g,objetsJ,objetsM,objetsCases):
    '''
    Fait appel a la fonction 'supprimerObjets' pour supprimer des élements.
    '''
    supprimerObjets(g,objetsJ)
    supprimerObjets(g,objetsM)
    supprimerObjets(g,objetsCases)



if __name__ == "__main__":

    g = creationGraphique()
    MISSIONS = creationMissions('map1.txt')
    JOUEURS = creationJoueurs(2)
    tour = 999
    

    while not finis(JOUEURS,tour):
        for joueur in JOUEURS:
            GRILLE=actualiserGrille(MISSIONS, JOUEURS)
            CASES = GrilleGraphique(GRILLE, g, MISSIONS)
            interfaceJ = actualiser_interface(g,joueur)
            interfaceM = interface_mission(g,MISSIONS[0])
            afficherGrille(GRILLE)
            clic = g.attendreClic()
            action = boutonCliqué(clic.x, clic.y, MISSIONS, JOUEURS)
            while not joueur.actions(JOUEURS,action):
                if action[0] == 3:
                    supprimerObjets(g, interfaceM)
                    interfaceM = interface_mission(g,action[1])
                clic = g.attendreClic()
                action = boutonCliqué(clic.x, clic.y,MISSIONS, JOUEURS)
            actualiserMission(joueur,MISSIONS)
            supprimerInterface(g,interfaceJ,interfaceM,CASES)
        tour +=1
    ecran_fin(g,finis(JOUEURS,tour))
    while g.attendreTouche() == '':
        continue

    g.fermerFenetre()