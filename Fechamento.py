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
hist_pag_a_group.columns=['ID DO PROCESSO', 'TIPO_PGTO', 'VALOR', 'ÁREA DO DIREITO', 'SUB TIPO', 'PARCELAMENTO CONDENAÇÃO', 'PARCELAMENTO ACORDO']


fechamento_trabalhista = pd.read_excel(r'C:\Users\2104998693\Downloads\Fechamento_trabalhista.xlsx')
fechamento_trabalhista.dropna(how='all')

status_m1 = ['BAIXA PROVISORIA', 'REMOVIDO', 'ENCERRADO']
status = ['ATIVO', 'REATIVADO']

fechamento_trabalhista['NOVOS'] = np.where(fechamento_trabalhista['LINHA'] == 'linha03', 1 , 0 )
fechamento_trabalhista['REATIVADOS'] = np.where((fechamento_trabalhista['STATUS (M)'].isin(status)) 
                                                & (fechamento_trabalhista['STATUS (M-1)'].isin(status_m1)) , 1 , 0 )
"""
fechamento_trabalhista['NOVOS'] = np.where((fechamento_trabalhista['LINHA'] == 'linha03') & (fechamento_trabalhista['Cadastro'] >= '18/02/2021'), 1 , 0 )
fechamento_trabalhista['REATIVADOS'] = np.where((fechamento_trabalhista['LINHA'] == 'linha03') & (fechamento_trabalhista['Cadastro'] <= '18/02/2021'), 1 , 0 )
fechamento_trabalhista['REATIVADOS'] = np.where((fechamento_trabalhista['STATUS (M)'].isin(status)) & (fechamento_trabalhista['STATUS (M-1)'].isin(status_m1)) , 1 , 0 )
"""
status = ['BAIXA PROVISORIA', 'REMOVIDO', 'ENCERRADO']
status_m1 = ['ATIVO', 'REATIVADO']

fechamento_trabalhista['ENCERRADOS'] = np.where((fechamento_trabalhista['LINHA'] == 'linha03') 
                                                & (fechamento_trabalhista['STATUS (M)'].isin(status)), 1 , 0 )

status = ['BAIXA PROVISORIA', 'ENCERRADO', 'REMOVIDO', 'BAIXA PAGAMENTO']

fechamento_trabalhista['ENCERRADOS'] = np.where((fechamento_trabalhista['LINHA'] != 'linha01') 
                                                & (fechamento_trabalhista['STATUS (M)'].isin(status)) 
                                                & (fechamento_trabalhista['STATUS (M-1)'].isin(status_m1)) , 1 , 0 )

status = ['ATIVO', 'REATIVADO']
empresa = ['FUNDAÇÃO VIA VAREJO', 'INDÚSTRIA DE MÓVEIS BARTIRA LTDA']

fechamento_trabalhista['ESTOQUE'] = np.where((fechamento_trabalhista['LINHA'] != 'linha01') 
                                             & (fechamento_trabalhista['STATUS (M)'].isin(status)) 
                                             & (~fechamento_trabalhista['Empresa (M)'].isin(empresa)), 1 , 0 )

fechamento = pd.merge(fechamento_trabalhista, hist_pag_a_group, left_on= "ID PROCESSO", right_on= "ID DO PROCESSO", how="left")

remove_cols = [col for col in fechamento.columns if 'Unnamed' in col]
fechamento.drop(remove_cols,axis='columns',inplace=True)

status = ['ATIVO', 'REATIVADO']

fechamento['STATUS (M)'] = np.where((fechamento['LINHA'] != 'linha01') 
                                    & (fechamento['STATUS (M)'].isin(status)) 
                                    & (fechamento['VALOR']>0) 
                                    & (fechamento['ENCERRADOS'] == 0) 
                                    & (fechamento['TIPO_PGTO'] != 'Condenacao Incontroverso')
                                    , "BAIXA PGTO" , fechamento['STATUS (M)'])

fechamento['ENCERRADOS'] = np.where((fechamento['LINHA'] != 'linha01') 
                                    & (fechamento['STATUS (M)'].isin(status)) 
                                    & (fechamento['VALOR']>0) 
                                    & (fechamento['ENCERRADOS'] == 0) 
                                    & (fechamento['TIPO_PGTO'] != 'Condenacao Incontroverso')
                                    ,1 ,fechamento['ENCERRADOS'])

