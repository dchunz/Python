# -*- coding: utf-8 -*-
"""
Created on Fri Mar 25 11:05:47 2022

@author: daniel.chun_kavak
"""

import pandas as pd
import numpy as np

inventario = pd.read_excel(r'C:\Users\daniel.chun_kavak\Desktop\Qualidade\GPS - Monitoria\Posição estoque KAVAK - Logística.xlsx', sheet_name="Sumário Geral", header = 2)
#Placa, stock id, location, status, data

ituran = pd.read_excel(r'C:\Users\daniel.chun_kavak\Desktop\Qualidade\GPS - Monitoria\BASE ATIVA KAVAK.xlsx', sheet_name = 'BASE')

ituran.rename(columns=({'PLaca': 'Placa'}), 
    inplace=True,)

iweb = pd.read_excel(r'C:\Users\daniel.chun_kavak\Desktop\Qualidade\GPS - Monitoria\iWeb.xlsx', sheet_name = 'Grid', header = 2)

inventario.drop_duplicates(subset = 'Placa', keep = 'last', inplace=True, ignore_index=True)

planodeacao = pd.read_excel(r'C:\Users\daniel.chun_kavak\Desktop\Qualidade\GPS - Monitoria\Plano de Ação Kavak Hubs.xlsx', sheet_name = 'Plano de Ação Kavak')

planodeacao['PLACA'] = planodeacao['PLACA'].str.strip()

planodeacao.drop_duplicates(subset = 'PLACA', keep = 'last', inplace=True, ignore_index=True)


inventario['Location'] = np.where(inventario['Status Aux'] == 'Vendido', 'Vendido', 
                                  np.where(inventario['Status Aux'] == 'Frota', 'Frota', 
                                           np.where(inventario['Status Aux'] == 'Pend.Criação Stock ID', 'Pend.Criação Stock ID',
                                                    np.where(inventario['Status Aux'] == 'Pendente de Roteirização (GPS)', 'Pendente de Roteirização (GPS)',
                                                             np.where(inventario['Status Aux'] == 'Trânsito', 'Trânsito', inventario['Location']
                                                                      )
                                                             )
                                                    )
                                           )
                                  )


ituran.drop_duplicates(subset = 'Placa', keep = 'first', inplace=True, ignore_index=True)

ituran_inventario = pd.merge(ituran, inventario[['Placa', 'Stock Id', 'Location', 'UF']], left_on='Placa', right_on = 'Placa', how='left', suffixes=('', '_DROP')).filter(regex='^(?!.*_DROP)')

iweb['HORA'] = pd.to_datetime(iweb['HORA'], infer_datetime_format = True)
iweb['Dias sem Comunicar'] = (pd.Timestamp('today')-iweb['HORA'] ).dt.days 


iweb['Status Comunicação'] = np.where(iweb['Dias sem Comunicar'] <= 3, "COMUNICOU ATÉ 72 HORAS",
                                      np.where(iweb['Dias sem Comunicar']<=7, "COMUNICOU ATÉ 7 DIAS",
                                               np.where(iweb['Dias sem Comunicar'] <= 15, "COMUNICOU ATÉ 15 DIAS",
                                                        np.where(iweb['Dias sem Comunicar'] <= 20, "COMUNICOU ATÉ 20 DIAS",
                                                                 np.where(iweb['Dias sem Comunicar'] <= 30, "COMUNICOU ATÉ 30 DIAS",
                                                                          np.where(iweb['Dias sem Comunicar'] <=45, "COMUNICOU ATÉ 45 DIAS",
                                                                                   np.where(iweb['Dias sem Comunicar'] <= 60, "COMUNICOU ATÉ 60 DIAS",
                                                                                            np.where(iweb["Dias sem Comunicar"] <= 90, "COMUNICOU ATÉ 90 DIAS",
                                                                                                     np.where(iweb['Dias sem Comunicar'] >= 90, "COMUNICOU HÁ MAIS DE 90 DIAS", "FORA DA LÓGICA")                                                                                                     
                                                                                                     )
                                                                                            )
                                                                                   )                                                                                   
                                                                          )
                                                                 )
                                                        )
                                               )
                                      )


ituran_inventario_iweb = pd.merge(ituran_inventario, iweb[['CHASSIS', 'HORA', 'Dias sem Comunicar', 'Status Comunicação', 'ESTADOS', 'ENDEREÇO']], left_on = 'Chassi', right_on = 'CHASSIS', how = 'left')

