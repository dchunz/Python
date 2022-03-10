# -*- coding: utf-8 -*-
"""
Created on Mon Dec  6 09:49:48 2021

@author: Daniel Chun
"""

#Carga das bibliotecas utilizadas no estudo

import pandas as pd

#biblioteca para gráficos mais amigáveis
import seaborn as sns

#carrega módulo decision tree
from sklearn import tree

#Carrega métricas de avaliação de modelos
#Para modelos de regressão utilizamos R-quadrado, MAPE e MAE
from sklearn.metrics import r2_score, mean_absolute_percentage_error, mean_absolute_error
#Para modelos de classificação utilizamos Acurácia, curva ROC / AUC
from sklearn.metrics import accuracy_score, roc_auc_score, roc_curve, auc

#carrega módulo para tratar variáveis categóricas. trabalhando com modelos de árvore podemos usar o Label Encoder
from sklearn import preprocessing

#ANOVA - teste de independência entre variável categórica e contínua
import statsmodels.api as sm
from statsmodels.formula.api import ols

#Biblioteca para exibição gráfica do resultado da árvore de decisão treinada
import graphviz

#força o pandas a mostrar todas as colunas do dataframe
pd.set_option('display.max_columns', None)

#força o pandas a mostrar todas as linhas do dataframe
#pd.set_option("max_rows", None)

#Carga da base de Dados
dados = pd.read_excel("C:/Users/2104998693/Downloads/Novo Histórico 20_10.xlsx")

estoque = pd.read_excel("C:/Users/2104998693/Desktop/Modelagem/FECHAMENTO_TRAB_20220307_4.xlsx")

"""
Análise Exploratória de Dados

Análise das variáveis disponíveis, sua distribuição. Testes das primeiras hipóteses e avaliação do efeito de possíveis variáveis explicativas na resposta (alvo do estudo) - análise bivariada.
"""
#Definição dos clusters (Histórico)
cluster_sp = ['SP']
cluster_rj = ['RJ']
cluster_alto_valor = ['MG', 'DF']
cluster_medio_valor = ['SC','PR','RS','BA','GO','MS'] 

#Criação de nova variável, agrupando os estados por perfil de faixa de valores
dados['cluster_valor'] = dados.ESTADO.apply(lambda x: 'ALTO VALOR' if x in cluster_alto_valor 
                                            else 'MEDIO VALOR' if x in cluster_medio_valor 
                                            else 'SP' if x in cluster_sp
                                            else 'RJ' if x in cluster_rj
                                            else 'OUTROS')

dados.groupby(dados['cluster_valor']).count()

#Definição dos clusters (Estoque)
cluster_sp = ['SP']
cluster_rj = ['RJ']
cluster_alto_valor = ['MG', 'DF']
cluster_medio_valor = ['SC','PR','RS','BA','GO','MS'] 

#Criação de nova variável, agrupando os estados por perfil de faixa de valores
estoque['cluster_valor'] = estoque.ESTADO.apply(lambda x: 'ALTO VALOR' if x in cluster_alto_valor 
                                            else 'MEDIO VALOR' if x in cluster_medio_valor 
                                            else 'SP' if x in cluster_sp
                                            else 'RJ' if x in cluster_rj
                                            else 'OUTROS')

estoque.groupby(estoque['cluster_valor']).count()

#Gerar o agrupamento de cargos definido como objeto do estudo
lista_cargos = ['VENDEDOR','MONTADOR','AJUDANTE', 'GERENTE', 'MOTORISTA','AJUDANTE EXTERNO', 'CAIXA','OPERADOR','AUXILIAR','ANALISTA']

dados['cargo_tratado'] = dados.PARTE_CONTRARIA_CARGO_GRUPO.apply(lambda x: x if x in lista_cargos else 'OUTROS')

dados.groupby(dados.cargo_tratado).count()

#Gerar o agrupamento de cargos definido como objeto do estudo
lista_cargos_estoque = ['VENDEDOR','MONTADOR','AJUDANTE', 'GERENTE', 'MOTORISTA','AJUDANTE EXTERNO', 'CAIXA','OPERADOR','AUXILIAR','ANALISTA']

estoque['cargo_tratado'] = estoque['Objeto Assunto/Cargo (M)'].apply(lambda x: x if x in lista_cargos else 'OUTROS')

estoque.groupby(estoque.cargo_tratado).count()

#Define o filtro geral

#Define os filtros a serem feitos na base
natureza_notin = ['TERCEIRO INSOLVENTE', 'SINDICATO / MINISTERIO PUBLICO','TERCEIRO SOLVENTE','ADMINISTRATIVO']
sub_area_direito_notin = ['PREVENTIVO AUTO DE INFRAÇÃO','CONTENCIOSO COLETIVO']

dados_condenacao_geral = dados[(dados['MOTIVO_ENC_AGRP'] == 'CONDENACAO')
                        & (~dados['NATUREZA_OPERACIONAL'].isin(natureza_notin))
                        & (~dados['SUB_AREA_DO_DIREITO'].isin(sub_area_direito_notin))
                       ]
                       
"""
Gerar a modelagem do cargo Vendedor, com 50 ramificações
"""

natureza_notin = ['TERCEIRO INSOLVENTE', 'SINDICATO / MINISTERIO PUBLICO','TERCEIRO SOLVENTE','ADMINISTRATIVO']
sub_area_direito_notin = ['PREVENTIVO AUTO DE INFRAÇÃO','CONTENCIOSO COLETIVO']
outlier_notin = ['Outlier']

dados_condenacao_cargo = dados[(dados['MOTIVO_ENC_AGRP'] == 'CONDENACAO')
                        & (~dados['NATUREZA_OPERACIONAL'].isin(natureza_notin))
                        & (~dados['SUB_AREA_DO_DIREITO'].isin(sub_area_direito_notin))
                        & (~dados['OUTLIER'].isin(outlier_notin))    
                            & (dados['cargo_tratado'] == 'VENDEDOR')      
                       ]

#Define o filtro para Estoque
ESTQ_natureza_notin = ['TERCEIRO INSOLVENTE']

estoque_cargo = estoque[(estoque['cargo_tratado'] == 'VENDEDOR')
                       & (~estoque['Natureza Operacional (M)'].isin(ESTQ_natureza_notin))
                       ]


#Cria um novo dataframe adequado ao scikit-learning para treinamento dos modelos
explicativas = pd.DataFrame()
explicativas['ID_PROCESSO'] = dados_condenacao_geral.ID_PROCESSO
explicativas_cargo = pd.DataFrame()
explicativas_cargo['ID_PROCESSO'] = dados_condenacao_cargo.ID_PROCESSO

explicativas_estoque = pd.DataFrame()
explicativas_estoque['ID PROCESSO'] = estoque_cargo['ID PROCESSO']



#Faz o Label Encoder, que converte dados qualitativos de texto para um índice numérico
#Com esse encoding, podemos facilmente voltar aos valores originais utilizando a função inverse_transform

#adiciona a variável Estado codificada ao dataframe
le_estado = preprocessing.LabelEncoder()
encode_estado = le_estado.fit(estoque['ESTADO'])
explicativas['ESTADO'] = encode_estado.transform(dados_condenacao_geral['ESTADO'])
explicativas_cargo['ESTADO'] = encode_estado.transform(dados_condenacao_cargo['ESTADO'])
explicativas_estoque['ESTADO'] = encode_estado.transform(estoque_cargo['ESTADO'])


#gera o de-para dos estados
estados = pd.DataFrame()
estados['codigos'] = explicativas_estoque.ESTADO.unique()
estados['estados'] = encode_estado.inverse_transform(estados.codigos)
estados.sort_values(by='codigos')


#adiciona a variável cluster valor codificada ao dataframe
le_cluster_valor = preprocessing.LabelEncoder()
encode_cluster_valor = le_cluster_valor.fit(dados_condenacao_geral['cluster_valor'])
explicativas['cluster_valor'] = encode_cluster_valor.transform(dados_condenacao_geral['cluster_valor'])
explicativas_cargo['cluster_valor'] = encode_cluster_valor.transform(dados_condenacao_cargo['cluster_valor'])
explicativas_estoque['cluster_valor'] = encode_cluster_valor.transform(estoque_cargo['cluster_valor'])

#gera o de-para dos cluster valor
cluster_valor = pd.DataFrame()
cluster_valor['codigos'] = explicativas.cluster_valor.unique()
cluster_valor['cluster_valor'] = encode_cluster_valor.inverse_transform(cluster_valor.codigos)
cluster_valor.sort_values(by='codigos')

#adiciona a variável cargo_tratado codificada ao dataframe
le_cargo_tratado = preprocessing.LabelEncoder()
encode_cargo_tratado = le_cargo_tratado.fit(dados_condenacao_geral['cargo_tratado'])
explicativas['cargo_tratado'] = encode_cargo_tratado.transform(dados_condenacao_geral['cargo_tratado'])
explicativas_cargo['cargo_tratado'] = encode_cargo_tratado.transform(dados_condenacao_cargo['cargo_tratado'])
explicativas_estoque['cargo_tratado'] = encode_cargo_tratado.transform(estoque_cargo['cargo_tratado'])


#gera o de-para dos cargos
cargo = pd.DataFrame()
cargo['codigos'] = explicativas.cargo_tratado.unique()
cargo['cargo'] = encode_cargo_tratado.inverse_transform(cargo.codigos)
cargo.sort_values(by='codigos')

#adiciona a variável Cluster Aging Tempo de Empresa codificada ao dataframe
le_tempo_empresa = preprocessing.LabelEncoder()
encode_tempo_empresa = le_tempo_empresa.fit(dados_condenacao_geral['Cluster Aging Tempo de Empresa'])
explicativas['Cluster Aging Tempo de Empresa'] = encode_tempo_empresa.transform(dados_condenacao_geral['Cluster Aging Tempo de Empresa'])
explicativas_cargo['Cluster Aging Tempo de Empresa'] = encode_tempo_empresa.transform(dados_condenacao_cargo['Cluster Aging Tempo de Empresa'])
explicativas_estoque['Cluster Aging Tempo de Empresa'] = encode_tempo_empresa.transform(estoque_cargo['Cluster Aging Tempo de Empresa'])

#gera o de-para dos cluster tempo de empresa
tempo_empresa = pd.DataFrame()
tempo_empresa['codigos'] = explicativas['Cluster Aging Tempo de Empresa'].unique()
tempo_empresa['tempo_empresa'] = encode_tempo_empresa.inverse_transform(tempo_empresa.codigos)
tempo_empresa.sort_values(by='codigos')

#adiciona a variável Cluster Aging codificada ao dataframe
le_cluster_aging = preprocessing.LabelEncoder()
encode_cluster_aging = le_cluster_aging.fit(dados_condenacao_geral['Cluster Aging'])
explicativas['Cluster Aging'] = encode_cluster_aging.transform(dados_condenacao_geral['Cluster Aging'])
explicativas_cargo['Cluster Aging'] = encode_cluster_aging.transform(dados_condenacao_cargo['Cluster Aging'])
explicativas_estoque['Cluster Aging'] = encode_cluster_aging.transform(estoque_cargo['Cluster Aging'])

#gera o de-para dos cluster aging
cluster_aging = pd.DataFrame()
cluster_aging['codigos'] = explicativas['Cluster Aging'].unique()
cluster_aging['cluster_aging'] = encode_cluster_aging.inverse_transform(cluster_aging.codigos)
cluster_aging.sort_values(by='codigos')

#adiciona a variável Safra de Reclamação codificada ao dataframe
le_safra_reclamacao = preprocessing.LabelEncoder()
encode_safra_reclamacao = le_safra_reclamacao.fit(estoque['Safra de Reclamação'].astype(str))
explicativas['safra_reclamacao'] = encode_safra_reclamacao.transform(dados_condenacao_geral['Safra de Reclamação'].astype(str))
dados_condenacao_geral['safra_reclamacao'] = encode_safra_reclamacao.transform(dados_condenacao_geral['Safra de Reclamação'].astype(str))
explicativas_cargo['safra_reclamacao'] = encode_safra_reclamacao.transform(dados_condenacao_cargo['Safra de Reclamação'].astype(str))
explicativas_estoque['safra_reclamacao'] = encode_safra_reclamacao.transform(estoque_cargo['Safra de Reclamação'].astype(str))

#gera o de-para dos cluster pedidos
safra_reclamacao = pd.DataFrame()
safra_reclamacao['codigos'] = explicativas_estoque['safra_reclamacao'].unique()
safra_reclamacao['safra_reclamacao'] = encode_safra_reclamacao.inverse_transform(safra_reclamacao.codigos)
safra_reclamacao.sort_values(by='codigos')

#substitui nulos nas variáveis qualitativas por -999
#Como estamos trabalhando com modelos de árvore, os valores sem dados serão tratados como uma categoria à parte, muito distante das demais
explicativas = explicativas.fillna(-999)
explicativas_cargo = explicativas_cargo.fillna(-999)
explicativas_estoque = explicativas_estoque.fillna(-999)


#prepara target
resposta = pd.DataFrame(dados_condenacao_geral['Pagamento Desindexado'])
resposta_cargo = pd.DataFrame(dados_condenacao_cargo['Pagamento Desindexado'])

#Construção do Modelo de Árvore de Decisão para Regressão - resposta numérica contínua
#Em cenários de classificação podemos usar a DecisionTreeClassifier
#É possível customizar critérios de parada através dos hiperparâmetros do modelo
DT = tree.DecisionTreeRegressor(random_state=42, 
                                max_depth=100, 
                                criterion='mae',
                                min_samples_leaf = 50)


#prepara target
resposta = pd.DataFrame(dados_condenacao_cargo['Pagamento Desindexado'])

DT = DT.fit(explicativas_cargo[['cluster_valor', 'Cluster Aging Tempo de Empresa', 'Cluster Aging', 'safra_reclamacao']],
            resposta_cargo['Pagamento Desindexado'])

y_true = resposta_cargo['Pagamento Desindexado']
#y_pred = valor previsto pelo modelo treinado
y_pred = DT.predict(explicativas_cargo[['cluster_valor', 'Cluster Aging Tempo de Empresa', 'Cluster Aging','safra_reclamacao']])

#Aplicação da predição no dataframe do estoque para obtenção dos valores de predição
dados_estoque_full = estoque_cargo
dados_estoque_full['prediction'] = DT.predict(explicativas_estoque[['cluster_valor', 'Cluster Aging Tempo de Empresa', 
                                                                    'Cluster Aging','safra_reclamacao']])

#Gera o recorte precificado do cargo utilizado
estoque_cargo_vendedor = estoque_cargo
"""
Gerar a modelagem do cargo Montador, com 50 ramificações
"""

natureza_notin = ['TERCEIRO INSOLVENTE', 'SINDICATO / MINISTERIO PUBLICO','TERCEIRO SOLVENTE','ADMINISTRATIVO']
sub_area_direito_notin = ['PREVENTIVO AUTO DE INFRAÇÃO','CONTENCIOSO COLETIVO']
outlier_notin = ['Outlier']

