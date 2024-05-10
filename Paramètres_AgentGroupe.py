# /////////////////////// Parametres Cas d'etude 1 Traverser passage pieton ///////////////
import numpy as np


# /////////////////////////////////////////////////////////////////////////////////////
nb_pop = 2                                      # Nb de population 
Nt = 750                                        # Nb d'iteration totale
dt = 0.025                                      # Pas de temps

L = 2                                           # Dimension du domaine
l = 2

# /////////////////////////////////////////////////////////////////////////////////////
                                                # Création des listes 
# Name  np.zeros(nb_pop)                        # Liste nom population
N = np.zeros(nb_pop)                            # Liste nombre de population
eps = np.zeros(nb_pop)                          # Liste Amplitude Force_de_Repulsion
alpha = np.zeros(nb_pop)                        # Liste Amplitude Force_de_Regroupement
mu = np.zeros(nb_pop)                           # Liste Amplitude Force_Auto_Propulsion
ramp = np.zeros(nb_pop)                         # Liste Amplitude Force_Aleatoire/Bruit
v0 = np.zeros(nb_pop)                           # Liste Vitesse_Visée
r0 = np.zeros(nb_pop)                           # Liste rayon Largeur épaule
rf = np.zeros(nb_pop)                           # Liste rayon de regroupement
objectifx = np.zeros((200, nb_pop))             # Tableau de l'objectif endroit final visée
objectify = np.zeros((200, nb_pop))
answr = ["oui",'oui']


# /////////////////////////////////////////////////////////////////////////////////////
                                                # Saisie des donnees

N = [25,25]                                     # Liste nb d'agent / population
eps = [0,0]                                     # Liste amplitude F_Rep
alpha = [0,0]                             # Liste amplitude F_flocking
mu = [5,5]                                      # Liste amplitude F_A_Prop
ramp = [0.,0.]                                  # Liste amplitude F_Alea
v0 = [1,1]                                      # Liste vitesse cible
r0 = [0.05,0.05]                                # Liste rayon agent (demie epaule)
rf = [0.2,0.2]                                  # Liste rayon de flocking
vx0 = [1,-1]                                    # Liste composante X vitesse initiale
vy0 = [0,0]                                     # Liste composante Y vitisse initiale

lmin = 0.5                                      # lmax-lmin = largeur passage pieton
lmax = 1.5

if nb_pop != 1:                                 # Amplitude Force_Repu_Extra_Pop
    I = 30
else :
    I = 0.
    
for i in range(nb_pop):                         # Distribution objectif
    if answr[i] == 'oui':
        if i == 0 :
            o = 2 
        else : 
            o = 0
        for j in range(int(N[i])):
            objectifx[j][i] = o
            objectify[j][i] = np.random.uniform(lmin, lmax)
                 

      
# /////////////////////////////////////////////////////////////////////////////////////
#N = N.astype(int)
Nmax = int(max(N))
np.random.seed(17)                              # Reproductibilite

# /////////////////////////////////////////////////////////////////////////////////////
                                                                # Creations Tableaux 
x, y = np.zeros((Nmax, nb_pop)), np.zeros((Nmax, nb_pop))       # Tableaux positions
vx, vy = np.zeros((Nmax, nb_pop)), np.zeros((Nmax, nb_pop))     # Tableaux vitesses
fx, fy = np.zeros((Nmax, nb_pop)), np.zeros((Nmax, nb_pop))     # Tableaux Resultante Force
                                                                    # Tableaux  etendues
xb, yb  = np.zeros((4*Nmax, nb_pop)), np.zeros((4*Nmax, nb_pop))    # Tableaux positions                       
vxb, vyb = np.zeros((4*Nmax, nb_pop)), np.zeros((4*Nmax, nb_pop))   # Tableaux vitesses

# /////////////////////////////////////////////////////////////////////////////////////
for z in range(nb_pop):                         # Initialisation position et vitesse 
    for j in range(N[z]): 
        if z == 0:
            x[j][z] = 0.
            y[j][z] = np.random.uniform(lmin, lmax)
            for k in range(N[z]):
                if k != z and x[j][z] == 0 and y[j][z] == y[k][z] :
                    y[j][z] = np.random.uniform(lmin, lmax)
            vx[j][z] = vx0[z]
            vy[j][z] = vy0[z]
        if z == 1:
            x[j][z] = 2
            y[j][z] = np.random.uniform(lmin, lmax)
            for k in range(N[z]):
                if k != z and x[j][z] == 1 and y[j][z] == y[k][z] :
                    y[j][z] = np.random.uniform(lmin, lmax)
            vx[j][z] = vx0[z]
            vy[j][z] = vy0[z]

