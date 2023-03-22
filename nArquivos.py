# -*- coding: utf-8 -*-
"""
Created on Fri Mar 10 10:36:20 2023

@author: erika
"""

from math import sqrt
from tkinter import filedialog
import matplotlib.pyplot as plt
import numpy as np
from scipy import signal, optimize
from scipy.io import loadmat

# cod para funcionar para N arquivos

#Variáveis
L = .45
D = .04
rho = 998
A = 50
T = .8
w = 2*np.pi/T

arquivos = [] #lista para fazer um compilado de todos os arqvs
grupos = []

#3 funções utilizadas nos arquivos
def filtrar(serie): #f serie crua pra serie filtrada
    N = 4 #ordem do filtro
    Wn = 0.1 #frequência critica?
    b, a = signal.butter(N,Wn) #numerador e denominador
    return signal.filtfilt(b, a, serie, padlen = 0) 

def picos(tempo, position): # f retorna os tempos que acontece os picos e periodo
    ind,_ = signal.find_peaks(position) #pega os ind dos picos
    difer = np.ediff1d(tempo[ind]) #tempo[1:] - tempo[:-1]
    Periodo = np.mean(difer) # média das diferenças
    return tempo[ind], Periodo
    
def derivar(position): #der a serie de posição pra pegar vel e acel
    h = 0.01 #t1-t0
    velocidade = []
    acel = []
    for i in range(len(position)-1): #det velocidade
        # v = (x1-x0)/ h
        v = (position[i+1] - position[i]) / h
        velocidade.append(v)
    for i in range(len(velocidade)-1):#det acel
        # a = (v1 - v0)/ h
        a = ( velocidade[i+1] - velocidade[i] )/ h
        acel.append(a)
    return position[:-2], np.array(velocidade[:-1]), np.array(acel)

def eq(vars, CD, CA): #det a equação usada pra achar os coef
    v,ac = vars
    termo1 = round(-.5*rho*L*D,3)
    termo2 = round(-rho*np.pi*(D**2)/(4*L),3)
    return CD*termo1*v*abs(v) + CA*termo2*ac

def coeficientes(force,velocidade,acel): #det os coeficientes cm e cd
    if len(force)==len(acel) and len(velocidade)==len(acel):
        popt, pcov = optimize.curve_fit(eq, (velocidade,acel), force)
        cd = popt[0];
        cm = popt[1];
        # pro coeficiente de determinação
        residuals = force - eq((velocidade,acel), *popt)
        ss_res = np.sum(residuals**2)
        ss_tot = np.sum((force-np.mean(force))**2)
        r_squared = 1 - (ss_res / ss_tot)
        return cd, cm , r_squared
    else:
        print('As séries não tem o mesmo tamanho')
        return 'erro', 'erro', 'erro'
   
#1 abrir os arquivos e listar seus caminhos numa lista/tupla

