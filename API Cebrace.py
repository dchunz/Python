import json
import requests
import pandas as pd

df = pd.read_excel(r'C:\Users\Daniel\Downloads\Listas do Automation Anywhere Cebrace.xlsx')


r = requests.post(url ='https://cebrace-1.my.automationanywhere.digital/v1/authentication' ,json = {"username":"rodrigo.abreu@dirwa.com","password":"Cebrace@10"})

resp = json.loads(r.text)
token = resp['token']

url_inicio = 'https://cebrace-1.my.automationanywhere.digital/v3/wlm/queues/'
url_final = '/workitems/list'

lista = list()

data_dic = {"page": {"offset": 0,"length": 2000}}

for item in df['id']:
    
    url_item = url_inicio + str(item) + url_final
    fila = requests.post(url = url_item, data = json.dumps(data_dic), headers= {"X-Authorization":token})
    filaresp = json.loads(fila.text)
    resposta = filaresp['list']

    export = pd.DataFrame(resposta)
    lista.append(export)
    
export_final = pd.concat(lista)

export_final.rename(
    columns=({'col1': 'Reference',
              'col2':'Tags',
              'col3':'Progress',
              'col4': 'DeferDate',
              'col5': 'ExceptionType',
              'col6': 'ExceptionDescription',
              'col7': 'Priority',
              'col8': 'LogFilePath',
              'col9': "StartTime",
              'col10':'ProcessTime'}), 
    inplace=True,)

export_final.to_excel(r'C:\Users\Daniel\Downloads\Listas do Automation Anywhere Cebrace Export_Ago16_v2.xlsx', index=False)