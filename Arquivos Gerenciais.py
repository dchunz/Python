# -*- coding: utf-8 -*-
"""
Created on Mon Sep 20 11:48:18 2021

@author: 2104998693
"""
import pandas as pd

civest1 = pd.read_excel(r'C:\Users\2104998693\Desktop\Bases diáriais\CIVEL_GERENCIAL_ESTRATEGICO_(ATIVOS).xlsx',header=5)
civest2 = pd.read_excel(r'C:\Users\2104998693\Desktop\Bases diáriais\CIVEL_GERENCIAL_ESTRATEGICO_(ENCERRADOS).xlsx',header=5)

civ_df = pd.concat([civest1, civest2],ignore_index=True)

civ_df.to_excel(r'C:\Users\2104998693\Desktop\Bases diáriais\CIVEL_GERENCIAL_ESTRATEGICO_(CONSOLIDADO).xlsx', sheet_name='Consolidado', index = False)

reg1 = pd.read_excel(r'C:\Users\2104998693\Desktop\Bases diáriais\REGULATORIO_GERENCIAL_(ATIVOS).xlsx',header=5)
reg2 = pd.read_excel(r'C:\Users\2104998693\Desktop\Bases diáriais\REGULATORIO_GERENCIAL_(ENCERRADOS).xlsx',header=5)

reg_df = pd.concat([reg1, reg2],ignore_index=True)
reg_df.to_excel(r'C:\Users\2104998693\Desktop\Bases diáriais\REGULATORIO_GERENCIAL_(CONSOLIDADO).xlsx', sheet_name='Consolidado', index = False)

trab1 = pd.read_excel(r'C:\Users\2104998693\Desktop\Bases diáriais\TRABALHISTA_GERENCIAL_(ATIVOS).xlsx',header=5)
trab2 = pd.read_excel(r'C:\Users\2104998693\Desktop\Bases diáriais\TRABALHISTA_GERENCIAL_(ENCERRADOS).xlsx',header=5)

trab_df = pd.concat([trab1, trab2],ignore_index=True)
trab_df.to_excel(r'C:\Users\2104998693\Desktop\Bases diáriais\TRABALHISTA_GERENCIAL_(CONSOLIDADO).xlsx', sheet_name='Consolidado', index = False)
