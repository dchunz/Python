# -*- coding: utf-8 -*-
"""
Created on Wed Sep  1 10:08:21 2021

@author: -
"""
import pandas as pd
from pandasql import sqldf

pysqldf = lambda q: sqldf(q, globals())

imob = pd.read_excel(r'Z:\01 PLANEJ FINANCEIRO JURIDICO\137.ANALYTICS\2 FECHAMENTO\Consolidado\Imobiliário Consolidado.xlsx')

garantias = pd.read_excel(r'Z:\01 PLANEJ FINANCEIRO JURIDICO\137.ANALYTICS\2 FECHAMENTO\Consolidado\Tratamento Garantias.xlsx',header=5)
garantias.dropna(how='all')

#hist_pag = pd.read_excel(r'Z:\jurcivel\FECHAMENTO\00.Planejamento Jurídico\03.Pagamentos\01.Hist_Pag\HISTORIO_DE-PAGAMENTOS_20210823.xlsx')
#hist_pag.dropna(how='all')

#q = '''
#SELECT *
#FROM imob i
#LEFT JOIN garantias g ON i.ProcessoID = g.IDProcesso
#WHERE i.data = g.Data Efetiva do Pagamento

#'''
#joined = pysqldf(q)
