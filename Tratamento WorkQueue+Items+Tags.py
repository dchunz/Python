# -*- coding: utf-8 -*-
"""
Created on Mon Oct 17 10:42:34 2022

@author: Daniel
"""

# function
def dfs_tabs(df_list, sheet_list, file_name):
    writer = pd.ExcelWriter(file_name,engine='xlsxwriter')   
    for dataframe, sheet in zip(df_list, sheet_list):
        dataframe.to_excel(writer, sheet_name=sheet, startrow=0 , startcol=0)   
    writer.save()

import pandas as pd
import numpy as np

work_queue = pd.read_csv(r'C:\Users\Daniel\Desktop\Dirwa\Análise EDP\Work Queues.csv', sep=";")
items_tags = pd.read_csv(r'C:\Users\Daniel\Desktop\Dirwa\Análise EDP\Itens x Tags.csv',sep =";")
items = pd.read_csv(r'C:\Users\Daniel\Desktop\Dirwa\Análise EDP\Itens.csv',sep =";")

workqueue_items = pd.merge(items, work_queue[['id', 'name']], left_on= 'queueid', right_on='id', how= 'left')

workqueue_items_tags = pd.merge(workqueue_items, items_tags, left_on = 'ident', right_on = 'queueitemident', how = 'left')


workqueue_items_tags["TipoExcecao"] = np.where(workqueue_items_tags['tagid'] == "", "", 
                                                   np.where(workqueue_items_tags['tagid'] == 50554, "Business Exception",
                                                            np.where(workqueue_items_tags['tagid'] == 50603, "System Exception", ""
                                                                     )
                                                            )
                                                   )


workqueue_items_tags.rename(
    columns=({ 'id_x': 'ID', 'queueid': "Queue ID", "ident":"Queue Item Ident", "name": "Nome Processo"}), 
    inplace=True,)


dropcolumns = (['id_y', 'queueitemident'])

workqueue_items_tags.drop(dropcolumns ,axis='columns',inplace=True)

workqueue_items_tags['lastupdated'] = pd.to_datetime(workqueue_items_tags['lastupdated'])

workqueue_items_sumary = pd.crosstab(workqueue_items_tags['lastupdated'].dt.to_period('d'), workqueue_items_tags['Nome Processo'])

df_semstatus = workqueue_items_tags[workqueue_items_tags['TipoExcecao']== ""]

df_semstatussummary = pd.crosstab(df_semstatus['lastupdated'].dt.to_period('d'), df_semstatus['Nome Processo'])

df_business = workqueue_items_tags[workqueue_items_tags['TipoExcecao']== "Business Exception"]

df_businesssummary = pd.crosstab(df_business['lastupdated'].dt.to_period('d'), df_business['Nome Processo'])

df_system = workqueue_items_tags[workqueue_items_tags['TipoExcecao']== "System Exception"]

df_systemssummary = pd.crosstab(df_system['lastupdated'].dt.to_period('d'), df_system['Nome Processo'])

# list of dataframes and sheet names
dfs = [workqueue_items_sumary, df_semstatussummary, df_businesssummary, df_systemssummary]
sheets = ['Sumário WorkQueue','Sumário Completed','Sumário Business Exception', "Sumário System Exception"]    

# run function
dfs_tabs(dfs, sheets, 'multi-test.xlsx')

