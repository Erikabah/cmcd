# -*- coding: utf-8 -*-
"""
Created on Mon Feb 27 12:48:09 2023

@author: erika
"""
""

import matplotlib.pyplot as plt
from math import sqrt
import numpy as np
from scipy.io import loadmat
from scipy import signal

folder = "H:\\ic-loc\\ss7\\CMCD\\Dozap\\"
files = ["S30_DUMMY_A50_T0,80_R1","S30_DUMMY_A50_T0,80_R1_100Hz",
         "S30_DUMMY_A50_T0,80_R1_4800Hz",'S30_DUMMY_A50_T0,80_R1_Qualisys']
caminhos = []
for file in files:
    caminhos.append(folder+file+'.mat')
#arquivo com as informações do que é cada .mat
infos = open('Infos_Dummy.txt','w')
for file in caminhos:
    mat = loadmat(file)
    titulo = '\n\n\n'+str(file)+'\n'
    infos.write(titulo)
    for chave in mat.keys():
        info = '\n'+str(chave)+'\t'+str(type(mat[chave]))+'\ttamanho:'+str(len(mat[chave]))
        infos.write(info)
infos.close()


#data 4800Hz Dummy
hz48_Dummy = loadmat(caminhos[2])
canal1_48hz_Dummy = hz48_Dummy['Channel_1_Data']
canal2_48hz_Dummy = hz48_Dummy['Channel_2_Data']
dp_canal2_48Hz_Dummy = np.std(canal2_48hz_Dummy.ravel())

#Data Qualisys Dummy
qua_Dummy = loadmat(caminhos[3])
time_s_Dummy = qua_Dummy['time_s']

x_filled_mm_Dummy = qua_Dummy['x_filled_mm']
dp_filled_Dummy = np.std(x_filled_mm_Dummy.ravel())

x_raw_mm_Dummy = qua_Dummy['x_raw_mm']
dp_raw_Dummy = np.std(x_raw_mm_Dummy.ravel())

#Dummy graf
fig_Dummy, axs_Dummy = plt.subplots(3)

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

#Data_Qualisys pós filtro
#testes
N_Dummy = 4
Wn_Dummy = 0.1
b_D, a_D = signal.butter(N_Dummy,Wn_Dummy)
x_filled_mm_Dummy_filt = signal.filtfilt(b_D, a_D, x_filled_mm_Dummy.ravel())
dp_filled_Dummy_filt = np.std(x_filled_mm_Dummy.ravel())
x_raw_mm_Dummy_filt = signal.filtfilt(b_D, a_D, x_raw_mm_Dummy.ravel())
axs_Dummy[2].set_xlabel('time_s')
axs_Dummy[2].set_ylabel('x_filled_mm_Dummy_filt',color='m')
axs_Dummy[2].plot(time_s_Dummy[1200:5000],x_filled_mm_Dummy_filt[1200:5000],'m')
axs_Dummy[2].axhline(sqrt(2)*dp_filled_Dummy_filt)
axs_Dummy[2].set_title('x_filled_mm_Dummy Pós Filtro')
axs_Dummy[2].tick_params(axis='y', labelcolor='m' )

fig_Dummy.tight_layout()
#fig_Dummy.savefig('Dummy.png')


#data 100Hz Dummy
hz1_Dummy = loadmat(caminhos[1])
'''
canal1_1hz_Dummy = hz1_Dummy['Channel_1_Data']
canal2_1hz_Dummy = hz1_Dummy['Channel_2_Data']
canal3_1hz_Dummy = hz1_Dummy['Channel_3_Data']
canal4_1hz_Dummy = hz1_Dummy['Channel_4_Data']
canal5_1hz_Dummy = hz1_Dummy['Channel_5_Data']
canal6_1hz_Dummy = hz1_Dummy['Channel_6_Data']
canal7_1hz_Dummy = hz1_Dummy['Channel_7_Data']
canal8_1hz_Dummy = hz1_Dummy['Channel_8_Data']
canal9_1hz_Dummy = hz1_Dummy['Channel_9_Data']'''