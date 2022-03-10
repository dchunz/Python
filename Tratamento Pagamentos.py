# -*- coding: utf-8 -*-
"""
Created on Fri Sep  3 17:01:45 2021

@author: 2104998693
"""

import pandas as pd
import numpy as np

"""
Atenção não esquecer de atualizar o caminho do ultimo histórico de Pagamentos!!
"""

hist_pag = pd.read_excel(r'C:\Users\2104998693\Desktop\ViaVarejo\Python\HISTORIO_DE-PAGAMENTOS_20210916.xlsx')
hist_pag.dropna(how='all')

acordo = ['ACORDO - CÍVEL', 'ACORDO - CÍVEL ESTRATÉGICO', 'ACORDO - CÍVEL MASSA',
          'ACORDO - TRABALHISTA', 'PAGAMENTO DE ACORDO - TRABALHISTA (FK)']

condenacao = ['CONDENAÇÃO - CÍVEL',	'CONDENAÇÃO - CÍVEL ESTRATÉGICO', 
              'CONDENAÇÃO - CÍVEL MASSA', 'CONDENAÇÃO - CÍVEL MASSA (INCONTROVERSO)',
              'CONDENAÇÃO - REGULATÓRIO', 'CONDENAÇÃO - TRABALHISTA',
              'CONDENAÇÃO - TRABALHISTA (INCONTROVERSO)', 'MULTA - REGULATÓRIO',
              'MULTA PROCESSUAL - CÍVEL', 'MULTA PROCESSUAL - TRABALHISTA',
              'RNO - CONDENAÇÃO - TRABALHISTA', 	'RNO - CONDENAÇÃO - TRABALHISTA (INCONTROVERSO)',
              'RNO - MULTA PROCESSUAL - TRABALHISTA']

custas = ['HONORÁRIOS CONCILIADOR - CIVEL MASSA', 'HONORÁRIOS PERICIAIS - CÍVEL ESTRATÉGICO',
          'HONORÁRIOS PERICIAIS - CÍVEL MASSA', 	'HONORÁRIOS PERICIAIS - IMOBILIÁRIO',
          'HONORÁRIOS PERICIAIS - TRABALHISTA', 	'PAGAMENTO DE HONORÁRIOS PERICIAIS - TRABALHISTA (FK)',
          'RNO - HONORÁRIOS PERICIAIS -TRABALHISTA', 'CUSTAS FK - TRABALHISTA',
          'CUSTAS PERITOS - CÍVEL', 	'CUSTAS PERITOS - IMOBILIÁRIO',
          'CUSTAS PROCESSUAIS - CÍVEL', 	'CUSTAS PROCESSUAIS - CÍVEL ESTRATÉGICO',
          'CUSTAS PROCESSUAIS - CÍVEL MASSA', 'CUSTAS PROCESSUAIS - IMOBILIÁRIO',
          'CUSTAS PROCESSUAIS - REGULATÓRIO', 'CUSTAS PROCESSUAIS - TRABALHISTA',
          'PAGAMENTO DE CUSTAS - TRIBUTÁRIO', 'PERITOS - REGULATÓRIO',
          'RNO - CUSTAS PROCESSUAIS - TRABALHISTA']

imposto = ['INSS - TRABALHISTA', 'IR - TRABALHISTA', 
           'PAGAMENTO DE INSS - INDENIZAÇÃO TRABALHISTA (FK)', 
           'PAGAMENTO DE IR - INDENIZAÇÃO TRABALHISTA (FK)',
           'RNO - INSS - TRABALHISTA', 'RNO - IR - TRABALHISTA ', #verificar se tem esse espaço mesmo
           'RNO - FGTS', 'FGTS']

penhora = ['LIBERAÇÃO DE PENHORA - MASSA', 'LIBERAÇÃO DE PENHORA MASSA']

pensao = ['PENSÃO - CÍVEL', 	'PENSÃO - CÍVEL ESTRATÉGICO', 'PENSÃO - CÍVEL MASSA']

outpag = ['ACERTO CONTÁBIL: BLOQUEIO COM TRANSFERÊNCIA BANCÁRIA - DEP. JUDICIAL  (PAG)',
          'ACERTO CONTÁBIL: BLOQUEIO COM TRANSFERÊNCIA BANCÁRIA - PAGAMENTO',
          'ACERTO CONTÁBIL: PAGAMENTO DE ACORDO COM BAIXA DE DEP. JUDICIAL',
          'ACORDO/ PROGRAMAS DE PARCELAMENTO - REGULATÓRIO', 'ATIVO',
          'LIMINAR (CÍV. MASSA)', 'PAGAMENTO', 
          'PAGAMENTO AUTUAÇÃO MINISTÉRIO DO TRABALHO - TRABALHISTA',
          'PAGAMENTO DE EXECUÇÃO - TRABALHISTA', 'PAGAMENTOS - ALL - VV',
          'PAGAMENTOS FK']

hist_pag['Valor Final'] = np.where(hist_pag['SUB TIPO'].isin(acordo), 'Acordo',
                                   np.where(hist_pag['SUB TIPO'].isin(condenacao), 'Condenação',
                                            np.where(hist_pag['SUB TIPO'].isin(custas), 'Custas',
                                                     np.where(hist_pag['SUB TIPO'].isin(imposto), 'Imposto',
                                                              np.where(hist_pag['SUB TIPO'].isin(penhora), 'Penhora',
                                                                       np.where(hist_pag['SUB TIPO'].isin(pensao), 'Pensão',
                                                                                np.where(hist_pag['SUB TIPO'].isin(outpag), 'Outros Pagamentos', ''
                                                                                         )
                                                                                )
                                                                       )
                                                              )
                                                     )
                                            )
                                   )


