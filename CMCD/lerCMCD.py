# -*- coding: utf-8 -*-
"""
Created on Tue Mar  7 10:08:08 2023

@author: erika
"""
import matplotlib.pyplot as plt
from math import sqrt
import numpy as np
from scipy.io import loadmat
from scipy import signal, optimize
'''
import matplotlib.mlab as mlab
from tkinter import filedialog
from scipy.io import loadmat
'''
#pasta onde tá os arquivos e os arquivos (fora os primeiros 'R1.mat')
folder = "H:\\ic-loc\\ss7\\CMCD\\" # Mudar aqui o caminho!!
files =     ['commodelo\\S30_DUMMY_A100_T0,80_R1_100Hz.MAT',
             'commodelo\\S30_DUMMY_A100_T0,80_R1_4800Hz.MAT',
             'commodelo\\S30_DUMMY_A100_T0,80_R2_100Hz.MAT',
             'commodelo\\S30_DUMMY_A100_T0,80_R2_4800Hz.MAT',
             'commodelo\\S30_DUMMY_A100_T0,80_R3_100Hz.MAT',
             'commodelo\\S30_DUMMY_A100_T0,80_R3_4800Hz.MAT',
             'semmodelo\\S30_STR_A100_T0,80_R1_100Hz.MAT',
             'semmodelo\\S30_STR_A100_T0,80_R1_4800Hz.MAT',
             'semmodelo\\S30_STR_A100_T0,80_R2_100Hz.MAT',
             'semmodelo\\S30_STR_A100_T0,80_R2_4800Hz.MAT',
             'semmodelo\\S30_STR_A100_T0,80_R3_100Hz.MAT',
             'semmodelo\\S30_STR_A100_T0,80_R3_4800Hz.MAT',
             "qua\\S30_DUMMY_A50_T0,80_R1_100Hz.MAT",
             "qua\\S30_DUMMY_A50_T0,80_R1_4800Hz.MAT",
             'qua\\S30_DUMMY_A50_T0,80_R1_Qualisys.MAT',
             'qua\\S30_STR_A50_T0,80_R1_100Hz.MAT',
             'qua\\S30_STR_A50_T0,80_R1_4800Hz.MAT',
             'qua\\S30_STR_A50_T0,80_R1_Qualisys.MAT',
             'qua\\S30_DUMMY_A50_T0,80_R1_Qualisys_2']
caminhos = []
for file in files:
    caminhos.append(folder+file)
    #caminho de todos arquivos que foram mandados até agora
#alternativa para pegar os arquivos:
#caminhos = filedialog.askopenfilenames(title="Escolha um Arquivo") 
    
#Dozap - qualisys e 100Hz para as comparações
#usando o loadmat para ter os arquivos .MAT como dic

#series com modelo 100Hz
dummy_hbm = loadmat(caminhos[12])
t_dummy_hbm = dummy_hbm['Channel_1_Data'].ravel()
x_dummy_hbm = dummy_hbm['Channel_8_Data'].ravel()
A_x_dummy_hbm = np.std(x_dummy_hbm)*sqrt(2)
f_dummy_hbm = dummy_hbm['Channel_9_Data'].ravel()
dummy_qua0 = loadmat(caminhos[14])
#series com modelo qualisys
dummy_qua = loadmat(caminhos[18])
t_dummy_qua = dummy_qua['time_s'].ravel()
x_dummy_qua = dummy_qua['x_filled_mm'].ravel()
A_x_dummy_qua = np.std(x_dummy_qua)*sqrt(2)
#series sem modelo 100Hz 
str_hbm = loadmat(caminhos[15])
t_str_hbm = str_hbm['Channel_1_Data'].ravel()
x_str_hbm = str_hbm['Channel_8_Data'].ravel()
f_str_hbm = str_hbm['Channel_9_Data'].ravel()
#series sem modelo qualisys
str_qua = loadmat(caminhos[17])
t_str_qua = str_qua['time_s'].ravel()
x_str_qua = str_qua['x_filled_mm'].ravel()

N = 4 #The order of the filter.
Wn = 0.1 #The critical frequency or frequencies.
#scipy.signal.butter(N, Wn, btype='low', analog=False, output='ba', fs=None)
b, a = signal.butter(N,Wn)
#Numerator (b) and denominator (a) polynomials of the IIR filter.
x_dummy_hbm_filt = signal.filtfilt(b, a, x_dummy_hbm)
x_dummy_qua_filt = signal.filtfilt(b, a, x_dummy_qua)

x_str_hbm_filt = signal.filtfilt(b, a, x_str_hbm)
x_str_qua_filt = signal.filtfilt(b, a, x_str_qua)

