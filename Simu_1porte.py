#//////////////////////SIMULATION EVACUATION 1 PORTE//////////////////////////////
import matplotlib.pyplot as plt 
import numpy as np
# /////////////////////////////////////////////////////////////////////////////////////
from Fonction_1porte import force,frontiere,OX,OY,n
from Para_1porte import nb_pop,objectif,answr,obstacle,N,eps,alpha,mu,ramp,v0,rb,r0,rf,Nt,dt,L,l,x,y,vx,a,vy,fx,fy,I#,FRX,FRY

# /////////////////////////////////////////////////////////////////////////////////////
# PROGRAMME PRINCIPAL
def main():
    global N,Nmax,nb_pop,rf,r0,eps,alpha,mu,ramp,v0
    global x,y,vx,vy,fx,fy
    
    # Prep figure
    fig = plt.figure(figsize=(4,4), dpi=80)
    cpt = 0.
    T = 1
    mi=0
    j = 0
    o = 0 
    A = 0
    # /////////////////////////////////////////////////////////////////////////////////////
    for i in range(Nt+1):                                                   # Boucle Temporelle pprincipale
        print("itération n°= ",i)
        sec=(dt*(i-j)*0.104166)/dt
        
        if sec> 59:
            mi+=1
            j = i 
        # /////////////////////////////////////////////////////////////////////////////////////
        fx,fy = force(N,x,y,vx,vy)                                          # Calcul Resultante des Forces
        vx, vy = frontiere(rb,x,y,vx,vy,n,OX,OY)

        # /////////////////////////////////////////////////////////////////////////////////////
        vx += fx*dt                                                         # MaJ P/V Methode Euler_Ex           
        vy += fy*dt                          
        x += vx*dt
        y += vy*dt
        #print("vx",vx)
        #print("vy",vy)
        # /////////////////////////////////////////////////////////////////////////////////////
        plotRealTime=True                                                   # Affichage 
        if plotRealTime or (i == Nt-1):
            plt.title(f'Temps : {mi} min et {sec:.0f} sec | C : {(3.1415*0.25**2*N/(400))*100:.3f} % [occ esp] | Ppm2 : {N/400} [pers/m2]')
            plt.suptitle(f'Evacuation Salle 400 m2 | N : {N}')
            # /////////////////////////////////////////////////////////////////////////////////////
            for z in range(nb_pop):                                         # Affichage positions/vitesses agents 
                plt.scatter(x[:, z], y[:, z], color = 'r', edgecolor='black', s = 75)
                plt.quiver(x[:, z], y[:, z], vx[:, z], vy[:, z], headlength = 10, color = 'r')
                #for u in range(6):                                         # Affichage Frontière
                    #plt.scatter(FRX[:, u], FRY[:, u], color='g', s = 0)   
                    
            # /////////////////////////////////////////////////////////////////////////////////////
            if objectif == 'oui' :                                                          # Affichage objectif
                plt.plot(objectif[0],objectif[1], color='b',marker='o', markersize=8)   
                
            # /////////////////////////////////////////////////////////////////////////////////////
            if obstacle == 'oui' :                                                          # Affichage obstacle                                          
                plt.scatter(OX[:], OY[:], color = 'm', s = 100)
                
            # /////////////////////////////////////////////////////////////////////////////////////
            plt.plot((L+a)/2,0,color='y',marker='o', markersize=5)                  # Affichage porte
            plt.plot((L/2-a/2),0,color='y',marker='o', markersize=5)                # Affichage porte 
           
            plt.axis([0.,L,0.,L])                 
            plt.pause(0.01)
            #plt.axis("equal")
        # /////////////////////////////////////////////////////////////////////////////////////
        for j in range(nb_pop):                                                     # Supprimer agents  
            for k in range(N):
                if y[k][j] <= 0.04:   
                    if T == 1 :                                                 
                        if ((L-a)/2 <= x[k][j] and x[k][j] <= (L+a)/2):
                            x[k][j] = -10.
                            y[k][j] = -10.
                            vx[k][j] = 0.
                            vy[k][j] = 0.    				
     
                if vx[k][j] == 0.:  
                    cpt += 1
                if cpt == N :
                    print(f"Evacuation en T = {mi} min et {sec:.0f} sec")
                    return 
                
        if (N - cpt) == 2 and o == 0:
             A = i
             o = 1
        if o == 1 and (i - A) > 20:
             print(f"Evacuation en T = {mi} min et {sec:.0f} sec")
             return
        
    plt.show()
    return 0

	

if __name__== "__main__":
  main()






