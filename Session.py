# -*- coding: utf-8 -*-
"""
Created on Thu Oct 13 15:57:57 2022

@author: Daniel
"""

def dfs_tabs(df_list, sheet_list, file_name):
    writer = pd.ExcelWriter(file_name,engine='xlsxwriter')   
    for dataframe, sheet in zip(df_list, sheet_list):
        dataframe.to_excel(writer, sheet_name=sheet, startrow=0 , startcol=0)   
    writer.save()

import pandas as pd
import numpy as np

BPA_process = pd.read_excel(r'C:\Users\Daniel\Desktop\Dirwa\Ultimos 6 meses\BPA Process.xlsx')

#BPA_process.to_excel(r'C:\Users\Daniel\Desktop\Dirwa\Ultimos 6 meses\BPA Processt.xlsx', index=False)

session_id = pd.read_csv(r'C:\Users\Daniel\Desktop\Dirwa\Ultimos 6 meses\Session - 04 a 09 2022.csv', sep=";")

ProcessTratado = pd.merge(session_id, BPA_process[['processid', 'name']], how="left")

ProcessTratado['Status'] = np.where(ProcessTratado['statusid'] == 2, "Terminated",
                                    np.where(ProcessTratado['statusid'] == 3, "Stopped",
                                             np.where(ProcessTratado['statusid'] == 4, "Success",
                                                      "N/A"
                                                      )
                                             )
                                    ) 

ProcessTratado['lastupdated'] = pd.to_datetime(ProcessTratado['lastupdated'])

process_cross = pd.crosstab(ProcessTratado['lastupdated'].dt.to_period('d'), ProcessTratado['name'])

process_cross_terminated = ProcessTratado[ProcessTratado['Status']=="Terminated"]
process_cross_stopped = ProcessTratado[ProcessTratado['Status']=="Stopped"]
process_cross_success = ProcessTratado[ProcessTratado['Status']=="Success"]

process_cross_terminated_summary = pd.crosstab(process_cross_terminated['lastupdated'].dt.to_period('d'), process_cross_terminated['name'])
process_cross_stopped_summary = pd.crosstab(process_cross_stopped['lastupdated'].dt.to_period('d'), process_cross_stopped['name'])
process_cross_success_summary = pd.crosstab(ProcessTratado['lastupdated'].dt.to_period('d'), ProcessTratado['name'])

# list of dataframes and sheet names
dfs = [ProcessTratado, process_cross_terminated_summary, process_cross_stopped_summary, process_cross_success_summary]
sheets = ['Processo Sessões','Sumário Completed','Sumário Stopped', "Sumário Sucess"]    

# run function
dfs_tabs(dfs, sheets, 'multi-test-session.xlsx')
