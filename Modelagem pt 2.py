# -*- coding: utf-8 -*-
"""
Created on Thu Dec 23 10:33:17 2021

@author: 2104998693
"""

import pandas as pd
import numpy as np

fech_atual = pd.read_excel(r'C:\Users\2104998693\Desktop\Modelagem\Consolidado Modelagem 07_03.xlsx')
fech_anterior = pd.read_excel(r'Z:\01 PLANEJ FINANCEIRO JURIDICO\137.ANALYTICS\10 Modelagem Trabalhista\2022\02.Fevereiro\Fechamento 16-02\AutomacaoFevereiro2102.xlsx', header=1)

fech_atual['MES_DATA_DISPENSA'] = pd.to_datetime(fech_atual['MES_DATA_DISPENSA'])
fech_atual['MES_DISTRIBUICAO'] = pd.to_datetime(fech_atual['MES_DISTRIBUICAO'])


fech_anterior.rename(
    columns=({'Cluster Aging':'Cluster Aging_anterior', 'prediction':'prediction_anter', 'Indexador IPCA': 'Indexador IPCA_anterior',
              'Indexador SELIC': 'Indexador SELIC_anterior', 'MES_DATA_DISPENSA': 'MES_DATA_DISPENSA_anterior', 'DISTRIBUICAO':'DISTRIBUICAO_anterior',
              'Valor de Modelagem Indexado':'Valor de Modelagem Indexado_anterior',
              #'FASE PROCESSUAL - Dez-21': 'FASE PROCESSUAL_anterior',
              #revisar a linha de cima!
              'Valor Final': 'Valor Final_ant'}), 
    inplace=True,)

dfNew = pd.merge(fech_atual, fech_anterior[['ID PROCESSO', 'Cluster Aging_anterior', 'prediction_anter', 'Indexador IPCA_anterior',
                                            'Indexador SELIC_anterior', 'MES_DATA_DISPENSA_anterior',
                                            'DISTRIBUICAO_anterior', 'Valor de Modelagem Indexado_anterior',
                                            'Tipo cálculo - Fev-22', 'Valor cálculo - Fev-22']]
                                             #revisar ultima linha quando mudar o mês
                 , on = "ID PROCESSO", how='left', suffixes=('', '_DROP')).filter(regex='^(?!.*_DROP)')





dfNew['Elegível'] = np.where((dfNew['Natureza Operacional (M)'] == "SINDICATO / MINISTERIO PUBLICO") & (dfNew['Sub-área do Direito']=="AUDIÊNCIAS 100% FK"), "Não", 
                             np.where((dfNew['Natureza Operacional (M)'] == "ADMINISTRATIVO") & ( dfNew['Sub-área do Direito']=="CONTENCIOSO INDIVIDUAL")
                                      , "Não", np.where((dfNew['Natureza Operacional (M)'] == "SINDICATO / MINISTERIO PUBLICO") & ( dfNew['Sub-área do Direito']=="CONTENCIOSO INDIVIDUAL")
                                                         , "Não", np.where((dfNew['Natureza Operacional (M)'] == "TERCEIRO SOLVENTE") & ( dfNew['Sub-área do Direito']=="CONTENCIOSO INDIVIDUAL"),
                                                                            "Não", np.where((dfNew['Natureza Operacional (M)'] == "ADMINISTRATIVO") & ( dfNew['Sub-área do Direito']=="TRATAMENTO - NÚCLEO DE GARANTIAS"),
                                                                                            "Não", np.where(dfNew['Sub-área do Direito'] == "CONTENCIOSO COLETIVO", "Não",
                                                                                                            np.where(dfNew['Sub-área do Direito']== "PREVENTIVO AUTO DE INFRAÇÃO", "Não","Sim"
                                                                                                                     )
                                                                                                            )
                                                                                            )
                                                                            )
                                                         )
                                      )
                             )

dfNew['Tipo cálculo - Fev-22'] = np.where(dfNew['Tipo cálculo - Fev-22'].isnull() == True, "Sem Cálculo", dfNew['Tipo cálculo - Fev-22'])

dfNew.to_excel(r'C:\Users\2104998693\Desktop\Modelagem\AutomacaoMarço0703.xlsx', sheet_name='Consolidado', index = False)

