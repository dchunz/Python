# -*- coding: utf-8 -*-
"""
Created on Fri Oct 22 15:03:44 2021

@author: 2104998693
"""

import pandas as pd
import numpy as np


hist_pag = pd.read_excel(r'C:\Users\2104998693\Downloads\Base_Pagamentos.xlsx')
hist_pag.dropna(how='all')

acordo = ['ACORDO - CÍVEL MASSA', 'ACORDO - CÍVEL ESTRATÉGICO', 'ACORDO - REGULATÓRIO - PROCON COM AUDIÊNCIA',
'ACORDO - TRABALHISTA', 'RNO - ACORDO - TRABALHISTA', 'ACORDO - IMOBILIÁRIO', 
'ACORDO/ PROGRAMAS DE PARCELAMENTO - REGULATÓRI', 'ACORDO - MEDIAÇÃO']

condenacao = ['CONDENAÇÃO - CÍVEL MASSA', 'CONDENAÇÃO - IMOBILIÁRIO', 
              'CONDENAÇÃO - REGULATÓRIO', 'CONDENAÇÃO - TRABALHISTA',
              'RNO - CONDENAÇÃO - TRABALHISTA', 'CONDENAÇÃO - CÍVEL ESTRATÉGICO']

condenacao_inc = ['CONDENAÇÃO - CÍVEL MASSA', 'CONDENAÇÃO - IMOBILIÁRIO', 'CONDENAÇÃO - REGULATÓRIO',
                  'CONDENAÇÃO - TRABALHISTA', 'RNO - CONDENAÇÃO - TRABALHISTA', 
                  'CONDENAÇÃO - CÍVEL ESTRATÉGICO']

imposto = ['FGTS', 'INSS - TRABALHISTA', 'IR - TRABALHISTA', 
           'RNO - INSS - TRABALHISTA',  'RNO - IR - TRABALHISTA']

multa_regulatorio = ['MULTA - REGULATÓRIO']

acordo_2 = ['ACORDO - CÍVEL MASSA - CARTÕES', 'ACORDO - CÍVEL MASSA - FORNECEDOR',
            'ACORDO - CÍVEL MASSA - MKTPLACE', 'ACORDO - CÍVEL MASSA - SEGURO']

condenacao_2 = ['CONDENAÇÃO - CÍVEL MASSA - CARTÕES', 'CONDENAÇÃO - CÍVEL MASSA - FORNECEDOR',
                'CONDENAÇÃO - CÍVEL MASSA - MKTPLACE', 'CONDENAÇÃO - CÍVEL MASSA - SEGURO']

condenacao_inc_2 = ['CONDENAÇÃO - CÍVEL MASSA (INCONTROVERSO) - CARTÕES',
                    'CONDENAÇÃO - CÍVEL MASSA (INCONTROVERSO) - FORNECEDOR',
                    'CONDENAÇÃO - CÍVEL MASSA (INCONTROVERSO) - MKTPLACE',
                    'CONDENAÇÃO - CÍVEL MASSA (INCONTROVERSO) - SEGURO']

responsabilidade = ['VIA VAREJO', 'SOLIDÁRIA']


hist_pag['TIPO_PGTO'] = np.where(hist_pag['SUB TIPO'].isin(acordo), 'Acordo',
                                   np.where(hist_pag['SUB TIPO'].isin(condenacao), 'Condenacao',
                                            np.where(hist_pag['SUB TIPO'].isin(condenacao_inc), 'Condenacao Incontroverso',
                                                     np.where(hist_pag['SUB TIPO'].isin(imposto), 'Imposto',
                                                              np.where(hist_pag['SUB TIPO'].isin(condenacao_2) & (hist_pag['RESPONSABILIDADE'].isin(responsabilidade)), 'Condenacao',
                                                                       np.where(hist_pag['SUB TIPO'].isin(acordo_2) & (hist_pag['RESPONSABILIDADE'].isin(responsabilidade)), 'Acordo',
                                                                                np.where(hist_pag['SUB TIPO'].isin(condenacao_inc_2) & (hist_pag['RESPONSABILIDADE'].isin(responsabilidade)), 'Condenacao Incontroverso',''
                                                                                         )
                                                                                )
                                                                       )
                                                              )
                                                     )
                                            )
                                   )
    
status_pagamento = ['Acordo', 'Condenacao', 'Condenacao Incontroverso', 'Multa - Regulatorio']

hist_pag_a = hist_pag[(hist_pag['STATUS DO PAGAMENTO'] != 'CANCELADO') & \
             (hist_pag['STATUS DO PAGAMENTO'] != 'EM CORREÇÃO') & (hist_pag['TIPO_PGTO'].isin(status_pagamento))]
 
hist_pag_a_group = hist_pag_a.groupby(['ID DO PROCESSO', 'TIPO_PGTO'], as_index=False).\
    agg({'VALOR': ['sum'], 'ÁREA DO DIREITO':['first'], 'SUB TIPO':['first'], 'PARCELAMENTO CONDENAÇÃO':['first'], 'PARCELAMENTO ACORDO':['first']})

