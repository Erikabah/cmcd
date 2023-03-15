# -*- coding: utf-8 -*-
"""
Created on Fri Mar 10 10:36:20 2023

@author: erika
"""

import matplotlib.pyplot as plt
from math import sqrt
import numpy as np
from scipy.io import loadmat
from scipy import signal, optimize
from tkinter import filedialog
# cod para funcionar para N arquivos

#1 abrir os arquivos e listar seus caminhos numa lista/tupla
#caminhos = filedialog.askopenfilenames(title="Escolha um Arquivo")
caminhos = ("H:\\ic-loc\\ss7\\CMCD\\qua\\S30_DUMMY_A50_T0,80_R1_100Hz.MAT",
            "H:\\ic-loc\\ss7\\CMCD\\qua\\S30_DUMMY_A50_T0,80_R1_4800Hz.MAT",
            'H:\\ic-loc\\ss7\\CMCD\\qua\\S30_DUMMY_A50_T0,80_R1_Qualisys_2')
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

#2 identificar/diferenciar os arquivos - agrupar
#str_hbm = {}
#str_qua = {}
arquivos = [] #lista para fazer um compilado de todos os arqvs
def compilado(files):
    #arquivos = filedialog.askopenfilenames(title="Selecione Dummy hbm e qualisys")
    for caminho in files:
        dic = loadmat(caminho)#passa pra um dicionário todo conteúdo do arq
#se o arquivo for hbm - 100Hz
#Canais de interesse: 1, 8(mm) e 9(N)
        if 'Channel_9_Data' in dic:
            hbm = dict([('file', caminho),
                        ('t', dic['Channel_1_Data'] ),
                        ('x', dic['Channel_8_Data'] ),
                        ('f', dic['Channel_8_Data'] )])
            if 'DUMMY' in caminho:
                hbm['tipo'] = 'hbm_dummy'
            else:
                hbm['tipo']='hbm_str'
            arquivos.append(hbm)
#se o arquivo for qualisys
#Variáeis de interesse: time_s e x_filled_mm
        elif 'time_s' in dic:
            qua = dict([('file', caminho),
                        ('t', dic['time_s'] ),
                        ('x', dic['x_filled_mm'] )])
            if 'DUMMY' in caminho:
                hbm['tipo'] = 'qualisys_dummy'
            else:
                hbm['tipo']='qualisys_str'
            arquivos.append(qua)

compilado(caminhos)
