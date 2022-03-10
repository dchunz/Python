import pandas as pd
#importar a biblioteca pandas para manipulação das bases

Set21 = pd.read_excel(r'Z:\01 PLANEJ FINANCEIRO JURIDICO\137.ANALYTICS\3 Prévias\2021\09. Setembro\21.09.2021 Fechamento Imobiliario.xlsx',sheet_name=('Base Fechamento'),header=1)
Set21['LINHA'] = "09/01/2021"
Set21['LINHA'] = pd.to_datetime(Set21['LINHA'])
Set21.dropna(how='all')

Ago21 = pd.read_excel(r'Z:\01 PLANEJ FINANCEIRO JURIDICO\137.ANALYTICS\3 Prévias\2021\08. Agosto\22.08.2021 Fechamento Imobiliario.xlsx',sheet_name=('Base Fechamento'),header=1)
Ago21['LINHA'] = "08/01/2021"
Ago21['LINHA'] = pd.to_datetime(Ago21['LINHA'])
Ago21.dropna(how='all')

Jul21 = pd.read_excel(r'Z:\01 PLANEJ FINANCEIRO JURIDICO\137.ANALYTICS\3 Prévias\2021\07. Julho\22.07.2021 Fechamento Imobiliario.xlsx',sheet_name=('Base Fechamento'),header=1)
#importar as bases de fechamento com seus respectivos períodos
Jul21['LINHA'] = "07/01/2021"
#fazer da primeira coluna uma coluna referencial da data da base de dados
Jul21['LINHA'] = pd.to_datetime(Jul21['LINHA'])
#converter o valor das datas armazenadas como texto para formato data
Jul21.dropna(how='all')
#excluir colunas vazias

Jun21 = pd.read_excel(r'Z:\01 PLANEJ FINANCEIRO JURIDICO\137.ANALYTICS\3 Prévias\2021\06. Junho\21.06.2021 Fechamento Imobiliario.xlsx',sheet_name=('Base Fechamento'),header=1)
Jun21['LINHA'] = "06/01/2021"
Jun21['LINHA'] = pd.to_datetime(Jun21['LINHA'])
Jun21.dropna(how='all')

Mai21 = pd.read_excel(r'Z:\01 PLANEJ FINANCEIRO JURIDICO\137.ANALYTICS\3 Prévias\2021\05. Maio\23.05.2021 Fechamento Imobiliario.xlsx',sheet_name=('Base Fechamento'),header=1)
Mai21['LINHA'] = "05/01/2021"
Mai21['LINHA'] = pd.to_datetime(Mai21['LINHA'])
Mai21.dropna(how='all')

Abr21 = pd.read_excel(r'Z:\01 PLANEJ FINANCEIRO JURIDICO\137.ANALYTICS\3 Prévias\2021\04. Abril\22.04.2021 Fechamento Imobiliario.xlsx',sheet_name=('Base Prévia'),header=1)
Abr21['LINHA'] = "04/01/2021"
Abr21['LINHA'] = pd.to_datetime(Abr21['LINHA'])
Abr21.dropna(how='all')

Mar21 = pd.read_excel(r'Z:\01 PLANEJ FINANCEIRO JURIDICO\137.ANALYTICS\3 Prévias\2021\03. Março\19.03.2021 Fechamento Imobiliario.xlsx',sheet_name=('Base Prévia'),header=1)
Mar21['LINHA'] = "03/01/2021"
Mar21['LINHA'] = pd.to_datetime(Mar21['LINHA'])
Mar21.dropna(how='all')

Fev21 = pd.read_excel(r'Z:\01 PLANEJ FINANCEIRO JURIDICO\137.ANALYTICS\3 Prévias\2021\02. Fevereiro\22.02 Fechamento Imob.xlsx',sheet_name=('Base Fechamento'),header=1)
Fev21['LINHA'] = "02/01/2021"
Fev21['LINHA'] = pd.to_datetime(Fev21['LINHA'])
Fev21.dropna(how='all')

Jan21 = pd.read_excel(r'Z:\01 PLANEJ FINANCEIRO JURIDICO\137.ANALYTICS\3 Prévias\2021\01. Janeiro\22.01 Fechamento Imob.xlsx',sheet_name=('Base Fechamento'),header=1)
Jan21['LINHA'] = "01/01/2021"
Jan21['LINHA'] = pd.to_datetime(Jan21['LINHA'])
Jan21.dropna(how='all')


