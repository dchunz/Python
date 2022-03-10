# -*- coding: utf-8 -*-
"""
Created on Tue Dec  7 08:41:16 2021

@author: 2104998693
"""

import pandas as pd
import seaborn as sns; sns.set()
import matplotlib.pyplot as plt
import numpy as np

import matplotlib
matplotlib.rcParams['figure.figsize'] = (16,8)

def consulta_bc(codigo_bcb):
  url = 'http://api.bcb.gov.br/dados/serie/bcdata.sgs.{}/dados?formato=json'.format(codigo_bcb)
  df = pd.read_json(url)
  df['data'] = pd.to_datetime(df['data'], dayfirst=True)
  df.set_index('data', inplace=True)
  return df

ipca = consulta_bc(433)

igpm = consulta_bc(189)

selic = consulta_bc(4390)

ipca_acumulado = np.cumprod((ipca/100) + 1)

igpm_acumulado = np.cumprod((igpm/100) + 1)

selic_acumulado = np.cumprod((selic/100) + 1)
selic_acumulado.reset_index(level=0, inplace=True)


fech_atual = pd.read_excel(r'C:\Users\2104998693\Desktop\Modelagem\Consolidado Modelagem 20_12_v1.xlsx')

fech_atual['MES_DATA_DISPENSA'] = pd.to_datetime(fech_atual['MES_DATA_DISPENSA'])
fech_atual['MES_DISTRIBUICAO'] = pd.to_datetime(fech_atual['MES_DISTRIBUICAO'])

fech_ipca_disp = pd.merge(fech_atual, ipca_acumulado, left_on = "MES_DATA_DISPENSA", right_on = "data", how = 'left')

fech_ipca_disp_dist = pd.merge(fech_ipca_disp, ipca_acumulado, left_on = "MES_DISTRIBUICAO", right_on = "data", how = 'left')


fech_ipca_selic = pd.merge(fech_ipca_disp_dist, selic_acumulado, left_on = "MES_DATA_DISPENSA", right_on = "data", how = 'left')

test = selic_acumulado.loc[selic_acumulado.data == "2021/09/01", "valor"]

test = test.reset_index()

fech_ipca_selic['Selic Setembro'] = test['valor'][0]

fech_ipca_selic.rename(
    columns=({'valor_x':'IPCA Dispensa', 'valor_y': 'IPCA Distribuição', 'valor':'Selic Dispensa'}), 
    inplace=True,)

fech_ipca_selic['Taxa IPCA'] = fech_ipca_selic['IPCA Distribuição'] / fech_ipca_selic['IPCA Dispensa']

fech_ipca_selic['Taxa Selic'] = fech_ipca_selic['Selic Setembro'] / fech_ipca_selic['Selic Dispensa']

fech_ipca_selic.to_excel(r'C:\Users\2104998693\Desktop\Modelagem\TesteSelicIPCA.xlsx', sheet_name='Consolidado', index = False)

