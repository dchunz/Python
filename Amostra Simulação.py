import pandas as pd
import numpy as np

amostra = 2
Ciclo = 'Ciclo 2'

#############################################################################################################################################

simulacao = pd.read_excel(r'C:\Users\daniel.chun_kavak\Desktop\Qualidade\Fila Simulação.xlsx', sheet_name = "Simulação")

simulacao['Data Final'] = pd.to_datetime(simulacao['Data Final'])

d = {'Não mapeado':[('01/01/1900','31/03/2022 23:59:59')],
    'Ciclo 1':[('04/01/2022','04/04/2022 23:59:59')],
    'Ciclo 2':[('04/05/2022','04/05/2022 23:59:59')],
    'Ciclo 3':[('04/06/2022','04/22/2022 23:59:59')],
    'Ciclo 4':[('04/23/2022','04/30/2022 23:59:59')],
}


for k, v in d.items():
    for s, e in v:
        simulacao.loc[simulacao['Data Final'].between(s,e, inclusive='both'), 'Data Final F'] = k


simulacao1 = simulacao[simulacao['Data Final F'] == Ciclo]

groupsim = simulacao1.groupby('Resp. Análise')['Estimativa', 'Data Inicial', 'Hora inicial', 'Nome Cliente'].apply(lambda s: s.sample(min(len(s), amostra))).reset_index()


#############################################################################################################################################

cancelamento = pd.read_excel(r'C:\Users\daniel.chun_kavak\Desktop\Qualidade\Fila Simulação.xlsx', sheet_name = 'Cancelamento - Acompanhamento')

cancelamento['Data Recebimento'] = pd.to_datetime(cancelamento['Data Recebimento'])

for k, v in d.items():
    for s, e in v:
        cancelamento.loc[cancelamento['Data Recebimento'].between(s,e, inclusive='both'), 'Data Final F'] = k
        
cancelamento1 = cancelamento[cancelamento['Data Final F'] == Ciclo]

groupcan = cancelamento1.groupby('Responsável')['Estimativa', 'Data Recebimento', 'Data do financiamento', 'Nº contrato'].apply(lambda s: s.sample(min(len(s), amostra))).reset_index()


#############################################################################################################################################

externo = pd.read_excel(r'C:\Users\daniel.chun_kavak\Desktop\Qualidade\Fila Simulação.xlsx', sheet_name = 'Externo - Março')

externo['DATA DE RECEBIMENTO'] = pd.to_datetime(externo['DATA DE RECEBIMENTO'])

externo['Responsável'] = "Caio"

for k, v in d.items():
    for s, e in v:
        externo.loc[externo['DATA DE RECEBIMENTO'].between(s,e, inclusive='both'), 'Data Final F'] = k
        
externo1 = externo[externo['Data Final F'] == Ciclo]

groupext = externo1.groupby('Responsável')['Nomes', 'DATA DE RECEBIMENTO', 'Estimativa', 'Status Cliente'].apply(lambda s: s.sample(min(len(s), amostra))).reset_index()

#############################################################################################################################################

pagamento = pd.read_excel(r'C:\Users\daniel.chun_kavak\Desktop\Qualidade\Fila Simulação.xlsx', sheet_name = 'Pagamento')

pagamento['Data Inicial'] = pd.to_datetime(pagamento['Data Inicial'])

pagamento['Responsável'] = "Caio"

for k, v in d.items():
    for s, e in v:
        pagamento.loc[pagamento['Data Inicial'].between(s,e, inclusive='both'), 'Data Final F'] = k
        
pagamento1 = pagamento[pagamento['Data Final F'] == Ciclo]

grouppag = pagamento1.groupby('Resp. Análise')['Nome', 'Data Inicial', 'Estimativa', 'Hora Final', 'STATUS'].apply(lambda s: s.sample(min(len(s), amostra))).reset_index()

#############################################################################################################################################



with pd.ExcelWriter('C:\\Users\daniel.chun_kavak\Desktop\Qualidade\Amostra.xlsx') as writer:
    groupsim.to_excel(writer, sheet_name='Simulação', index = False)
    groupcan.to_excel(writer, sheet_name='Cancelamento', index = False)
    groupext.to_excel(writer, sheet_name='Externa', index = False)
    grouppag.to_excel(writer, sheet_name='Pagamento', index = False)

