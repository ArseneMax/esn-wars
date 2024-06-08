from random import randint

######################################################################################################
#Déclaration variable d'environnement
######################################################################################################

GRILLE=[]
LONGUEUR = 21
COORD_JC = (LONGUEUR//2,LONGUEUR//2)
TOURS_MAX = 1000
OBJECTIF = 5000
NBR_MISSIONS = 10
placementMissions = {'X':(COORD_JC[0], COORD_JC[1])}

######################################################################################################
#Création de la classe Joueur
######################################################################################################

class Joueur:
  '''
  Crée un objet joueur qui permet l'indépendance des données pour chaque joueur.
  paramètre: sa position x, sa position y, son ID qui va être son numéro de joueur, son CL (coding level), son EM (energie max), son E (energie) , son R (revenu)  
  '''
  def __init__(self, ID):
    self.x = COORD_JC[0]
    self.y = COORD_JC[1]
    self.ID = ID
    self.CL = 1
    self.EM = 1
    self.E = 1
    self.R = 0  
    

######################################################################################################
#Changement des stats Joueur
######################################################################################################

  def augmenterStat(self, stat):
    '''
    Vérifie si on parle du CL (coding level) ou bien de l'EM (énergie max).
    Dans les 2 cas ça vérifie si le revenu est suffisant et si oui ça augmente la stat de 1. 
    Entrée: str 'CL' ou 'EM'
    Sortie: un booléen 
    '''
    match stat:
      case 'CL':
          if self.R >= ((self.CL+1)**2)*10:
            self.setR( self.R - ((self.CL+1)**2)*10 )
            self.CL += 1
      case 'EM':
          if self.R >= ((self.EM+1)**2)*10:
            self.setR( self.R - ((self.EM+1)**2)*10 )
            self.EM += 1
            self.E = self.EM
          
    return True
  
  def setE(self, valeur):
    '''
    Definie l'énergie d'un joueur à 0 et si l'énergie descend en dessous de 0 en faisant une mission ça remet la valeur a 0
    '''
    self.E = valeur
    if self.E < 0:
      self.E = 0

  def setR(self, valeur):
    '''
    Definie les revenues d'un joueur à 0 et si les revenues descendent en dessous de 0 ça remet la valeur a 0
    '''
    self.R = valeur
    if self.R < 0:
      self.R = 0

  def afficheStats(self):
    '''
    Prend en entrée un joueur rt affiche ses stats
    Sortie: un str avec les stats des joueurs 
    '''
    strStats = 'Statistique JOUEUR{id} \n Coding Level : {cl} \n Energie Max : {em} \n Energie actuelle : {e} \n Bitcoin : {r}'
    return strStats

######################################################################################################
#Actions des joueurs
######################################################################################################

  def upgradePossible(self, stat):
    '''
    Fonction qui va regarder si une upgrade est possible.
    Si la stat c'est EM (énergie max) alors ça set sa condition, pareil pour le CL (coding level) 
    et ensuite si les coordonnées du joueur sont les même que le JC (job center) et que leur revenues sont suffisant alors on retourne True sinon on reourne False
    entrée: str, soit EM soit CL
    Sortie: un booléen
    '''
    if stat == 'EM':
      condition = ((self.EM+1)**2)*10
    elif stat == 'CL':
      condition = ((self.CL+1)**2)*10
    if (self.x, self.y) == COORD_JC and  self.R >= condition:
      return True
    return False

  def actions(self, JOUEURS, action):
    '''
    Effectue le choix de l'action du joueur dans les actions possible renvoyées par actionPossible()
    Sortie : int action, permet l'identification de l'action dans le programme principale
    '''
    passerTour = False
    match action[0]:
      case 0:
        print('Tour Passe !!')
        passerTour = True
      case 1:
        passerTour = self.deplacer(JOUEURS, action[1])
      case 2:
        statJoueur(action[1],JOUEURS)
        passerTour = False
      case 3:
        passerTour = False
      case 4:
        if self.augmenterStat('EM'):
          passerTour = True
      case 5:
        if self.augmenterStat('CL'):
          passerTour = True
    return passerTour

  def deplacer(self, JOUEURS, direction):
    '''
    Permet le déplacement du joueur, en faisant attention a certaines contraintes : le joueur ne doit pas sortir de la grille et ne peut pas etre au meme endroit qu'un autre joueur.
    Change le X et Y du joueur dans la position souhaiter.
    '''
    dictDirection = {'bas':(self.x+0,self.y+1), 'haut':(self.x+0,self.y-1), 'droite':(self.x+1,self.y+0), 'gauche':(self.x-1,self.y+0)}
    if (dictDirection[direction] in [(joueur.x, joueur.y) for joueur in JOUEURS] and not dictDirection[direction] == COORD_JC) or dictDirection[direction] not in [(x,y) for x in range(0,21) for y in range(0,21)]:
      return False   
    self.x, self.y = dictDirection[direction][0], dictDirection[direction][1]
    return True

######################################################################################################
#Création de la classe Mission
######################################################################################################

class Mission:
  '''
  Crée un objet mision qui permet l'indépendance des données pour chaque mission.
  paramètre: sa position x et y, son ID, sa SW (starting workload), sa dificultée , son état (valide ou terminé) et son compteur pour sa réapparition.
  '''
  def __init__(self, ID, x, y, sw, d):
    self.x, self.y = x, y
    placementMissions[ID] = x,y
    baseSW = sw
    self.SW = baseSW
    self.RW = baseSW
    self.D = d
    self.etat = 'Valide'
    self.cptReap = 0
    self.ID = ID

  def infoMission(self):
    '''
    Prend en entrée une mission et affiche ses stats
    Sortie: un str avec les stats des missions
    '''
    MissionStats = 'Mission {id} \n Starting workload : {SW} \n Remaining workload : {RW} \n Difficultée : {D} \n Etat : {etat}'
    print(MissionStats.format(id=self.ID, SW=self.SW, RW=self.RW, D=self.D, etat = self.etat))

  def setRW(self, valeur):
    '''
    Prends une mission et regarde son RW (remaining workload) et si il est en dessous de 0 ça le remet a 0
    '''
    self.RW = valeur
    if self.RW < 0:
      self.RW = 0

  def cptPlusUn(self):
    '''
    Rajoute un tour au compteur de tour d'une mission
    '''
    self.cptReap += 1

  def finis(self):
    '''
    Met l'état dune mission a terminé
    '''
    self.etat = 'Terminé'

  def reapparition(self):
    '''
    Fait réapparaitre une mission en changeant ses paramètres.
    '''
    self.RW = self.SW
    self.etat = 'Valide'
    self.cptReap=0
    


######################################################################################################
#Fonctions de la grille
######################################################################################################

def afficherGrille(GRILLE):
  '''
  ça affiche la grille
  '''
  for ligne in GRILLE:
    for element in ligne:
      print(element, end=" | ")
    print()

def actualiserGrille(MISSIONS,JOUEURS):
  '''
  ça actualise la grille
  '''
  GRILLE = [["_" for i in range(LONGUEUR)] for i in range(LONGUEUR)]
  for joueur in JOUEURS:
    GRILLE[joueur.y][joueur.x] = joueur.ID
  for mission in MISSIONS:
    if not mission.x == None and not mission.y == None:
      if not isinstance(GRILLE[mission.y][mission.x], int):
        GRILLE[mission.y][mission.x] = mission.ID
      else:
        GRILLE[mission.y][mission.x] = mission.ID
  GRILLE[COORD_JC[0]][COORD_JC[1]]="X"
  return GRILLE

######################################################################################################
#Fonctions régles du jeu
######################################################################################################

def finis(JOUEURS, tour):
  '''
  Vérifie si les conditions de victoires sont remplies, si un joueur arrive à 5000 de revenu 
  il retourne son ID et si il n'y a pas de gagnant avant les 1000 tours il regarde le joueur avec le plus de revenu
  et retourne son ID et si 2 Joueurs sont à égalités la partie est nulle.
  Entrée: un int le nomre de tour
  Sortie: soit un int soit un booléen
  '''
  for joueur in JOUEURS:
    if joueur.R >= 5000:
      return joueur.ID
  if tour == 1000:
    pass
   # gagnant=joueur
    #for joueur in JOUEURS:
      #if gagnant.ID==joueur.ID:
       # pass
      #if gagnant.R<joueur.R:
        #gagnant=joueur
     #elif gagnant.R==joueur.R:
        #return False
    #return gagnant.ID
  return False

def actualiserMission(joueur,MISSIONS):
  '''
  Vérifie si un joueur est sur une mission, que la mission est 'Valide' (toujours active) et que le joueur a au moins 1 d'energie
  et si c'est le cas on retire a l'énergie du joueur le montant de la difficulté de la mission et on retire à la remaining workload
  de la mission le montant du coding level du joueur. Ensuite on vérifie si la remaining workload de la mission est inférieur a 0,
  si c'est le cas on met l'etat de la mission à 'Terminé' avec la fonction 'finis' et on rajoute au revenu du joueur qui a fini la mission
  le montant du produit de la starting workload de la mission et de sa difficulté.

  Si l'état de la mission est 'Terminé' on rajoute 1 a son compteur de tour pour sa réapparition.
  Si le compteur de la mission est égale au produit de sa difficulté par 10on fait réapparaitre la mission.
  Si les coordonées du joueur sont les même que celles du JC on remet son énergie à son EM.
  '''
  for mission in MISSIONS:
    if mission.etat == 'Valide' and (joueur.x, joueur.y) == (mission.x, mission.y) and joueur.E > 0:
      joueur.setE(joueur.E - mission.D)
      mission.setRW(mission.RW-joueur.CL)
      if mission.RW <= 0:
        mission.finis()
        joueur.setR(joueur.R+mission.SW*mission.D)
    if mission.etat == 'Terminé':
      mission.cptPlusUn()
    if mission.cptReap == mission.D * 10:
      mission.reapparition()
  if (joueur.x, joueur.y) == COORD_JC:
    joueur.setE(joueur.EM)

def choisirMission(MISSIONS):
  '''
  Plus besoin de celle la nn?
  '''
  choix=str(input('De quel mission tu veux voir les stats:'))
  while choix not in placementMissions:
    print('mauvais input')
    choix=str(input('De quel mission tu veux voir les stats:'))
  if choix=='X':
    print("C'est le job center, ici vous pouvez vous reposer pour récuperer votre énergie ou bien l'augmenter et vous pouvez aussi améliorez votre Coding Level.")
  for mission in MISSIONS:
    if choix == mission.ID:
      mission.infoMission()



######################################################################################################
#Fichiers
######################################################################################################

def lecture(fichier):
  '''
  ça les fichier j'ai rien compris
  '''
  fichier = open(fichier, "r")
  lignes = fichier.readlines()
  fichier.close()
  infoMissions = []
  for l in lignes:
    l = l.strip()
    x, y, sw, d, rw = l.split()
    infoMission = [int(x),int(y),int(sw),int(d), int(rw)]
    infoMissions.append(infoMission)     
  return infoMissions


def sauvegarde(MISSIONS):
  a=True
  N=0
  while a:
    N+=1
    try: 
      s=open('save{n}.txt'.format(n=N), 'x')
      a=False
    except:
      pass
  for mission in MISSIONS:
    s.write('{x} {y} {sw} {d} {rw}\n'.format(x = str(mission.x), y=str(mission.y), sw =str(mission.SW), d=str(mission.D), rw=str(mission.RW)))



######################################################################################################
#Programme principale
######################################################################################################

def statJoueur(id, JOUEURS):
  '''
  affiche les stats du joueur voulu
  Sortie: un str
  '''
  for joueur in JOUEURS:
    if joueur.ID == id:
      return joueur.afficheStats()


def creationJoueurs(NBR_JOUEURS):
    '''
    crée des joueurs et les mets dans une liste
    '''
    JOUEURS = []
    for i in range(1,NBR_JOUEURS+1):
        JOUEURS.append(Joueur(i))
    return JOUEURS

def creationMissions(map):
    infos = lecture(map)
    MISSIONS = []
    i=0
    for info in infos:
        MISSIONS.append(Mission(chr(i+65), info[0], info[1], info[2], info[3]))
        i+=1
    return MISSIONS


if __name__== '__main__':     



  JOUEURS = creationJoueurs(2)
  MISSIONS = creationMissions('map1.txt')
  while not finis(JOUEURS):
    for joueur in JOUEURS:
      GRILLE=actualiserGrille(MISSIONS, JOUEURS)
      afficherGrille(GRILLE)
      while joueur.action(JOUEURS, MISSIONS) not in ['0','1','4','5']:
        pass
      actualiserMission(joueur,MISSIONS)