hist_pag['Acordo'] = np.where(hist_pag['Valor Final'] == 'Acordo', hist_pag['VALOR'], 0 )
hist_pag['Condenação'] = np.where(hist_pag['Valor Final'] == 'Condenação', hist_pag['VALOR'], 0 )
hist_pag['Custas'] = np.where(hist_pag['Valor Final'] == 'Custas', hist_pag['VALOR'], 0 )
hist_pag['Impostos'] = np.where(hist_pag['Valor Final'] == 'Impostos', hist_pag['VALOR'], 0 )
hist_pag['Penhora'] = np.where(hist_pag['Valor Final'] == 'Penhora', hist_pag['VALOR'], 0 )
hist_pag['Pensão'] = np.where(hist_pag['Valor Final'] == 'Pensão', hist_pag['VALOR'], 0 )
hist_pag['Outros Pagamentos'] = np.where(hist_pag['Valor Final'] == 'Outros Pagamentos', hist_pag['VALOR'], 0 )

status_pag = ['CANCELADO', 'REMOVIDO', 'REJEITADO' ]



hist_pag_a = hist_pag[(~hist_pag['STATUS DO PAGAMENTO'].isin(status_pag) & \
            (hist_pag['STATUS DO PAGAMENTO'].str.contains('PAGAMENTO DEVOLVIDO') == False) &\
            (~hist_pag['STATUS DO PROCESSO'].isin(status_pag)) & \
            (hist_pag['STATUS DO PROCESSO'].str.contains('PAGAMENTO DEVOLVIDO') == False))]
    

d = {'01/11/2018':[('01/01/1900','20/11/2018 23:59:59')],
     '01/12/2018':[('21/11/2018','17/12/2018 23:59:59')],
     '01/01/2019':[('18/12/2018','21/01/2019 23:59:59')],
     '01/02/2019':[('22/01/2019','18/02/2019 23:59:59')],
     '01/03/2019':[('19/02/2019','19/03/2019 23:59:59')],
     '01/04/2019':[('20/03/2019','21/04/2019 23:59:59')],
     '01/05/2019':[('22/04/2019','21/05/2019 23:59:59')],
     '01/06/2019':[('22/05/2019','17/06/2019 23:59:59')],
     '01/07/2019':[('18/06/2019','21/07/2019 23:59:59')],
     '01/08/2019':[('22/07/2019','20/08/2019 23:59:59')],
     '01/09/2019':[('21/08/2019','22/09/2019 23:59:59')],
     '01/10/2019':[('23/09/2019','23/10/2019 23:59:59')],
     '01/11/2019':[('24/10/2019','21/11/2019 23:59:59')],
     '01/12/2019':[('22/11/2019','19/12/2020 23:59:59')],
     '01/01/2020':[('20/12/2019','26/01/2020 23:59:59')],
     '01/02/2020':[('27/01/2020','28/02/2020 23:59:59')],
     '01/03/2020':[('29/02/2020','24/03/2020 23:59:59')],
    '01/04/2020':[('25/03/2020','20/04/2020 23:59:59')],
    '01/05/2020':[('21/04/2020','19/05/2020 23:59:59')],
    '01/06/2020':[('20/05/2020','23/06/2020 23:59:59')],
    '01/07/2020':[('24/06/2020','29/07/2020 23:59:59')],
    '01/08/2020':[('30/07/2020','21/08/2020 23:59:59')],
    '01/09/2020':[('22/08/2020','22/09/2020 23:59:59')],
    '01/10/2020':[('23/09/2020','22/10/2020 23:59:59')],
    '01/11/2020':[('23/10/2020','24/11/2020 23:59:59')],
    '01/12/2020':[('25/11/2020','18/12/2020 23:59:59')],
    '01/01/2021':[('19/12/2020','23/01/2021 23:59:59')],
    '01/02/2021':[('24/01/2021','22/02/2021 23:59:59')],
    '01/03/2021':[('23/02/2021','21/03/2021 23:59:59')],
    '01/04/2021':[('22/03/2021','21/04/2021 23:59:59')],
    '01/05/2021':[('22/04/2021','23/05/2021 23:59:59')],
    '01/06/2021':[('24/05/2021','21/06/2021 23:59:59')],
    '01/07/2021':[('22/06/2021','22/07/2021 23:59:59')],
    '01/08/2021':[('23/07/2021','22/08/2021 23:59:59')],
    '01/09/2021':[('23/08/2021','21/09/2021 23:59:59')]
}

for k, v in d.items():
    for s, e in v:
        hist_pag_a.loc[hist_pag_a['DATA EFETIVA DO PAGAMENTO'].between(s,e, inclusive='both'), 'Data Efetiva Pagamento F'] = k
    

hist_pag_a_group = hist_pag_a.groupby(['PROCESSO - ID', 'Data Efetiva Pagamento F'], as_index=False).\
    agg({'Acordo': ['sum'], 'Condenação':['sum'], 'Custas':['sum'], 'Impostos':['sum'], 
         'Penhora':['sum'], 'Pensão':['sum'], 'Outros Pagamentos':['sum']})



hist_pag_a_group.to_excel('Tratamento Pagamentos.xlsx')
#Exportar os arquivos para Excel