# /////////////////////////////////////// FONCTION PASSAGE PIETON COLINEAIRE  ////////////////////////////////////////
import numpy as np 
import os
import matplotlib.pyplot as plt
from Paramètres_AgentGroupe import nb_pop,answr,objectifx,objectify,N,Nmax,vx0,vy0,lmax,lmin,eps,alpha,mu,ramp,v0,r0,rf,Nt,dt,L,x,y,vx,vy,fx,fy,xb,yb,vxb,vyb,I

# //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
def marge(x,y,vx,vy):                                                           
    xb[0:Nmax, 0:nb_pop] = x[0:Nmax, 0:nb_pop]
    yb[0:Nmax, 0:nb_pop] = y[0:Nmax, 0:nb_pop]
    vxb[0:Nmax, 0:nb_pop] = vx[0:Nmax, 0:nb_pop]
    vyb[0:Nmax, 0:nb_pop] = vy[0:Nmax, 0:nb_pop]
    nb = np.zeros(nb_pop)
    for z in range(nb_pop):
        nb[z] = N[z]-1 
        nb = nb.astype(int)
        rb = max(r0[z],rf[z])
                                 
        for k in range(0,N[z]):                    
            if (x[k][z]<=rb):                          # Zone gauche
                nb[z] += 1                      
                xb[nb[z]][z] = x[k][z]+L                   
                yb[nb[z]][z],vxb[nb[z]][z],vyb[nb[z]][z] = y[k][z],vx[k][z],vy[k][z]
                
            if (x[k][z]>=L-rb):                        # zone droite
                nb[z] += 1   
                xb[nb[z]][z] = x[k][z]-L
                yb[nb[z]][z],vxb[nb[z]][z],vyb[nb[z]][z] = y[k][z],vx[k][z],vy[k][z]
                
            if (y[k][z]<=rb):                          # zone basse
                nb[z] += 1   
                yb[nb[z]][z] = y[k][z]-L
                xb[nb[z]][z],vxb[nb[z]][z],vyb[nb[z]][z] = x[k][z],vx[k][z],vy[k][z]
                
            if (y[k][z]>=L-rb):                        # zone haute
                nb[z] += 1   
                yb[nb[z]][z] = y[k][z]-L
                xb[nb[z]][z],vxb[nb[z]][z],vyb[nb[z]][z] = x[k][z],vx[k][z],vy[k][z]
                
            if (x[k][z]<= rb and y[k][z]<=rb):         # Coin bas gauche 
                nb[z] += 1   
                xb[nb[z]][z],yb[nb[z]][z] = x[k][z]+L,y[k][z]+L
                vxb[nb[z]][z],vyb[nb[z]][z] = vx[k][z],vy[k][z]
                
            if (x[k][z]>= L-rb and y[k][z]<=rb):       # Coin bas droit 
                nb[z] += 1   
                xb[nb[z]][z],yb[nb[z]][z] = x[k][z]-L,y[k][z]+L
                vxb[nb[z]][z],vyb[nb[z]][z] = vx[k][z],vy[k][z]
                
            if (x[k][z]<=rb and y[k][z]>=L-rb):        # Coin haut gauche
                nb[z] += 1   
                xb[nb[z]][z],yb[nb[z]][z] = x[k][z]+L,y[k][z]-L
                vxb[nb[z]][z],vyb[nb[z]][z] = vx[k][z],vy[k][z]
                
            if (x[k][z]>= L-rb and y[k][z]>=L-rb):     # Coin haut droit 
                nb[z] += 1   
                xb[nb[z]][z],yb[nb[z]][z] = x[k][z]-L,y[k][z]-L
                vxb[nb[z]][z],vyb[nb[z]][z] = vx[k][z],vy[k][z]    
                
    return nb,xb,yb,vxb,vyb

