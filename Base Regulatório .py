#!/usr/bin/env python
# coding: utf-8

# In[2]:


import pandas as pd

import seaborn as sb

import numpy as np

import matplotlib as mp



# BASES PROCESSO REGULATÓRIO

# In[3]:


regulatório = pd.read_excel(r'Z:\01 PLANEJ FINANCEIRO JURIDICO\137.ANALYTICS\6 Bases de Dados MIS\Projetos Informações Gerenciais\Códigos Py\Regulatório Consolidado.xlsx')

garantias = pd.read_excel(r'Z:\01 PLANEJ FINANCEIRO JURIDICO\137.ANALYTICS\6 Bases de Dados MIS\Projetos Informações Gerenciais\Códigos Py\Tratamento Garantias Janeiro22.xlsx')

pagamentos = pd.read_excel(r'Z:\01 PLANEJ FINANCEIRO JURIDICO\137.ANALYTICS\6 Bases de Dados MIS\Projetos Informações Gerenciais\Códigos Py\Pagamentos_tratamentoTESTE.xlsx')


# Consolidação da Base Histórica Regulatório 
# 
# 

# In[4]:


Jan22 = pd.read_excel(r'Z:\01 PLANEJ FINANCEIRO JURIDICO\137.ANALYTICS\3 Prévias\2022\01. Janeiro\20.01.2022 Fechamento Regulatório.xlsx',sheet_name=('Base Fechamento'),header=1)
Jan22['LINHA'] = "01/01/2022"
Jan22['LINHA'] = pd.to_datetime(Jan22['LINHA'])
Jan22.dropna(how='all')


Dez21 = pd.read_excel(r'Z:\01 PLANEJ FINANCEIRO JURIDICO\137.ANALYTICS\3 Prévias\2021\12. Dezembro\20.12.2021 Fechamento Regulatório.xlsx',sheet_name=('Base Fechamento'),header=1)
Dez21['LINHA'] = "12/01/2021"
Dez21['LINHA'] = pd.to_datetime(Dez21['LINHA'])
Dez21.dropna(how='all')

Nov21 = pd.read_excel(r'Z:\01 PLANEJ FINANCEIRO JURIDICO\137.ANALYTICS\3 Prévias\2021\11. Novembro\21.11.2021 Fechamento Regulatório.xlsx',sheet_name=('Base Fechamento'),header=1)
Nov21['LINHA'] = "11/01/2021"
Nov21['LINHA'] = pd.to_datetime(Nov21['LINHA'])
Nov21.dropna(how='all')



Out21 = pd.read_excel(r'Z:\01 PLANEJ FINANCEIRO JURIDICO\137.ANALYTICS\3 Prévias\2021\10. Outubro\21.10.2021 Fechamento Regulatório.xlsx',sheet_name=('Base Fechamento'),header=1)
Out21['LINHA'] = "10/01/2021"
Out21['LINHA'] = pd.to_datetime(Out21['LINHA'])
Out21.dropna(how='all')

Set21 = pd.read_excel(r'Z:\01 PLANEJ FINANCEIRO JURIDICO\137.ANALYTICS\3 Prévias\2021\09. Setembro\21.09.2021 Fechamento Regulatório.xlsx',sheet_name=('Base Fechamento'),header=1)
Set21['LINHA'] = "09/01/2021"
Set21['LINHA'] = pd.to_datetime(Set21['LINHA'])
Set21.dropna(how='all')

Ago21 = pd.read_excel(r'Z:\01 PLANEJ FINANCEIRO JURIDICO\137.ANALYTICS\3 Prévias\2021\08. Agosto\22.08.2021 Fechamento Regulatório.xlsx',sheet_name=('Base Fechamento'),header=1)
Ago21['LINHA'] = "08/01/2021"
Ago21['LINHA'] = pd.to_datetime(Ago21['LINHA'])
Ago21.dropna(how='all')