caminhos = filedialog.askopenfilenames()
#root=tk.Tk()
#root.mainloop()
'''
caminhos =   ('H:\\ic-loc\\ss7\\CMCD\\commodelo\\S30_DUMMY_A100_T0,80_R1_100Hz.MAT',
             'H:\\ic-loc\\ss7\\CMCD\\commodelo\\S30_DUMMY_A100_T0,80_R1_4800Hz.MAT',
             'H:\\ic-loc\\ss7\\CMCD\\commodelo\\S30_DUMMY_A100_T0,80_R2_100Hz.MAT',
             'H:\\ic-loc\\ss7\\CMCD\\commodelo\\S30_DUMMY_A100_T0,80_R2_4800Hz.MAT',
             'H:\\ic-loc\\ss7\\CMCD\\commodelo\\S30_DUMMY_A100_T0,80_R3_100Hz.MAT',
             'H:\\ic-loc\\ss7\\CMCD\\commodelo\\S30_DUMMY_A100_T0,80_R3_4800Hz.MAT',
             'H:\\ic-loc\\ss7\\CMCD\\semmodelo\\S30_STR_A100_T0,80_R1_100Hz.MAT',
             'H:\\ic-loc\\ss7\\CMCD\\semmodelo\\S30_STR_A100_T0,80_R1_4800Hz.MAT',
             'H:\\ic-loc\\ss7\\CMCD\\semmodelo\\S30_STR_A100_T0,80_R2_100Hz.MAT',
             'H:\\ic-loc\\ss7\\CMCD\\semmodelo\\S30_STR_A100_T0,80_R2_4800Hz.MAT',
             'H:\\ic-loc\\ss7\\CMCD\\semmodelo\\S30_STR_A100_T0,80_R3_100Hz.MAT',
             'H:\\ic-loc\\ss7\\CMCD\\semmodelo\\S30_STR_A100_T0,80_R3_4800Hz.MAT',
             "H:\\ic-loc\\ss7\\CMCD\\qua\\S30_DUMMY_A50_T0,80_R1_100Hz.MAT",
             "H:\\ic-loc\\ss7\\CMCD\\qua\\S30_DUMMY_A50_T0,80_R1_4800Hz.MAT",
             'H:\\ic-loc\\ss7\\CMCD\\qua\\S30_DUMMY_A50_T0,80_R1_Qualisys.MAT',
             'H:\\ic-loc\\ss7\\CMCD\\qua\\S30_STR_A50_T0,80_R1_100Hz.MAT',
             'H:\\ic-loc\\ss7\\CMCD\\qua\\S30_STR_A50_T0,80_R1_4800Hz.MAT',
             'H:\\ic-loc\\ss7\\CMCD\\qua\\S30_STR_A50_T0,80_R1_Qualisys.MAT',
             'H:\\ic-loc\\ss7\\CMCD\\qua\\S30_DUMMY_A50_T0,80_R1_Qualisys_2')
'''
#2 identificar os arquivos
def compilado(files):
    #arquivos = filedialog.askopenfilenames(title="Selecione Dummy hbm e qualisys")
    for caminho in files:
        dic = loadmat(caminho)#passa pra um dicionário todo conteúdo do arq
        nome = caminho.rpartition('/')[2]
        if 'Qualisys' in nome:
            file = dict([('name', nome),
                        ('t', dic['time_s']),
                        ('x', dic['x_filled_mm'])])
            arquivos.append(file)

        elif '4800Hz' in nome:
            continue
            #file = dict([('name', nome),
             #           ('t', dic['Channel_1_Data']),
             #           ('x', dic['Channel_2_Data'])])
            #arquivos.append(file)
    
        elif '100Hz' in nome:
            file = dict([('name',nome)])
            for n in range(17):
                key = 'Channel_{}_Data'.format(n)
                if n == 1:
                    file['t'] = dic[key]
                elif n == 8:
                    file['x'] = dic[key]
                elif n == 9:
                    file['f'] = dic[key]
                else:
                    continue
            arquivos.append(file)
        else:
            continue

def aplicarFunc (compilado_arquivos):
    
    for file in compilado_arquivos:
        
         # det x filtrado
        file['x_filt'] = filtrar(file['x'])
        picos_t, Periodo  = picos( file['t'], file['x_filt'].ravel() )
        file['picos_t'] = picos_t
        file['Periodo'] = Periodo
        
        dp = np.std(file['x_filt'])
        file['Amplitude'] = sqrt(2)*dp
        
        x, v, a = derivar(file['x_filt'].ravel())
        #file['x_filt'] = x
        
        if 'f' in file:
            cd, cm, r_squared = coeficientes(file['f'][:-2], v, a)
            file['cd'] = cd
            file['cm'] = cm
            file['r_squared'] = r_squared

#aplicarFunc(arquivos)

def agrupar(files):
    for n in range():
        Rn = 'R{}'.format(n)
        mesmo_Rn = dict()
        for file in files:
            if Rn in file['name'] and 'DUMMY' in file['name']:
                key = 'DUMMY_' + file['name'].rpartition('_')[2][:-4]
                mesmo_Rn[key] = file
            elif Rn in file['name'] and 'STR' in file['name']:
                key = 'STR_' + file['name'].rpartition('_')[2][:-4]
                mesmo_Rn[key] = file
            else:
                continue
        grupos[Rn] = mesmo_Rn