dados_condenacao_cargo = dados[(dados['MOTIVO_ENC_AGRP'] == 'CONDENACAO')
                        & (~dados['NATUREZA_OPERACIONAL'].isin(natureza_notin))
                        & (~dados['SUB_AREA_DO_DIREITO'].isin(sub_area_direito_notin))
                        & (~dados['OUTLIER'].isin(outlier_notin))    
                            & (dados['cargo_tratado'] == 'MONTADOR')      
                       ]

#Define o filtro para Estoque
ESTQ_natureza_notin = ['TERCEIRO INSOLVENTE']

estoque_cargo = estoque[(estoque['cargo_tratado'] == 'MONTADOR')
                       & (~estoque['Natureza Operacional (M)'].isin(ESTQ_natureza_notin))
                       ]


#Cria um novo dataframe adequado ao scikit-learning para treinamento dos modelos
explicativas = pd.DataFrame()
explicativas['ID_PROCESSO'] = dados_condenacao_geral.ID_PROCESSO
explicativas_cargo = pd.DataFrame()
explicativas_cargo['ID_PROCESSO'] = dados_condenacao_cargo.ID_PROCESSO

explicativas_estoque = pd.DataFrame()
explicativas_estoque['ID PROCESSO'] = estoque_cargo['ID PROCESSO']



#Faz o Label Encoder, que converte dados qualitativos de texto para um índice numérico
#Com esse encoding, podemos facilmente voltar aos valores originais utilizando a função inverse_transform

#adiciona a variável Estado codificada ao dataframe
le_estado = preprocessing.LabelEncoder()
encode_estado = le_estado.fit(estoque['ESTADO'])
explicativas['ESTADO'] = encode_estado.transform(dados_condenacao_geral['ESTADO'])
explicativas_cargo['ESTADO'] = encode_estado.transform(dados_condenacao_cargo['ESTADO'])
explicativas_estoque['ESTADO'] = encode_estado.transform(estoque_cargo['ESTADO'])


#gera o de-para dos estados
estados = pd.DataFrame()
estados['codigos'] = explicativas_estoque.ESTADO.unique()
estados['estados'] = encode_estado.inverse_transform(estados.codigos)
estados.sort_values(by='codigos')


#adiciona a variável cluster valor codificada ao dataframe
le_cluster_valor = preprocessing.LabelEncoder()
encode_cluster_valor = le_cluster_valor.fit(dados_condenacao_geral['cluster_valor'])
explicativas['cluster_valor'] = encode_cluster_valor.transform(dados_condenacao_geral['cluster_valor'])
explicativas_cargo['cluster_valor'] = encode_cluster_valor.transform(dados_condenacao_cargo['cluster_valor'])
explicativas_estoque['cluster_valor'] = encode_cluster_valor.transform(estoque_cargo['cluster_valor'])

#gera o de-para dos cluster valor
cluster_valor = pd.DataFrame()
cluster_valor['codigos'] = explicativas.cluster_valor.unique()
cluster_valor['cluster_valor'] = encode_cluster_valor.inverse_transform(cluster_valor.codigos)
cluster_valor.sort_values(by='codigos')

#adiciona a variável cargo_tratado codificada ao dataframe
le_cargo_tratado = preprocessing.LabelEncoder()
encode_cargo_tratado = le_cargo_tratado.fit(dados_condenacao_geral['cargo_tratado'])
explicativas['cargo_tratado'] = encode_cargo_tratado.transform(dados_condenacao_geral['cargo_tratado'])
explicativas_cargo['cargo_tratado'] = encode_cargo_tratado.transform(dados_condenacao_cargo['cargo_tratado'])
explicativas_estoque['cargo_tratado'] = encode_cargo_tratado.transform(estoque_cargo['cargo_tratado'])


#gera o de-para dos cargos
cargo = pd.DataFrame()
cargo['codigos'] = explicativas.cargo_tratado.unique()
cargo['cargo'] = encode_cargo_tratado.inverse_transform(cargo.codigos)
cargo.sort_values(by='codigos')

#adiciona a variável Cluster Aging Tempo de Empresa codificada ao dataframe
le_tempo_empresa = preprocessing.LabelEncoder()
encode_tempo_empresa = le_tempo_empresa.fit(dados_condenacao_geral['Cluster Aging Tempo de Empresa'])
explicativas['Cluster Aging Tempo de Empresa'] = encode_tempo_empresa.transform(dados_condenacao_geral['Cluster Aging Tempo de Empresa'])
explicativas_cargo['Cluster Aging Tempo de Empresa'] = encode_tempo_empresa.transform(dados_condenacao_cargo['Cluster Aging Tempo de Empresa'])
explicativas_estoque['Cluster Aging Tempo de Empresa'] = encode_tempo_empresa.transform(estoque_cargo['Cluster Aging Tempo de Empresa'])

#gera o de-para dos cluster tempo de empresa
tempo_empresa = pd.DataFrame()
tempo_empresa['codigos'] = explicativas['Cluster Aging Tempo de Empresa'].unique()
tempo_empresa['tempo_empresa'] = encode_tempo_empresa.inverse_transform(tempo_empresa.codigos)
tempo_empresa.sort_values(by='codigos')

#adiciona a variável Cluster Aging codificada ao dataframe
le_cluster_aging = preprocessing.LabelEncoder()
encode_cluster_aging = le_cluster_aging.fit(dados_condenacao_geral['Cluster Aging'])
explicativas['Cluster Aging'] = encode_cluster_aging.transform(dados_condenacao_geral['Cluster Aging'])
explicativas_cargo['Cluster Aging'] = encode_cluster_aging.transform(dados_condenacao_cargo['Cluster Aging'])
explicativas_estoque['Cluster Aging'] = encode_cluster_aging.transform(estoque_cargo['Cluster Aging'])

#gera o de-para dos cluster aging
cluster_aging = pd.DataFrame()
cluster_aging['codigos'] = explicativas['Cluster Aging'].unique()
cluster_aging['cluster_aging'] = encode_cluster_aging.inverse_transform(cluster_aging.codigos)
cluster_aging.sort_values(by='codigos')

#adiciona a variável Safra de Reclamação codificada ao dataframe
le_safra_reclamacao = preprocessing.LabelEncoder()
encode_safra_reclamacao = le_safra_reclamacao.fit(estoque['Safra de Reclamação'].astype(str))
explicativas['safra_reclamacao'] = encode_safra_reclamacao.transform(dados_condenacao_geral['Safra de Reclamação'].astype(str))
dados_condenacao_geral['safra_reclamacao'] = encode_safra_reclamacao.transform(dados_condenacao_geral['Safra de Reclamação'].astype(str))
explicativas_cargo['safra_reclamacao'] = encode_safra_reclamacao.transform(dados_condenacao_cargo['Safra de Reclamação'].astype(str))
explicativas_estoque['safra_reclamacao'] = encode_safra_reclamacao.transform(estoque_cargo['Safra de Reclamação'].astype(str))

#gera o de-para dos cluster pedidos
safra_reclamacao = pd.DataFrame()
safra_reclamacao['codigos'] = explicativas_estoque['safra_reclamacao'].unique()
safra_reclamacao['safra_reclamacao'] = encode_safra_reclamacao.inverse_transform(safra_reclamacao.codigos)
safra_reclamacao.sort_values(by='codigos')

#substitui nulos nas variáveis qualitativas por -999
#Como estamos trabalhando com modelos de árvore, os valores sem dados serão tratados como uma categoria à parte, muito distante das demais
explicativas = explicativas.fillna(-999)
explicativas_cargo = explicativas_cargo.fillna(-999)
explicativas_estoque = explicativas_estoque.fillna(-999)


#prepara target
resposta = pd.DataFrame(dados_condenacao_geral['Pagamento Desindexado'])
resposta_cargo = pd.DataFrame(dados_condenacao_cargo['Pagamento Desindexado'])

#Construção do Modelo de Árvore de Decisão para Regressão - resposta numérica contínua
#Em cenários de classificação podemos usar a DecisionTreeClassifier
#É possível customizar critérios de parada através dos hiperparâmetros do modelo
DT = tree.DecisionTreeRegressor(random_state=42, 
                                max_depth=100, 
                                criterion='mae',
                                min_samples_leaf = 50)


#prepara target
resposta = pd.DataFrame(dados_condenacao_cargo['Pagamento Desindexado'])

DT = DT.fit(explicativas_cargo[['cluster_valor', 'Cluster Aging Tempo de Empresa', 'Cluster Aging', 'safra_reclamacao']],
            resposta_cargo['Pagamento Desindexado'])

y_true = resposta_cargo['Pagamento Desindexado']
#y_pred = valor previsto pelo modelo treinado
y_pred = DT.predict(explicativas_cargo[['cluster_valor', 'Cluster Aging Tempo de Empresa', 'Cluster Aging','safra_reclamacao']])

#Aplicação da predição no dataframe do estoque para obtenção dos valores de predição
dados_estoque_full = estoque_cargo
dados_estoque_full['prediction'] = DT.predict(explicativas_estoque[['cluster_valor', 'Cluster Aging Tempo de Empresa', 
                                                                    'Cluster Aging','safra_reclamacao']])

#Gera o recorte precificado do cargo utilizado
estoque_cargo_montador = estoque_cargo

"""
Gerar a modelagem de Outros Cargos, com 50 ramificações
"""

natureza_notin = ['TERCEIRO INSOLVENTE', 'SINDICATO / MINISTERIO PUBLICO','TERCEIRO SOLVENTE','ADMINISTRATIVO']
sub_area_direito_notin = ['PREVENTIVO AUTO DE INFRAÇÃO','CONTENCIOSO COLETIVO']
outlier_notin = ['Outlier']

dados_condenacao_cargo = dados[(dados['MOTIVO_ENC_AGRP'] == 'CONDENACAO')
                        & (~dados['NATUREZA_OPERACIONAL'].isin(natureza_notin))
                        & (~dados['SUB_AREA_DO_DIREITO'].isin(sub_area_direito_notin))
                        & (~dados['OUTLIER'].isin(outlier_notin))    
                            & (dados['cargo_tratado'] == 'OUTROS')      
                       ]

#Define o filtro para Estoque
ESTQ_natureza_notin = ['TERCEIRO INSOLVENTE']

estoque_cargo = estoque[(estoque['cargo_tratado'] == 'OUTROS')
                       & (~estoque['Natureza Operacional (M)'].isin(ESTQ_natureza_notin))
                       ]


#Cria um novo dataframe adequado ao scikit-learning para treinamento dos modelos
explicativas = pd.DataFrame()
explicativas['ID_PROCESSO'] = dados_condenacao_geral.ID_PROCESSO
explicativas_cargo = pd.DataFrame()
explicativas_cargo['ID_PROCESSO'] = dados_condenacao_cargo.ID_PROCESSO

explicativas_estoque = pd.DataFrame()
explicativas_estoque['ID PROCESSO'] = estoque_cargo['ID PROCESSO']



#Faz o Label Encoder, que converte dados qualitativos de texto para um índice numérico
#Com esse encoding, podemos facilmente voltar aos valores originais utilizando a função inverse_transform

#adiciona a variável Estado codificada ao dataframe
le_estado = preprocessing.LabelEncoder()
encode_estado = le_estado.fit(estoque['ESTADO'])
explicativas['ESTADO'] = encode_estado.transform(dados_condenacao_geral['ESTADO'])
explicativas_cargo['ESTADO'] = encode_estado.transform(dados_condenacao_cargo['ESTADO'])
explicativas_estoque['ESTADO'] = encode_estado.transform(estoque_cargo['ESTADO'])


#gera o de-para dos estados
estados = pd.DataFrame()
estados['codigos'] = explicativas_estoque.ESTADO.unique()
estados['estados'] = encode_estado.inverse_transform(estados.codigos)
estados.sort_values(by='codigos')


#adiciona a variável cluster valor codificada ao dataframe
le_cluster_valor = preprocessing.LabelEncoder()
encode_cluster_valor = le_cluster_valor.fit(dados_condenacao_geral['cluster_valor'])
explicativas['cluster_valor'] = encode_cluster_valor.transform(dados_condenacao_geral['cluster_valor'])
explicativas_cargo['cluster_valor'] = encode_cluster_valor.transform(dados_condenacao_cargo['cluster_valor'])
explicativas_estoque['cluster_valor'] = encode_cluster_valor.transform(estoque_cargo['cluster_valor'])

#gera o de-para dos cluster valor
cluster_valor = pd.DataFrame()
cluster_valor['codigos'] = explicativas.cluster_valor.unique()
cluster_valor['cluster_valor'] = encode_cluster_valor.inverse_transform(cluster_valor.codigos)
cluster_valor.sort_values(by='codigos')

#adiciona a variável cargo_tratado codificada ao dataframe
le_cargo_tratado = preprocessing.LabelEncoder()
encode_cargo_tratado = le_cargo_tratado.fit(dados_condenacao_geral['cargo_tratado'])
explicativas['cargo_tratado'] = encode_cargo_tratado.transform(dados_condenacao_geral['cargo_tratado'])
explicativas_cargo['cargo_tratado'] = encode_cargo_tratado.transform(dados_condenacao_cargo['cargo_tratado'])
explicativas_estoque['cargo_tratado'] = encode_cargo_tratado.transform(estoque_cargo['cargo_tratado'])


#gera o de-para dos cargos
cargo = pd.DataFrame()
cargo['codigos'] = explicativas.cargo_tratado.unique()
cargo['cargo'] = encode_cargo_tratado.inverse_transform(cargo.codigos)
cargo.sort_values(by='codigos')

#adiciona a variável Cluster Aging Tempo de Empresa codificada ao dataframe
le_tempo_empresa = preprocessing.LabelEncoder()
encode_tempo_empresa = le_tempo_empresa.fit(dados_condenacao_geral['Cluster Aging Tempo de Empresa'])
explicativas['Cluster Aging Tempo de Empresa'] = encode_tempo_empresa.transform(dados_condenacao_geral['Cluster Aging Tempo de Empresa'])
explicativas_cargo['Cluster Aging Tempo de Empresa'] = encode_tempo_empresa.transform(dados_condenacao_cargo['Cluster Aging Tempo de Empresa'])
explicativas_estoque['Cluster Aging Tempo de Empresa'] = encode_tempo_empresa.transform(estoque_cargo['Cluster Aging Tempo de Empresa'])

#gera o de-para dos cluster tempo de empresa
tempo_empresa = pd.DataFrame()
tempo_empresa['codigos'] = explicativas['Cluster Aging Tempo de Empresa'].unique()
tempo_empresa['tempo_empresa'] = encode_tempo_empresa.inverse_transform(tempo_empresa.codigos)
tempo_empresa.sort_values(by='codigos')

#adiciona a variável Cluster Aging codificada ao dataframe
le_cluster_aging = preprocessing.LabelEncoder()
encode_cluster_aging = le_cluster_aging.fit(dados_condenacao_geral['Cluster Aging'])
explicativas['Cluster Aging'] = encode_cluster_aging.transform(dados_condenacao_geral['Cluster Aging'])
explicativas_cargo['Cluster Aging'] = encode_cluster_aging.transform(dados_condenacao_cargo['Cluster Aging'])
explicativas_estoque['Cluster Aging'] = encode_cluster_aging.transform(estoque_cargo['Cluster Aging'])

#gera o de-para dos cluster aging
cluster_aging = pd.DataFrame()
cluster_aging['codigos'] = explicativas['Cluster Aging'].unique()
cluster_aging['cluster_aging'] = encode_cluster_aging.inverse_transform(cluster_aging.codigos)
cluster_aging.sort_values(by='codigos')