#Renomear inconsistências de nome dentro das colunas
Mar21.rename(
    columns=({'Cadastro':'DATACADASTRO'}), 
    inplace=True,)

Mai20 = pd.read_excel(r'Z:\01 PLANEJ FINANCEIRO JURIDICO\137.ANALYTICS\3 Prévias\2020\Imobiliário\FECHAMENTO IMOBILIÁRIO_MAIO_20_FINAL.xlsx',sheet_name=('Exportar Planilha'),header=3)
Mai20['LINHA'] = "05/01/2020"
Mai20['LINHA'] = pd.to_datetime(Mai20['LINHA'])
Mai20.dropna(how='all')

Mai20.rename(
    columns=({'ENCERRADO':'ENCERRADOS','Cadastro':'DATACADASTRO', 'SOCIO: Correção (M-1)': 'SOCIO: Correção (M-1)_0001', 'EMPRESA: Correção (M-1)': 'EMPRESA: Correção (M-1)_0001'}), 
    inplace=True,)

Jun20 = pd.read_excel(r'Z:\01 PLANEJ FINANCEIRO JURIDICO\137.ANALYTICS\3 Prévias\2020\Imobiliário\FECHAMENTO IMOBILIÁRIO_JUNHO_20_REv_2 (003).xlsx',sheet_name=('Exportar Planilha'),header=4)
Jun20['LINHA'] = "06/01/2020"
Jun20['LINHA'] = pd.to_datetime(Jun20['LINHA'])
Jun20.dropna(how='all')

Jun20.rename(
    columns=({'NOVO': 'NOVOS', 'ENCERRADO':'ENCERRADOS', 'Cadastro':'DATACADASTRO', 'FILIAL': 'Filial (M)', 'EMPRESA: Correção (M-1)': 'EMPRESA: Correção (M-1)_0001'}), 
    inplace=True,)

Jul20 = pd.read_excel(r'Z:\01 PLANEJ FINANCEIRO JURIDICO\137.ANALYTICS\3 Prévias\2020\Imobiliário\FECHAMENTO IMOBILIARIO_JULHO_20 (002).xlsx',sheet_name=('Exportar Planilha'),header=4)
Jul20['LINHA'] = "07/01/2020"
Jul20['LINHA'] = pd.to_datetime(Jul20['LINHA'])
Jul20.dropna(how='all')

Jul20.rename(
    columns=({'Cadastro':'DATACADASTRO', 'FILIAL': 'Filial (M)'}), 
    inplace=True,)


Ago20 = pd.read_excel(r'Z:\01 PLANEJ FINANCEIRO JURIDICO\137.ANALYTICS\3 Prévias\2020\Imobiliário\FECHAMENTO IMOBILIARIO_AGOSTO_20.xlsx',sheet_name=('Exportar Planilha'),header=2)
Ago20['LINHA'] = "08/01/2020"
Ago20['LINHA'] = pd.to_datetime(Ago20['LINHA'])
Ago20.dropna(how='all')

Ago20.rename(
    columns=({'NOVO': 'NOVOS', 'ENCERRADO':'ENCERRADOS', 'Cadastro':'DATACADASTRO'}), 
    inplace=True,)

Set20 = pd.read_excel(r'Z:\01 PLANEJ FINANCEIRO JURIDICO\137.ANALYTICS\3 Prévias\2020\Imobiliário\FECHAMENTO IMOBILIARIO SETEMBRO_20.xlsx',sheet_name=('Exportar Planilha'),header=3)
Set20.dropna(subset = ["ID PROCESSO"], inplace=True)
Set20['LINHA'] = "09/01/2020"
Set20['LINHA'] = pd.to_datetime(Set20['LINHA'])
Set20.dropna(how='all')

Set20.rename(
    columns=({'Cadastro':'DATACADASTRO'}), 
    inplace=True,)


Out20 = pd.read_excel(r'Z:\01 PLANEJ FINANCEIRO JURIDICO\137.ANALYTICS\3 Prévias\2020\Imobiliário\FECHAMENTO IMOBILIÁRIO OUTUBRO 2020.xlsx',sheet_name=('Fechamento'),header=3)
Out20.dropna(subset = ["ID PROCESSO"], inplace=True)
Out20['LINHA'] = "10/01/2020"
Out20['LINHA'] = pd.to_datetime(Out20['LINHA'])
Out20.dropna(how='all')

