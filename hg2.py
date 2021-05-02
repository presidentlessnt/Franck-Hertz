#! /usr/bin/python3
import sys
import numpy as np
import scipy.stats
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import warnings
warnings.filterwarnings("ignore")


#obtener datos del .txt
raw=np.loadtxt('Hg_Total.txt')
m=len(raw[0])

#primera etapa: obtener lista picos
radio=50
lraw=len(raw)
A=np.zeros((20,m))  #valor de voltaje pico
B=np.zeros((20,m))  #ordinal de voltaje pico

for j in range(1,m):
    cont=0
    val=0
    for i in range(radio,lraw-radio):
        if raw[i,j]==max(raw[i-radio:i+radio,j]) and raw[i,0]>15:
            if cont==0:
                A[cont,j]=raw[i,0]
                B[cont,j]=i
                val=raw[i,j]
                cont+=1
            elif cont>0 and abs(raw[i,0]-A[cont-1,j])>1:
                A[cont,j]=raw[i,0]
                B[cont,j]=i
                val=raw[i,j]
                cont+=1


#segunda etapa: limpiar ordinal lista picos
plr=list(B[:,1])
pl=[]
for i in range(len(plr)):
    if plr[i]!=0:
        pl.append(int(plr[i]))

#tercera etapa: formar array de valores I_A picos
C=np.zeros((len(pl),m))
for j in range(m):
    for i in range(len(pl)):
        C[i,j]=raw[pl[i],j]


#Diferencias de energias U_1 picos
ener=[]
for i in range(1,len(pl)):
    ener.append(raw[pl[i],0]-raw[pl[i-1],0])

print('Energía (prom):%1.4f [eV]'%np.mean(ener))
print('Desviación Std:%1.4f [eV]'%np.std(ener))



#GRAFICA
colors1=iter(cm.jet(np.linspace(0,1,m)))
colors2=iter(cm.jet(np.linspace(0,1,m)))
eti=['z','A','B','C','D','E','F','G','H','I','J','K','L']

plt.figure(1)
for i in range(1,m):
    plt.plot(C[:,0],C[:,i],'s',markersize=5, color=next(colors1))

for i in range(1,m):
    plt.plot(raw[:,0],raw[:,i],'--',alpha=.5,markersize=1, color=next(colors2),label=eti[i])

plt.grid(ls=':',color='grey',alpha=.5)
plt.title('Hg')
plt.text(20,9,'$U_2=2V, U_H=6.3V, T=175°C$')
plt.xlabel('$\dfrac{U_1}{V}$')
plt.ylabel('$\dfrac{I_A}{nA}$')
plt.xlim(0,60)
plt.legend()



plt.figure(2)
plt.plot(raw[:,0],raw[:,10],':',alpha=.5,markersize=1,color='blue')
plt.boxplot(list(C[:,1:]), positions=list(C[:,0]))
plt.grid(ls=':',color='grey',alpha=.5)
plt.title('Hg')
plt.xlabel('$\dfrac{U_1}{V}$')
plt.ylabel('$\dfrac{I_A}{nA}$')
plt.xlim(0,60)


plt.show()