fechamento['ESTOQUE'] = np.where((fechamento['LINHA'] != 'linha01') 
                                    & (fechamento['STATUS (M)'].isin(status)) 
                                    & (fechamento['VALOR']>0) 
                                    & (fechamento['ENCERRADOS'] == 0) 
                                    & (fechamento['TIPO_PGTO']!= 'Condenacao Incontroverso')
                                    ,0, fechamento['ESTOQUE'])

fechamento['Classificação Mov. (M)'] = np.where((fechamento['LINHA'] != 'linha01') 
                                    & (fechamento['STATUS (M)'].isin(status)) 
                                    & (fechamento['VALOR']>0) 
                                    & (fechamento['ENCERRADOS'] == 0) 
                                    & (fechamento['TIPO_PGTO']!= 'Condenacao Incontroverso')
                                    ,"BAIXA PAGTO", fechamento['Classificação Mov. (M)'])


fechamento['Provisão Mov. (M)'] = np.where((fechamento['LINHA'] != 'linha01') 
                                    & (fechamento['STATUS (M)'].isin(status)) 
                                    & (fechamento['VALOR']>0) 
                                    & (fechamento['ENCERRADOS'] == 0) 
                                    & (fechamento['TIPO_PGTO']!= 'Condenacao Incontroverso')
                                    ,-abs(fechamento['Provisão Mov. (M)'])
                                    , fechamento['Provisão Mov. (M)'])
#abs aqui porque acho que é um upgrade no código, para "forçar" os números a serem negativos caso haja algum erro na base

fechamento['Correção Mov. (M)'] = np.where((fechamento['LINHA'] != 'linha01') 
                                    & (fechamento['STATUS (M)'].isin(status)) 
                                    & (fechamento['VALOR']>0) 
                                    & (fechamento['ENCERRADOS'] == 0) 
                                    & (fechamento['TIPO_PGTO']!= 'Condenacao Incontroverso')
                                    ,-abs(fechamento['Correção Mov. (M)'])
                                    , fechamento['Correção Mov. (M)'])

fechamento['Provisão Mov. Total (M)'] = np.where((fechamento['LINHA'] != 'linha01') 
                                    & (fechamento['STATUS (M)'].isin(status)) 
                                    & (fechamento['VALOR']>0) 
                                    & (fechamento['ENCERRADOS'] == 0) 
                                    & (fechamento['TIPO_PGTO']!= 'Condenacao Incontroverso')
                                    ,-abs(fechamento['Provisão Mov. Total (M)'])
                                    , fechamento['Provisão Mov. Total (M)'])

fechamento['Provisão Total (M)'] = np.where((fechamento['LINHA'] != 'linha01') 
                                    & (fechamento['STATUS (M)'].isin(status)) 
                                    & (fechamento['VALOR']>0) 
                                    & (fechamento['ENCERRADOS'] == 0) 
                                    & (fechamento['TIPO_PGTO']!= 'Condenacao Incontroverso')
                                    ,0, fechamento['Provisão Total (M)'])

fechamento['Correção (M-1)'] = np.where((fechamento['LINHA'] != 'linha01') 
                                    & (fechamento['STATUS (M)'].isin(status)) 
                                    & (fechamento['VALOR']>0) 
                                    & (fechamento['ENCERRADOS'] == 0) 
                                    & (fechamento['TIPO_PGTO']!= 'Condenacao Incontroverso')
                                    ,0, fechamento['Correção (M-1)'])

fechamento['Correção (M)'] = np.where((fechamento['LINHA'] != 'linha01') 
                                    & (fechamento['STATUS (M)'].isin(status)) 
                                    & (fechamento['VALOR']>0) 
                                    & (fechamento['ENCERRADOS'] == 0) 
                                    & (fechamento['TIPO_PGTO']!= 'Condenacao Incontroverso')
                                    ,0, fechamento['Correção (M-1)'])