#   determinar a amplitude e periodo do sinal
#usando a função find_peaks() para pegar os indices dos picos
i_dummy_hbm, _ = signal.find_peaks(x_dummy_hbm_filt) #sem esse ,_ não funciona (?)
picos_dummy_hbm = x_dummy_hbm_filt[i_dummy_hbm]
t_picos_dummy_hbm = t_dummy_hbm[i_dummy_hbm]

i_dummy_qua, _ = signal.find_peaks(x_dummy_qua_filt)
picos_dummy_qua = x_dummy_hbm_filt[i_dummy_qua]
t_picos_dummy_qua = t_dummy_qua[i_dummy_qua]

#defasagem dummy - diferença entre o tempo dos picos - com média dos valores
#dif_crua = t_picos_dummy_hbm-t_picos_dummy_qua
#mean_dif = np.mean(dif_crua)
#diferença dos picos
#delta_t = t_picos_dummy_hbm[:-2]-t_picos_dummy_qua[2:]
#mean_delta_t = np.mean(delta_t)

#defasagem str
i_str_hbm, _ = signal.find_peaks(x_str_hbm_filt)
picos_str_hbm = x_dummy_hbm_filt[i_str_hbm]
t_picos_str_hbm = t_str_hbm[i_str_hbm]

i_str_qua, _ = signal.find_peaks(x_str_qua_filt)
picos_str_qua = x_dummy_hbm_filt[i_str_qua]
t_picos_str_qua = t_str_qua[i_str_qua]

#derivando o movimento - ponto por ponto h=t1-t0
#v = (x1-x0)/h
v_dummy_hbm = []
v_dummy_qua = []
v_str_hbm = []
v_str_qua = []
# a = (v1-v0)/h
a_dummy_hbm = []
a_dummy_qua = []
a_str_hbm = []
a_str_qua = []
h=0.01
for n in range(len(x_dummy_hbm_filt)-1):#para velocidade
    vdh = (x_dummy_hbm_filt[n+1] - x_dummy_hbm_filt[n]) / h
    v_dummy_hbm.append(vdh)
    
    vdq = (x_dummy_qua_filt[n+1] - x_dummy_qua_filt[n]) / h
    v_dummy_qua.append(vdq)
    
    vsh = (x_str_hbm_filt[n+1] - x_str_hbm_filt[n]) / h
    v_str_hbm.append(vsh)
    
    vsq = (x_str_qua_filt[n+1] - x_str_qua_filt[n]) / h
    v_str_qua.append(vsq)
 
for n in range(len(v_dummy_hbm)-1):#para aceleração
    adh = (v_dummy_hbm[n+1] - v_dummy_hbm[n]) / h
    a_dummy_hbm.append(adh)
        
    adq = (v_dummy_qua[n+1] - v_dummy_qua[n]) / h
    a_dummy_qua.append(adq)
        
    ash = (v_str_hbm[n+1] - v_str_hbm[n]) / h
    a_str_hbm.append(ash)
        
    asq = (v_str_qua[n+1] - v_str_qua[n]) / h
    a_str_qua.append(asq)
'''
#derivando usando numpy.polyfit(x,y,3) para ter uma função derivável
coef = np.polyfit(x=t_dummy_hbm.ravel(), y=x_dummy_hbm_filt, deg=3)

#integrando para v e a com a função abaixo e comparar com o de cima
#scipy.misc.derivative(func, x0, dx=1.0, n=1, args=(), order=3)
def func( var = x_dummy_hbm_filt[0]):
    result = coef[0]*var**3 + coef[1]*var**2 + coef[2]*var + coef[3]
    return result
for i in x_dummy_hbm_filt:
    v_dummy_hbm = scipy.misc.derivative(func,i)
#o mesmo para aceleração
'''
#integrar a série de Força - RK4?
'''
com v e a: 
scipy.optimize.curve_fit(f, xdata, ydata, p0=None, sigma=None,
                         absolute_sigma=False, check_finite=True,
                         bounds=(-inf, inf), method=None, jac=None, *,
                         full_output=False, **kwargs)'''
L = .45 #?
D = .04 #?
rho = 998 #?
A = 50 #amplitude - do arq ou calculada?
T = 0.8 #período - do arq ou calculada?
w = 2*np.pi/T
def eq(x , CD, CA):
    v,ac = x
    termo1 = round(-.5*rho*L*D,3)
    termo2 = round(-rho*np.pi*(D**2)/(4*L),3)
    return CD*termo1*v*abs(v) + CA*termo2*ac

