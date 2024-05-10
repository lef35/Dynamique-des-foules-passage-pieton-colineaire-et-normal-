#////////////////////// PARAMETRE EVACUATION 1 PORTE //////////////////////////////
import numpy as np
import random

# /////////////////////////////////////////////////////////////////////////////////////
                                                # Saisi donnee simulation
nb_pop = 1                                      # Nb de population 
Nt = 1000                                       # Nombre Iteration Totale 
dt = 0.025                                      # Pas de Temps 
                                                
L = 4.                                          # Dimension du domaine  
l = 4.                                      
                                                
N = 200                                        # Nombre d'agent
eps = 80                                        # Amplitude Force_de_Repulsion
alpha = 0.66                                    # Amplitude Force_de_Regroupement
mu = 3.5                                        # Amplitude Force_Auto_Propulsion
ramp = 1                                        # Amplitude Force_Aleatoire/Bruit
I = 8                                           # Amplitude de Force_Repulsion_Frontiere 
v0 = 1                                          # Vitesse_Visee
r0 = 0.05                                       # Rayon Largeur epaule
rf = 0.2                                        # Rayon de regroupement
objectif = np.zeros(2)                          # Tableau de l'objectif endroit final visee
a = 0.2                                         # Largeur porte
rb = 0.001                                      # Largeur frontiere

obstacle = 'oui'                                # Presence obstacle
o = int(input("choix obstacle point = 1, ligne = 2, triangle = 3 "))

T = 1                                           # nb de porte 

answr = 'oui' #str(input("Objectif pour la population ? (oui/non) : "))      # Saisie Objectif

    


        
# ////////////////////////////////////////////////////////////////////////////////////
np.random.seed(17)                                      # Graine pour Reproductibilité 
                                                        # Creation tableaux
x, y = np.zeros((N, nb_pop)), np.zeros((N, nb_pop))     # Tableaux positions
vx, vy = np.zeros((N, nb_pop)), np.zeros((N, nb_pop))   # Tableaux vitesses
fx, fy = np.zeros((N, nb_pop)), np.zeros((N, nb_pop))   # Tableaux composantes forces

objx = np.zeros((N, nb_pop))                            # Tableau de l'objectif endroit final visée
objy = np.zeros((N, nb_pop))

# /////////////////////////////////////////////////////////////////////////////////////                                                        
                                                        #♀ Initialisation vitesses/positions
for z in range(nb_pop):  
    for j in range(N):  
        # Génération de positions aléatoires
        x[j][z] = np.random.uniform(0.1, 3.9)
        y[j][z] = np.random.uniform(0.3, 3.9)
        
        # Vérification si un obstacle est présent
        if obstacle == 'oui':
            # Tant que la position générée est dans la zone de l'obstacle
            
            while 1.8 <= x[j][z] <= 2.2 and 0.65 <= y[j][z] <= 1:
                # Réinitialisation de la position dans une zone sans obstacle
                x[j][z] = np.random.uniform(0+1e-10, L-1e-10)
                y[j][z] = np.random.uniform(0.4, l-1e-10)
        
        # Génération de vitesses aléatoires non nulles
        while vx[j][z] == 0 or vy[j][z] == 0:
            vx[j][z] = np.random.uniform(-v0, v0)
            vy[j][z] = np.random.uniform(-v0, v0)
        
        # Si la condition answr est 'oui', initialisation des objectifs
        if answr == 'oui':
            objx[j][z] = 2
            objy[j][z] = 0.05



                