#adiciona a variável Safra de Reclamação codificada ao dataframe
le_safra_reclamacao = preprocessing.LabelEncoder()
encode_safra_reclamacao = le_safra_reclamacao.fit(estoque['Safra de Reclamação'].astype(str))
explicativas['safra_reclamacao'] = encode_safra_reclamacao.transform(dados_condenacao_geral['Safra de Reclamação'].astype(str))
dados_condenacao_geral['safra_reclamacao'] = encode_safra_reclamacao.transform(dados_condenacao_geral['Safra de Reclamação'].astype(str))
explicativas_cargo['safra_reclamacao'] = encode_safra_reclamacao.transform(dados_condenacao_cargo['Safra de Reclamação'].astype(str))
explicativas_estoque['safra_reclamacao'] = encode_safra_reclamacao.transform(estoque_cargo['Safra de Reclamação'].astype(str))

#gera o de-para dos cluster pedidos
safra_reclamacao = pd.DataFrame()
safra_reclamacao['codigos'] = explicativas_estoque['safra_reclamacao'].unique()
safra_reclamacao['safra_reclamacao'] = encode_safra_reclamacao.inverse_transform(safra_reclamacao.codigos)
safra_reclamacao.sort_values(by='codigos')

#substitui nulos nas variáveis qualitativas por -999
#Como estamos trabalhando com modelos de árvore, os valores sem dados serão tratados como uma categoria à parte, muito distante das demais
explicativas = explicativas.fillna(-999)
explicativas_cargo = explicativas_cargo.fillna(-999)
explicativas_estoque = explicativas_estoque.fillna(-999)


#prepara target
resposta = pd.DataFrame(dados_condenacao_geral['Pagamento Desindexado'])
resposta_cargo = pd.DataFrame(dados_condenacao_cargo['Pagamento Desindexado'])

#Construção do Modelo de Árvore de Decisão para Regressão - resposta numérica contínua
#Em cenários de classificação podemos usar a DecisionTreeClassifier
#É possível customizar critérios de parada através dos hiperparâmetros do modelo
DT = tree.DecisionTreeRegressor(random_state=42, 
                                max_depth=100, 
                                criterion='mae',
                                min_samples_leaf = 50)


#prepara target
resposta = pd.DataFrame(dados_condenacao_cargo['Pagamento Desindexado'])

DT = DT.fit(explicativas_cargo[['cluster_valor', 'Cluster Aging Tempo de Empresa', 'Cluster Aging', 'safra_reclamacao']],
            resposta_cargo['Pagamento Desindexado'])

y_true = resposta_cargo['Pagamento Desindexado']
#y_pred = valor previsto pelo modelo treinado
y_pred = DT.predict(explicativas_cargo[['cluster_valor', 'Cluster Aging Tempo de Empresa', 'Cluster Aging','safra_reclamacao']])

#Aplicação da predição no dataframe do estoque para obtenção dos valores de predição
dados_estoque_full = estoque_cargo
dados_estoque_full['prediction'] = DT.predict(explicativas_estoque[['cluster_valor', 'Cluster Aging Tempo de Empresa', 
                                                                    'Cluster Aging','safra_reclamacao']])

#Gera o recorte precificado do cargo utilizado
estoque_cargo_outros = estoque_cargo

"""
Gerar a modelagem do cargo Ajudante, com 50 ramificações
"""

natureza_notin = ['TERCEIRO INSOLVENTE', 'SINDICATO / MINISTERIO PUBLICO','TERCEIRO SOLVENTE','ADMINISTRATIVO']
sub_area_direito_notin = ['PREVENTIVO AUTO DE INFRAÇÃO','CONTENCIOSO COLETIVO']
outlier_notin = ['Outlier']

dados_condenacao_cargo = dados[(dados['MOTIVO_ENC_AGRP'] == 'CONDENACAO')
                        & (~dados['NATUREZA_OPERACIONAL'].isin(natureza_notin))
                        & (~dados['SUB_AREA_DO_DIREITO'].isin(sub_area_direito_notin))
                        & (~dados['OUTLIER'].isin(outlier_notin))    
                            & (dados['cargo_tratado'] == 'AJUDANTE')      
                       ]

#Define o filtro para Estoque
ESTQ_natureza_notin = ['TERCEIRO INSOLVENTE']

estoque_cargo = estoque[(estoque['cargo_tratado'] == 'AJUDANTE')
                       & (~estoque['Natureza Operacional (M)'].isin(ESTQ_natureza_notin))
                       ]


#Cria um novo dataframe adequado ao scikit-learning para treinamento dos modelos
explicativas = pd.DataFrame()
explicativas['ID_PROCESSO'] = dados_condenacao_geral.ID_PROCESSO
explicativas_cargo = pd.DataFrame()
explicativas_cargo['ID_PROCESSO'] = dados_condenacao_cargo.ID_PROCESSO

explicativas_estoque = pd.DataFrame()
explicativas_estoque['ID PROCESSO'] = estoque_cargo['ID PROCESSO']



#Faz o Label Encoder, que converte dados qualitativos de texto para um índice numérico
#Com esse encoding, podemos facilmente voltar aos valores originais utilizando a função inverse_transform

#adiciona a variável Estado codificada ao dataframe
le_estado = preprocessing.LabelEncoder()
encode_estado = le_estado.fit(estoque['ESTADO'])
explicativas['ESTADO'] = encode_estado.transform(dados_condenacao_geral['ESTADO'])
explicativas_cargo['ESTADO'] = encode_estado.transform(dados_condenacao_cargo['ESTADO'])
explicativas_estoque['ESTADO'] = encode_estado.transform(estoque_cargo['ESTADO'])


#gera o de-para dos estados
estados = pd.DataFrame()
estados['codigos'] = explicativas_estoque.ESTADO.unique()
estados['estados'] = encode_estado.inverse_transform(estados.codigos)
estados.sort_values(by='codigos')


#adiciona a variável cluster valor codificada ao dataframe
le_cluster_valor = preprocessing.LabelEncoder()
encode_cluster_valor = le_cluster_valor.fit(dados_condenacao_geral['cluster_valor'])
explicativas['cluster_valor'] = encode_cluster_valor.transform(dados_condenacao_geral['cluster_valor'])
explicativas_cargo['cluster_valor'] = encode_cluster_valor.transform(dados_condenacao_cargo['cluster_valor'])
explicativas_estoque['cluster_valor'] = encode_cluster_valor.transform(estoque_cargo['cluster_valor'])

#gera o de-para dos cluster valor
cluster_valor = pd.DataFrame()
cluster_valor['codigos'] = explicativas.cluster_valor.unique()
cluster_valor['cluster_valor'] = encode_cluster_valor.inverse_transform(cluster_valor.codigos)
cluster_valor.sort_values(by='codigos')

#adiciona a variável cargo_tratado codificada ao dataframe
le_cargo_tratado = preprocessing.LabelEncoder()
encode_cargo_tratado = le_cargo_tratado.fit(dados_condenacao_geral['cargo_tratado'])
explicativas['cargo_tratado'] = encode_cargo_tratado.transform(dados_condenacao_geral['cargo_tratado'])
explicativas_cargo['cargo_tratado'] = encode_cargo_tratado.transform(dados_condenacao_cargo['cargo_tratado'])
explicativas_estoque['cargo_tratado'] = encode_cargo_tratado.transform(estoque_cargo['cargo_tratado'])


#gera o de-para dos cargos
cargo = pd.DataFrame()
cargo['codigos'] = explicativas.cargo_tratado.unique()
cargo['cargo'] = encode_cargo_tratado.inverse_transform(cargo.codigos)
cargo.sort_values(by='codigos')

#adiciona a variável Cluster Aging Tempo de Empresa codificada ao dataframe
le_tempo_empresa = preprocessing.LabelEncoder()
encode_tempo_empresa = le_tempo_empresa.fit(dados_condenacao_geral['Cluster Aging Tempo de Empresa'])
explicativas['Cluster Aging Tempo de Empresa'] = encode_tempo_empresa.transform(dados_condenacao_geral['Cluster Aging Tempo de Empresa'])
explicativas_cargo['Cluster Aging Tempo de Empresa'] = encode_tempo_empresa.transform(dados_condenacao_cargo['Cluster Aging Tempo de Empresa'])
explicativas_estoque['Cluster Aging Tempo de Empresa'] = encode_tempo_empresa.transform(estoque_cargo['Cluster Aging Tempo de Empresa'])

#gera o de-para dos cluster tempo de empresa
tempo_empresa = pd.DataFrame()
tempo_empresa['codigos'] = explicativas['Cluster Aging Tempo de Empresa'].unique()
tempo_empresa['tempo_empresa'] = encode_tempo_empresa.inverse_transform(tempo_empresa.codigos)
tempo_empresa.sort_values(by='codigos')

#adiciona a variável Cluster Aging codificada ao dataframe
le_cluster_aging = preprocessing.LabelEncoder()
encode_cluster_aging = le_cluster_aging.fit(dados_condenacao_geral['Cluster Aging'])
explicativas['Cluster Aging'] = encode_cluster_aging.transform(dados_condenacao_geral['Cluster Aging'])
explicativas_cargo['Cluster Aging'] = encode_cluster_aging.transform(dados_condenacao_cargo['Cluster Aging'])
explicativas_estoque['Cluster Aging'] = encode_cluster_aging.transform(estoque_cargo['Cluster Aging'])

#gera o de-para dos cluster aging
cluster_aging = pd.DataFrame()
cluster_aging['codigos'] = explicativas['Cluster Aging'].unique()
cluster_aging['cluster_aging'] = encode_cluster_aging.inverse_transform(cluster_aging.codigos)
cluster_aging.sort_values(by='codigos')

#adiciona a variável Safra de Reclamação codificada ao dataframe
le_safra_reclamacao = preprocessing.LabelEncoder()
encode_safra_reclamacao = le_safra_reclamacao.fit(estoque['Safra de Reclamação'].astype(str))
explicativas['safra_reclamacao'] = encode_safra_reclamacao.transform(dados_condenacao_geral['Safra de Reclamação'].astype(str))
dados_condenacao_geral['safra_reclamacao'] = encode_safra_reclamacao.transform(dados_condenacao_geral['Safra de Reclamação'].astype(str))
explicativas_cargo['safra_reclamacao'] = encode_safra_reclamacao.transform(dados_condenacao_cargo['Safra de Reclamação'].astype(str))
explicativas_estoque['safra_reclamacao'] = encode_safra_reclamacao.transform(estoque_cargo['Safra de Reclamação'].astype(str))

#gera o de-para dos cluster pedidos
safra_reclamacao = pd.DataFrame()
safra_reclamacao['codigos'] = explicativas_estoque['safra_reclamacao'].unique()
safra_reclamacao['safra_reclamacao'] = encode_safra_reclamacao.inverse_transform(safra_reclamacao.codigos)
safra_reclamacao.sort_values(by='codigos')

#substitui nulos nas variáveis qualitativas por -999
#Como estamos trabalhando com modelos de árvore, os valores sem dados serão tratados como uma categoria à parte, muito distante das demais
explicativas = explicativas.fillna(-999)
explicativas_cargo = explicativas_cargo.fillna(-999)
explicativas_estoque = explicativas_estoque.fillna(-999)


#prepara target
resposta = pd.DataFrame(dados_condenacao_geral['Pagamento Desindexado'])
resposta_cargo = pd.DataFrame(dados_condenacao_cargo['Pagamento Desindexado'])

#Construção do Modelo de Árvore de Decisão para Regressão - resposta numérica contínua
#Em cenários de classificação podemos usar a DecisionTreeClassifier
#É possível customizar critérios de parada através dos hiperparâmetros do modelo
DT = tree.DecisionTreeRegressor(random_state=42, 
                                max_depth=100, 
                                criterion='mae',
                                min_samples_leaf = 50)


#prepara target
resposta = pd.DataFrame(dados_condenacao_cargo['Pagamento Desindexado'])

DT = DT.fit(explicativas_cargo[['cluster_valor', 'Cluster Aging Tempo de Empresa', 'Cluster Aging', 'safra_reclamacao']],
            resposta_cargo['Pagamento Desindexado'])

y_true = resposta_cargo['Pagamento Desindexado']
#y_pred = valor previsto pelo modelo treinado
y_pred = DT.predict(explicativas_cargo[['cluster_valor', 'Cluster Aging Tempo de Empresa', 'Cluster Aging','safra_reclamacao']])

#Aplicação da predição no dataframe do estoque para obtenção dos valores de predição
dados_estoque_full = estoque_cargo
dados_estoque_full['prediction'] = DT.predict(explicativas_estoque[['cluster_valor', 'Cluster Aging Tempo de Empresa', 
                                                                    'Cluster Aging','safra_reclamacao']])

#Gera o recorte precificado do cargo utilizado
estoque_cargo_ajudante = estoque_cargo
"""
Gerar a modelagem do cargo Ajudante Externo, com 50 ramificações
"""

natureza_notin = ['TERCEIRO INSOLVENTE', 'SINDICATO / MINISTERIO PUBLICO','TERCEIRO SOLVENTE','ADMINISTRATIVO']
sub_area_direito_notin = ['PREVENTIVO AUTO DE INFRAÇÃO','CONTENCIOSO COLETIVO']
outlier_notin = ['Outlier']

dados_condenacao_cargo = dados[(dados['MOTIVO_ENC_AGRP'] == 'CONDENACAO')
                        & (~dados['NATUREZA_OPERACIONAL'].isin(natureza_notin))
                        & (~dados['SUB_AREA_DO_DIREITO'].isin(sub_area_direito_notin))
                        & (~dados['OUTLIER'].isin(outlier_notin))    
                            & (dados['cargo_tratado'] == 'AJUDANTE EXTERNO')      
                       ]

#Define o filtro para Estoque
ESTQ_natureza_notin = ['TERCEIRO INSOLVENTE']

estoque_cargo = estoque[(estoque['cargo_tratado'] == 'AJUDANTE EXTERNO')
                       & (~estoque['Natureza Operacional (M)'].isin(ESTQ_natureza_notin))
                       ]


#Cria um novo dataframe adequado ao scikit-learning para treinamento dos modelos
explicativas = pd.DataFrame()
explicativas['ID_PROCESSO'] = dados_condenacao_geral.ID_PROCESSO
explicativas_cargo = pd.DataFrame()
explicativas_cargo['ID_PROCESSO'] = dados_condenacao_cargo.ID_PROCESSO

explicativas_estoque = pd.DataFrame()
explicativas_estoque['ID PROCESSO'] = estoque_cargo['ID PROCESSO']



#Faz o Label Encoder, que converte dados qualitativos de texto para um índice numérico
#Com esse encoding, podemos facilmente voltar aos valores originais utilizando a função inverse_transform

#adiciona a variável Estado codificada ao dataframe
le_estado = preprocessing.LabelEncoder()
encode_estado = le_estado.fit(estoque['ESTADO'])
explicativas['ESTADO'] = encode_estado.transform(dados_condenacao_geral['ESTADO'])
explicativas_cargo['ESTADO'] = encode_estado.transform(dados_condenacao_cargo['ESTADO'])
explicativas_estoque['ESTADO'] = encode_estado.transform(estoque_cargo['ESTADO'])