#pra achar coeficientes de uma série com optimize
f = f_dummy_hbm[:5998]
vel = np.array(v_dummy_hbm[:5998])
acel = np.array(a_dummy_hbm)
popt,pcov = optimize.curve_fit(eq,(vel,acel),f)
cd_top_fit = popt[0];
cm_top_fit = popt[1];

# pro coeficiente de determinação
residuals = f - eq((vel,acel), *popt)
ss_res = np.sum(residuals**2)
ss_tot = np.sum((f_dummy_hbm-np.mean(f_dummy_hbm))**2)
r_squared = 1 - (ss_res / ss_tot)

#Gráficos
fig_dummy, axs_dummy = plt.subplots()

axs_dummy.set_title('S30_DUMMY_A50_T0,80_R1')
axs_dummy.set_xlabel('time_s')
axs_dummy.set_ylabel('x_mm_dummy',color='b')
axs_dummy.plot(t_dummy_hbm,x_dummy_hbm_filt,'b', label='hbm')
axs_dummy.plot(t_dummy_qua, x_dummy_qua_filt, 'r', label='qualisys')
axs_dummy.legend()
axs_dummy.tick_params(axis='y',labelcolor='b')
axs_dummy.axhline(A_x_dummy_hbm, color = 'm')
axs_dummy.axhline(A_x_dummy_qua, color = 'g')
plt.show()

fig_str, axs_str = plt.subplots()

axs_str.set_title('S30_STR_A50_T0,80_R1')
axs_str.set_xlabel('time_s')
axs_str.set_ylabel('x_str_hbm',color='b')
axs_str.plot(t_str_hbm,x_str_hbm_filt,'b')
axs_str.tick_params(axis='y',labelcolor='b')

ax2 = axs_str.twinx()
ax2.set_ylabel('x_str_qualisys',color='r')
ax2.plot(t_str_qua, x_str_qua_filt, 'r')
ax2.tick_params(axis='y', labelcolor='r')
plt.show()

'''
#Textos pra ajudar a localizar as variáveis
infos_commodelo = open('Infos_sm.txt','w', encoding= 'utf-8')
infos_semmodelo = open('Infos_cm.txt','w', encoding= 'utf-8')
infos_Dozap = open('Infos_dozap.txt','w', encoding= 'utf-8')

for file in caminhos[0:6]:
    mat1 = loadmat(file)#cria um dicionario com o arquivo
    #as chaves são as vaiáveis e os valores o conteúdo da variável
    titulo = '\n\n\n'+str(file)+'\n'
    infos_commodelo.write(titulo)
    #header = mat['__header__']
    #infos_commodelo.write(str(header))
    for chave in mat1.keys():
        info1 = '\n'+str(chave)+'\t'+str(type(mat1[chave]))
        #para entender o que tem em cada arquivo e qual variável preciso usar
        info2 = '\n\ttamanho:'+str(len(mat1[chave]))
        if len(mat1[chave])<80:
            info3 = mat1[chave]
            info3 = '\n'+str(info3)
            info = info1+info2+info3
        else:
            info = info1+info2
        infos_commodelo.write(info)
infos_commodelo.close()
#informações com os arquivos com modelo

for arq1 in caminhos[6:12]:
    mat2 = loadmat(arq1)
    titulo = '\n\n\n'+str(arq1)+'\n'
    infos_semmodelo.write(titulo)
    #header = mat['__header__']
    #infos_commodelo.write(str(header))
    for chave in mat2.keys():
        info1 = '\n'+str(chave)+'\t'+str(type(mat2[chave]))
        info2 = '\n\ttamanho:'+str(len(mat2[chave]))
        if len(mat2[chave])<80:
            info3 = mat2[chave]
            info3 = '\n'+str(info3)
            info = info1+info2+info3
        else:
            info = info1+info2
        infos_semmodelo.write(info)
infos_semmodelo.close()
#informações com os arquivos sem modelo

for arq2 in caminhos[12:]:
    mat2 = loadmat(arq2)
    titulo = '\n\n\n'+str(arq2)+'\n'
    infos_Dozap.write(titulo)
    #header = mat['__header__']
    #infos_commodelo.write(str(header))
    for chave in mat2.keys():
        info1 = '\n'+str(chave)+'\t'+str(type(mat2[chave]))
        info2 = '\n\ttamanho:'+str(len(mat2[chave]))
        if len(mat2[chave])<80:
            info3 = mat2[chave]
            info3 = '\n'+str(info3)
            info = info1+info2+info3
        else:
            info = info1+info2
        infos_Dozap.write(info)
infos_Dozap.close()
#informações com os últimos arquivos mandados - sobre o qualisys
'''