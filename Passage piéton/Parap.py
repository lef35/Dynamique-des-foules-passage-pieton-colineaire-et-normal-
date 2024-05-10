# /////////////////////// PARAMETRE PASSAGE PIETON NORMAL ///////////////
import numpy as np

# /////////////////////////////////////////////////////////////////////////////////////
nb_pop = 1
Nt = 750
dt = 0.025

L = 2                                          # Dimension du domaine
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
objectifx = np.zeros((300, nb_pop))             # Tableau de l'objectif endroit final visée
objectify = np.zeros((300, nb_pop))
answr = ["oui",'oui']


# /////////////////////////////////////////////////////////////////////////////////////
                                                # Saisie des donnees

N =[75,75]
eps = [10,10]
alpha = [0,0]
mu = [5,5]
ramp = [0.,0.]
v0 = [1,1]
r0 = [0.05,0.05]
rf = [0.2,0.2]
vx0 = [1,0]
vy0 = [0,-1]
lmin = 0.5 
lmax = 1.5

if nb_pop != 1:                                 # Amplitude Force_Repu_Extra_Pop
    I = 30
else :
    I = 0.
    
for i in range(nb_pop):
    if answr[i] == 'oui':
        if i == 0:
            for j in range(int(N[i])):
                objectifx[j][i] = L
                objectify[j][i] = np.random.uniform(lmin, lmax)
        else : 
            for j in range(int(N[i])):
                objectifx[j][i] = np.random.uniform(lmin, lmax)
                objectify[j][i] = 0
                 
    
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
for z in range(nb_pop):                         # Initialisation posi/vitesse
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
            x[j][z] = np.random.uniform(lmin, lmax)
            y[j][z] = L
            for k in range(N[z]):
                if k != z and x[j][z] == x[k][z] and y[j][z] == L :
                    x[j][z] = np.random.uniform(lmin, lmax)
            vx[j][z] = vx0[z]
            vy[j][z] = vy0[z]