def comparar2(grupos):
    for Rn in grupos:
        
        fig1, ax = plt.subplots()
        S = [Rn['STR_100Hz'],Rn['STR_Qualisys']]
        ax.set_xlabel('time_s',color='b')
        ax.set_ylabel('STR_x',color='b')
        ax.set_title('{} STR - 100Hz e Qualisys'.format(Rn))
        ax.plot(S[0]['t'], S[0]['x_filt'], 'g',
                S[1]['t'], S[1]['x_filt'], 'b')
        
        nome_figura = 'STR_{}.png'.format(Rn)
        fig1.savefig(nome_figura)

        fig2, axs = plt.subplots(2)
        D = [ Rn['DUMMY_100Hz'], Rn['DUMMY_Qualisys'], Rn['DUMMY_2']]
        axs[0].set_xlabel('time_s',color='b')
        axs[0].set_ylabel('DUMMY_x',color='b')
        axs[0].set_title('{} DUMMY - 100Hz, Qualisys e Qualisys_2'.format(Rn))
        axs[0].plot(D[0]['t'], D[0]['x_filt'], 'g',
                    D[1]['t'], D[1]['x_filt'], 'b',
                    D[2]['t'], D[2]['x_filt'], 'm' )
        axs[1].set_xlabel('time_s',color='b')
        axs[0].set_ylabel('DUMMY_x',color='b')
        axs[0].set_title('{} DUMMY - 100Hz e Qualisys_2'.format(Rn))
        axs[0].plot(D[0]['t'], D[0]['x_filt'], 'b',
                    D[2]['t'], D[2]['x_filt'], 'm' )
        nome_figura = 'DUMMY_{}.png'.format(Rn)
        fig2.savefig(nome_figura)
        
        
def delay(picos_t1, picos_t2): #determinar a defasagem entre 2 series
    if len(picos_t1)==len(picos_t2):
        diff = picos_t1 - picos_t2 #delta_t
        return diff, np.mean(diff)
    else:
        mensagem = ['Um tem mais picos que o outro\n']
        print(mensagem)
        return 'erro'

def comparar (hbm, qua):
    
    difers, mean = delay(hbm['picos_t'],qua['picos_t'])
    
    fig, ax = plt.subplots()
    title = '{1} and {2}'.format_map({'1':hbm['name'],'2':qua['name']})
    ax.set_title(title)
    ax.set_xlabel('time_s')
    ax.set_ylabel('Posições')
    leg1 = '{1}; CD:{2}, CM:{3}, R²:{4}'.format_map({'1':hbm['tipo'],
                                                     '2':hbm['cd'],'3':hbm['cm'],
                                                     '4':hbm['r_squared']})
    leg2 = '{1}; delta_t:{2}'.format_map({'1':qua['tipo'],
                                         '2':mean})
    
    ax.plot(hbm['t'], hbm['x_filt'],'b', label = leg1 )
    ax.plot(qua['t'], qua['x_filt'],'g', label = leg2 )
    ax.legend()
    ax.tick_params()
    fig.savefig('defasagem = {}'.format(mean))    
    plt.show()
    
compilado(caminhos)
aplicarFunc(arquivos)
agrupar(arquivos)
comparar2(grupos)

'''
def iniciar():

    print('Escolha 2 arquivos da lista, um 100Hz e um arquivo Qualisys para fazer a comparação')
    n = 0
    for file in arquivos:
        print('{} {}'.format(n, file['name']))
        n+=1
    
    escolha_hbm = int(input('Arquivo hbm:'))
    pegar_hbm = arquivos[escolha_hbm]
    escolha_qua = int(input('Arquivo Qualisys:'))
    pegar_qua = arquivos[escolha_qua]
    if escolha_qua == escolha_hbm or 'f' not in pegar_hbm or 'f' in pegar_qua:
        print('Esse par não funciona')
        return iniciar()
    else:
        comparar(pegar_hbm, pegar_qua)
        print('Figura salva')

iniciar()
'''     
        