Jul21 = pd.read_excel(r'Z:\01 PLANEJ FINANCEIRO JURIDICO\137.ANALYTICS\3 Prévias\2021\07. Julho\22.07.2021 Fechamento Regulatório.xlsx',sheet_name=('Base Fechamento'),header=1)
Jul21['LINHA'] = "07/01/2021"
Jul21['LINHA'] = pd.to_datetime(Jul21['LINHA'])
Jul21.dropna(how='all')

Jun21 = pd.read_excel(r'Z:\01 PLANEJ FINANCEIRO JURIDICO\137.ANALYTICS\3 Prévias\2021\06. Junho\21.06.2021 Fechamento Regulatório.xlsx',sheet_name=('Base Fechamento'),header=1)
Jun21['LINHA'] = "06/01/2021"
Jun21['LINHA'] = pd.to_datetime(Jun21['LINHA'])
Jun21.dropna(how='all')

Mai21 = pd.read_excel(r'Z:\01 PLANEJ FINANCEIRO JURIDICO\137.ANALYTICS\3 Prévias\2021\05. Maio\23.05.2021 Fechamento Regulatório.xlsx',sheet_name=('Base Fechamento'),header=1)
Mai21['LINHA'] = "05/01/2021"
Mai21['LINHA'] = pd.to_datetime(Mai21['LINHA'])
Mai21.dropna(how='all')

Abr21 = pd.read_excel(r'Z:\01 PLANEJ FINANCEIRO JURIDICO\137.ANALYTICS\3 Prévias\2021\04. Abril\22.04.2021 Fechamento Regulatório.xlsx',sheet_name=('Base Fechamento'),header=1)
Abr21['LINHA'] = "04/01/2021"
Abr21['LINHA'] = pd.to_datetime(Abr21['LINHA'])
Abr21.dropna(how='all')

Mar21 = pd.read_excel(r'Z:\01 PLANEJ FINANCEIRO JURIDICO\137.ANALYTICS\3 Prévias\2021\03. Março\19.03.2021 Fechamento Regulatório.xlsx',sheet_name=('Base Fechamento'),header=1)
Mar21['LINHA'] = "03/01/2021"
Mar21['LINHA'] = pd.to_datetime(Mar21['LINHA'])
Mar21.dropna(how='all')

Mar21.rename(
    columns=({'Cadastro':'DATACADASTRO'}), 
    inplace=True,)

Fev21 = pd.read_excel(r'Z:\01 PLANEJ FINANCEIRO JURIDICO\137.ANALYTICS\3 Prévias\2021\02. Fevereiro\22.02.2021 Fechamento Regulatório fevereiro.xlsx',sheet_name=('Fechamento Regulatório'),header=3)
Fev21['LINHA'] = "02/01/2021"
Fev21['LINHA'] = pd.to_datetime(Fev21['LINHA'])
Fev21.dropna(how='all')

Fev21.rename(
    columns=({'Cadastro':'DATACADASTRO','Novos':'NOVOS', 'Encerrados':'ENCERRADOS', 'Estoque':'ESTOQUE', 'SOCIO: Correção (M-1)':'SOCIO: Correção (M-1)_0001','EMPRESA: Correção (M-1)':'EMPRESA: Correção (M-1)_0001'}), 
    inplace=True,)

Jan21 = pd.read_excel(r'Z:\01 PLANEJ FINANCEIRO JURIDICO\137.ANALYTICS\3 Prévias\2021\01. Janeiro\15.01 REGULATÓRIO - Fechamento 15.01.xlsx',sheet_name=('Fechamento Regulatório'),header=5)
Jan21['LINHA'] = "01/01/2021"
Jan21['LINHA'] = pd.to_datetime(Jan21['LINHA'])
Jan21.dropna(how='all')

Jan21.rename(
    columns=({'Cadastro':'DATACADASTRO','novos':'NOVOS', 'encerrados':'ENCERRADOS', 'estoque':'ESTOQUE', 'SOCIO: Correção (M-1)':'SOCIO: Correção (M-1)_0001','EMPRESA: Correção (M-1)':'EMPRESA: Correção (M-1)_0001'}), 
    inplace=True,)