#gera o de-para dos estados
estados = pd.DataFrame()
estados['codigos'] = explicativas_estoque.ESTADO.unique()
estados['estados'] = encode_estado.inverse_transform(estados.codigos)
estados.sort_values(by='codigos')


#adiciona a variável cluster valor codificada ao dataframe
le_cluster_valor = preprocessing.LabelEncoder()
encode_cluster_valor = le_cluster_valor.fit(dados_condenacao_geral['cluster_valor'])
explicativas['cluster_valor'] = encode_cluster_valor.transform(dados_condenacao_geral['cluster_valor'])
explicativas_cargo['cluster_valor'] = encode_cluster_valor.transform(dados_condenacao_cargo['cluster_valor'])
explicativas_estoque['cluster_valor'] = encode_cluster_valor.transform(estoque_cargo['cluster_valor'])

#gera o de-para dos cluster valor
cluster_valor = pd.DataFrame()
cluster_valor['codigos'] = explicativas.cluster_valor.unique()
cluster_valor['cluster_valor'] = encode_cluster_valor.inverse_transform(cluster_valor.codigos)
cluster_valor.sort_values(by='codigos')

#adiciona a variável cargo_tratado codificada ao dataframe
le_cargo_tratado = preprocessing.LabelEncoder()
encode_cargo_tratado = le_cargo_tratado.fit(dados_condenacao_geral['cargo_tratado'])
explicativas['cargo_tratado'] = encode_cargo_tratado.transform(dados_condenacao_geral['cargo_tratado'])
explicativas_cargo['cargo_tratado'] = encode_cargo_tratado.transform(dados_condenacao_cargo['cargo_tratado'])
explicativas_estoque['cargo_tratado'] = encode_cargo_tratado.transform(estoque_cargo['cargo_tratado'])


#gera o de-para dos cargos
cargo = pd.DataFrame()
cargo['codigos'] = explicativas.cargo_tratado.unique()
cargo['cargo'] = encode_cargo_tratado.inverse_transform(cargo.codigos)
cargo.sort_values(by='codigos')

#adiciona a variável Cluster Aging Tempo de Empresa codificada ao dataframe
le_tempo_empresa = preprocessing.LabelEncoder()
encode_tempo_empresa = le_tempo_empresa.fit(dados_condenacao_geral['Cluster Aging Tempo de Empresa'])
explicativas['Cluster Aging Tempo de Empresa'] = encode_tempo_empresa.transform(dados_condenacao_geral['Cluster Aging Tempo de Empresa'])
explicativas_cargo['Cluster Aging Tempo de Empresa'] = encode_tempo_empresa.transform(dados_condenacao_cargo['Cluster Aging Tempo de Empresa'])
explicativas_estoque['Cluster Aging Tempo de Empresa'] = encode_tempo_empresa.transform(estoque_cargo['Cluster Aging Tempo de Empresa'])

#gera o de-para dos cluster tempo de empresa
tempo_empresa = pd.DataFrame()
tempo_empresa['codigos'] = explicativas['Cluster Aging Tempo de Empresa'].unique()
tempo_empresa['tempo_empresa'] = encode_tempo_empresa.inverse_transform(tempo_empresa.codigos)
tempo_empresa.sort_values(by='codigos')

#adiciona a variável Cluster Aging codificada ao dataframe
le_cluster_aging = preprocessing.LabelEncoder()
encode_cluster_aging = le_cluster_aging.fit(dados_condenacao_geral['Cluster Aging'])
explicativas['Cluster Aging'] = encode_cluster_aging.transform(dados_condenacao_geral['Cluster Aging'])
explicativas_cargo['Cluster Aging'] = encode_cluster_aging.transform(dados_condenacao_cargo['Cluster Aging'])
explicativas_estoque['Cluster Aging'] = encode_cluster_aging.transform(estoque_cargo['Cluster Aging'])

#gera o de-para dos cluster aging
cluster_aging = pd.DataFrame()
cluster_aging['codigos'] = explicativas['Cluster Aging'].unique()
cluster_aging['cluster_aging'] = encode_cluster_aging.inverse_transform(cluster_aging.codigos)
cluster_aging.sort_values(by='codigos')

#adiciona a variável Safra de Reclamação codificada ao dataframe
le_safra_reclamacao = preprocessing.LabelEncoder()
encode_safra_reclamacao = le_safra_reclamacao.fit(estoque['Safra de Reclamação'].astype(str))
explicativas['safra_reclamacao'] = encode_safra_reclamacao.transform(dados_condenacao_geral['Safra de Reclamação'].astype(str))
dados_condenacao_geral['safra_reclamacao'] = encode_safra_reclamacao.transform(dados_condenacao_geral['Safra de Reclamação'].astype(str))
explicativas_cargo['safra_reclamacao'] = encode_safra_reclamacao.transform(dados_condenacao_cargo['Safra de Reclamação'].astype(str))
explicativas_estoque['safra_reclamacao'] = encode_safra_reclamacao.transform(estoque_cargo['Safra de Reclamação'].astype(str))

#gera o de-para dos cluster pedidos
safra_reclamacao = pd.DataFrame()
safra_reclamacao['codigos'] = explicativas_estoque['safra_reclamacao'].unique()
safra_reclamacao['safra_reclamacao'] = encode_safra_reclamacao.inverse_transform(safra_reclamacao.codigos)
safra_reclamacao.sort_values(by='codigos')

#substitui nulos nas variáveis qualitativas por -999
#Como estamos trabalhando com modelos de árvore, os valores sem dados serão tratados como uma categoria à parte, muito distante das demais
explicativas = explicativas.fillna(-999)
explicativas_cargo = explicativas_cargo.fillna(-999)
explicativas_estoque = explicativas_estoque.fillna(-999)


#prepara target
resposta = pd.DataFrame(dados_condenacao_geral['Pagamento Desindexado'])
resposta_cargo = pd.DataFrame(dados_condenacao_cargo['Pagamento Desindexado'])

#Construção do Modelo de Árvore de Decisão para Regressão - resposta numérica contínua
#Em cenários de classificação podemos usar a DecisionTreeClassifier
#É possível customizar critérios de parada através dos hiperparâmetros do modelo
DT = tree.DecisionTreeRegressor(random_state=42, 
                                max_depth=100, 
                                criterion='mae',
                                min_samples_leaf = 50)


#prepara target
resposta = pd.DataFrame(dados_condenacao_cargo['Pagamento Desindexado'])

DT = DT.fit(explicativas_cargo[['cluster_valor', 'Cluster Aging Tempo de Empresa', 'Cluster Aging', 'safra_reclamacao']],
            resposta_cargo['Pagamento Desindexado'])

y_true = resposta_cargo['Pagamento Desindexado']
#y_pred = valor previsto pelo modelo treinado
y_pred = DT.predict(explicativas_cargo[['cluster_valor', 'Cluster Aging Tempo de Empresa', 'Cluster Aging','safra_reclamacao']])

#Aplicação da predição no dataframe do estoque para obtenção dos valores de predição
dados_estoque_full = estoque_cargo
dados_estoque_full['prediction'] = DT.predict(explicativas_estoque[['cluster_valor', 'Cluster Aging Tempo de Empresa', 
                                                                    'Cluster Aging','safra_reclamacao']])

#Gera o recorte precificado do cargo utilizado
estoque_cargo_ajudanteexterno = estoque_cargo

"""
Gerar a modelagem do cargo Auxiliar, com 50 ramificações
"""

natureza_notin = ['TERCEIRO INSOLVENTE', 'SINDICATO / MINISTERIO PUBLICO','TERCEIRO SOLVENTE','ADMINISTRATIVO']
sub_area_direito_notin = ['PREVENTIVO AUTO DE INFRAÇÃO','CONTENCIOSO COLETIVO']
outlier_notin = ['Outlier']

dados_condenacao_cargo = dados[(dados['MOTIVO_ENC_AGRP'] == 'CONDENACAO')
                        & (~dados['NATUREZA_OPERACIONAL'].isin(natureza_notin))
                        & (~dados['SUB_AREA_DO_DIREITO'].isin(sub_area_direito_notin))
                        & (~dados['OUTLIER'].isin(outlier_notin))    
                            & (dados['cargo_tratado'] == 'AUXILIAR')      
                       ]

#Define o filtro para Estoque
ESTQ_natureza_notin = ['TERCEIRO INSOLVENTE']

estoque_cargo = estoque[(estoque['cargo_tratado'] == 'AUXILIAR')
                       & (~estoque['Natureza Operacional (M)'].isin(ESTQ_natureza_notin))
                       ]


#Cria um novo dataframe adequado ao scikit-learning para treinamento dos modelos
explicativas = pd.DataFrame()
explicativas['ID_PROCESSO'] = dados_condenacao_geral.ID_PROCESSO
explicativas_cargo = pd.DataFrame()
explicativas_cargo['ID_PROCESSO'] = dados_condenacao_cargo.ID_PROCESSO

explicativas_estoque = pd.DataFrame()
explicativas_estoque['ID PROCESSO'] = estoque_cargo['ID PROCESSO']



#Faz o Label Encoder, que converte dados qualitativos de texto para um índice numérico
#Com esse encoding, podemos facilmente voltar aos valores originais utilizando a função inverse_transform

#adiciona a variável Estado codificada ao dataframe
le_estado = preprocessing.LabelEncoder()
encode_estado = le_estado.fit(estoque['ESTADO'])
explicativas['ESTADO'] = encode_estado.transform(dados_condenacao_geral['ESTADO'])
explicativas_cargo['ESTADO'] = encode_estado.transform(dados_condenacao_cargo['ESTADO'])
explicativas_estoque['ESTADO'] = encode_estado.transform(estoque_cargo['ESTADO'])


#gera o de-para dos estados
estados = pd.DataFrame()
estados['codigos'] = explicativas_estoque.ESTADO.unique()
estados['estados'] = encode_estado.inverse_transform(estados.codigos)
estados.sort_values(by='codigos')


#adiciona a variável cluster valor codificada ao dataframe
le_cluster_valor = preprocessing.LabelEncoder()
encode_cluster_valor = le_cluster_valor.fit(dados_condenacao_geral['cluster_valor'])
explicativas['cluster_valor'] = encode_cluster_valor.transform(dados_condenacao_geral['cluster_valor'])
explicativas_cargo['cluster_valor'] = encode_cluster_valor.transform(dados_condenacao_cargo['cluster_valor'])
explicativas_estoque['cluster_valor'] = encode_cluster_valor.transform(estoque_cargo['cluster_valor'])

#gera o de-para dos cluster valor
cluster_valor = pd.DataFrame()
cluster_valor['codigos'] = explicativas.cluster_valor.unique()
cluster_valor['cluster_valor'] = encode_cluster_valor.inverse_transform(cluster_valor.codigos)
cluster_valor.sort_values(by='codigos')

#adiciona a variável cargo_tratado codificada ao dataframe
le_cargo_tratado = preprocessing.LabelEncoder()
encode_cargo_tratado = le_cargo_tratado.fit(dados_condenacao_geral['cargo_tratado'])
explicativas['cargo_tratado'] = encode_cargo_tratado.transform(dados_condenacao_geral['cargo_tratado'])
explicativas_cargo['cargo_tratado'] = encode_cargo_tratado.transform(dados_condenacao_cargo['cargo_tratado'])
explicativas_estoque['cargo_tratado'] = encode_cargo_tratado.transform(estoque_cargo['cargo_tratado'])


#gera o de-para dos cargos
cargo = pd.DataFrame()
cargo['codigos'] = explicativas.cargo_tratado.unique()
cargo['cargo'] = encode_cargo_tratado.inverse_transform(cargo.codigos)
cargo.sort_values(by='codigos')

#adiciona a variável Cluster Aging Tempo de Empresa codificada ao dataframe
le_tempo_empresa = preprocessing.LabelEncoder()
encode_tempo_empresa = le_tempo_empresa.fit(dados_condenacao_geral['Cluster Aging Tempo de Empresa'])
explicativas['Cluster Aging Tempo de Empresa'] = encode_tempo_empresa.transform(dados_condenacao_geral['Cluster Aging Tempo de Empresa'])
explicativas_cargo['Cluster Aging Tempo de Empresa'] = encode_tempo_empresa.transform(dados_condenacao_cargo['Cluster Aging Tempo de Empresa'])
explicativas_estoque['Cluster Aging Tempo de Empresa'] = encode_tempo_empresa.transform(estoque_cargo['Cluster Aging Tempo de Empresa'])

#gera o de-para dos cluster tempo de empresa
tempo_empresa = pd.DataFrame()
tempo_empresa['codigos'] = explicativas['Cluster Aging Tempo de Empresa'].unique()
tempo_empresa['tempo_empresa'] = encode_tempo_empresa.inverse_transform(tempo_empresa.codigos)
tempo_empresa.sort_values(by='codigos')

#adiciona a variável Cluster Aging codificada ao dataframe
le_cluster_aging = preprocessing.LabelEncoder()
encode_cluster_aging = le_cluster_aging.fit(dados_condenacao_geral['Cluster Aging'])
explicativas['Cluster Aging'] = encode_cluster_aging.transform(dados_condenacao_geral['Cluster Aging'])
explicativas_cargo['Cluster Aging'] = encode_cluster_aging.transform(dados_condenacao_cargo['Cluster Aging'])
explicativas_estoque['Cluster Aging'] = encode_cluster_aging.transform(estoque_cargo['Cluster Aging'])

#gera o de-para dos cluster aging
cluster_aging = pd.DataFrame()
cluster_aging['codigos'] = explicativas['Cluster Aging'].unique()
cluster_aging['cluster_aging'] = encode_cluster_aging.inverse_transform(cluster_aging.codigos)
cluster_aging.sort_values(by='codigos')

#adiciona a variável Safra de Reclamação codificada ao dataframe
le_safra_reclamacao = preprocessing.LabelEncoder()
encode_safra_reclamacao = le_safra_reclamacao.fit(estoque['Safra de Reclamação'].astype(str))
explicativas['safra_reclamacao'] = encode_safra_reclamacao.transform(dados_condenacao_geral['Safra de Reclamação'].astype(str))
dados_condenacao_geral['safra_reclamacao'] = encode_safra_reclamacao.transform(dados_condenacao_geral['Safra de Reclamação'].astype(str))
explicativas_cargo['safra_reclamacao'] = encode_safra_reclamacao.transform(dados_condenacao_cargo['Safra de Reclamação'].astype(str))
explicativas_estoque['safra_reclamacao'] = encode_safra_reclamacao.transform(estoque_cargo['Safra de Reclamação'].astype(str))

#gera o de-para dos cluster pedidos
safra_reclamacao = pd.DataFrame()
safra_reclamacao['codigos'] = explicativas_estoque['safra_reclamacao'].unique()
safra_reclamacao['safra_reclamacao'] = encode_safra_reclamacao.inverse_transform(safra_reclamacao.codigos)
safra_reclamacao.sort_values(by='codigos')

#substitui nulos nas variáveis qualitativas por -999
#Como estamos trabalhando com modelos de árvore, os valores sem dados serão tratados como uma categoria à parte, muito distante das demais
explicativas = explicativas.fillna(-999)
explicativas_cargo = explicativas_cargo.fillna(-999)
explicativas_estoque = explicativas_estoque.fillna(-999)


