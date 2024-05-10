#////////////////////// FONCTION EVACUATION 2 PORTES //////////////////////////////
import numpy as np 

# /////////////////////////////////////////////////////////////////////////////////////
from Paramètres_Casdetude2 import nb_pop,answr,obstacle,objx,objy,o,N,eps,alpha,mu,ramp,v0,r0,a,rf,rb,Nt,dt,L,x,y,vx,vy,fx,fy,L,l,I,oby,obx

# /////////////////////////////////////////////////////////////////////////////////////
def force(N,x,y,vx,vy):
    for z in range(nb_pop):
        for j in range(N):
            repx,repy,flockx,flocky,nflock = 0.,0.,0.,0.,0. 
            
            # ////////////////////////////////////////////////////////////////////////////////////////////////////////////
            for k in range(0,N):                                                    # Calcul Force_Globale
                d2 = (x[k][z]-x[j][z])**2+(y[k][z]-y[j][z])**2 
                if (d2 <= rf**2) and (j!=k):
                    flockx += vx[k][z]
                    flocky += vy[k][z]
                    nflock += 1
                    if(d2 <=4.*r0**2):
                        d = np.sqrt(d2)
                        repx += eps*(1.-d/(2.*r0))**1.5*(x[j][z]-x[k][z])/d    
                        repy += eps*(1.-d/(2.*r0))**1.5*(y[j][z]-y[k][z])/d
            
            # ///////////////////////////////////////////////////////////////////////////////////////////////////////////
                                                                                    # Calculs des forces
            vnorm = np.sqrt(vx[j][z]**2+vy[j][z]**2)                                # Calcul Force_Auto_Prop
            if answr == 'non':
                X,Y = 1.,1.
                fpropx = mu*(v0*X-vnorm) * (vx[j][z]/vnorm)
                fpropy = mu*(v0*Y-vnorm) * (vy[j][z]/vnorm)
            else :
                dnorm = np.sqrt((x[j][z]-objx[j][z])**2 + (y[j][z]-objy[j][z])**2)
                X = (objx[j][z] - x[j][z])/dnorm
                Y = (objy[j][z] - y[j][z])/dnorm
                fpropx = mu *(v0*X - vx[j][z])
                fpropy = mu *(v0*Y - vy[j][z])
                
            normflock = np.sqrt(flockx**2 + flocky**2)                              # Calcul Force_Flocking
            if (nflock == 0 ): normflock = 1                                        # Eviter 0/0 division   
            flockx = alpha*flockx/normflock                                         
            flocky = alpha*flocky/normflock
                                                                                    # Calcul Force_Aleatoire
            frandx = ramp*np.random.uniform(-1.,1.)       
            frandy = ramp*np.random.uniform(-1.,1.)
            
            # ///////////////////////////////////////////////////////////////////////////////////////////////////////////
            fx[j][z] = (flockx + frandx + fpropx + repx )                     # Calcul Resultante
            fy[j][z] = (flocky + frandy + fpropy + repy ) 
    return fx,fy 
             
# ///////////////////////////////////////////////////////////////////////////////////////////////////////////
def frontiere(rb,x,y,vx,vy,n,OX,OY):
    global T
    for j in range(nb_pop):                               
        for i in range(N):  
                                    
            if(x[i][j] <= rb):                          #Zone gauche

                    vx[i][j] = 0.
                    vy[i][j] = 0. 
                        
            if (x[i][j] >= L-rb):                       #zone droite

                    vx[i][j] = 0.
                    vy[i][j] = 0.


            if (y[i][j] >= L-rb):                       #zone haute

                    vx[i][j] = 0.
                    vy[i][j] = 0.
                                               
            if (y[i][j] <= rb) and (x[i][j] <= 0.25) :  #zone basse gauche 
   
                vx[i][j] = 0.
                vy[i][j] = 0.
                
            elif (y[i][j] <= rb) and (x[i][j] >= 3.75) :  
                vx[i][j] = 0.
                vy[i][j] = 0.
                
            #elif (y[i][j] <= rb):                         #zone basse droite 
                #if (x[i][j] <= 0.7) and (x[i][j] >= 0.3):
                    
                        #vx[i][j] = 0.
                        #vy[i][j] = 0.
                            
            # //////////////////////////////////////////////////////////////////// 
            
            if obstacle == 'oui':
                if o == 1 :
                    if (x[i][j]>= 0.9 and x[i][j]<=1.1) or (x[i][j]>= 2.9and x[i][j]<=3.1): 
                        if (y[i][j] <= 0.95 and y[i][j] >0.75) : 
                            vy[i][j] = 0.
                            if x[i][j]>1  and  x[i][j]<3 : 
                                objx[i][j] = 2 
                                objy[i][j] = 0
                            elif  x[i][j]<1 : 
                                objx[i][j] = 0 
                                objy[i][j] = 0
                            elif x[i][j]>3 :
                                objx[i][j] = 4 
                                objy[i][j] = 0
                    else :   
                        objx[i][j] = obx[i][j]
                        objy[i][j] = oby[i][j]

                if o == 2 : 
                    if (x[i][j]>= 0.75 and x[i][j]<=1.25) or (x[i][j]>= 2.75 and x[i][j]<=3.25) : 
                        if (y[i][j] <= 0.95 and y[i][j] >0.75) : 
                            vy[i][j] = 0.
                            if x[i][j]>1 and x[i][j]<3 : 
                                objx[i][j] = 2
                                objy[i][j] = 0
                            elif  x[i][j]<1: 
                                objx[i][j] = 0 
                                objy[i][j] = 0
                            elif x[i][j]>3 : 
                                objx[i][j] = 4 
                                objy[i][j] = 0
                    else :   
                        objx[i][j] = obx[i][j] 
                        objy[i][j] = oby[i][j]
                     
    return vx, vy


# ///////////////////////////////////////////////////////////////////////////////////////////////////////////
def obst(o):
    if o == 1 : 
                                # Obstacle point 
        ox = [1,3]                                       
        oy = [0.75,0.75]
        n = 2
        return ox,oy,n
    
    if o == 2 : 
                                # Obstacle ligne 
        n = 41                  # Nb de point 
        oy = np.zeros(n)
        ox = [0.80,0.82,0.84,0.86,0.88,0.90,0.92,0.94,0.96,0.98,1,1.02,1.04,1.06,1.08,1.1,1.12,1.14,1.16,1.18,1.2,2.8,2.82,2.84,2.86,2.88,2.9,2.92,2.94,2.96,2.98,3,3.02,3.06,3.08,3.1,3.12,3.14,3.16,3.18,3.2]                                       
        for i in range(n) : 
            oy[i] = 0.75
        return ox,oy,n  
                              
if obstacle == 'oui':
    OX,OY,n = obst(o)   
else :
    OX = 0. 
    OY = 0. 
    n = 0.






