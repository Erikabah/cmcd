# -*- coding: utf-8 -*-
"""
Created on Fri Mar 10 10:36:20 2023

@author: erika
"""

from tkinter import filedialog
# cod para funcionar para N arquivos

#1 abrir os arquivos e listar seus caminhos numa lista/tupla
arquivos = filedialog.askopenfilenames(title="Escolha um Arquivo") 
#DICIONARIO = executarFormatacaoDoArquivo(arquivos)
#2a identificar os arquivos que devem ser utilizados em conjunto e agrupar

#2b trabalhar com cada arquivo sem precisar agrupar 