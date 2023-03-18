
import matplotlib.pyplot as plt
from math import sqrt
import numpy as np
from scipy.io import loadmat
from scipy import signal
from scipy.signal import find_peaks

#   o arquivo
folderS_STR = 'H:\\ic-loc\\ss7\\CMCD\\semmodelo\\S30_STR_A100_T0,80_'
folderC_DUMMY = 'H:\\ic-loc\\ss7\\CMCD\\commodelo\\S30_DUMMY_A100_T0,80_'
folder = [folderS_STR , folderC_DUMMY]
file = ['R1_100Hz.MAT','R1_4800Hz.MAT',
        'R2_100Hz.MAT','R2_4800Hz.MAT',
        'R3_100Hz.MAT','R3_4800Hz.MAT']
caminhos = []
for pasta in folder:
    for arquivo in file:
        caminho = pasta + arquivo
        caminhos.append(caminho)
#arquivo com as informações de cada .MAT
infos = open('Infos_lerSS7.txt','w')
for f in caminhos:
    d = loadmat(f)
    info1 = '\n\nArquivo:'+str(f)+'\nDados:'
    infos.write(info1)
    for key in d.keys():
        info = '\n'+str(key)+'\t'+str(type(d[key]))+'\ttamanho:'+str(len(d[key]))
        infos.write(info)
infos.close()    

# nd.arrays para o plot
KC = [] #Keulegan-Carpenter number 2pi*amplitude/diametro
for f in caminhos:   
    d = loadmat(f)
    t0 = d['Channel_1_Data']
    A0 = d['Channel_2_Data']
    #não usar os primeiros 3000 pontos dos ndarray:
    t = t0[3000:].ravel() # 'ndarray'[start:stop:step] : ou ,
    A = A0[3000:].ravel() # 'ndarray'.ravel() passo o array pra 1D
    dp = np.std(A.ravel()) #std-desvio padrão
    amplitude = sqrt(2)*dp #raiz de 2 vezes o dp(do sinal geral)
    diametro = 1
    KC.append(2*np.pi*amplitude/diametro)
    #print('Entradas usadas(t,A): Channel_1_Data e Channel_2_Data','\n')
    plt.plot(t,A,'r')
    plt.show()
print(KC)

#para o filtro Butterworth de 4ª ordem
#b, a = scipy.signal.butter(N = 4, Wn, #ba-numeador/denominador
#                           btype='low',analog = False,
#                           output='ba', fs=None)
#N: 'int ordem do filtro (4a ordem?)'
#Wn: 'array_like, critical frequency or frequencies-5*frequência de excitação'

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
#dp_A = np.std(picos)
#var_A = np.var(picos)
#CVP_A = np.corrcoef(picos)

'''
A média - {ainda que considerada como um número
que tem a faculdade de representar uma série de valores -
não pode, por si mesma, destacar o grau de homogeneidade
ou heterogeneidade que existe entre os valores que compõem o conjunto.}
'''

'''
fs: the sampling frequency of the digital system - frequência de excitação
# Specifications of Filter
 # sampling frequency - frequencia de excitação
f_sample = 40000 
# pass band frequency
f_pass = 4000  
# stop band frequency
f_stop = 8000  
# pass band ripple - 
fs = 0.5 #pass/stop = 4000/8000
# pass band freq in radian
wp = f_pass/(f_sample/2)  
# stop band freq in radian
ws = f_stop/(f_sample/2) 
# Sampling Time - periodo
Td = 1  
 # pass band ripple 
g_pass = 0.5 
# stop band attenuation
g_stop = 40
'''