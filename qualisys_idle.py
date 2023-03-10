# -*- coding: utf-8 -*-
"""
Created on Thu Feb 23 16:03:31 2023

@author: ERIKA
"""

import matplotlib.pyplot as plt
from math import sqrt
import numpy as np
from scipy.io import loadmat
import matplotlib.mlab as mlab
#from scipy import signal
#from scipy.signal import find_peaks

folder = "H:\\ic-loc\\ss7\\CMCD\\Dozap\\"
files = ["S30_DUMMY_A50_T0,80_R1","S30_DUMMY_A50_T0,80_R1_100Hz",
         "S30_DUMMY_A50_T0,80_R1_4800Hz",'S30_DUMMY_A50_T0,80_R1_Qualisys',
         'S30_STR_A50_T0,80_R1','S30_STR_A50_T0,80_R1_100Hz',
         'S30_STR_A50_T0,80_R1_4800Hz','S30_STR_A50_T0,80_R1_Qualisys']
caminhos = []
for file in files:
    caminhos.append(folder+file+'.mat')
#arquivo com as informações do que é cada .mat
infos = open('Infos_qualisys.txt','w')
for file in caminhos:
    mat = loadmat(file)
    titulo = '\n\n\n'+str(file)+'\n'
    infos.write(titulo)
    for chave in mat.keys():
        info = '\n'+str(chave)+'\t'+str(type(mat[chave]))+'\ttamanho:'+str(len(mat[chave]))
        infos.write(info)
infos.close()

#data 100Hz Dummy
hz1_Dummy = loadmat(caminhos[1])
canal1_1hz_Dummy = hz1_Dummy['Channel_1_Data']
canal2_1hz_Dummy = hz1_Dummy['Channel_2_Data']
canal3_1hz_Dummy = hz1_Dummy['Channel_3_Data']
canal4_1hz_Dummy = hz1_Dummy['Channel_4_Data']
canal5_1hz_Dummy = hz1_Dummy['Channel_5_Data']
canal6_1hz_Dummy = hz1_Dummy['Channel_6_Data']
canal7_1hz_Dummy = hz1_Dummy['Channel_7_Data']
canal8_1hz_Dummy = hz1_Dummy['Channel_8_Data']
canal9_1hz_Dummy = hz1_Dummy['Channel_9_Data']
#data 4800Hz Dummy
hz48_Dummy = loadmat(caminhos[2])
canal1_48hz_Dummy = hz48_Dummy['Channel_1_Data']
canal2_48hz_Dummy = hz48_Dummy['Channel_2_Data']
#gráficos Qualisys Dummy
qua_Dummy = loadmat(caminhos[3])
time_s_Dummy = qua_Dummy['time_s']
x_filled_mm_Dummy = qua_Dummy['x_filled_mm']
x_raw_mm_Dummy = qua_Dummy['x_raw_mm']
dp_filled_Dummy = np.std(x_filled_mm_Dummy.ravel())
dp_raw_Dummy = np.std(x_raw_mm_Dummy.ravel())
dp_canal2_48Hz_Dummy = np.std(canal2_48hz_Dummy.ravel())
#Dummy graf
fig_Dummy, axs_Dummy = plt.subplots(2)

#axs_Dummy[0].set_ylabel('Canal6')
#axs_Dummy[0].plot(canal1_1hz_Dummy,canal6_1hz_Dummy)
#axs_Dummy[0].set_title('100Hz_Dummy')

#axs_Dummy[1].set_ylabel('canal1')
axs_Dummy[0].plot(canal1_48hz_Dummy[40000:240000],canal2_48hz_Dummy[40000:240000])
#axs_Dummy[0].axhline(sqrt(2)*dp_canal2_48Hz_Dummy)
axs_Dummy[0].set_title('S30_DUMMY_A50_T0,80_R1_4800Hz')

axs_Dummy[1].set_xlabel('time_s')
axs_Dummy[1].set_ylabel('x_filled_mm_Dummy',color='b')
axs_Dummy[1].plot(time_s_Dummy[1200:5000],x_filled_mm_Dummy[1200:5000],'b')
axs_Dummy[1].axhline(sqrt(2)*dp_filled_Dummy)
axs_Dummy[1].set_title('S30_DUMMY_A50_T0,80_R1_Qualisys')
axs_Dummy[1].tick_params(axis='y',labelcolor='b')

ax = axs_Dummy[1].twinx()
ax.set_ylabel('x_raw_mm_Dummy',color='r')
ax.plot(time_s_Dummy[1200:5000], x_raw_mm_Dummy[1200:5000], 'r')
ax.tick_params(axis='y', labelcolor='r')
ax.axhline(sqrt(2)*dp_raw_Dummy, color='r')
fig_Dummy.tight_layout()
plt.show()
fig_Dummy.savefig('Dummy_idle.png')
###################################################