fechamento['Provisão Total Passivo (M)'] = np.where((fechamento['LINHA'] != 'linha01') 
                                    & (fechamento['STATUS (M)'].isin(status)) 
                                    & (fechamento['VALOR']>0) 
                                    & (fechamento['ENCERRADOS'] == 0) 
                                    & (fechamento['TIPO_PGTO']!= 'Condenacao Incontroverso')
                                    ,0, fechamento['Provisão Total Passivo (M)'])

fechamento['EMPRESA: Classificação Mov.(M)'] = np.where((fechamento['LINHA'] != 'linha01') 
                                    & (fechamento['STATUS (M)'].isin(status)) 
                                    & (fechamento['VALOR']>0) 
                                    & (fechamento['ENCERRADOS'] == 0) 
                                    & (fechamento['TIPO_PGTO'] != 'Condenacao Incontroverso')
                                    , "BAIXA PGTO" , fechamento['EMPRESA: Classificação Mov.(M)'])

fechamento['EMPRESA: Provisão Mov. (M)'] = np.where((fechamento['LINHA'] != 'linha01') 
                                    & (fechamento['STATUS (M)'].isin(status)) 
                                    & (fechamento['VALOR']>0) 
                                    & (fechamento['ENCERRADOS'] == 0) 
                                    & (fechamento['TIPO_PGTO']!= 'Condenacao Incontroverso')
                                    ,-abs(fechamento['EMPRESA: Provisão Mov. (M)'])
                                    , fechamento['EMPRESA: Provisão Mov. (M)'])

#FIM PRIMEIRO BLOCO
status = ['ATIVO', 'REATIVADO']

fechamento['Classificação Mov. (M)'] = np.where((fechamento['LINHA'] != 'linha01') 
                                    & (fechamento['STATUS (M)'].isin(status)) 
                                    & (fechamento['VALOR']>0) 
                                    & (fechamento['ENCERRADOS'] == 0) 
                                    & (fechamento['TIPO_PGTO'] == 'Condenacao Incontroverso')
                                    ,"BAIXA PGTO", fechamento['Classificação Mov. (M)'])

fechamento['Provisão Mov. (M)'] = np.where((fechamento['LINHA'] != 'linha01') 
                                    & (fechamento['STATUS (M)'].isin(status)) 
                                    & (fechamento['VALOR']>0) 
                                    & (fechamento['ENCERRADOS'] == 0) 
                                    & (fechamento['TIPO_PGTO'] == 'Condenacao Incontroverso')
                                    ,-abs(fechamento['Provisão Mov. (M)'])
                                    , fechamento['Provisão Mov. (M)'])

fechamento['Correção Mov. (M)'] = np.where((fechamento['LINHA'] != 'linha01') 
                                    & (fechamento['STATUS (M)'].isin(status)) 
                                    & (fechamento['VALOR']>0) 
                                    & (fechamento['ENCERRADOS'] == 0) 
                                    & (fechamento['TIPO_PGTO'] == 'Condenacao Incontroverso')
                                    ,-abs(fechamento['Correção Mov. (M)'])
                                    , fechamento['Correção Mov. (M)'])

fechamento['Provisão Mov. Total (M)'] = np.where((fechamento['LINHA'] != 'linha01') 
                                    & (fechamento['STATUS (M)'].isin(status)) 
                                    & (fechamento['VALOR']>0) 
                                    & (fechamento['ENCERRADOS'] == 0) 
                                    & (fechamento['TIPO_PGTO'] == 'Condenacao Incontroverso')
                                    ,-abs(fechamento['Provisão Mov. Total (M)'])
                                    , fechamento['Provisão Mov. Total (M)'])

fechamento['Provisão Total (M)'] = np.where((fechamento['LINHA'] != 'linha01') 
                                    & (fechamento['STATUS (M)'].isin(status)) 
                                    & (fechamento['VALOR']>0) 
                                    & (fechamento['ENCERRADOS'] == 0) 
                                    & (fechamento['TIPO_PGTO'] == 'Condenacao Incontroverso')
                                    ,0, fechamento['Provisão Total (M)'])

fechamento['Correção (M-1)'] = np.where((fechamento['LINHA'] != 'linha01') 
                                    & (fechamento['STATUS (M)'].isin(status)) 
                                    & (fechamento['VALOR']>0) 
                                    & (fechamento['ENCERRADOS'] == 0) 
                                    & (fechamento['TIPO_PGTO'] == 'Condenacao Incontroverso')
                                    ,0, fechamento['Correção (M-1)'])

fechamento['Correção (M)'] = np.where((fechamento['LINHA'] != 'linha01') 
                                    & (fechamento['STATUS (M)'].isin(status)) 
                                    & (fechamento['VALOR']>0) 
                                    & (fechamento['ENCERRADOS'] == 0) 
                                    & (fechamento['TIPO_PGTO'] == 'Condenacao Incontroverso')
                                    ,0, fechamento['Correção (M)'])

fechamento['Provisão Total Passivo (M)'] = np.where((fechamento['LINHA'] != 'linha01') 
                                    & (fechamento['STATUS (M)'].isin(status)) 
                                    & (fechamento['VALOR']>0) 
                                    & (fechamento['ENCERRADOS'] == 0) 
                                    & (fechamento['TIPO_PGTO'] == 'Condenacao Incontroverso')
                                    ,0, fechamento['Provisão Total Passivo (M)'])

fechamento['EMPRESA: Classificação Mov.(M)'] = np.where((fechamento['LINHA'] != 'linha01') 
                                    & (fechamento['STATUS (M)'].isin(status)) 
                                    & (fechamento['VALOR']>0) 
                                    & (fechamento['ENCERRADOS'] == 0) 
                                    & (fechamento['TIPO_PGTO'] == 'Condenacao Incontroverso')
                                    ,"BAIXA PGTO", fechamento['EMPRESA: Classificação Mov.(M)'])

fechamento['EMPRESA: Provisão Mov. (M)'] = np.where((fechamento['LINHA'] != 'linha01') 
                                    & (fechamento['STATUS (M)'].isin(status)) 
                                    & (fechamento['VALOR']>0) 
                                    & (fechamento['ENCERRADOS'] == 0) 
                                    & (fechamento['TIPO_PGTO'] == 'Condenacao Incontroverso')
                                    ,-abs(fechamento['EMPRESA: Provisão Mov. (M)'])
                                    ,fechamento['EMPRESA: Provisão Mov. (M)'])

#FIM DO SEGUNDO BLOCO

fechamento['SUB TIPO'] = np.where((fechamento['LINHA'] == 'linha01')
                                                    ,"",fechamento['SUB TIPO'])
fechamento['TIPO_PGTO'] = np.where((fechamento['LINHA'] == 'linha01')
                                                    ,"",fechamento['TIPO_PGTO'])
fechamento['PARCELAMENTO CONDENAÇÃO'] = np.where((fechamento['LINHA'] == 'linha01')
                                                    ,"",fechamento['PARCELAMENTO CONDENAÇÃO'])
fechamento['PARCELAMENTO ACORDO'] = np.where((fechamento['LINHA'] == 'linha01')
                                                    ,"",fechamento['PARCELAMENTO ACORDO'])
fechamento['VALOR'] = np.where((fechamento['LINHA'] == 'linha01')
                                                    ,0,fechamento['VALOR'])
fechamento['OUTRAS_ADICOES'] = np.where((fechamento['LINHA'] == 'linha01')
                                                    ,0,"")
fechamento['OUTRAS_REVERSOES'] = np.where((fechamento['LINHA'] == 'linha01')
                                                    ,0,"")
#FIM DO TERCEIRO BLOCO

fechamento['OUTRAS_ADICOES'] = np.where((fechamento['NOVOS'] != 1) &
                                        (fechamento['REATIVADOS'] != 1) &
                                        (fechamento['ENCERRADOS'] != 1) &
                                        (fechamento['Provisão Mov. (M)'] > 0)
                                        ,1,0)

fechamento['OUTRAS_REVERSOES'] = np.where((fechamento['NOVOS'] != 1) &
                                        (fechamento['REATIVADOS'] != 1) &
                                        (fechamento['ENCERRADOS'] != 1) &
                                        (fechamento['Provisão Mov. (M)'] < 0)
                                        ,1,0)

#fechamento.to_excel(r'C:\Users\CAMINHO DO LAERCIO', sheet_name='Consolidado', index = False)

# ^ DESCOMENTAR E MUDAR O CAMINHO PARA EXPORTAR PARA EXCEL SE QUISER VALIDAR POR LÁ