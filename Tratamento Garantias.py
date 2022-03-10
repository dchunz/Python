# -*- coding: utf-8 -*-
"""
Created on Fri Sep  3 17:01:27 2021

@author: 2104998693
"""
import pandas as pd
import numpy as np

gar = pd.read_excel(r'C:\Users\2104998693\Downloads\Garantias_20211111.xlsx',header=5)
gar.dropna(how='all')

tipo_garantia = ['ACERTO CONTÁBIL: BLOQUEIO COM TRANSFERÊNCIA BANCÁRIA - DEP. JUDICIAL',
								'BEM MÓVEL - CÍVEL',
								'BEM MÓVEL - CÍVEL MASSA',
								'BEM MÓVEL - REGULATÓRIO',
								'CARTA DE FIANÇA - CÍVEL',
								'CARTA DE FIANÇA - CÍVEL MASSA',
								'CARTA DE FIANÇA - REGULATÓRIO',
								'DEPÓSITO',
								'DEPÓSITO GARANTIA DE JUIZO - CÍVEL',
								'DEPÓSITO JUDICIAL',
								'DEPÓSITO JUDICIAL - CÍVEL',
								'DEPÓSITO JUDICIAL - CÍVEL ESTRATÉGICO',
								'DEPÓSITO JUDICIAL - CÍVEL MASSA',
								'DEPÓSITO JUDICIAL - REGULATÓRIO',
								'DEPÓSITO JUDICAL REGULATÓRIO',
								'DEPÓSITO JUDICIAL TRIBUTÁRIO',
								'DEPÓSITO RECURSAL - AIRR',
								'DESPÓSITO RECURSAL - CÍVEL MASSA',
								'DEPÓSITO RECURSAL - EMBARGOS TST',
								'DEPÓSITO RECURSAL AIRR',
								'DEPÓSITO RECURSAL RO',
								'IMÓVEL - CÍVEL MASSA',
								'IMÓVEL - REGULATÓRIO',
								'INATIVO',
								'LEVANTAMENTO DE CRÉDITO',
								'LEVANTAMENTO DE CRÉDITO - CÍVEL MASSA',
								'PENHORA - GARANTIA',
								'PENHORA - REGULATÓRIO']

gar_a = gar[(gar['STATUS DA GARANTIA'] != 'CANCELADO') & \
            (gar['STATUS DA GARANTIA'].str.contains('PAGAMENTO DEVOLVIDO') == False) &\
             (gar['STATUS'] != 'REMOVIDO') & (gar['TIPO GARANTIA'].isin(tipo_garantia)) ]
    

    
gar_b = gar_a[gar_a['DATA DE LEVANTAMENTO (PARTE CONTRÁRIA)'].isnull() == False]



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
    '01/09/2021':[('23/08/2021','21/09/2021 23:59:59')],
    '01/10/2021':[('22/09/2021','21/10/2021 23:59:59')],
    '01/11/2021':[('22/10/2021','21/11/2021 23:59:59')],
        
    
}


for k, v in d.items():
    for s, e in v:
        gar_b.loc[gar_b['DATA DE LEVANTAMENTO (PARTE CONTRÁRIA)'].between(s,e, inclusive='both'), 'Data Levantamento F'] = k

gar_b['Data Levantamento F'] = pd.to_datetime(gar_b['Data Levantamento F'])

group_b = gar_b.sort_values('Data Levantamento F').groupby(['(PROCESSO) ID', 'STATUS DA GARANTIA']).agg({'VALOR LEVANTADO (PARTE CONTRÁRIA)': ['sum'], 'Data Levantamento F':[np.max]})


group_b.reset_index().to_excel('Tratamento Garantias Novembro.xlsx')
#Exportar os arquivos para Excel