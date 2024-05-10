# ///////////////////////////// SIMU PASSAGE PIETON NORMAL ///////////////////
import matplotlib.pyplot as plt 
import numpy as np

# ////////////////////////////////////////////////////////////////////////////////////////////////
from Fonctionp import force, marge,front,histog_pdf,moy,Moy,ecatype_bary
from Parap import nb_pop,objectifx,objectify,N,Nmax,lmin,lmax,eps,alpha,mu,ramp,v0,r0,rf,Nt,dt,L,l,x,y,vx,vy,fx,fy,xb,yb,vxb,vyb,I,answr


# ////////////////////////////////////////////////////////////////////////////////////////////////
def main():                                                         # Fonction Principale
    global N,Nmax,nb_pop,rf,r0,eps,alpha,mu,ramp,v0
    global x,y,xb,yb,vx,vy,vxb,vyb,fx,fy
    
    # Prep figure
    fig = plt.figure(figsize=(4,4), dpi=80)
    ax = plt.gca()
    # //////////////////////////////////////////////////////////////////////////////////////////////////
                                                                    # Partie Analyse
    t = np.zeros(Nt+2)                                              # Liste temps 
    D = np.zeros((Nt+2,nb_pop))                                     # Liste Vmx/v0
    D1 = np.zeros((Nt+2,nb_pop))                                    # Liste Vmy/v0
    ex = np.zeros((Nt+2,Nt+2))                                      # Liste ecart-type x
    ey = np.zeros((Nt+2,Nt+2))                                      # Liste ecart-type y
    evx = np.zeros((Nt+2,Nt+2))                                     # Liste ecart-type vx
    evy = np.zeros((Nt+2,Nt+2))                                     # Liste ecart-type vy
    D[0][0] = 1
    D1[0][0]= 1 
    ex[0][0],ey[0][0],evx[0][0],evy[0][0] = 0.,0.,0.,0.
    if nb_pop !=1 :
        D[0][1] = 1
        D1[0][1]= 1 
        ex[0][1],ey[0][1],evx[0][1],evy[0][1] = 0.,0.,0.,0.
    t[0] = 0.
    mi=0
    j = 0
    # ////////////////////////////////////////////////////////////////////////////////////////////
    for i in range(Nt+1):                                            # Boucle Temporelle principale
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
            plt.title(f'C : {(3.1415*0.25**2*N[0])/(50)*100:.3f} % [occ esp] | {(N[0])/50:.3f} [pers/m2]')
            sec=(dt*(i-j)*0.10416)/dt
            
            if sec> 59:
                mi+=1
                j = i 
                
            plt.suptitle(f'Graphique itération : {i} | Temps : {mi} [min] {sec:.0f} [sec] ')
            
            colors = ['r', 'g', 'b', 'c']                           # Liste Couleurs/Popu
            
            Xm,Ym,Vmx,Vmy = moy(x,y,vx,vy,nb_pop)                   # Calcul posi/vites moyenne
            
            for z in range(nb_pop):                                 # Affichage Posi/Vit
                plt.scatter(x[:, z], y[:, z], color = colors[z],edgecolor='black', s = 180)    
                plt.quiver(x[:, z], y[:, z], vx[:, z], vy[:, z], headlength = 4,edgecolor='black', color = colors[z]) 
                                                                    # Affichage barycentre
                plt.scatter(Xm[z], Ym[z], color = 'm',edgecolor='black', s = 80)
                plt.quiver(Xm[z] ,Ym[z] ,Vmx[z] ,Vmy[z] , headlength=4,color = 'm')
                                                                    # Affichage Largeur passage pieton 
                plt.plot(0, lmin, color = 'b',marker = 'o', markersize = 4) 
                plt.plot(0, lmax, color = 'b',marker = 'o', markersize = 4)
                plt.plot(L, lmin, color = 'b',marker = 'o', markersize = 4) 
                plt.plot(L, lmax, color = 'b',marker = 'o', markersize = 4)
                plt.plot(lmin, L, color = 'y',marker = 'o', markersize = 4) 
                plt.plot(lmax, L, color = 'y',marker = 'o', markersize = 4) 
                plt.plot(lmin, 0, color = 'y',marker = 'o', markersize = 4) 
                plt.plot(lmax, 0, color = 'y',marker = 'o', markersize = 4) 
                                                                    # Calcul ecart-type posi/vitess
                c,v,b,n = ecatype_bary(x, y, vx, vy,nb_pop)
                ex[i+1][z] =  c[z]/v0[z]
                ey[i+1][z] =  v[z]/v0[z]
                evx[i+1][z] =  b[z]/v0[z]
                evy[i+1][z] =  n[z]/v0[z]
                D[i+1][z] = abs(Vmx[z]/v0[z])
                D1[i+1][z] = abs(Vmy[z]/v0[z])
                
            plt.axis([0.,L,0.,l])                                   # Dimension domaine
            plt.pause(0.01)                                         # Pause pour Maj
            #plt.subplot(2,4,2)
            #a = histog_pdf(x, y, vx, vy)
            #print(a)
            #plt.save('image{0}.jpeg'.format(i))    
            
    plt.show()
    
                                                                    # Graphiques + donnees   
    plt.plot(t,D[:,0])
    plt.title(f'Tf : {mi} min et {sec:.0f} sec | C: {(3.1415*0.25**2*N[0]+3.1415*0.25**2*N[1])/(75)*100:.3f} % [occ esp] | {(N[0]+N[1])/75:.3f} [pers/m2] | pop{z+1}')
    plt.suptitle(f'Graphique Vmx/v0 fonction T/T0 | Population : {z+1} | N{z+1} = {N[z]}')
    plt.axis([0.,len(t)*dt,0.,2*L]) 
    plt.grid()
    plt.xlabel("Temps/T0")
    plt.ylabel("Vmx/v0")
    plt.show()

    plt.plot(t,evx[:,0])
    plt.title(f'Tf : {mi} min et {sec:.0f} sec | C: {(3.1415*0.25**2*N[0]+3.1415*0.25**2*N[1])/(75)*100:.3f} % [occ esp] | {(N[0]+N[1])/75:.3f} [pers/m2] | pop{z+1}')
    plt.suptitle(f'Graphique EcVmx/v0 fonction T/T0| Population : {z+1} | N{z+1} = {N[z]}')
    plt.axis([0.,len(t)*dt,0.,2*L]) 
    plt.grid()
    plt.xlabel("Temps/T0")
    plt.ylabel("EcVmx/v0")
    plt.show()
    moyenne_colonne = [np.mean(D[201:, 0])]
    """
    plt.plot(t,evy[:,1])
    plt.title(f'Tf : {mi} min et {sec:.0f} sec | C: {(3.1415*0.25**2*N[0]+3.1415*0.25**2*N[1])/(75)*100:.3f} % [occ esp] | {(N[0]+N[1])/75:.3f} [pers/m2] | pop{z+1}')
    plt.suptitle(f'Graphique EcVmy/v0 fonction T/T0| Population : {z+1} | N{z+1} = {N[z]}')
    plt.axis([0.,len(t)*dt,0.,2*L]) 
    plt.grid()
    plt.xlabel("Temps/T0")
    plt.ylabel("EcVmy/v0")
    plt.show()
    
    
    
    plt.plot(t,D1[:,1])
    plt.title(f'Tf : {mi} min et {sec:.0f} sec | C: {(3.1415*0.25**2*N[0]+3.1415*0.25**2*N[1])/(75)*100:.3f} % [occ esp] | {(N[0]+N[1])/75:.3f} [pers/m2] | pop{z+1}')
    plt.suptitle(f'Graphique Vmy/v0 fonction T/T0 | Population : {z+1} | N{z+1} = {N[z]}')
    plt.axis([0.,len(t)*dt,0.,2*L]) 
    plt.grid()
    plt.xlabel("Temps/T0")
    plt.ylabel("Vmy/v0")
    plt.show()
    """
    
    print(f"La moyenne de la colonne Vmx/V0{1} est : {moyenne_colonne[0]}")
    print(f"La Moyenne evx {1} est : {np.mean(evx[201:,0])}")
    print(f"Moyenne ex {1} est : {np.mean(ex[201:,0])}")
    print(f"Moyenne ey {1} est : {np.mean(ey[201:,0])}")
    print(f"Moyenne evy {1} est : {np.mean(evy[201:,0])}")
    """
    print(f"La moyenne de la colonne Vmy/V0{2} est : {moyenne_colonne[1]}")
    print(f"La Moyenne evx {2} est : {np.mean(evx[201:,1])}")
    print(f"Moyenne ex {2} est : {np.mean(ex[201:,1])}")
    print(f"Moyenne ey {2} est : {np.mean(ey[201:,1])}")
    print(f"Moyenne evy {2} est : {np.mean(evy[201:,1])}")
    """
    return 0
	

if __name__== "__main__":
  main()