#prepara target
resposta = pd.DataFrame(dados_condenacao_geral['Pagamento Desindexado'])
resposta_cargo = pd.DataFrame(dados_condenacao_cargo['Pagamento Desindexado'])

#Construção do Modelo de Árvore de Decisão para Regressão - resposta numérica contínua
#Em cenários de classificação podemos usar a DecisionTreeClassifier
#É possível customizar critérios de parada através dos hiperparâmetros do modelo
DT = tree.DecisionTreeRegressor(random_state=42, 
                                max_depth=100, 
                                criterion='mae',
                                min_samples_leaf = 50)


#prepara target
resposta = pd.DataFrame(dados_condenacao_cargo['Pagamento Desindexado'])

DT = DT.fit(explicativas_cargo[['cluster_valor', 'Cluster Aging Tempo de Empresa', 'Cluster Aging', 'safra_reclamacao']],
            resposta_cargo['Pagamento Desindexado'])

y_true = resposta_cargo['Pagamento Desindexado']
#y_pred = valor previsto pelo modelo treinado
y_pred = DT.predict(explicativas_cargo[['cluster_valor', 'Cluster Aging Tempo de Empresa', 'Cluster Aging','safra_reclamacao']])

#Aplicação da predição no dataframe do estoque para obtenção dos valores de predição
dados_estoque_full = estoque_cargo
dados_estoque_full['prediction'] = DT.predict(explicativas_estoque[['cluster_valor', 'Cluster Aging Tempo de Empresa', 
                                                                    'Cluster Aging','safra_reclamacao']])

#Gera o recorte precificado do cargo utilizado
estoque_cargo_auxiliar = estoque_cargo

"""
Gerar a modelagem do cargo Motorista, com 50 ramificações
"""

natureza_notin = ['TERCEIRO INSOLVENTE', 'SINDICATO / MINISTERIO PUBLICO','TERCEIRO SOLVENTE','ADMINISTRATIVO']
sub_area_direito_notin = ['PREVENTIVO AUTO DE INFRAÇÃO','CONTENCIOSO COLETIVO']
outlier_notin = ['Outlier']

dados_condenacao_cargo = dados[(dados['MOTIVO_ENC_AGRP'] == 'CONDENACAO')
                        & (~dados['NATUREZA_OPERACIONAL'].isin(natureza_notin))
                        & (~dados['SUB_AREA_DO_DIREITO'].isin(sub_area_direito_notin))
                        & (~dados['OUTLIER'].isin(outlier_notin))    
                            & (dados['cargo_tratado'] == 'MOTORISTA')      
                       ]

#Define o filtro para Estoque
ESTQ_natureza_notin = ['TERCEIRO INSOLVENTE']

estoque_cargo = estoque[(estoque['cargo_tratado'] == 'MOTORISTA')
                       & (~estoque['Natureza Operacional (M)'].isin(ESTQ_natureza_notin))
                       ]


#Cria um novo dataframe adequado ao scikit-learning para treinamento dos modelos
explicativas = pd.DataFrame()
explicativas['ID_PROCESSO'] = dados_condenacao_geral.ID_PROCESSO
explicativas_cargo = pd.DataFrame()
explicativas_cargo['ID_PROCESSO'] = dados_condenacao_cargo.ID_PROCESSO

explicativas_estoque = pd.DataFrame()
explicativas_estoque['ID PROCESSO'] = estoque_cargo['ID PROCESSO']



#Faz o Label Encoder, que converte dados qualitativos de texto para um índice numérico
#Com esse encoding, podemos facilmente voltar aos valores originais utilizando a função inverse_transform

#adiciona a variável Estado codificada ao dataframe
le_estado = preprocessing.LabelEncoder()
encode_estado = le_estado.fit(estoque['ESTADO'])
explicativas['ESTADO'] = encode_estado.transform(dados_condenacao_geral['ESTADO'])
explicativas_cargo['ESTADO'] = encode_estado.transform(dados_condenacao_cargo['ESTADO'])
explicativas_estoque['ESTADO'] = encode_estado.transform(estoque_cargo['ESTADO'])


#gera o de-para dos estados
estados = pd.DataFrame()
estados['codigos'] = explicativas_estoque.ESTADO.unique()
estados['estados'] = encode_estado.inverse_transform(estados.codigos)
estados.sort_values(by='codigos')


#adiciona a variável cluster valor codificada ao dataframe
le_cluster_valor = preprocessing.LabelEncoder()
encode_cluster_valor = le_cluster_valor.fit(dados_condenacao_geral['cluster_valor'])
explicativas['cluster_valor'] = encode_cluster_valor.transform(dados_condenacao_geral['cluster_valor'])
explicativas_cargo['cluster_valor'] = encode_cluster_valor.transform(dados_condenacao_cargo['cluster_valor'])
explicativas_estoque['cluster_valor'] = encode_cluster_valor.transform(estoque_cargo['cluster_valor'])

#gera o de-para dos cluster valor
cluster_valor = pd.DataFrame()
cluster_valor['codigos'] = explicativas.cluster_valor.unique()
cluster_valor['cluster_valor'] = encode_cluster_valor.inverse_transform(cluster_valor.codigos)
cluster_valor.sort_values(by='codigos')

#adiciona a variável cargo_tratado codificada ao dataframe
le_cargo_tratado = preprocessing.LabelEncoder()
encode_cargo_tratado = le_cargo_tratado.fit(dados_condenacao_geral['cargo_tratado'])
explicativas['cargo_tratado'] = encode_cargo_tratado.transform(dados_condenacao_geral['cargo_tratado'])
explicativas_cargo['cargo_tratado'] = encode_cargo_tratado.transform(dados_condenacao_cargo['cargo_tratado'])
explicativas_estoque['cargo_tratado'] = encode_cargo_tratado.transform(estoque_cargo['cargo_tratado'])


#gera o de-para dos cargos
cargo = pd.DataFrame()
cargo['codigos'] = explicativas.cargo_tratado.unique()
cargo['cargo'] = encode_cargo_tratado.inverse_transform(cargo.codigos)
cargo.sort_values(by='codigos')

#adiciona a variável Cluster Aging Tempo de Empresa codificada ao dataframe
le_tempo_empresa = preprocessing.LabelEncoder()
encode_tempo_empresa = le_tempo_empresa.fit(dados_condenacao_geral['Cluster Aging Tempo de Empresa'])
explicativas['Cluster Aging Tempo de Empresa'] = encode_tempo_empresa.transform(dados_condenacao_geral['Cluster Aging Tempo de Empresa'])
explicativas_cargo['Cluster Aging Tempo de Empresa'] = encode_tempo_empresa.transform(dados_condenacao_cargo['Cluster Aging Tempo de Empresa'])
explicativas_estoque['Cluster Aging Tempo de Empresa'] = encode_tempo_empresa.transform(estoque_cargo['Cluster Aging Tempo de Empresa'])

#gera o de-para dos cluster tempo de empresa
tempo_empresa = pd.DataFrame()
tempo_empresa['codigos'] = explicativas['Cluster Aging Tempo de Empresa'].unique()
tempo_empresa['tempo_empresa'] = encode_tempo_empresa.inverse_transform(tempo_empresa.codigos)
tempo_empresa.sort_values(by='codigos')

#adiciona a variável Cluster Aging codificada ao dataframe
le_cluster_aging = preprocessing.LabelEncoder()
encode_cluster_aging = le_cluster_aging.fit(dados_condenacao_geral['Cluster Aging'])
explicativas['Cluster Aging'] = encode_cluster_aging.transform(dados_condenacao_geral['Cluster Aging'])
explicativas_cargo['Cluster Aging'] = encode_cluster_aging.transform(dados_condenacao_cargo['Cluster Aging'])
explicativas_estoque['Cluster Aging'] = encode_cluster_aging.transform(estoque_cargo['Cluster Aging'])

#gera o de-para dos cluster aging
cluster_aging = pd.DataFrame()
cluster_aging['codigos'] = explicativas['Cluster Aging'].unique()
cluster_aging['cluster_aging'] = encode_cluster_aging.inverse_transform(cluster_aging.codigos)
cluster_aging.sort_values(by='codigos')

#adiciona a variável Safra de Reclamação codificada ao dataframe
le_safra_reclamacao = preprocessing.LabelEncoder()
encode_safra_reclamacao = le_safra_reclamacao.fit(estoque['Safra de Reclamação'].astype(str))
explicativas['safra_reclamacao'] = encode_safra_reclamacao.transform(dados_condenacao_geral['Safra de Reclamação'].astype(str))
dados_condenacao_geral['safra_reclamacao'] = encode_safra_reclamacao.transform(dados_condenacao_geral['Safra de Reclamação'].astype(str))
explicativas_cargo['safra_reclamacao'] = encode_safra_reclamacao.transform(dados_condenacao_cargo['Safra de Reclamação'].astype(str))
explicativas_estoque['safra_reclamacao'] = encode_safra_reclamacao.transform(estoque_cargo['Safra de Reclamação'].astype(str))

#gera o de-para dos cluster pedidos
safra_reclamacao = pd.DataFrame()
safra_reclamacao['codigos'] = explicativas_estoque['safra_reclamacao'].unique()
safra_reclamacao['safra_reclamacao'] = encode_safra_reclamacao.inverse_transform(safra_reclamacao.codigos)
safra_reclamacao.sort_values(by='codigos')

#substitui nulos nas variáveis qualitativas por -999
#Como estamos trabalhando com modelos de árvore, os valores sem dados serão tratados como uma categoria à parte, muito distante das demais
explicativas = explicativas.fillna(-999)
explicativas_cargo = explicativas_cargo.fillna(-999)
explicativas_estoque = explicativas_estoque.fillna(-999)


#prepara target
resposta = pd.DataFrame(dados_condenacao_geral['Pagamento Desindexado'])
resposta_cargo = pd.DataFrame(dados_condenacao_cargo['Pagamento Desindexado'])

#Construção do Modelo de Árvore de Decisão para Regressão - resposta numérica contínua
#Em cenários de classificação podemos usar a DecisionTreeClassifier
#É possível customizar critérios de parada através dos hiperparâmetros do modelo
DT = tree.DecisionTreeRegressor(random_state=42, 
                                max_depth=100, 
                                criterion='mae',
                                min_samples_leaf = 50)


#prepara target
resposta = pd.DataFrame(dados_condenacao_cargo['Pagamento Desindexado'])

DT = DT.fit(explicativas_cargo[['cluster_valor', 'Cluster Aging Tempo de Empresa', 'Cluster Aging', 'safra_reclamacao']],
            resposta_cargo['Pagamento Desindexado'])

y_true = resposta_cargo['Pagamento Desindexado']
#y_pred = valor previsto pelo modelo treinado
y_pred = DT.predict(explicativas_cargo[['cluster_valor', 'Cluster Aging Tempo de Empresa', 'Cluster Aging','safra_reclamacao']])

#Aplicação da predição no dataframe do estoque para obtenção dos valores de predição
dados_estoque_full = estoque_cargo
dados_estoque_full['prediction'] = DT.predict(explicativas_estoque[['cluster_valor', 'Cluster Aging Tempo de Empresa', 
                                                                    'Cluster Aging','safra_reclamacao']])

#Gera o recorte precificado do cargo utilizado
estoque_cargo_motorista = estoque_cargo

"""
Gerar a modelagem do cargo Analista, com 15 ramificações
"""

natureza_notin = ['TERCEIRO INSOLVENTE', 'SINDICATO / MINISTERIO PUBLICO','TERCEIRO SOLVENTE','ADMINISTRATIVO']
sub_area_direito_notin = ['PREVENTIVO AUTO DE INFRAÇÃO','CONTENCIOSO COLETIVO']
outlier_notin = ['Outlier']

dados_condenacao_cargo = dados[(dados['MOTIVO_ENC_AGRP'] == 'CONDENACAO')
                        & (~dados['NATUREZA_OPERACIONAL'].isin(natureza_notin))
                        & (~dados['SUB_AREA_DO_DIREITO'].isin(sub_area_direito_notin))
                        & (~dados['OUTLIER'].isin(outlier_notin))    
                            & (dados['cargo_tratado'] == 'ANALISTA')      
                       ]

#Define o filtro para Estoque
ESTQ_natureza_notin = ['TERCEIRO INSOLVENTE']

estoque_cargo = estoque[(estoque['cargo_tratado'] == 'ANALISTA')
                       & (~estoque['Natureza Operacional (M)'].isin(ESTQ_natureza_notin))
                       ]


#Cria um novo dataframe adequado ao scikit-learning para treinamento dos modelos
explicativas = pd.DataFrame()
explicativas['ID_PROCESSO'] = dados_condenacao_geral.ID_PROCESSO
explicativas_cargo = pd.DataFrame()
explicativas_cargo['ID_PROCESSO'] = dados_condenacao_cargo.ID_PROCESSO

explicativas_estoque = pd.DataFrame()
explicativas_estoque['ID PROCESSO'] = estoque_cargo['ID PROCESSO']



#Faz o Label Encoder, que converte dados qualitativos de texto para um índice numérico
#Com esse encoding, podemos facilmente voltar aos valores originais utilizando a função inverse_transform

#adiciona a variável Estado codificada ao dataframe
le_estado = preprocessing.LabelEncoder()
encode_estado = le_estado.fit(estoque['ESTADO'])
explicativas['ESTADO'] = encode_estado.transform(dados_condenacao_geral['ESTADO'])
explicativas_cargo['ESTADO'] = encode_estado.transform(dados_condenacao_cargo['ESTADO'])
explicativas_estoque['ESTADO'] = encode_estado.transform(estoque_cargo['ESTADO'])


#gera o de-para dos estados
estados = pd.DataFrame()
estados['codigos'] = explicativas_estoque.ESTADO.unique()
estados['estados'] = encode_estado.inverse_transform(estados.codigos)
estados.sort_values(by='codigos')


#adiciona a variável cluster valor codificada ao dataframe
le_cluster_valor = preprocessing.LabelEncoder()
encode_cluster_valor = le_cluster_valor.fit(dados_condenacao_geral['cluster_valor'])
explicativas['cluster_valor'] = encode_cluster_valor.transform(dados_condenacao_geral['cluster_valor'])
explicativas_cargo['cluster_valor'] = encode_cluster_valor.transform(dados_condenacao_cargo['cluster_valor'])
explicativas_estoque['cluster_valor'] = encode_cluster_valor.transform(estoque_cargo['cluster_valor'])

#gera o de-para dos cluster valor
cluster_valor = pd.DataFrame()
cluster_valor['codigos'] = explicativas.cluster_valor.unique()
cluster_valor['cluster_valor'] = encode_cluster_valor.inverse_transform(cluster_valor.codigos)
cluster_valor.sort_values(by='codigos')

#adiciona a variável cargo_tratado codificada ao dataframe
le_cargo_tratado = preprocessing.LabelEncoder()
encode_cargo_tratado = le_cargo_tratado.fit(dados_condenacao_geral['cargo_tratado'])
explicativas['cargo_tratado'] = encode_cargo_tratado.transform(dados_condenacao_geral['cargo_tratado'])
explicativas_cargo['cargo_tratado'] = encode_cargo_tratado.transform(dados_condenacao_cargo['cargo_tratado'])
explicativas_estoque['cargo_tratado'] = encode_cargo_tratado.transform(estoque_cargo['cargo_tratado'])