#data 100Hz STR
hz1_STR = loadmat(caminhos[5])
canal1_1hz_STR = hz1_STR['Channel_1_Data']
canal2_1hz_STR = hz1_STR['Channel_2_Data']
canal3_1hz_STR = hz1_STR['Channel_3_Data']
canal4_1hz_STR = hz1_STR['Channel_4_Data']
canal5_1hz_STR = hz1_STR['Channel_5_Data']
canal6_1hz_STR = hz1_STR['Channel_6_Data']
canal7_1hz_STR = hz1_STR['Channel_7_Data']
canal8_1hz_STR = hz1_STR['Channel_8_Data']
canal9_1hz_STR = hz1_STR['Channel_9_Data']
#data 4800Hz STR
hz48_STR = loadmat(caminhos[6])
canal1_48hz_STR = hz48_STR['Channel_1_Data']
canal2_48hz_STR = hz48_STR['Channel_2_Data']
dp_canal2_48Hz_STR = np.std(canal2_48hz_Dummy[40000:240000].ravel())
#gráficos Qualisys STR
qua_STR = loadmat(caminhos[7])
time_s_STR = qua_STR['time_s']
x_filled_mm_STR = qua_STR['x_filled_mm']
x_raw_mm_STR = qua_STR['x_raw_mm']
dp_filled_STR = np.std(x_filled_mm_STR[1200:5000].ravel())
dp_raw_STR = np.std(x_raw_mm_STR[1200:5000].ravel())

#STR graf
fig_STR, axs_STR = plt.subplots(2)

#axs_STR[0].set_ylabel('Canal6')
#axs_STR[0].plot(canal1_1hz_STR,canal6_1hz_STR)
#axs_STR[0].set_title('100Hz_STR')

#axs_STR[1].set_ylabel('canal1')
axs_STR[0].plot(canal1_48hz_STR[40000:240000],canal2_48hz_STR[40000:240000])
#axs_STR[0].axhline(sqrt(2)*dp_canal2_48Hz_STR)
axs_STR[0].set_title('S30_STR_A50_T0,80_R1_4800Hz')

axs_STR[1].set_xlabel('time_s')
axs_STR[1].set_ylabel('x_filled_mm_STR',color='b')
axs_STR[1].plot(time_s_STR[1200:5000],x_filled_mm_STR[1200:5000],'b')
axs_STR[1].axhline(sqrt(2)*dp_filled_STR)
axs_STR[1].set_title('S30_STR_A50_T0,80_R1_Qualisys')
axs_STR[1].tick_params(axis='y',labelcolor='b')

ax = axs_STR[1].twinx()
ax.set_ylabel('x_raw_mm_STR',color='r')
ax.plot(time_s_STR[1200:5000], x_raw_mm_STR[1200:5000], 'r')
ax.tick_params(axis='y', labelcolor='r')
ax.axhline(sqrt(2)*dp_raw_STR, color='r')
fig_STR.tight_layout()
fig_STR.savefig('STR_idle.png')


'''
#gráficos sem modelo

# nd.arrays para o plot
d = loadmat(caminhos[-1])
t0 = d['Channel_1_Data']
A0 = d['Channel_2_Data']
print('Entradas usadas(t,A): Channel_1_Data e Channel_2_Data','\n')

#não usar os primeiros 3000 pontos dos ndarray:
t = t0[3000:].ravel() # 'ndarray'[start:stop:step] : ou ,
A = A0[3000:].ravel() # 'ndarray'.ravel() passo o array pra 1D

dp = np.std(A.ravel())

# grafico A(t)
def graf():
    #plt.xlabel('t - canal 1')
    #plt.ylabel('A - canal 6')
    plt.plot(t,A,'r')
    #plt.axhline(y=sqrt(2)*dp)
    plt.show()

#   determinar a amplitude e periodo do sinal
#usando a função find_peaks() para pegar os indices dos picos
indices, _ = find_peaks(A) #sem esse ,_ não funciona (?)

#funções do np: mean-media; std-desvio padrão; var-variância; corrcoef-coeficiente de Person.
#amplitude
picos = A[indices]
media_A = np.mean(picos)
dp_A = np.std(picos)
var_A = np.var(picos)
CVP_A = np.corrcoef(picos)
#raiz de 2 vezes o dp(do sinal geral)
#periodo
def periodos():
    tempos = t[indices]
    Ts = []
    for i in range(len(tempos)-1):
        Ts.append(tempos[i+1]-tempos[i])
    return Ts
Ts = periodos()
media_T = np.mean(Ts)
dp_T = np.std(Ts)
var_T = np.var(Ts)
CVP_T = np.corrcoef(Ts)

#   resulados
print( 'Valores de amplitude e periodo e seu desvio padrão')
print( 'Média das Amplitudes:', media_A,', dp:', dp_A,
       '\nMédia dos Periodos:', media_T,', dp:', dp_T,'\n',
       'Amplitude:', sqrt(2)*dp) #desvio padrão do sinal * raiz de 2


'''