pdList = [Jan22, Dez21, Nov21, Out21, Set21, Ago21, Jul21, Jun21, Mai21, Abr21, Mar21, Fev21, Jan21]  # List of your dataframes
new_df = pd.concat(pdList,ignore_index=True)


new_df.rename(
    columns=({ 'LINHA': 'Data'}), 
    inplace=True,)

remove_cols = [col for col in new_df.columns if 'Unnamed' in col]
new_df.drop(remove_cols,axis='columns',inplace=True)


new_df.to_excel(r'Z:\01 PLANEJ FINANCEIRO JURIDICO\137.ANALYTICS\6 Bases de Dados MIS\Projetos Informações Gerenciais\Códigos Py\Regulatório Consolidado Janeiro 2022.xlsx', index=False)


# Base de Pagamentos (Tratamento Critérios Regulatório)

# In[11]:


hist_pag = pd.read_excel(r'C:\Users\2104990641\Desktop\HISTORIO_DE-PAGAMENTOS_20220125.xlsx')
hist_pag.dropna(how='all')

acordo = ['ACORDO - REGULATÓRIO - PROCON COM AUDIÊNCIA','ACORDO/ PROGRAMAS DE PARCELAMENTO - REGULATÓRIO']
                                                                  

condenacao = ['CONDENAÇÃO - REGULATÓRIO','MULTA - REGULATÓRIO']

custas = ['CUSTAS PROCESSUAIS - REGULATÓRIO']

penhora = ['LIBERAÇÃO DE PENHORA - REGULATÓRIO']
        
hist_pag['Valor Final'] = np.where(hist_pag['SUB TIPO'].isin(acordo), 'Acordo',
                              np.where(hist_pag['SUB TIPO'].isin(condenacao), 'Condenação',
                                  np.where(hist_pag['SUB TIPO'].isin(custas), 'Custas',
                                     np.where(hist_pag['SUB TIPO'].isin(penhora), 'Penhora',''
                                                                      
                                                                         
                                                                                         )
                                                                                )
                                                                       )
                                                              )
                                                     
                                            
                                


hist_pag['Acordo'] = np.where(hist_pag['Valor Final'] == 'Acordo', hist_pag['VALOR'], 0 )
hist_pag['Condenação'] = np.where(hist_pag['Valor Final'] == 'Condenação', hist_pag['VALOR'], 0 )
hist_pag['Custas'] = np.where(hist_pag['Valor Final'] == 'Custas', hist_pag['VALOR'], 0 )
hist_pag['Penhora'] = np.where(hist_pag['Valor Final'] == 'Penhora', hist_pag['VALOR'], 0 )



status_pag = ['CANCELADO', 'REMOVIDO', 'REJEITADO' ]



hist_pag_a = hist_pag[(~hist_pag['STATUS DO PAGAMENTO'].isin(status_pag) &             (hist_pag['STATUS DO PAGAMENTO'].str.contains('PAGAMENTO DEVOLVIDO') == False) &            (~hist_pag['STATUS DO PROCESSO'].isin(status_pag)) &             (hist_pag['STATUS DO PROCESSO'].str.contains('PAGAMENTO DEVOLVIDO') == False))]
    
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
     '01/10/2021':[('22/09/2021', '01/10/2021 23:59:59')],
     '01/11/2021':[('22/10/2021','21/11/2021 23:59:59')],
     '01/12/2021':[('22/11/2021','20/12/2021 23:59:59')],
     '01/01/2022':[('21/12/2021','20/01/2022 23:59:59')], 
     }

for k, v in d.items():
    for s, e in v:
        hist_pag_a.loc[hist_pag_a['DATA EFETIVA DO PAGAMENTO'].between(s,e, inclusive='both'), 'Data Efetiva Pagamento F'] = k
    