#gera o de-para dos cargos
cargo = pd.DataFrame()
cargo['codigos'] = explicativas.cargo_tratado.unique()
cargo['cargo'] = encode_cargo_tratado.inverse_transform(cargo.codigos)
cargo.sort_values(by='codigos')

#adiciona a variável Cluster Aging Tempo de Empresa codificada ao dataframe
le_tempo_empresa = preprocessing.LabelEncoder()
encode_tempo_empresa = le_tempo_empresa.fit(dados_condenacao_geral['Cluster Aging Tempo de Empresa'])
explicativas['Cluster Aging Tempo de Empresa'] = encode_tempo_empresa.transform(dados_condenacao_geral['Cluster Aging Tempo de Empresa'])
explicativas_cargo['Cluster Aging Tempo de Empresa'] = encode_tempo_empresa.transform(dados_condenacao_cargo['Cluster Aging Tempo de Empresa'])
explicativas_estoque['Cluster Aging Tempo de Empresa'] = encode_tempo_empresa.transform(estoque_cargo['Cluster Aging Tempo de Empresa'])

#gera o de-para dos cluster tempo de empresa
tempo_empresa = pd.DataFrame()
tempo_empresa['codigos'] = explicativas['Cluster Aging Tempo de Empresa'].unique()
tempo_empresa['tempo_empresa'] = encode_tempo_empresa.inverse_transform(tempo_empresa.codigos)
tempo_empresa.sort_values(by='codigos')

#adiciona a variável Cluster Aging codificada ao dataframe
le_cluster_aging = preprocessing.LabelEncoder()
encode_cluster_aging = le_cluster_aging.fit(dados_condenacao_geral['Cluster Aging'])
explicativas['Cluster Aging'] = encode_cluster_aging.transform(dados_condenacao_geral['Cluster Aging'])
explicativas_cargo['Cluster Aging'] = encode_cluster_aging.transform(dados_condenacao_cargo['Cluster Aging'])
explicativas_estoque['Cluster Aging'] = encode_cluster_aging.transform(estoque_cargo['Cluster Aging'])

#gera o de-para dos cluster aging
cluster_aging = pd.DataFrame()
cluster_aging['codigos'] = explicativas['Cluster Aging'].unique()
cluster_aging['cluster_aging'] = encode_cluster_aging.inverse_transform(cluster_aging.codigos)
cluster_aging.sort_values(by='codigos')

#adiciona a variável Safra de Reclamação codificada ao dataframe
le_safra_reclamacao = preprocessing.LabelEncoder()
encode_safra_reclamacao = le_safra_reclamacao.fit(estoque['Safra de Reclamação'].astype(str))
explicativas['safra_reclamacao'] = encode_safra_reclamacao.transform(dados_condenacao_geral['Safra de Reclamação'].astype(str))
dados_condenacao_geral['safra_reclamacao'] = encode_safra_reclamacao.transform(dados_condenacao_geral['Safra de Reclamação'].astype(str))
explicativas_cargo['safra_reclamacao'] = encode_safra_reclamacao.transform(dados_condenacao_cargo['Safra de Reclamação'].astype(str))
explicativas_estoque['safra_reclamacao'] = encode_safra_reclamacao.transform(estoque_cargo['Safra de Reclamação'].astype(str))

#gera o de-para dos cluster pedidos
safra_reclamacao = pd.DataFrame()
safra_reclamacao['codigos'] = explicativas_estoque['safra_reclamacao'].unique()
safra_reclamacao['safra_reclamacao'] = encode_safra_reclamacao.inverse_transform(safra_reclamacao.codigos)
safra_reclamacao.sort_values(by='codigos')

#substitui nulos nas variáveis qualitativas por -999
#Como estamos trabalhando com modelos de árvore, os valores sem dados serão tratados como uma categoria à parte, muito distante das demais
explicativas = explicativas.fillna(-999)
explicativas_cargo = explicativas_cargo.fillna(-999)
explicativas_estoque = explicativas_estoque.fillna(-999)


#prepara target
resposta = pd.DataFrame(dados_condenacao_geral['Pagamento Desindexado'])
resposta_cargo = pd.DataFrame(dados_condenacao_cargo['Pagamento Desindexado'])

#Construção do Modelo de Árvore de Decisão para Regressão - resposta numérica contínua
#Em cenários de classificação podemos usar a DecisionTreeClassifier
#É possível customizar critérios de parada através dos hiperparâmetros do modelo
DT = tree.DecisionTreeRegressor(random_state=42, 
                                max_depth=100, 
                                criterion='mae',
                                min_samples_leaf = 15)


#prepara target
resposta = pd.DataFrame(dados_condenacao_cargo['Pagamento Desindexado'])

DT = DT.fit(explicativas_cargo[['cluster_valor', 'Cluster Aging Tempo de Empresa', 'Cluster Aging', 'safra_reclamacao']],
            resposta_cargo['Pagamento Desindexado'])

y_true = resposta_cargo['Pagamento Desindexado']
#y_pred = valor previsto pelo modelo treinado
y_pred = DT.predict(explicativas_cargo[['cluster_valor', 'Cluster Aging Tempo de Empresa', 'Cluster Aging','safra_reclamacao']])

#Aplicação da predição no dataframe do estoque para obtenção dos valores de predição
dados_estoque_full = estoque_cargo
dados_estoque_full['prediction'] = DT.predict(explicativas_estoque[['cluster_valor', 'Cluster Aging Tempo de Empresa', 
                                                                    'Cluster Aging','safra_reclamacao']])

#Gera o recorte precificado do cargo utilizado
estoque_cargo_analista = estoque_cargo



"""
Gerar a modelagem do cargo Operador, com 15 ramificações
"""

natureza_notin = ['TERCEIRO INSOLVENTE', 'SINDICATO / MINISTERIO PUBLICO','TERCEIRO SOLVENTE','ADMINISTRATIVO']
sub_area_direito_notin = ['PREVENTIVO AUTO DE INFRAÇÃO','CONTENCIOSO COLETIVO']
outlier_notin = ['Outlier']

dados_condenacao_cargo = dados[(dados['MOTIVO_ENC_AGRP'] == 'CONDENACAO')
                        & (~dados['NATUREZA_OPERACIONAL'].isin(natureza_notin))
                        & (~dados['SUB_AREA_DO_DIREITO'].isin(sub_area_direito_notin))
                        & (~dados['OUTLIER'].isin(outlier_notin))    
                            & (dados['cargo_tratado'] == 'OPERADOR')      
                       ]

#Define o filtro para Estoque
ESTQ_natureza_notin = ['TERCEIRO INSOLVENTE']

estoque_cargo = estoque[(estoque['cargo_tratado'] == 'OPERADOR')
                       & (~estoque['Natureza Operacional (M)'].isin(ESTQ_natureza_notin))
                       ]


#Cria um novo dataframe adequado ao scikit-learning para treinamento dos modelos
explicativas = pd.DataFrame()
explicativas['ID_PROCESSO'] = dados_condenacao_geral.ID_PROCESSO
explicativas_cargo = pd.DataFrame()
explicativas_cargo['ID_PROCESSO'] = dados_condenacao_cargo.ID_PROCESSO

explicativas_estoque = pd.DataFrame()
explicativas_estoque['ID PROCESSO'] = estoque_cargo['ID PROCESSO']



#Faz o Label Encoder, que converte dados qualitativos de texto para um índice numérico
#Com esse encoding, podemos facilmente voltar aos valores originais utilizando a função inverse_transform

#adiciona a variável Estado codificada ao dataframe
le_estado = preprocessing.LabelEncoder()
encode_estado = le_estado.fit(estoque['ESTADO'])
explicativas['ESTADO'] = encode_estado.transform(dados_condenacao_geral['ESTADO'])
explicativas_cargo['ESTADO'] = encode_estado.transform(dados_condenacao_cargo['ESTADO'])
explicativas_estoque['ESTADO'] = encode_estado.transform(estoque_cargo['ESTADO'])


#gera o de-para dos estados
estados = pd.DataFrame()
estados['codigos'] = explicativas_estoque.ESTADO.unique()
estados['estados'] = encode_estado.inverse_transform(estados.codigos)
estados.sort_values(by='codigos')


#adiciona a variável cluster valor codificada ao dataframe
le_cluster_valor = preprocessing.LabelEncoder()
encode_cluster_valor = le_cluster_valor.fit(dados_condenacao_geral['cluster_valor'])
explicativas['cluster_valor'] = encode_cluster_valor.transform(dados_condenacao_geral['cluster_valor'])
explicativas_cargo['cluster_valor'] = encode_cluster_valor.transform(dados_condenacao_cargo['cluster_valor'])
explicativas_estoque['cluster_valor'] = encode_cluster_valor.transform(estoque_cargo['cluster_valor'])

#gera o de-para dos cluster valor
cluster_valor = pd.DataFrame()
cluster_valor['codigos'] = explicativas.cluster_valor.unique()
cluster_valor['cluster_valor'] = encode_cluster_valor.inverse_transform(cluster_valor.codigos)
cluster_valor.sort_values(by='codigos')

#adiciona a variável cargo_tratado codificada ao dataframe
le_cargo_tratado = preprocessing.LabelEncoder()
encode_cargo_tratado = le_cargo_tratado.fit(dados_condenacao_geral['cargo_tratado'])
explicativas['cargo_tratado'] = encode_cargo_tratado.transform(dados_condenacao_geral['cargo_tratado'])
explicativas_cargo['cargo_tratado'] = encode_cargo_tratado.transform(dados_condenacao_cargo['cargo_tratado'])
explicativas_estoque['cargo_tratado'] = encode_cargo_tratado.transform(estoque_cargo['cargo_tratado'])


#gera o de-para dos cargos
cargo = pd.DataFrame()
cargo['codigos'] = explicativas.cargo_tratado.unique()
cargo['cargo'] = encode_cargo_tratado.inverse_transform(cargo.codigos)
cargo.sort_values(by='codigos')

#adiciona a variável Cluster Aging Tempo de Empresa codificada ao dataframe
le_tempo_empresa = preprocessing.LabelEncoder()
encode_tempo_empresa = le_tempo_empresa.fit(dados_condenacao_geral['Cluster Aging Tempo de Empresa'])
explicativas['Cluster Aging Tempo de Empresa'] = encode_tempo_empresa.transform(dados_condenacao_geral['Cluster Aging Tempo de Empresa'])
explicativas_cargo['Cluster Aging Tempo de Empresa'] = encode_tempo_empresa.transform(dados_condenacao_cargo['Cluster Aging Tempo de Empresa'])
explicativas_estoque['Cluster Aging Tempo de Empresa'] = encode_tempo_empresa.transform(estoque_cargo['Cluster Aging Tempo de Empresa'])

#gera o de-para dos cluster tempo de empresa
tempo_empresa = pd.DataFrame()
tempo_empresa['codigos'] = explicativas['Cluster Aging Tempo de Empresa'].unique()
tempo_empresa['tempo_empresa'] = encode_tempo_empresa.inverse_transform(tempo_empresa.codigos)
tempo_empresa.sort_values(by='codigos')

#adiciona a variável Cluster Aging codificada ao dataframe
le_cluster_aging = preprocessing.LabelEncoder()
encode_cluster_aging = le_cluster_aging.fit(dados_condenacao_geral['Cluster Aging'])
explicativas['Cluster Aging'] = encode_cluster_aging.transform(dados_condenacao_geral['Cluster Aging'])
explicativas_cargo['Cluster Aging'] = encode_cluster_aging.transform(dados_condenacao_cargo['Cluster Aging'])
explicativas_estoque['Cluster Aging'] = encode_cluster_aging.transform(estoque_cargo['Cluster Aging'])

#gera o de-para dos cluster aging
cluster_aging = pd.DataFrame()
cluster_aging['codigos'] = explicativas['Cluster Aging'].unique()
cluster_aging['cluster_aging'] = encode_cluster_aging.inverse_transform(cluster_aging.codigos)
cluster_aging.sort_values(by='codigos')

#adiciona a variável Safra de Reclamação codificada ao dataframe
le_safra_reclamacao = preprocessing.LabelEncoder()
encode_safra_reclamacao = le_safra_reclamacao.fit(estoque['Safra de Reclamação'].astype(str))
explicativas['safra_reclamacao'] = encode_safra_reclamacao.transform(dados_condenacao_geral['Safra de Reclamação'].astype(str))
dados_condenacao_geral['safra_reclamacao'] = encode_safra_reclamacao.transform(dados_condenacao_geral['Safra de Reclamação'].astype(str))
explicativas_cargo['safra_reclamacao'] = encode_safra_reclamacao.transform(dados_condenacao_cargo['Safra de Reclamação'].astype(str))
explicativas_estoque['safra_reclamacao'] = encode_safra_reclamacao.transform(estoque_cargo['Safra de Reclamação'].astype(str))

#gera o de-para dos cluster pedidos
safra_reclamacao = pd.DataFrame()
safra_reclamacao['codigos'] = explicativas_estoque['safra_reclamacao'].unique()
safra_reclamacao['safra_reclamacao'] = encode_safra_reclamacao.inverse_transform(safra_reclamacao.codigos)
safra_reclamacao.sort_values(by='codigos')

#substitui nulos nas variáveis qualitativas por -999
#Como estamos trabalhando com modelos de árvore, os valores sem dados serão tratados como uma categoria à parte, muito distante das demais
explicativas = explicativas.fillna(-999)
explicativas_cargo = explicativas_cargo.fillna(-999)
explicativas_estoque = explicativas_estoque.fillna(-999)


#prepara target
resposta = pd.DataFrame(dados_condenacao_geral['Pagamento Desindexado'])
resposta_cargo = pd.DataFrame(dados_condenacao_cargo['Pagamento Desindexado'])

#Construção do Modelo de Árvore de Decisão para Regressão - resposta numérica contínua
#Em cenários de classificação podemos usar a DecisionTreeClassifier
#É possível customizar critérios de parada através dos hiperparâmetros do modelo
DT = tree.DecisionTreeRegressor(random_state=42, 
                                max_depth=100, 
                                criterion='mae',
                                min_samples_leaf = 15)


#prepara target
resposta = pd.DataFrame(dados_condenacao_cargo['Pagamento Desindexado'])

DT = DT.fit(explicativas_cargo[['cluster_valor', 'Cluster Aging Tempo de Empresa', 'Cluster Aging', 'safra_reclamacao']],
            resposta_cargo['Pagamento Desindexado'])

y_true = resposta_cargo['Pagamento Desindexado']
#y_pred = valor previsto pelo modelo treinado
y_pred = DT.predict(explicativas_cargo[['cluster_valor', 'Cluster Aging Tempo de Empresa', 'Cluster Aging','safra_reclamacao']])

#Aplicação da predição no dataframe do estoque para obtenção dos valores de predição
dados_estoque_full = estoque_cargo
dados_estoque_full['prediction'] = DT.predict(explicativas_estoque[['cluster_valor', 'Cluster Aging Tempo de Empresa', 
                                                                    'Cluster Aging','safra_reclamacao']])

