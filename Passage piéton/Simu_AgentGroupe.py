# ///////////////////////////// SIMU PASSAGE PIETON COLINEAIRE ///////////////////
import matplotlib.pyplot as plt 
import numpy as np

# ////////////////////////////////////////////////////////////////////////////////////////////////
from Fonction_Simu_AgentGroupe import force, marge,front,moy,Moy,ecatype_bary
from Paramètres_AgentGroupe import nb_pop,objectifx,objectify,N,Nmax,lmin,lmax,eps,alpha,mu,ramp,v0,r0,rf,Nt,dt,L,l,x,y,vx,vy,fx,fy,xb,yb,vxb,vyb,I,answr


# ////////////////////////////////////////////////////////////////////////////////////////////////
def main():                                                         # Fonction Principale
    global N,Nmax,nb_pop,rf,r0,eps,alpha,mu,ramp,v0
    global x,y,xb,yb,vx,vy,vxb,vyb,fx,fy
    
                                                                    # Preparation figure
    fig = plt.figure(figsize=(4,4), dpi=80)
    ax = plt.gca()
    # //////////////////////////////////////////////////////////////////////////////////////////////////
                                                                    # Partie Analyse
    t = np.zeros(Nt+2)                                              # Liste temps
    D = np.zeros((Nt+2,nb_pop))                                     # Liste Vm/v0
    ex = np.zeros((Nt+2,Nt+2))                                      # Liste ecart-type x
    ey = np.zeros((Nt+2,Nt+2))                                      # Liste ecart-type y
    evx = np.zeros((Nt+2,Nt+2))                                     # Liste ecart-type vx
    evy = np.zeros((Nt+2,Nt+2))                                     # Liste ecart-type vy
    D[0][0] = 1
    ex[0][0],ey[0][0],evx[0][0],evy[0][0] = 0.,0.,0.,0.
    if nb_pop !=1 :
        D[0][1] = 1
        ex[0][1],ey[0][1],evx[0][1],evy[0][1] = 0.,0.,0.,0.
    t[0] = 0.
    mi=0
    j=0
    # ////////////////////////////////////////////////////////////////////////////////////////////
    for i in range(Nt+1):                                           # Boucle Temporelle principale

        nb,xb,yb,vxb,vyb = marge(x,y,vx,vy)                         # Fonction marge return listes etendues positions/vitesses agents (repliquaunt inclus)
        fx,fy = force(nb,xb,yb,vxb,vyb,x,y,vx,vy)                   # Fonction Force 
        
        # ////////////////////////////////////////////////////////////////////////////////////////////
        vx += fx*dt                                                 # Maj Positions/Vitesses Euler_Ex                  
        vy += fy*dt                          
        x += vx*dt
        y += vy*dt
        t[i+1] = t[i] + dt                                          # Ajout temps 
        x,y =front(x,y)                                             # Periodicite
        
        
        
        # ////////////////////////////////////////////////////////////////////////////////////////////
        plotRealTime=True                                           # Affichage 
        if plotRealTime or (i == Nt-1):
            plt.title(f'Compacite : {((3.1415*0.25**2*N[0]+3.1415*0.25**2*N[1])/50)*100:.3f} % [occ esp] | nb_pers par m2 : {(N[0]+N[1])/50} [pers/m2] ')
            sec=(dt*(i-j)*0.1041)/dt
            
            if sec> 59:
                mi+=1
                j = i 
                
            plt.suptitle(f'Graphique iteration : {i} | Temps : {mi} [min] {sec:.0f} [sec] ')
            #plt.clf()  # Nettoie la figure actuelle
            
            colors = ['r', 'g', 'b', 'c']                           # Liste Couleurs/Popu
            
            Xm,Ym,Vmx,Vmy = moy(x,y,vx,vy,nb_pop)                   # Calcul posi/vites moyenne 
            
            for z in range(nb_pop):                                 # Affichage Posi/Vit
                plt.scatter(x[:, z], y[:, z], color = colors[z],edgecolor='black', s = 150)    
                plt.quiver(x[:, z], y[:, z], vx[:, z], vy[:, z], headlength = 4,edgecolor='black', color = colors[z]) 
                                                                    # Affichage barycentre
                plt.scatter(Xm[z], Ym[z], color = 'm',edgecolor='black', s = 80)
                plt.quiver(Xm[z] ,Ym[z] ,Vmx[z] ,Vmy[z] , headlength=4,color = 'm')
                                                                    # Affichage Largeur passage pieton 
                plt.plot(0, lmin, color = 'b',marker = 'o', markersize = 4) 
                plt.plot(0, lmax, color = 'b',marker = 'o', markersize = 4) 
                plt.plot(L, lmin, color = 'b',marker = 'o', markersize = 4) 
                plt.plot(L, lmax, color = 'b',marker = 'o', markersize = 4) 
                
                c,v,b,n = ecatype_bary(x, y, vx, vy,nb_pop)         # Calcul ecart-type posi/vitess
                ex[i+1][z] =  c[z]/v0[z]
                ey[i+1][z] =  v[z]/v0[z]
                evx[i+1][z] =  b[z]/v0[z]
                evy[i+1][z] =  n[z]/v0[z]
                D[i+1][z] = abs(Vmx[z]/v0[z])
                
            plt.xlim(0, L)
            plt.ylim(0, L)

            plt.pause(0.01)  
    
    plt.show()
    
    for z in range(nb_pop):                                         # Graphiques + donnees 
        
        plt.plot(t,D[:,z])
        plt.title(f'Tf : {mi} min et {sec:.0f} sec | C: {(3.1415*0.25**2*N[z]/50)*100:.3f} | pop{z+1}')
        plt.suptitle(f'Graphique Vmx/v0 fonction T/T0 | Population : {z+1} | N{z+1} = {N[z]}')
        plt.axis([0.,len(t)*dt,0.,2*L]) 
        plt.grid()
        plt.xlabel("Temps/T0")
        plt.ylabel("Vmx/v0")
        plt.show()
        plt.plot(t,evx[:,z])
        plt.title(f'Tf : {mi} min et {sec:.0f} sec | C : {(3.1415*0.25**2*N[z]/50)*100:.3f} | pop{z+1}')
        plt.suptitle(f'Graphique EcVmx/v0 fonction T/T0| Population : {z+1} | N{z+1} = {N[z]}')
        plt.axis([0.,len(t)*dt,0.,2*L]) 
        plt.grid()
        plt.xlabel("Temps/T0")
        plt.ylabel("EcVmx/v0")
        plt.show()
        
        moyenne_colonne = np.mean(D[201:, z])
        
        print(f"La moyenne de la colonne {z+1} est : {moyenne_colonne}")
        print(f"La Moyenne evx {z+1} est : {np.mean(evx[201:,z])}")
        print(f"Moyenne ex {z+1} est : {np.mean(ex[201:,z])}")
        print(f"Moyenne ey {z+1} est : {np.mean(ey[201:,z])}")
        print(f"Moyenne evy {z+1} est : {np.mean(evy[201:,z])}")
    return 0
	

if __name__== "__main__":
  main()

