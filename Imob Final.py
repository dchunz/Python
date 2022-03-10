# -*- coding: utf-8 -*-
"""
Created on Mon Aug 30 09:01:10 2021

@author: 2104998693
"""
import pandas as pd
#importar a biblioteca pandas para manipulação das bases

Imob = pd.read_excel(r'C:\Users\2104998693\.spyder-py3\Imobiliário Consolidado.xlsx')
Imob.rename(
    columns=({'ID PROCESSO':'(Processo) ID', 'PASTA':'Pasta'}), 
    inplace=True,)
#Importar a base do Imobiliário Consolidada

imob_df1 = pd.read_excel(r'C:\Users\2104998693\Desktop\ViaVarejo\Python\IMOBILIARIO_GERENCIAL_(ATIVOS).xlsx', header=5)
imob_df2 = pd.read_excel(r'C:\Users\2104998693\Desktop\ViaVarejo\Python\IMOBILIARIO_GERENCIAL_(ENCERRADOS).xlsx', header=5)
imob_df3 = pd.read_excel(r'C:\Users\2104998693\Desktop\ViaVarejo\Python\Imobiliario_Gerencial_(Ativos)-20201020.xlsx')
imob_df4 = pd.read_excel(r'C:\Users\2104998693\Desktop\ViaVarejo\Python\Imobiliario_Gerencial_(Encerrados)-20201020.xlsx')
#Importar as bases gerenciais de 2021 e 2020

new_df = pd.concat([imob_df1, imob_df2, imob_df3, imob_df4]).drop_duplicates().reset_index(drop=True)
#Empilhar as bases gerenciais em uma base consolidada e remover duplicatas

remove_cols = [col for col in new_df.columns if 'Unnamed' in col]
new_df.drop(remove_cols,axis='columns',inplace=True)
drop_columns = (['REMOTO', 'POSSÍVEL', 'PROVÁVEL', 'Filial', 'Data de Cadastro', 'Status', 'Grupo', 'Centro de Custo / Área Demandante - Código', ''])
new_df.drop(drop_columns ,axis='columns',inplace=True)
#Remover colunas sem nome e colunas de 2020 obsoletas

imob_merged = pd.merge(Imob, new_df, how='left', on='(Processo) ID', suffixes=('', '_drop'))
imob_merged.drop([col for col in imob_merged.columns if 'drop' in col], axis=1, inplace=True)
#Fazer um Left Join para a criação de uma base mais completa
#Definir como _drop os colunas duplicadas entre os dois datasets e manter apenas as colunas originais da base de fechamento

imob_merged.to_excel('Final Imobiliário.xlsx', index=False)
#Exportar o arquivo final para excel