#Gera o recorte precificado do cargo utilizado
estoque_cargo_operador = estoque_cargo



"""
Gerar a modelagem do cargo Caixa, com 15 ramificações
"""

natureza_notin = ['TERCEIRO INSOLVENTE', 'SINDICATO / MINISTERIO PUBLICO','TERCEIRO SOLVENTE','ADMINISTRATIVO']
sub_area_direito_notin = ['PREVENTIVO AUTO DE INFRAÇÃO','CONTENCIOSO COLETIVO']
outlier_notin = ['Outlier']

dados_condenacao_cargo = dados[(dados['MOTIVO_ENC_AGRP'] == 'CONDENACAO')
                        & (~dados['NATUREZA_OPERACIONAL'].isin(natureza_notin))
                        & (~dados['SUB_AREA_DO_DIREITO'].isin(sub_area_direito_notin))
                        & (~dados['OUTLIER'].isin(outlier_notin))    
                            & (dados['cargo_tratado'] == 'CAIXA')      
                       ]

#Define o filtro para Estoque
ESTQ_natureza_notin = ['TERCEIRO INSOLVENTE']

estoque_cargo = estoque[(estoque['cargo_tratado'] == 'CAIXA')
                       & (~estoque['Natureza Operacional (M)'].isin(ESTQ_natureza_notin))
                       ]


#Cria um novo dataframe adequado ao scikit-learning para treinamento dos modelos
explicativas = pd.DataFrame()
explicativas['ID_PROCESSO'] = dados_condenacao_geral.ID_PROCESSO
explicativas_cargo = pd.DataFrame()
explicativas_cargo['ID_PROCESSO'] = dados_condenacao_cargo.ID_PROCESSO

explicativas_estoque = pd.DataFrame()
explicativas_estoque['ID PROCESSO'] = estoque_cargo['ID PROCESSO']



#Faz o Label Encoder, que converte dados qualitativos de texto para um índice numérico
#Com esse encoding, podemos facilmente voltar aos valores originais utilizando a função inverse_transform

#adiciona a variável Estado codificada ao dataframe
le_estado = preprocessing.LabelEncoder()
encode_estado = le_estado.fit(estoque['ESTADO'])
explicativas['ESTADO'] = encode_estado.transform(dados_condenacao_geral['ESTADO'])
explicativas_cargo['ESTADO'] = encode_estado.transform(dados_condenacao_cargo['ESTADO'])
explicativas_estoque['ESTADO'] = encode_estado.transform(estoque_cargo['ESTADO'])


#gera o de-para dos estados
estados = pd.DataFrame()
estados['codigos'] = explicativas_estoque.ESTADO.unique()
estados['estados'] = encode_estado.inverse_transform(estados.codigos)
estados.sort_values(by='codigos')


#adiciona a variável cluster valor codificada ao dataframe
le_cluster_valor = preprocessing.LabelEncoder()
encode_cluster_valor = le_cluster_valor.fit(dados_condenacao_geral['cluster_valor'])
explicativas['cluster_valor'] = encode_cluster_valor.transform(dados_condenacao_geral['cluster_valor'])
explicativas_cargo['cluster_valor'] = encode_cluster_valor.transform(dados_condenacao_cargo['cluster_valor'])
explicativas_estoque['cluster_valor'] = encode_cluster_valor.transform(estoque_cargo['cluster_valor'])

#gera o de-para dos cluster valor
cluster_valor = pd.DataFrame()
cluster_valor['codigos'] = explicativas.cluster_valor.unique()
cluster_valor['cluster_valor'] = encode_cluster_valor.inverse_transform(cluster_valor.codigos)
cluster_valor.sort_values(by='codigos')

#adiciona a variável cargo_tratado codificada ao dataframe
le_cargo_tratado = preprocessing.LabelEncoder()
encode_cargo_tratado = le_cargo_tratado.fit(dados_condenacao_geral['cargo_tratado'])
explicativas['cargo_tratado'] = encode_cargo_tratado.transform(dados_condenacao_geral['cargo_tratado'])
explicativas_cargo['cargo_tratado'] = encode_cargo_tratado.transform(dados_condenacao_cargo['cargo_tratado'])
explicativas_estoque['cargo_tratado'] = encode_cargo_tratado.transform(estoque_cargo['cargo_tratado'])


#gera o de-para dos cargos
cargo = pd.DataFrame()
cargo['codigos'] = explicativas.cargo_tratado.unique()
cargo['cargo'] = encode_cargo_tratado.inverse_transform(cargo.codigos)
cargo.sort_values(by='codigos')

#adiciona a variável Cluster Aging Tempo de Empresa codificada ao dataframe
le_tempo_empresa = preprocessing.LabelEncoder()
encode_tempo_empresa = le_tempo_empresa.fit(dados_condenacao_geral['Cluster Aging Tempo de Empresa'])
explicativas['Cluster Aging Tempo de Empresa'] = encode_tempo_empresa.transform(dados_condenacao_geral['Cluster Aging Tempo de Empresa'])
explicativas_cargo['Cluster Aging Tempo de Empresa'] = encode_tempo_empresa.transform(dados_condenacao_cargo['Cluster Aging Tempo de Empresa'])
explicativas_estoque['Cluster Aging Tempo de Empresa'] = encode_tempo_empresa.transform(estoque_cargo['Cluster Aging Tempo de Empresa'])

#gera o de-para dos cluster tempo de empresa
tempo_empresa = pd.DataFrame()
tempo_empresa['codigos'] = explicativas['Cluster Aging Tempo de Empresa'].unique()
tempo_empresa['tempo_empresa'] = encode_tempo_empresa.inverse_transform(tempo_empresa.codigos)
tempo_empresa.sort_values(by='codigos')

#adiciona a variável Cluster Aging codificada ao dataframe
le_cluster_aging = preprocessing.LabelEncoder()
encode_cluster_aging = le_cluster_aging.fit(dados_condenacao_geral['Cluster Aging'])
explicativas['Cluster Aging'] = encode_cluster_aging.transform(dados_condenacao_geral['Cluster Aging'])
explicativas_cargo['Cluster Aging'] = encode_cluster_aging.transform(dados_condenacao_cargo['Cluster Aging'])
explicativas_estoque['Cluster Aging'] = encode_cluster_aging.transform(estoque_cargo['Cluster Aging'])

#gera o de-para dos cluster aging
cluster_aging = pd.DataFrame()
cluster_aging['codigos'] = explicativas['Cluster Aging'].unique()
cluster_aging['cluster_aging'] = encode_cluster_aging.inverse_transform(cluster_aging.codigos)
cluster_aging.sort_values(by='codigos')

#adiciona a variável Safra de Reclamação codificada ao dataframe
le_safra_reclamacao = preprocessing.LabelEncoder()
encode_safra_reclamacao = le_safra_reclamacao.fit(estoque['Safra de Reclamação'].astype(str))
explicativas['safra_reclamacao'] = encode_safra_reclamacao.transform(dados_condenacao_geral['Safra de Reclamação'].astype(str))
dados_condenacao_geral['safra_reclamacao'] = encode_safra_reclamacao.transform(dados_condenacao_geral['Safra de Reclamação'].astype(str))
explicativas_cargo['safra_reclamacao'] = encode_safra_reclamacao.transform(dados_condenacao_cargo['Safra de Reclamação'].astype(str))
explicativas_estoque['safra_reclamacao'] = encode_safra_reclamacao.transform(estoque_cargo['Safra de Reclamação'].astype(str))

#gera o de-para dos cluster pedidos
safra_reclamacao = pd.DataFrame()
safra_reclamacao['codigos'] = explicativas_estoque['safra_reclamacao'].unique()
safra_reclamacao['safra_reclamacao'] = encode_safra_reclamacao.inverse_transform(safra_reclamacao.codigos)
safra_reclamacao.sort_values(by='codigos')

#substitui nulos nas variáveis qualitativas por -999
#Como estamos trabalhando com modelos de árvore, os valores sem dados serão tratados como uma categoria à parte, muito distante das demais
explicativas = explicativas.fillna(-999)
explicativas_cargo = explicativas_cargo.fillna(-999)
explicativas_estoque = explicativas_estoque.fillna(-999)


#prepara target
resposta = pd.DataFrame(dados_condenacao_geral['Pagamento Desindexado'])
resposta_cargo = pd.DataFrame(dados_condenacao_cargo['Pagamento Desindexado'])

#Construção do Modelo de Árvore de Decisão para Regressão - resposta numérica contínua
#Em cenários de classificação podemos usar a DecisionTreeClassifier
#É possível customizar critérios de parada através dos hiperparâmetros do modelo
DT = tree.DecisionTreeRegressor(random_state=42, 
                                max_depth=100, 
                                criterion='mae',
                                min_samples_leaf = 15)


#prepara target
resposta = pd.DataFrame(dados_condenacao_cargo['Pagamento Desindexado'])

DT = DT.fit(explicativas_cargo[['cluster_valor', 'Cluster Aging Tempo de Empresa', 'Cluster Aging', 'safra_reclamacao']],
            resposta_cargo['Pagamento Desindexado'])

y_true = resposta_cargo['Pagamento Desindexado']
#y_pred = valor previsto pelo modelo treinado
y_pred = DT.predict(explicativas_cargo[['cluster_valor', 'Cluster Aging Tempo de Empresa', 'Cluster Aging','safra_reclamacao']])

#Aplicação da predição no dataframe do estoque para obtenção dos valores de predição
dados_estoque_full = estoque_cargo
dados_estoque_full['prediction'] = DT.predict(explicativas_estoque[['cluster_valor', 'Cluster Aging Tempo de Empresa', 
                                                                    'Cluster Aging','safra_reclamacao']])

#Gera o recorte precificado do cargo utilizado
estoque_cargo_caixa = estoque_cargo


"""
Gerar a modelagem do cargo Gerente, com 15 ramificações
"""

natureza_notin = ['TERCEIRO INSOLVENTE', 'SINDICATO / MINISTERIO PUBLICO','TERCEIRO SOLVENTE','ADMINISTRATIVO']
sub_area_direito_notin = ['PREVENTIVO AUTO DE INFRAÇÃO','CONTENCIOSO COLETIVO']
outlier_notin = ['Outlier']

dados_condenacao_cargo = dados[(dados['MOTIVO_ENC_AGRP'] == 'CONDENACAO')
                        & (~dados['NATUREZA_OPERACIONAL'].isin(natureza_notin))
                        & (~dados['SUB_AREA_DO_DIREITO'].isin(sub_area_direito_notin))
                        & (~dados['OUTLIER'].isin(outlier_notin))    
                            & (dados['cargo_tratado'] == 'GERENTE')      
                       ]

#Define o filtro para Estoque
ESTQ_natureza_notin = ['TERCEIRO INSOLVENTE']

estoque_cargo = estoque[(estoque['cargo_tratado'] == 'GERENTE')
                       & (~estoque['Natureza Operacional (M)'].isin(ESTQ_natureza_notin))
                       ]


#Cria um novo dataframe adequado ao scikit-learning para treinamento dos modelos
explicativas = pd.DataFrame()
explicativas['ID_PROCESSO'] = dados_condenacao_geral.ID_PROCESSO
explicativas_cargo = pd.DataFrame()
explicativas_cargo['ID_PROCESSO'] = dados_condenacao_cargo.ID_PROCESSO

explicativas_estoque = pd.DataFrame()
explicativas_estoque['ID PROCESSO'] = estoque_cargo['ID PROCESSO']



#Faz o Label Encoder, que converte dados qualitativos de texto para um índice numérico
#Com esse encoding, podemos facilmente voltar aos valores originais utilizando a função inverse_transform

#adiciona a variável Estado codificada ao dataframe
le_estado = preprocessing.LabelEncoder()
encode_estado = le_estado.fit(estoque['ESTADO'])
explicativas['ESTADO'] = encode_estado.transform(dados_condenacao_geral['ESTADO'])
explicativas_cargo['ESTADO'] = encode_estado.transform(dados_condenacao_cargo['ESTADO'])
explicativas_estoque['ESTADO'] = encode_estado.transform(estoque_cargo['ESTADO'])


#gera o de-para dos estados
estados = pd.DataFrame()
estados['codigos'] = explicativas_estoque.ESTADO.unique()
estados['estados'] = encode_estado.inverse_transform(estados.codigos)
estados.sort_values(by='codigos')


#adiciona a variável cluster valor codificada ao dataframe
le_cluster_valor = preprocessing.LabelEncoder()
encode_cluster_valor = le_cluster_valor.fit(dados_condenacao_geral['cluster_valor'])
explicativas['cluster_valor'] = encode_cluster_valor.transform(dados_condenacao_geral['cluster_valor'])
explicativas_cargo['cluster_valor'] = encode_cluster_valor.transform(dados_condenacao_cargo['cluster_valor'])
explicativas_estoque['cluster_valor'] = encode_cluster_valor.transform(estoque_cargo['cluster_valor'])

#gera o de-para dos cluster valor
cluster_valor = pd.DataFrame()
cluster_valor['codigos'] = explicativas.cluster_valor.unique()
cluster_valor['cluster_valor'] = encode_cluster_valor.inverse_transform(cluster_valor.codigos)
cluster_valor.sort_values(by='codigos')

#adiciona a variável cargo_tratado codificada ao dataframe
le_cargo_tratado = preprocessing.LabelEncoder()
encode_cargo_tratado = le_cargo_tratado.fit(dados_condenacao_geral['cargo_tratado'])
explicativas['cargo_tratado'] = encode_cargo_tratado.transform(dados_condenacao_geral['cargo_tratado'])
explicativas_cargo['cargo_tratado'] = encode_cargo_tratado.transform(dados_condenacao_cargo['cargo_tratado'])
explicativas_estoque['cargo_tratado'] = encode_cargo_tratado.transform(estoque_cargo['cargo_tratado'])


#gera o de-para dos cargos
cargo = pd.DataFrame()
cargo['codigos'] = explicativas.cargo_tratado.unique()
cargo['cargo'] = encode_cargo_tratado.inverse_transform(cargo.codigos)
cargo.sort_values(by='codigos')

#adiciona a variável Cluster Aging Tempo de Empresa codificada ao dataframe
le_tempo_empresa = preprocessing.LabelEncoder()
encode_tempo_empresa = le_tempo_empresa.fit(dados_condenacao_geral['Cluster Aging Tempo de Empresa'])
explicativas['Cluster Aging Tempo de Empresa'] = encode_tempo_empresa.transform(dados_condenacao_geral['Cluster Aging Tempo de Empresa'])
explicativas_cargo['Cluster Aging Tempo de Empresa'] = encode_tempo_empresa.transform(dados_condenacao_cargo['Cluster Aging Tempo de Empresa'])
explicativas_estoque['Cluster Aging Tempo de Empresa'] = encode_tempo_empresa.transform(estoque_cargo['Cluster Aging Tempo de Empresa'])

#gera o de-para dos cluster tempo de empresa
tempo_empresa = pd.DataFrame()
tempo_empresa['codigos'] = explicativas['Cluster Aging Tempo de Empresa'].unique()
tempo_empresa['tempo_empresa'] = encode_tempo_empresa.inverse_transform(tempo_empresa.codigos)
tempo_empresa.sort_values(by='codigos')

