# -*- coding: utf-8 -*-
"""
Created on Mon Aug 30 09:59:44 2021

@author: 2104998693
"""
import pandas as pd

imob_df1 = pd.read_excel(r'C:\Users\2104998693\Desktop\ViaVarejo\Python\IMOBILIARIO_GERENCIAL_(ATIVOS).xlsx', header=5)
imob_df2 = pd.read_excel(r'C:\Users\2104998693\Desktop\ViaVarejo\Python\IMOBILIARIO_GERENCIAL_(ENCERRADOS).xlsx', header=5)
imob_df3 = pd.read_excel(r'C:\Users\2104998693\Desktop\ViaVarejo\Python\Imobiliario_Gerencial_(Consolidado)_20201123.xlsx')

new_df = pd.concat([imob_df1, imob_df2, imob_df3]).drop_duplicates().reset_index(drop=True)
remove_cols = [col for col in new_df.columns if 'Unnamed' in col]
new_df.drop(remove_cols,axis='columns',inplace=True)
new_df.drop('REMOTO',axis='columns',inplace=True)

