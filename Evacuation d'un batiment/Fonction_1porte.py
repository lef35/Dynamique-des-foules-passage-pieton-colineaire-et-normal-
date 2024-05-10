#////////////////////// FONCTION EVACUATION 1 PORTE //////////////////////////////
import numpy as np 

# /////////////////////////////////////////////////////////////////////////////////////
from Para_1porte import nb_pop,answr,obstacle,objx,objy,o,N,eps,alpha,mu,ramp,v0,r0,a,rf,rb,Nt,dt,L,x,y,vx,vy,fx,fy,L,l,I#,FRX,FRY,n

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
    t = 1
    T = 1
    for j in range(nb_pop):                               
        for i in range(N):  
                                    
            if(x[i][j] <= rb):                          #Zone gauche
                if t == 1 :
                    vx[i][j] = 0.
                    vy[i][j] = 0.

                        
            if (x[i][j] >= L-rb):                       #zone droite
                vx[i][j] = 0.
                vy[i][j] = 0.


            if (y[i][j] >= L-rb):                       #zone haute
                vx[i][j] = 0.
                vy[i][j] = 0.
                    
            
            if T == 1 :                                     # Cas 1 porte 
                if (y[i][j] <= rb):                         #zone basse gauche 
                    if (x[i][j] <= (L/2-a/2)):

                        vx[i][j] = 0.
                        vy[i][j] = 0.

                            
                if (y[i][j] <= rb):                         #zone basse droite 
                    if (x[i][j] >= (L+a)/2):
                        vx[i][j] = 0.
                        vy[i][j] = 0.
                            
                

            
            # //////////////////////////////////////////////////////////////////// 
            
            if obstacle == 'oui':
                if o == 1 :
                    if (x[i][j]>= 1.9 and x[i][j]<=2.1) : 
                        if (y[i][j] <= 1 and y[i][j] >=0.75) : 
                            if x[i][j]<2 : 
                                objx[i][j] = 0 
                                objy[i][j] = 0
                            else : 
                                objx[i][j] = 4 
                                objy[i][j] = 0
                            vy[i][j] = 0.
                    else :   
                        objx[i][j] = 2 
                        objy[i][j] = 0
                        
                if o == 2 : 
                    if (x[i][j]>= 1.65 and x[i][j]<= 2.35) : 
                        if (y[i][j] < 0.95 and y[i][j] >0.75) : 
                            if x[i][j]<2 : 
                                objx[i][j] = 0 
                                objy[i][j] = 0
                            else : 
                                objx[i][j] = 4 
                                objy[i][j] = 0
                            vy[i][j] = 0.
                    else :   
                        objx[i][j] = 2
                        objy[i][j] = 0
                        
                if o == 3 : 
                    if (x[i][j]>= 1.75 and x[i][j]<=2.25) : 
                        if (y[i][j] <= 1.35 and y[i][j] >=0.8) :
                            if x[i][j]<2 : 
                                objx[i][j] = 0 
                                objy[i][j] = 0
                            else : 
                                objx[i][j] = 4 
                                objy[i][j] = 0
                            vy[i][j] = 0.
                    if (x[i][j]>= 1.55 and x[i][j]<=2.55) : 
                        if (y[i][j] <= 0.95 and y[i][j] >=0.75) :
                            if x[i][j]<2 : 
                                objx[i][j] = 0 
                                objy[i][j] = 0
                            else : 
                                objx[i][j] = 4
                                objy[i][j] = 0
                            vy[i][j] = 0.        
                    else :   
                        objx[i][j] = 2 
                        objy[i][j] = 0
                    
    return vx, vy


# ///////////////////////////////////////////////////////////////////////////////////////////////////////////
def obst(o): 
    if o == 1 : 
                                # Obstacle point 
        ox = [2]                                       
        oy = [0.75]
        n = 1
        return ox,oy,n
    
    # //////////////////////////////////////////////////////////////////// 
    if o == 2 : 
                                # Obstacle ligne 
        n = 11                  # Nb de point 
        ox = [L/2-4*r0,L/2-3*r0,L/2-2*r0,L/2-1*r0,L/2,L/2+1*r0,L/2+2*r0,L/2+3*r0,L/2+4*r0]
        oy = [0.75,0.75,0.75,0.75,0.75,0.75,0.75,0.75,0.75]
        return ox,oy,n  
    
    # //////////////////////////////////////////////////////////////////// 
    if o == 3 :  
                                # Obstacle triangle 
        ox = [L/2-4*r0,L/2-3*r0,L/2-2*r0,L/2-1*r0,L/2,L/2+1*r0,L/2+2*r0,L/2+3*r0,L/2+4*r0,L/2-4*r0,L/2-3*r0,L/2-2*r0,L/2-1*r0,L/2,L/2+1*r0,L/2+2*r0,L/2+3*r0,L/2+4*r0,L/2-3*r0,L/2-2*r0,L/2-1*r0,L/2,L/2+1*r0,L/2+2*r0,L/2+3*r0,L/2-2*r0,L/2-1*r0,L/2,L/2+1*r0,L/2+2*r0,L/2-1*r0,L/2,L/2+1*r0,L/2]
        oy = [0.80,0.80,0.80,0.80,0.80,0.8,0.8,0.8,0.8,0.8+r0,0.8+r0,0.8+r0,0.8+r0,0.8+r0,0.8+r0,0.8+r0,0.8+r0,0.8+r0,0.8+2*r0,0.8+2*r0,0.8+2*r0,0.8+2*r0,0.8+2*r0,0.8+2*r0,0.8+2*r0,0.8+3*r0,0.8+3*r0,0.8+3*r0,0.8+3*r0,0.8+3*r0,0.8+4*r0,0.8+4*r0,0.8+4*r0,0.8+5*r0]
        n = 36
        return ox,oy,n
                             
if obstacle == 'oui':
    OX,OY,n = obst(o)   
else :
    OX = 0. 
    OY = 0. 
    n = 0.