#adiciona a variável Cluster Aging codificada ao dataframe
le_cluster_aging = preprocessing.LabelEncoder()
encode_cluster_aging = le_cluster_aging.fit(dados_condenacao_geral['Cluster Aging'])
explicativas['Cluster Aging'] = encode_cluster_aging.transform(dados_condenacao_geral['Cluster Aging'])
explicativas_cargo['Cluster Aging'] = encode_cluster_aging.transform(dados_condenacao_cargo['Cluster Aging'])
explicativas_estoque['Cluster Aging'] = encode_cluster_aging.transform(estoque_cargo['Cluster Aging'])

#gera o de-para dos cluster aging
cluster_aging = pd.DataFrame()
cluster_aging['codigos'] = explicativas['Cluster Aging'].unique()
cluster_aging['cluster_aging'] = encode_cluster_aging.inverse_transform(cluster_aging.codigos)
cluster_aging.sort_values(by='codigos')

#adiciona a variável Safra de Reclamação codificada ao dataframe
le_safra_reclamacao = preprocessing.LabelEncoder()
encode_safra_reclamacao = le_safra_reclamacao.fit(estoque['Safra de Reclamação'].astype(str))
explicativas['safra_reclamacao'] = encode_safra_reclamacao.transform(dados_condenacao_geral['Safra de Reclamação'].astype(str))
dados_condenacao_geral['safra_reclamacao'] = encode_safra_reclamacao.transform(dados_condenacao_geral['Safra de Reclamação'].astype(str))
explicativas_cargo['safra_reclamacao'] = encode_safra_reclamacao.transform(dados_condenacao_cargo['Safra de Reclamação'].astype(str))
explicativas_estoque['safra_reclamacao'] = encode_safra_reclamacao.transform(estoque_cargo['Safra de Reclamação'].astype(str))

#gera o de-para dos cluster pedidos
safra_reclamacao = pd.DataFrame()
safra_reclamacao['codigos'] = explicativas_estoque['safra_reclamacao'].unique()
safra_reclamacao['safra_reclamacao'] = encode_safra_reclamacao.inverse_transform(safra_reclamacao.codigos)
safra_reclamacao.sort_values(by='codigos')

#substitui nulos nas variáveis qualitativas por -999
#Como estamos trabalhando com modelos de árvore, os valores sem dados serão tratados como uma categoria à parte, muito distante das demais
explicativas = explicativas.fillna(-999)
explicativas_cargo = explicativas_cargo.fillna(-999)
explicativas_estoque = explicativas_estoque.fillna(-999)


#prepara target
resposta = pd.DataFrame(dados_condenacao_geral['Pagamento Desindexado'])
resposta_cargo = pd.DataFrame(dados_condenacao_cargo['Pagamento Desindexado'])

#Construção do Modelo de Árvore de Decisão para Regressão - resposta numérica contínua
#Em cenários de classificação podemos usar a DecisionTreeClassifier
#É possível customizar critérios de parada através dos hiperparâmetros do modelo
DT = tree.DecisionTreeRegressor(random_state=42, 
                                max_depth=100, 
                                criterion='mae',
                                min_samples_leaf = 15)


#prepara target
resposta = pd.DataFrame(dados_condenacao_cargo['Pagamento Desindexado'])

DT = DT.fit(explicativas_cargo[['cluster_valor', 'Cluster Aging Tempo de Empresa', 'Cluster Aging', 'safra_reclamacao']],
            resposta_cargo['Pagamento Desindexado'])

y_true = resposta_cargo['Pagamento Desindexado']
#y_pred = valor previsto pelo modelo treinado
y_pred = DT.predict(explicativas_cargo[['cluster_valor', 'Cluster Aging Tempo de Empresa', 'Cluster Aging','safra_reclamacao']])

#Aplicação da predição no dataframe do estoque para obtenção dos valores de predição
dados_estoque_full = estoque_cargo
dados_estoque_full['prediction'] = DT.predict(explicativas_estoque[['cluster_valor', 'Cluster Aging Tempo de Empresa', 
                                                                    'Cluster Aging','safra_reclamacao']])

#Gera o recorte precificado do cargo utilizado
estoque_cargo_gerente = estoque_cargo

"""
INSOLVENTE
"""
#Gerar o agrupamento de cargos definido como objeto do estudo
lista_cargos_estoque = ['VENDEDOR','MONTADOR','AJUDANTE', 'GERENTE', 'MOTORISTA','AJUDANTE EXTERNO', 'CAIXA','OPERADOR','AUXILIAR','ANALISTA']

estoque['cargo_tratado'] = estoque['Objeto Assunto/Cargo (M)'].apply(lambda x: x if x in lista_cargos else 'OUTROS')

estoque.groupby(estoque.cargo_tratado).count()

dados_condenacao_geral = estoque

natureza_notin = ['TERCEIRO INSOLVENTE']
sub_area_direito_notin = ['PREVENTIVO AUTO DE INFRAÇÃO','CONTENCIOSO COLETIVO']
Outlier_notin = ['Outlier']

dados_condenacao_cargo = dados[(dados['MOTIVO_ENC_AGRP'] == 'CONDENACAO')
                        & (dados['NATUREZA_OPERACIONAL'].isin(natureza_notin))
                        & (~dados['SUB_AREA_DO_DIREITO'].isin(sub_area_direito_notin))
                        & (~dados['OUTLIER'].isin(Outlier_notin))       
                       ]
                       

#Define o filtro para Vendedor TREINO
estoque_cargo = estoque[(estoque['Natureza Operacional (M)'] == "TERCEIRO INSOLVENTE")]

#Cria um novo dataframe adequado ao scikit-learning para treinamento dos modelos
explicativas = pd.DataFrame()
explicativas['ID PROCESSO'] = dados_condenacao_geral['ID PROCESSO']
explicativas_cargo = pd.DataFrame()
explicativas_cargo['ID_PROCESSO'] = dados_condenacao_cargo.ID_PROCESSO

explicativas_estoque = pd.DataFrame()
explicativas_estoque['ID PROCESSO'] = estoque_cargo['ID PROCESSO']



#Faz o Label Encoder, que converte dados qualitativos de texto para um índice numérico
#Com esse encoding, podemos facilmente voltar aos valores originais utilizando a função inverse_transform

#adiciona a variável Estado codificada ao dataframe
le_estado = preprocessing.LabelEncoder()
encode_estado = le_estado.fit(estoque['ESTADO'])
explicativas['ESTADO'] = encode_estado.transform(dados_condenacao_geral['ESTADO'])
explicativas_cargo['ESTADO'] = encode_estado.transform(dados_condenacao_cargo['ESTADO'])
explicativas_estoque['ESTADO'] = encode_estado.transform(estoque_cargo['ESTADO'])


#gera o de-para dos estados
estados = pd.DataFrame()
estados['codigos'] = explicativas_estoque.ESTADO.unique()
estados['estados'] = encode_estado.inverse_transform(estados.codigos)
estados.sort_values(by='codigos')

#adiciona a variável cluster valor codificada ao dataframe
le_cluster_valor = preprocessing.LabelEncoder()
encode_cluster_valor = le_cluster_valor.fit(dados_condenacao_geral['cluster_valor'])
explicativas['cluster_valor'] = encode_cluster_valor.transform(dados_condenacao_geral['cluster_valor'])
explicativas_cargo['cluster_valor'] = encode_cluster_valor.transform(dados_condenacao_cargo['cluster_valor'])
explicativas_estoque['cluster_valor'] = encode_cluster_valor.transform(estoque_cargo['cluster_valor'])

#gera o de-para dos cluster valor
cluster_valor = pd.DataFrame()
cluster_valor['codigos'] = explicativas.cluster_valor.unique()
cluster_valor['cluster_valor'] = encode_cluster_valor.inverse_transform(cluster_valor.codigos)
cluster_valor.sort_values(by='codigos')

#adiciona a variável cargo_tratado codificada ao dataframe
le_cargo_tratado = preprocessing.LabelEncoder()
encode_cargo_tratado = le_cargo_tratado.fit(dados_condenacao_geral['cargo_tratado'])
explicativas['cargo_tratado'] = encode_cargo_tratado.transform(dados_condenacao_geral['cargo_tratado'])
explicativas_cargo['cargo_tratado'] = encode_cargo_tratado.transform(dados_condenacao_cargo['cargo_tratado'])
explicativas_estoque['cargo_tratado'] = encode_cargo_tratado.transform(estoque_cargo['cargo_tratado'])


#gera o de-para dos cargos
cargo = pd.DataFrame()
cargo['codigos'] = explicativas.cargo_tratado.unique()
cargo['cargo'] = encode_cargo_tratado.inverse_transform(cargo.codigos)
cargo.sort_values(by='codigos')

#adiciona a variável Cluster Aging Tempo de Empresa codificada ao dataframe
le_tempo_empresa = preprocessing.LabelEncoder()
encode_tempo_empresa = le_tempo_empresa.fit(dados_condenacao_geral['Cluster Aging Tempo de Empresa'])
explicativas['Cluster Aging Tempo de Empresa'] = encode_tempo_empresa.transform(dados_condenacao_geral['Cluster Aging Tempo de Empresa'])
explicativas_cargo['Cluster Aging Tempo de Empresa'] = encode_tempo_empresa.transform(dados_condenacao_cargo['Cluster Aging Tempo de Empresa'])
explicativas_estoque['Cluster Aging Tempo de Empresa'] = encode_tempo_empresa.transform(estoque_cargo['Cluster Aging Tempo de Empresa'])

#gera o de-para dos cluster tempo de empresa
tempo_empresa = pd.DataFrame()
tempo_empresa['codigos'] = explicativas['Cluster Aging Tempo de Empresa'].unique()
tempo_empresa['tempo_empresa'] = encode_tempo_empresa.inverse_transform(tempo_empresa.codigos)
tempo_empresa.sort_values(by='codigos')

#adiciona a variável Cluster Aging codificada ao dataframe
le_cluster_aging = preprocessing.LabelEncoder()
encode_cluster_aging = le_cluster_aging.fit(dados_condenacao_geral['Cluster Aging'])
explicativas['Cluster Aging'] = encode_cluster_aging.transform(dados_condenacao_geral['Cluster Aging'])
explicativas_cargo['Cluster Aging'] = encode_cluster_aging.transform(dados_condenacao_cargo['Cluster Aging'])
explicativas_estoque['Cluster Aging'] = encode_cluster_aging.transform(estoque_cargo['Cluster Aging'])

#gera o de-para dos cluster aging
cluster_aging = pd.DataFrame()
cluster_aging['codigos'] = explicativas['Cluster Aging'].unique()
cluster_aging['cluster_aging'] = encode_cluster_aging.inverse_transform(cluster_aging.codigos)
cluster_aging.sort_values(by='codigos')

#adiciona a variável Safra de Reclamação codificada ao dataframe
le_safra_reclamacao = preprocessing.LabelEncoder()
encode_safra_reclamacao = le_safra_reclamacao.fit(estoque['Safra de Reclamação'].astype(str))
explicativas['safra_reclamacao'] = encode_safra_reclamacao.transform(dados_condenacao_geral['Safra de Reclamação'].astype(str))
dados_condenacao_geral['safra_reclamacao'] = encode_safra_reclamacao.transform(dados_condenacao_geral['Safra de Reclamação'].astype(str))
explicativas_cargo['safra_reclamacao'] = encode_safra_reclamacao.transform(dados_condenacao_cargo['Safra de Reclamação'].astype(str))
explicativas_estoque['safra_reclamacao'] = encode_safra_reclamacao.transform(estoque_cargo['Safra de Reclamação'].astype(str))

#gera o de-para dos cluster pedidos
safra_reclamacao = pd.DataFrame()
safra_reclamacao['codigos'] = explicativas_estoque['safra_reclamacao'].unique()
safra_reclamacao['safra_reclamacao'] = encode_safra_reclamacao.inverse_transform(safra_reclamacao.codigos)
safra_reclamacao.sort_values(by='codigos')

le_ET = preprocessing.LabelEncoder()
encode_ET = le_ET.fit(estoque['ET'])
explicativas['ET'] = encode_ET.transform(dados_condenacao_geral['ET'])
explicativas_cargo['ET'] = encode_ET.transform(dados_condenacao_cargo['ET'])
explicativas_estoque['ET'] = encode_ET.transform(estoque_cargo['ET'])

#gera o de-para dos cluster aging
ET = pd.DataFrame()
ET['codigos'] = explicativas_estoque['ET'].unique()
ET['ET'] = encode_ET.inverse_transform(ET.codigos)
ET.sort_values(by='codigos')


    
#substitui nulos nas variáveis qualitativas por -999
#Como estamos trabalhando com modelos de árvore, os valores sem dados serão tratados como uma categoria à parte, muito distante das demais
explicativas = explicativas.fillna(-999)
explicativas_cargo = explicativas_cargo.fillna(-999)
explicativas_estoque = explicativas_estoque.fillna(-999)


#prepara target
resposta_cargo = pd.DataFrame(dados_condenacao_cargo['Pagamento Desindexado'])

#Construção do Modelo de Árvore de Decisão para Regressão - resposta numérica contínua
#Em cenários de classificação podemos usar a DecisionTreeClassifier
#É possível customizar critérios de parada através dos hiperparâmetros do modelo
DT = tree.DecisionTreeRegressor(random_state=42, 
                                max_depth=100, 
                                criterion='mae',
                                min_samples_leaf = 50)


#prepara target
resposta = pd.DataFrame(dados_condenacao_cargo['Pagamento Desindexado'])

DT = DT.fit(explicativas_cargo[['cluster_valor', 'Cluster Aging', 'ET','cargo_tratado']], resposta_cargo['Pagamento Desindexado'])

y_true = resposta_cargo['Pagamento Desindexado']
#y_pred = valor previsto pelo modelo treinado
y_pred = DT.predict(explicativas_cargo[['cluster_valor', 'Cluster Aging', 'ET','cargo_tratado']])

dados_estoque_full = estoque_cargo
#dados_estoque_full = dados_estoque
dados_estoque_full['prediction'] = DT.predict(explicativas_estoque[['cluster_valor', 'Cluster Aging', 'ET','cargo_tratado']])
#dados_estoque_full['prediction'] = DT.predict(explicativas_estoque[['cluster_valor', 'Cluster Aging Tempo de Empresa', 'Cluster Aging','safra_reclamacao']][explicativas.cargo_tratado == 10])

#dados_estoque.to_excel('previsao_condenacao_outros.xls')

"""
Cria uma lista com todos os dataframes e compila para exportar
"""

pdlist = [estoque_cargo_vendedor, estoque_cargo_montador, estoque_cargo_outros, estoque_cargo_ajudante,
          estoque_cargo_ajudanteexterno, estoque_cargo_auxiliar, estoque_cargo_motorista,
          estoque_cargo_analista, estoque_cargo_operador, estoque_cargo_caixa, 
          estoque_cargo_gerente, dados_estoque_full]


#cria uma lista com todos os dataframes importados
new_df = pd.concat(pdlist,ignore_index=True)
new_df.to_excel(r'C:\Users\2104998693\Desktop\Modelagem\Consolidado Modelagem 07_03.xlsx', sheet_name='Consolidado', index = False)