Out20.rename(
    columns=({'NOVO': 'NOVOS', 'ENCERRADO':'ENCERRADOS', 'Cadastro':'DATACADASTRO'}), 
    inplace=True,)

Nov20 = pd.read_excel(r'Z:\01 PLANEJ FINANCEIRO JURIDICO\137.ANALYTICS\3 Prévias\2020\Imobiliário\FECHAMENTO IMOBILIÁRIO NOVEMBRO 2020.xlsx',sheet_name=('Fechamento'),header=3)
Nov20.dropna(subset = ["ID PROCESSO"], inplace=True)
Nov20['LINHA'] = "11/01/2020"
Nov20['LINHA'] = pd.to_datetime(Nov20['LINHA'])
Nov20.dropna(how='all')

Nov20.rename(
    columns=({'NOVO': 'NOVOS', 'ENCERRADO':'ENCERRADOS', 'Cadastro':'DATACADASTRO', 'SOCIO: Correção (M-1)': 'SOCIO: Correção (M-1)_0001', 'EMPRESA: Correção (M-1)': 'EMPRESA: Correção (M-1)_0001'}), 
    inplace=True,)


Dez20 = pd.read_excel(r'Z:\01 PLANEJ FINANCEIRO JURIDICO\137.ANALYTICS\3 Prévias\2020\Imobiliário\FECHAMENTO IMOBILIÁRIO NOVEMBRO 2020.xlsx',sheet_name=('Fechamento'),header=3)
Dez20.dropna(subset = ["ID PROCESSO"], inplace=True)
Dez20['LINHA'] = "12/01/2020"
Dez20['LINHA'] = pd.to_datetime(Dez20['LINHA'])
Dez20.dropna(how='all')

Dez20.rename(
    columns=({'NOVO': 'NOVOS', 'ENCERRADO':'ENCERRADOS', 'Cadastro':'DATACADASTRO', 'SOCIO: Correção (M-1)': 'SOCIO: Correção (M-1)_0001', 'EMPRESA: Correção (M-1)':'EMPRESA: Correção (M-1)_0001'}), 
    inplace=True,)


pdList = [Set21, Ago21, Jul21, Abr21, Mai21, Jun21, Mar21, Fev21, Jan21, 
          Mai20, Jun20, Jul20, Ago20, Set20, Out20, Nov20, Dez20]  # List of your dataframes
#cria uma lista com todos os dataframes importados
new_df = pd.concat(pdList,ignore_index=True)
#new_df é a junção de todos os dataframes listados


new_df.rename(
    columns=({ 'LINHA': 'Data'}), 
    inplace=True,)
#Substitui a coluna 'LINHA' por uma coluna chamada Data

drop_columns = (['PASTA','Grupo (M-1)', 'Empresa (M-1)', 'Grupo (M)', 'STATUS (M-1)', 'Centro de Custo (M-1)', 'Reabertura',\
                 'Objeto Assunto/Cargo (M-1)', 'Sub Objeto Assunto/Cargo (M-1)', 'Órgão ofensor (Fluxo) (M-1)',\
                 'Órgão ofensor (Fluxo) (M)', 'Natureza Operacional (M-1)', 'Média de Pagamento', 'Nº Processo', '% Sócio (M-1)',\
                 '% Empresa (M-1)', 'Demitido por Reestruturação', 'Filial (M)', 'Grupo (Fechamento)', 'PAGAMENTOS', \
                 'PAGAMENTO', 'REATIVADO', 'Pagamentos', 'Valor', 'REATIVADOS', 'Pgto', 'Pgto 2'])
#Grupo (Fechamento)	PAGAMENTOS	PAGAMENTO	REATIVADO	Pagamentos	Valor	REATIVADOS	Pgto	Pgto 2
new_df.drop(drop_columns ,axis='columns',inplace=True)

remove_cols = [col for col in new_df.columns if 'Unnamed' in col]
new_df.drop(remove_cols,axis='columns',inplace=True)
#Remover todas as colunas sem some nos dataframes


new_df.to_excel('Imobiliário Consolidado.xlsx', index=False)
#Exportar os arquivos para Excel