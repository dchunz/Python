# -*- coding: utf-8 -*-
"""
Created on Wed Aug 24 13:19:20 2022

@author: Daniel
"""

import pandas as pd
from croniter import croniter_range
from datetime import datetime
from cron_descriptor import get_description, ExpressionDescriptor

#print(get_description("* 2 3 * *"))
#print(str(ExpressionDescriptor("* 2 3 * *")))

df = pd.read_excel(r'C:\Users\Daniel\Downloads\Evolução Indicadores EDP - Import.xlsx', sheet_name = 'Agendamentos')

d = []

for id in range(len(df['ID'])):
    #print(expression)

    expression = df['cron'][id]
    
    for date in croniter_range(datetime(2022,8,1), datetime(2022, 9, 1), str(expression)):
        
        d.append(
            {
            'ID' : df['ID'][id],
            'Período': df['Período'][id],
            'Quantidade': df['Quantidade'][id],
            'Critério': df['Critério'][id],
            'Horário Agendamento': df['Horário Agendamento'][id],
            'Pool' : df['Pool'][id],
            'Automações/Processos Blue Prism': df['Automações/Processos Blue Prism'][id],
            'Expression': expression,
            'Tasks': df['Tasks'][id],
            'cron': date

            })
        #print(date)
        
export = pd.DataFrame(d)
export['Tasks'] = export['Tasks'].str.strip(' \t\n\r')
export.to_excel(r'C:\Users\Daniel\Downloads\Cron EDP.xlsx', index=False)