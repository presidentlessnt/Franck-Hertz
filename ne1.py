#! /usr/bin/python3
import sys
import numpy as np
import scipy.stats
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import warnings
warnings.filterwarnings("ignore")


#obtener datos del .txt
raw=np.loadtxt('Ne_Total.txt')
m=len(raw[0])



#primera etapa: obtener lista picos
radio=100
lraw=len(raw)
A=np.zeros((5,3*(m-1)))


for j in range(1,m):
    cont=0
    val=0
    for i in range(radio,lraw-radio):
        if raw[i,j]==max(raw[i-radio:i+radio,j]) and raw[i,0]>12 and raw[i,j]>.18 and raw[i,j]<49:
            if cont==0:
                A[cont,3*(j-1)]=raw[i,0]
                A[cont,3*(j-1)+1]=i
                A[cont,3*(j-1)+2]=raw[i,j]
                val=raw[i,j]
                cont+=1
            elif cont>0 and abs(raw[i,0]-A[cont-1,3*(j-1)])>1 and raw[i,j]!=val:
                A[cont,3*(j-1)]=raw[i,0]
                A[cont,3*(j-1)+1]=i
                A[cont,3*(j-1)+2]=raw[i,j]
                val=raw[i,j]
                cont+=1


#segunda etapa: limpiar lista picos
plr=list(A[:,1])
pl=[]
for i in range(len(plr)):
    if plr[i]!=0:
        pl.append(int(plr[i]))


#Diferencias de energías pico
E=np.zeros((7,m-1))
for i in range(1,5):
    val=0
    for j in range(m-1):
        val=A[i,3*j]-A[i-1,3*j]
        if val>0:
            E[i,j]=val

#promedio aritmetico
for j in range(m-1):
    cont=0
    for i in range(5):
        if E[i,j]!=0:
            E[5,j]+=E[i,j]
            cont+=1
    E[5,j]=E[5,j]/cont

#desviacion std
for j in range(m-1):
    cont=0
    for i in range(5):
        if E[i,j]!=0:
            E[6,j]+=(E[5,j]-E[i,j])**2
            cont+=1
    E[6,j]=(E[6,j]/(cont-1))**.5



eti=['z','H - 4.5','C - 4.5','F - 4.7','X - 5.0','E - 5.2','A - 5.5','L - 5.7','M - 5.9','B - 6.0','G - 6.5','D - 7.0']

for i in range(m-1):
    print('Energía ',eti[i+1],': %1.4f +-%1.4f [eV]'%(E[5,i],E[6,i]))



#GRAFICA
colors1=iter(cm.jet(np.linspace(0,1,m)))
colors2=iter(cm.jet(np.linspace(0,1,m)))


plt.figure(1)
for i in range(m-1):
    plt.plot(A[:,3*i],A[:,3*i+2],'s',markersize=5, color=next(colors1))

for i in range(1,m):
    plt.plot(raw[1:,0],raw[1:,i],'--',alpha=.5,markersize=1, color=next(colors2),label=eti[i])


plt.grid(ls=':',color='grey',alpha=.5)
plt.title('Ne')
plt.xlabel('$\dfrac{U_1}{V}$')
plt.ylabel('$\dfrac{I_A}{nA}$')
plt.legend(title='Linea - $U_H$')
plt.xlim(0,100)

#plt.show()