new = ituran_inventario_iweb["ESTADOS"].str.split(", ", n=-1, expand = True)

ituran_inventario_iweb['Status 1'] = new[0]
ituran_inventario_iweb['Status 2'] = new[1]
ituran_inventario_iweb['Status 3'] = new[2]
ituran_inventario_iweb['Status 4'] = new[3]
ituran_inventario_iweb['Status 5'] = new[4]
ituran_inventario_iweb['Status 6'] = new[5]
ituran_inventario_iweb['Status 7'] = new[6]
ituran_inventario_iweb['Status 8'] = new[7]
ituran_inventario_iweb['Status 9'] = new[8]
ituran_inventario_iweb['Status 10'] = new[9]
ituran_inventario_iweb['Status 11'] = new[10]

ituran_inventario_iweb['Ultimo Status'] = np.where((ituran_inventario_iweb['Dias sem Comunicar'] > 30) & (ituran_inventario_iweb['Status 11'] == " Bateria desconectada"), "Bateria desconectada",
                                                   np.where((ituran_inventario_iweb['Dias sem Comunicar'] > 30) & (ituran_inventario_iweb['Status 11'] == " Motor desligado"), "Motor desligado",
                                           
                                                       np.where((ituran_inventario_iweb['Dias sem Comunicar'] > 30) & (ituran_inventario_iweb['Status 10'] == "Bateria desconectada"), "Bateria desconectada",
                                                                np.where((ituran_inventario_iweb['Dias sem Comunicar'] > 30) & (ituran_inventario_iweb['Status 10'] == "Motor desligado"), "Motor desligado",
                                                                                                  
                                                                         np.where((ituran_inventario_iweb['Dias sem Comunicar'] > 30) & (ituran_inventario_iweb['Status 9'] == "Bateria desconectada"), "Bateria desconectada",
                                                                                  np.where((ituran_inventario_iweb['Dias sem Comunicar'] > 30) & (ituran_inventario_iweb['Status 9'] == "Motor desligado"), "Motor desligado",
                                                                                           
                                                                                           np.where((ituran_inventario_iweb['Dias sem Comunicar'] > 30) & (ituran_inventario_iweb['Status 8'] == "Bateria desconectada"), "Bateria desconectada",
                                                                                                    np.where((ituran_inventario_iweb['Dias sem Comunicar'] > 30) & (ituran_inventario_iweb['Status 8'] == "Motor desligado"), "Motor desligado",
                                                                                                             
                                                                                                             np.where((ituran_inventario_iweb['Dias sem Comunicar'] > 30) & (ituran_inventario_iweb['Status 7'] == "Bateria desconectada"), "Bateria desconectada",
                                                                                                                      np.where((ituran_inventario_iweb['Dias sem Comunicar'] > 30) & (ituran_inventario_iweb['Status 7'] == "Motor desligado"), "Motor desligado",
                                                                                                                               
                                                                                                                               np.where((ituran_inventario_iweb['Dias sem Comunicar'] > 30) & (ituran_inventario_iweb['Status 6'] == "Bateria desconectada"), "Bateria desconectada",
                                                                                                                                        np.where((ituran_inventario_iweb['Dias sem Comunicar'] > 30) & (ituran_inventario_iweb['Status 6'] == "Motor desligado"), "Motor desligado",
                                                                                                                                                 
                                                                                                                                                 np.where((ituran_inventario_iweb['Dias sem Comunicar'] > 30) & (ituran_inventario_iweb['Status 5'] == "Bateria desconectada"), "Bateria desconectada",
                                                                                                                                                          np.where((ituran_inventario_iweb['Dias sem Comunicar'] > 30) & (ituran_inventario_iweb['Status 5'] == "Motor desligado"), "Motor desligado",
                                                                                                                                                                   
                                                                                                                                                                   np.where((ituran_inventario_iweb['Dias sem Comunicar'] > 30) & (ituran_inventario_iweb['Status 4'] == "Bateria desconectada"), "Bateria desconectada",
                                                                                                                                                                            np.where((ituran_inventario_iweb['Dias sem Comunicar'] > 30) & (ituran_inventario_iweb['Status 4'] == "Motor desligado"), "Motor desligado",
                                                                                                                                                                                     
                                                                                                                                                                                     np.where((ituran_inventario_iweb['Dias sem Comunicar'] > 30) & (ituran_inventario_iweb['Status 3'] == "Bateria desconectada"), "Bateria desconectada",
                                                                                                                                                                                              np.where((ituran_inventario_iweb['Dias sem Comunicar'] > 30) & (ituran_inventario_iweb['Status 3'] == "Motor desligado"), "Motor desligado",
                                                                                                                                                                                                       
                                                                                                                                                                                                       np.where((ituran_inventario_iweb['Dias sem Comunicar'] > 30) & (ituran_inventario_iweb['Status 2'] == "Bateria desconectada"), "Bateria desconectada",
                                                                                                                                                                                                                np.where((ituran_inventario_iweb['Dias sem Comunicar'] > 30) & (ituran_inventario_iweb['Status 2'] == "Motor desligado"), "Motor desligado",
                                                                                                                                                                                                                         
                                                                                                                                                                                                                         np.where((ituran_inventario_iweb['Dias sem Comunicar'] > 30) & (ituran_inventario_iweb['Status 1'] == "Bateria desconectada"), "Bateria desconectada",
                                                                                                                                                                                                                                  np.where((ituran_inventario_iweb['Dias sem Comunicar'] > 30) & (ituran_inventario_iweb['Status 1'] == "Motor desligado"), "Motor desligado",
                                                                                                                                                                                                                                           "Não se aplica"
                                                                                                                                                                                                                                           )
                                                                                                                                                                                                                                  )
                                                                                                                                                                                                                         )
                                                                                                                                                                                                                )
                                                                                                                                                                                                       )
                                                                                                                                                                                              )
                                                                                                                                                                                     )
                                                                                                                                                                            )
                                                                                                                                                                   
                                                                                                                                                                   )
                                                                                                                                                          )
                                                                                                                                                 )
                                                                                                                                     )
                                                                                                                            )
                                                                                                                   )
                                                                                                          )
                                                                                                 )
                                                                                        )
                                                                               )
                                                                      )
                                                             )
                                                    )
                                           )

