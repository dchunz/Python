import pandas as pd

#importar as bases 2021



#Jul21 = pd.read_excel(r'Z:\01 PLANEJ FINANCEIRO JURIDICO\137.ANALYTICS\3 Prévias\2021\07. Julho\22.07.2021 Fechamento Imobiliario.xlsx',sheet_name=('Base Fechamento'),header=1)
#Jul21['LINHA'] = "01/07/2021"
#Jul21['LINHA'] = pd.to_datetime(Jul21['LINHA'])


Jun21 = pd.read_excel(r'Z:\01 PLANEJ FINANCEIRO JURIDICO\137.ANALYTICS\3 Prévias\2021\06. Junho\21.06.2021 Fechamento Imobiliario.xlsx',sheet_name=('Base Fechamento'),header=1)
Jun21['LINHA'] = "01/06/2021"
Jun21['LINHA'] = pd.to_datetime(Jul21['LINHA'])

#Mai21 = pd.read_excel(r'Z:\01 PLANEJ FINANCEIRO JURIDICO\137.ANALYTICS\3 Prévias\2021\05. Maio\23.05.2021 Fechamento Imobiliario.xlsx',sheet_name=('Base Fechamento'),header=1)
#Mai21['LINHA'] = "01/05/2021"
#Mai21['LINHA'] = pd.to_datetime(Jul21['LINHA'])

#Abr21 = pd.read_excel(r'Z:\01 PLANEJ FINANCEIRO JURIDICO\137.ANALYTICS\3 Prévias\2021\04. Abril\22.04.2021 Fechamento Imobiliario.xlsx',sheet_name=('Base Prévia'),header=1)
#Abr21['LINHA'] = "01/04/2021"
#Abr21['LINHA'] = pd.to_datetime(Jul21['LINHA'])

#Mar21 = pd.read_excel(r'Z:\01 PLANEJ FINANCEIRO JURIDICO\137.ANALYTICS\3 Prévias\2021\03. Março\19.03.2021 Fechamento Imobiliario.xlsx',sheet_name=('Base Prévia'),header=1)
#Mar21['LINHA'] = "01/03/2021"
#Mar21['LINHA'] = pd.to_datetime(Jul21['LINHA'])

#Mai20 = pd.read_excel(r'Z:\01 PLANEJ FINANCEIRO JURIDICO\137.ANALYTICS\3 Prévias\2020\Imobiliário\FECHAMENTO IMOBILIÁRIO_MAIO_20_FINAL.xlsx',sheet_name=('Exportar Planilha'),header=3)
#Mai20['LINHA'] = "01/05/2020"
#Mai20['LINHA'] = pd.to_datetime(Jul21['LINHA'])

#Jun20 = pd.read_excel(r'Z:\01 PLANEJ FINANCEIRO JURIDICO\137.ANALYTICS\3 Prévias\2020\Imobiliário\FECHAMENTO IMOBILIÁRIO_JUNHO_20_REv_2 (003).xlsx',sheet_name=('Exportar Planilha'),header=4)
#Jun20['LINHA'] = "01/06/2020"
#Jun20['LINHA'] = pd.to_datetime(Jul21['LINHA'])

#Jul20 = pd.read_excel(r'Z:\01 PLANEJ FINANCEIRO JURIDICO\137.ANALYTICS\3 Prévias\2020\Imobiliário\FECHAMENTO IMOBILIARIO_JULHO_20 (002).xlsx',sheet_name=('Exportar Planilha'),header=4)
#Jul20['LINHA'] = "01/07/2020"
#Jul20['LINHA'] = pd.to_datetime(Jul21['LINHA'])

#Ago20 = pd.read_excel(r'Z:\01 PLANEJ FINANCEIRO JURIDICO\137.ANALYTICS\3 Prévias\2020\Imobiliário\FECHAMENTO IMOBILIARIO_AGOSTO_20.xlsx',sheet_name=('Exportar Planilha'),header=2)
#Ago20['LINHA'] = "01/08/2020"
#Ago20['LINHA'] = pd.to_datetime(Jul21['LINHA'])

#Set20 = pd.read_excel(r'Z:\01 PLANEJ FINANCEIRO JURIDICO\137.ANALYTICS\3 Prévias\2020\Imobiliário\FECHAMENTO IMOBILIARIO SETEMBRO_20.xlsx',sheet_name=('Exportar Planilha'),header=3)
#Set20['LINHA'] = "01/09/2020"
#Set20['LINHA'] = pd.to_datetime(Jul21['LINHA'])

#Out20 = pd.read_excel(r'Z:\01 PLANEJ FINANCEIRO JURIDICO\137.ANALYTICS\3 Prévias\2020\Imobiliário\FECHAMENTO IMOBILIÁRIO OUTUBRO 2020.xlsx',sheet_name=('Fechamento'),header=3)
#Out20['LINHA'] = "01/10/2020"
#Out20['LINHA'] = pd.to_datetime(Jul21['LINHA'])

#Nov20 = pd.read_excel(r'Z:\01 PLANEJ FINANCEIRO JURIDICO\137.ANALYTICS\3 Prévias\2020\Imobiliário\FECHAMENTO IMOBILIÁRIO NOVEMBRO 2020.xlsx',sheet_name=('Fechamento'),header=3)
#Nov20['LINHA'] = "01/11/2020"
#Nov20['LINHA'] = pd.to_datetime(Jul21['LINHA'])

#Dez20 = pd.read_excel(r'Z:\01 PLANEJ FINANCEIRO JURIDICO\137.ANALYTICS\3 Prévias\2020\Imobiliário\FECHAMENTO IMOBILIÁRIO NOVEMBRO 2020.xlsx',sheet_name=('Fechamento'),header=3)
#Dez20['LINHA'] = "01/12/2020"
#Dez20['LINHA'] = pd.to_datetime(Jul21['LINHA'])

pdList = [Mai20, Jun20, Jul20, Ago20, Set20, Out20, Nov20, Dez20, \
          Mar21, Abr21, Mai21, Jun21, Jul21]  # List of your dataframes
new_df = pd.concat(pdList)


#ds.rename(
    #columns=({ 'LINHA': 'Data'}), 
    #inplace=True,)