# //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
def force(nb,xb,yb,vxb,vyb,x,y,vx,vy):
    #boucle pour nb_pop
    for z in range(nb_pop):
        
        #Calcul force entre population 
        for j in range(N[z]):
            repx,repy,flockx,flocky,nflock = 0.,0.,0.,0.,0. 
            
            for k in range(0,nb[z]):
                d2 = (xb[k][z] - x[j][z])**2 + (yb[k][z] - y[j][z])**2 
                
                if (d2 <= rf[z]**2) and (j!=k):
                    flockx += vxb[k][z]
                    flocky += vyb[k][z]
                    nflock += 1
                    
                    if(d2 <=4.*r0[z]**2):
                        d = np.sqrt(d2)
                        repx += eps[z] * (1. - d/(2.*r0[z]))**1.5 * (x[j][z] - xb[k][z])/d    
                        repy += eps[z] * (1. - d/(2.*r0[z]))**1.5 * (y[j][z] - yb[k][z])/d
                        
            
            vnorm = np.sqrt(vx[j][z]**2+vy[j][z]**2)
            
            if answr[z] == 'non':                               # Calcul si pas de position visee
                X,Y = 1.,1.
                fpropx = mu[z]*(v0[z]*X-vnorm)*(vx[j][z]/vnorm)
                fpropy = mu[z]*(v0[z]*Y-vnorm)*(vy[j][z]/vnorm)
                
            if answr[z] == 'oui':                               # Calcul si position visee
                dnorm = np.sqrt((x[j][z]-objectifx[j][z])**2+(y[j][z]-objectify[j][z])**2)
                X = (objectifx[j][z]-x[j][z])/dnorm
                Y = (objectify[j][z]-y[j][z])/dnorm
                fpropx = mu[z]*(v0[z]*X-vx[j][z])
                fpropy = mu[z]*(v0[z]*Y-vy[j][z]) 
                
            normflock = np.sqrt(flockx**2+flocky**2)      
            if (nflock == 0 ): normflock = 1               #Eviter 0/0 division  
            
            flockx = alpha[z] * flockx/normflock
            flocky = alpha[z] * flocky/normflock
            frandx = ramp[z] * np.random.uniform(-1.,1.)       
            frandy = ramp[z] * np.random.uniform(-1.,1.)
            fx[j][z] = (flockx + frandx + fpropx + repx)
            fy[j][z] = (flocky + frandy + fpropy + repy)
            
        if nb_pop != 1. :                                  #Calcul Force_Repulsion_Extra_Pop 
            for i in range(N[z]):                               
                popx,popy = 0.,0.
                for k in range(nb_pop):
                    if k!=z :
                        for w in range(N[k]):
                            d1 = (x[i][z]-x[w][k])**2+(y[i][z]-y[w][k])**2   
                            if d1<(r0[z]+r0[k])**2:                                          #Condition d'action de la force 
                                d=np.sqrt(d1)
                                popx += I*(1.-d/(2.*r0[z]+r0[k]))**1.5*(x[i][z]-x[w][k])/d    #Calcule des composantes des forces 
                                popy += I*(1.-d/(2.*r0[z]+r0[k]))**1.5*(y[i][z]-y[w][k])/d      
                fx[i][z] += popx
                fy[i][z] += popy 
                
        #print("flockx | frandx | fpropx | repx | popx")
        #print(f"{flockx:.3f},{frandx:.3f},{fpropx:.3f},{repx:.3f},0")
        #print("flockx | frandx | fpropx | repx |popy")
        #print(f"{flocky:.3f},{frandy:.3f},{fpropy:.3f},{repy:.3f},0")
    return fx,fy 
   

# /////////////////////////////////////////////////////////////////////////////////////
def moy(x,y,vx,vy,nb_pop):
    Xm = np.zeros(nb_pop)
    Ym = np.zeros(nb_pop)
    Vmx = np.zeros(nb_pop)
    Vmy = np.zeros(nb_pop)
    
    for z in range(nb_pop):
        s = 0.
        r = 0.
        t = 0. 
        u = 0.
        for i in range(N[z]):
            s += vx[i][z]
            r += vy[i][z]
            t += x[i][z]
            u += y[i][z]   
        Vmx[z] = ((1/N[z])*s)
        Vmy[z] = ((1/N[z])*r)
        Xm[z] = ((1/N[z])*t)
        Ym[z] = ((1/N[z])*u)
        
    return Xm,Ym,Vmx, Vmy

# /////////////////////////////////////////////////////////////////////////////////////
def Moy(D):
    M = np.zeros(nb_pop)
    
    for z in range(nb_pop):
        for i in range(N[z]):
            s = 0.
            for i in range(N[z]):
                s += D[i][z]
        M[z] = ((1/N[z])*s)
        
    return M