ituran_inventario_iweb['Ultimo Status'] = np.where(ituran_inventario_iweb['ENDEREÇO'] == '!! Endereço não encontrado !!', 'ATIVAÇÃO EM CERCA', ituran_inventario_iweb['Ultimo Status'] )

drop_columns = (['Status 1', 'Status 2', 'Status 3', 'Status 4', 'Status 5', 'Status 6',
                 'Status 7', 'Status 8', 'Status 9', 'Status 10', 'Status 11'])
#Grupo (Fechamento)	PAGAMENTOS	PAGAMENTO	REATIVADO	Pagamentos	Valor	REATIVADOS	Pgto	Pgto 2
ituran_inventario_iweb.drop(drop_columns ,axis='columns',inplace=True)


ituran_inventario_iweb_plano = pd.merge(ituran_inventario_iweb, planodeacao[['PLACA', 'TESTES/TROCA/REVISÃO']], left_on = 'Placa', right_on = 'PLACA', how='left', suffixes=('', '_DROP')).filter(regex='^(?!.*_DROP)')

ituran_inventario_iweb_plano['Ultimo Status'] = np.where(ituran_inventario_iweb_plano['Ultimo Status'] == "Bateria desconectada", ituran_inventario_iweb_plano['Ultimo Status'],
                                                         np.where(ituran_inventario_iweb_plano['Ultimo Status'] == "Motor desligado", ituran_inventario_iweb_plano['Ultimo Status'],
                                                                  np.where(ituran_inventario_iweb_plano['Ultimo Status'] == "ATIVAÇÃO EM CERCA", ituran_inventario_iweb_plano['Ultimo Status'],
                                                                           np.where(~ituran_inventario_iweb_plano['TESTES/TROCA/REVISÃO'].isnull(), 'ATUAÇÃO HUBS',
                                                                                    ituran_inventario_iweb_plano['Ultimo Status'])
                                                                           )
                                                                  )
                                                         )

basefinal_group = ituran_inventario_iweb_plano.groupby(['Ultimo Status', 'Status Comunicação', 'STATUS' ]).size()

ituran_inventario_iweb_plano.to_excel(r'C:\Users\daniel.chun_kavak\Desktop\Qualidade\GPS.xlsx',index=False)