hist_pag_a['Data Efetiva Pagamento F'] = pd.to_datetime(hist_pag_a['Data Efetiva Pagamento F'])
hist_pag_a_group = hist_pag_a.sort_values('Data Efetiva Pagamento F').groupby(['PROCESSO - ID']).    agg({'Acordo': ['sum'], 'Condenação':['sum'], 'Custas':['sum'],
         'Penhora':['sum'], 'Data Efetiva Pagamento F':[np.max]})

hist_pag_a_group.reset_index().to_excel (r'C:\Users\2104990641\Desktop\Pagamentos_tratamentoJaneiro2022.xlsx', header=True)


# Base de Garantias  (Tratamento Critérios Regulatório)

# In[9]:


gar = pd.read_excel(r'C:\Users\2104990641\Desktop\Garantias_20220201.xlsx',header=5)
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

gar_a = gar[(gar['STATUS DA GARANTIA'] != 'CANCELADO') &             (gar['STATUS DA GARANTIA'].str.contains('PAGAMENTO DEVOLVIDO') == False) &             (gar['STATUS'] != 'REMOVIDO') & (gar['TIPO GARANTIA'].isin(tipo_garantia)) ]
    

    
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
    '01/12/2021':[('22/11/2021','20/12/2021 23:59:59')],   
    '01/01/2022':[('21/12/2021','20/01/2022 23:59:59')], 
}


for k, v in d.items():
    for s, e in v:
        gar_b.loc[gar_b['DATA DE LEVANTAMENTO (PARTE CONTRÁRIA)'].between(s,e, inclusive='both'), 'Data Levantamento F'] = k

gar_b['Data Levantamento F'] = pd.to_datetime(gar_b['Data Levantamento F'])

group_b = gar_b.sort_values('Data Levantamento F').groupby(['(PROCESSO) ID', 'STATUS DA GARANTIA']).agg({'VALOR LEVANTADO (PARTE CONTRÁRIA)': ['sum'], 'Data Levantamento F':[np.max]})


group_b.reset_index().to_excel(r'Z:\01 PLANEJ FINANCEIRO JURIDICO\137.ANALYTICS\6 Bases de Dados MIS\Projetos Informações Gerenciais\Códigos Py\Tratamento Garantias Janeiro22.xlsx')
#Exportar os arquivos para Excel


# Junção das Bases (Consolidado Regulatório, Pagamentos, Garantias)

# In[13]:


regulatório = pd.read_excel(r'Z:\01 PLANEJ FINANCEIRO JURIDICO\137.ANALYTICS\6 Bases de Dados MIS\Projetos Informações Gerenciais\Códigos Py\Regulatório Consolidado Janeiro 2022.xlsx.')

garantias = pd.read_excel(r'Z:\01 PLANEJ FINANCEIRO JURIDICO\137.ANALYTICS\6 Bases de Dados MIS\Projetos Informações Gerenciais\Códigos Py\Tratamento Garantias Janeiro22.xlsx')

pagamentos = pd.read_excel(r'Z:\01 PLANEJ FINANCEIRO JURIDICO\137.ANALYTICS\6 Bases de Dados MIS\Projetos Informações Gerenciais\Códigos Py\Pagamentos_tratamentoJaneiro2022.xlsx')

#União 



reg_pag = pd.merge(regulatório, pagamentos, how = "left", left_on='ID PROCESSO', right_on="PROCESSO - ID")


reg_pag_gar = pd.merge(reg_pag, garantias, how ='left', left_on = 'ID PROCESSO', right_on='(PROCESSO) ID')


reg_pag_gar.reset_index().to_excel (r'Z:\01 PLANEJ FINANCEIRO JURIDICO\137.ANALYTICS\6 Bases de Dados MIS\Projetos Informações Gerenciais\Códigos Py\REG_PAGAMENTOS_FINAL_JANEIRO_2022.xlsx')


# In[ ]:




