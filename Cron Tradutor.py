# -*- coding: utf-8 -*-
"""
Created on Fri Aug 26 09:25:37 2022

@author: Daniel
"""
import pandas as pd
import numpy as np
from cron_descriptor import Options, CasingTypeEnum, DescriptionTypeEnum, ExpressionDescriptor

df = pd.read_excel(r'C:\Users\Daniel\Downloads\Cron EDP - Ag.xlsx', sheet_name = 'Base de Agendamentos')

# Consult Options.py/CasingTypeEnum.py/DescriptionTypeEnum.py for more info

d= []

for i in range(len(df)):
    descriptor = ExpressionDescriptor(
        expression = str(df['cron'][i]),
        throw_exception_on_parse_error = True, 
        casing_type = CasingTypeEnum.Sentence, 
        use_24hour_time_format = True
    )
    
    d.append(descriptor.get_description())

df['cron_traduzido'] = np.array(d)
    
df.to_excel(r'C:\Users\Daniel\Downloads\Análise de Dados de Agendamento EDP - Cron.xlsx', index=False)