# /////////////////////////////////////////////////////////////////////////////////////
def ecatype_bary(x, y, vx, vy,nb_pop):
    ecaX = np.zeros(nb_pop)
    ecaY = np.zeros(nb_pop)
    ecaVX = np.zeros(nb_pop)
    ecaVY = np.zeros(nb_pop)
    
    Xm,Ym,Vmx,Vmy = moy(x,y,vx,vy,nb_pop)
    
    for z in range(nb_pop):
        c = 0.
        d = 0.
        e = 0.
        f = 0.
        for i in range(N[z]):
            c += (x[i][z] - Xm[z])**2
            d += (y[i][z] - Ym[z])**2
            e += (vx[i][z] - Vmx[z])**2
            f += (vy[i][z] - Vmy[z])**2

        ecaX[z] = np.sqrt(c/N[z])
        ecaY[z] = np.sqrt(d/N[z])
        ecaVX[z] = np.sqrt(e/N[z])
        ecaVY[z] = np.sqrt(f/N[z])

    #print("L'écart type position x est :", ecaX)
    #print("L'écart type position y est :", ecaY)
    #print("L'écart type vx est :", ecaVX)
    #print("L'écart type vy vitesse est :", ecaVY)
    
    return ecaX,ecaY,ecaVX,ecaVY
  

# /////////////////////////////////////////////////////////////////////////////////////    
def front(x,y):
    for j in range(nb_pop):
        for i in range(N[j]):
            
            if (x[i][j] >= L or x[i][j] <= 0.) :
                if j == 0:
                    x[i][j] = 0.
                    y[i][j] = np.random.uniform(lmin, lmax)
                    vx[i][j] = vx0[j]
                    vy[i][j] = vy0[j]
                if j == 1:
                    x[i][j] = L
                    y[i][j] = np.random.uniform(lmin, lmax)
                    vx[i][j] = vx0[j]
                    vy[i][j] = vy0[j]
          
            if (y[i][j] >= L or y[i][j] <= 0):
                if j == 0:
                    x[i][j] = 0.
                    y[i][j] = np.random.uniform(lmin, lmax)
                    vx[i][j] = vx0[j]
                    vy[i][j] = vy0[j]
                if j == 1:
                    x[i][j] = L
                    y[i][j] = np.random.uniform(lmin, lmax)
                    vx[i][j] = vx0[j]
                    vy[i][j] = vy0[j]
    return x,y

"""
def histog_pdf(x, y, vx, vy):   
    
    

    # Tracé de l'histogramme + PDF (variable aléatoire densité) donne une fonction qui décrit comment les probabilités sont réparties sur l'ensemble des positions possibles
    for z in range(nb_pop):
        X = x[:,z]
        Y = y[:,z]
        VX = vx[:,z]
        VY = vy[:,z]
        plt.figure(f"Histogramme position pop{z+1}")
        plt.subplot(1,2,1)
        plt.title(f'Histogramme des position x et y des agents pop{z+1}')
        plt.hist(X, bins=30, edgecolor='black')  
        plt.xlabel('Position x')
        plt.ylabel('Fréquence')
        plt.plot(np.linspace(min(X), max(X), 100), norm.pdf(np.linspace(min(X), max(X), 100), np.mean(X), np.std(X)), 'r-', lw=2,label='PDF (Normal)')
        plt.grid()
        plt.subplot(1,2,2)
        plt.hist(Y, bins=30, edgecolor='black')  
        plt.xlabel('Position y')
        plt.plot(np.linspace(min(Y), max(Y), 100), norm.pdf(np.linspace(min(Y), max(Y), 100), np.mean(Y), np.std(Y)), 'r-', lw=2,label='PDF (Normal)')
        plt.subplots_adjust(wspace=0.4) 
        plt.grid()
        plt.savefig(f"Positions pop {z+1}.png", dpi=300)
        plt.figure(f"Histogramme vitesse pop{z+1}")
        plt.subplot(1,2,1)
        plt.title(f'Histogramme des vitesses vx et vy des agents pop{z+1} ')
        plt.hist(VX, bins=30, edgecolor='black')  
        plt.xlabel('Vitesse vx')
        plt.ylabel('Fréquence')
        plt.plot(np.linspace(min(VX), max(VX), 100), norm.pdf(np.linspace(min(VX), max(VX), 100), np.mean(VX), np.std(VX)), 'r-', lw=2,label='PDF (Normal)')
        plt.grid()
        plt.subplots_adjust(wspace=0.4) 
        plt.subplot(1,2,2)
        plt.hist(VY, bins=30, edgecolor='black')  
        plt.xlabel('Vitesse  vy')
        plt.plot(np.linspace(min(VY), max(VY), 100), norm.pdf(np.linspace(min(VY), max(VY), 100), np.mean(VY), np.std(VY)), 'r-', lw=2,label='PDF (Normal)')
        plt.grid()
        plt.savefig(f"Vitesses pop {z+1}.png", dpi=300)
    
    return

"""


