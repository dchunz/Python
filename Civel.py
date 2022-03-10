
import pandas as pd
#importar a biblioteca pandas para manipulação das bases

Set21 = pd.read_excel(r'Z:\01 PLANEJ FINANCEIRO JURIDICO\137.ANALYTICS\3 Prévias\2021\09. Setembro\21.09.2021 Fechamento Cível.xlsx',sheet_name=('Base Fechamento'),header=1)
#importar as bases de fechamento com seus respectivos períodos
Set21['LINHA'] = "09/01/2021"
#fazer da primeira coluna uma coluna referencial da data da base de dados
Set21['LINHA'] = pd.to_datetime(Set21['LINHA'])
#converter o valor das datas armazenadas como texto para formato data
Set21.dropna(how='all')
#excluir colunas vazias

Ago21 = pd.read_excel(r'Z:\01 PLANEJ FINANCEIRO JURIDICO\137.ANALYTICS\3 Prévias\2021\08. Agosto\22.08.2021 Fechamento Cível.xlsx',sheet_name=('Base Fechamento'),header=1)
Ago21['LINHA'] = "08/01/2021"
Ago21['LINHA'] = pd.to_datetime(Ago21['LINHA'])
Ago21.dropna(how='all')

Jul21 = pd.read_excel(r'Z:\01 PLANEJ FINANCEIRO JURIDICO\137.ANALYTICS\3 Prévias\2021\07. Julho\22.07.2021 Fechamento Cível.xlsx',sheet_name=('Base Fechamento'),header=1)
Jul21['LINHA'] = "07/01/2021"
Jul21['LINHA'] = pd.to_datetime(Jul21['LINHA'])
Jul21.dropna(how='all')

Jun21 = pd.read_excel(r'Z:\01 PLANEJ FINANCEIRO JURIDICO\137.ANALYTICS\3 Prévias\2021\06. Junho\21.06.2021 Fechamento Cível.xlsx',sheet_name=('Base Prévia'),header=1)
Jun21['LINHA'] = "06/01/2021"
Jun21['LINHA'] = pd.to_datetime(Jun21['LINHA'])
Jun21.dropna(how='all')

Mai21 = pd.read_excel(r'Z:\01 PLANEJ FINANCEIRO JURIDICO\137.ANALYTICS\3 Prévias\2021\05. Maio\23.05.2021 Fechamento Cível.xlsx',sheet_name=('Base Fechamento'),header=1)
Mai21['LINHA'] = "05/01/2021"
Mai21['LINHA'] = pd.to_datetime(Mai21['LINHA'])
Mai21.dropna(how='all')

Abr21 = pd.read_excel(r'Z:\01 PLANEJ FINANCEIRO JURIDICO\137.ANALYTICS\3 Prévias\2021\04. Abril\22.04.2021 Fechamento Cível.xlsx',sheet_name=('Base Fechamento'),header=1)
Abr21['LINHA'] = "04/01/2021"
Abr21['LINHA'] = pd.to_datetime(Abr21['LINHA'])
Abr21.dropna(how='all')

Mar21 = pd.read_excel(r'Z:\01 PLANEJ FINANCEIRO JURIDICO\137.ANALYTICS\3 Prévias\2021\03. Março\19.03.2021 Fechamento Cível.xlsx',sheet_name=('Base Fechamento'),header=1)
Mar21['LINHA'] = "03/01/2021"
Mar21['LINHA'] = pd.to_datetime(Mar21['LINHA'])
Mar21.dropna(how='all')

Mar21.rename(
    columns=({'Cadastro':'DATACADASTRO'}), 
    inplace=True,)


Fev21 = pd.read_excel(r'Z:\01 PLANEJ FINANCEIRO JURIDICO\137.ANALYTICS\3 Prévias\2021\02. Fevereiro\22.02.2021 Fechamento Cível fevereiro.xlsx',sheet_name=('Fechamento Civel'),header=3)
Fev21['LINHA'] = "02/01/2021"
Fev21['LINHA'] = pd.to_datetime(Fev21['LINHA'])
Fev21.dropna(how='all')

Fev21.rename(
    columns=({'Cadastro':'DATACADASTRO', 'SOCIO: Correção (M-1)':'SOCIO: Correção (M-1)_0001', 'Novos':'NOVOS', 'Encerrados':'ENCERRADOS', 'Estoque': 'ESTOQUE', 'EMPRESA: Correção (M-1)':'EMPRESA: Correção (M-1)_0001'}), 
    inplace=True,)

Jan21 = pd.read_excel(r'Z:\01 PLANEJ FINANCEIRO JURIDICO\137.ANALYTICS\3 Prévias\2021\01. Janeiro\15.01 CIVEL - Fechamento 15.01.xlsx',sheet_name=('Fechamento Civel'),header=5)
Jan21['LINHA'] = "01/01/2021"
Jan21['LINHA'] = pd.to_datetime(Jan21['LINHA'])
Jan21.dropna(how='all')

Jan21.rename(
    columns=({'Cadastro':'DATACADASTRO', 'SOCIO: Correção (M-1)':'SOCIO: Correção (M-1)_0001', 'novos':'NOVOS', 'encerrado':'ENCERRADOS', 'Estoque': 'ESTOQUE', 'Sub tipo': 'SUB TIPO', 'EMPRESA: Correção (M-1)':'EMPRESA: Correção (M-1)_0001'}), 
    inplace=True,)

Dez20 = pd.read_excel(r'Z:\01 PLANEJ FINANCEIRO JURIDICO\137.ANALYTICS\3 Prévias\2020\Cível\12 Consolidado Dezembro 20.xlsx',sheet_name=('Fechamento'),header=3)
Dez20['LINHA'] = "12/01/2020"
Dez20['LINHA'] = pd.to_datetime(Dez20['LINHA'])
Dez20.dropna(how='all')
Dez20.reset_index(inplace=True, drop=True)

Dez20.rename(
    columns=({'Cadastro':'DATACADASTRO', 'Novos':'NOVOS', 'Encerrados':'ENCERRADOS', 'Estoque': 'ESTOQUE'}), 
    inplace=True,)

Nov20 = pd.read_excel(r'Z:\01 PLANEJ FINANCEIRO JURIDICO\137.ANALYTICS\3 Prévias\2020\Cível\11 Consolidado Novembo 20.xlsx',sheet_name=('Fechamento'),header=3)
Nov20['LINHA'] = "11/01/2020"
Nov20['LINHA'] = pd.to_datetime(Nov20['LINHA'])
Nov20.dropna(how='all')
Nov20.reset_index(inplace=True, drop=True)

Nov20.rename(
    columns=({'Cadastro':'DATACADASTRO'}), 
    inplace=True,)

Out20 = pd.read_excel(r'Z:\01 PLANEJ FINANCEIRO JURIDICO\137.ANALYTICS\3 Prévias\2020\Cível\10 Consolidado Outubro20.xlsx',sheet_name=('Fechamento'),header=3)
Out20['LINHA'] = "10/01/2020"
Out20['LINHA'] = pd.to_datetime(Out20['LINHA'])
Out20.dropna(how='all')
Out20.reset_index(inplace=True, drop=True)

Out20.rename(
    columns=({'Cadastro':'DATACADASTRO'}), 
    inplace=True,)

Set20 = pd.read_excel(r'Z:\01 PLANEJ FINANCEIRO JURIDICO\137.ANALYTICS\3 Prévias\2020\Cível\09 Consolidado Setembro20.xlsx',sheet_name=('Fechamento'),header=3)
Set20['LINHA'] = "09/01/2020"
Set20['LINHA'] = pd.to_datetime(Set20['LINHA'])
Set20.dropna(how='all')
Set20.reset_index(inplace=True, drop=True)


Set20.rename(
    columns=({'Cadastro':'DATACADASTRO', 'novo':'NOVOS' , 'encerrado':'ENCERRADOS', 'Estoque': 'ESTOQUE'}), 
    inplace=True,)

Ago20 = pd.read_excel(r'Z:\01 PLANEJ FINANCEIRO JURIDICO\137.ANALYTICS\3 Prévias\2020\Cível\08 Consolidado Agosto20.xlsx',sheet_name=('Fechamento'),header=3)
Ago20['LINHA'] = "08/01/2020"
Ago20['LINHA'] = pd.to_datetime(Ago20['LINHA'])
Ago20.dropna(how='all')

Ago20.rename(
    columns=({'Cadastro':'DATACADASTRO', 'EMPRESA: Correção (M-1)':'EMPRESA: Correção (M-1)_0001', 'novos':'NOVOS', 'estoque':'ESTOQUE', 'encerrado':'ENCERRADOS'}), 
    inplace=True,)

Jul20 = pd.read_excel(r'Z:\01 PLANEJ FINANCEIRO JURIDICO\137.ANALYTICS\3 Prévias\2020\Cível\07 Consolidado Julho20.xlsx',sheet_name=('Exportar Planilha'),header=5)
Jul20['LINHA'] = "07/01/2020"
Jul20['LINHA'] = pd.to_datetime(Jul20['LINHA'])
Jul20.dropna(how='all')
Jul20.reset_index(inplace=True, drop=True)


Jul20.rename(
    columns=({'Cadastro':'DATACADASTRO', 'EMPRESA: Correção (M-1)':'EMPRESA: Correção (M-1)_0001', 'Novos':'NOVOS', 'Encerrados':'ENCERRADOS', 'Estoque': 'ESTOQUE'}), 
    inplace=True,)

Jun20 = pd.read_excel(r'Z:\01 PLANEJ FINANCEIRO JURIDICO\137.ANALYTICS\3 Prévias\2020\Cível\06 Consolidado Junho20.xlsx',sheet_name=('Exportar Planilha'),header=6)
Jun20['LINHA'] = "06/01/2020"
Jun20['LINHA'] = pd.to_datetime(Jun20['LINHA'])
Jun20.dropna(how='all')
Jun20.reset_index(inplace=True, drop=True)


Jun20.rename(
    columns=({'Novos':'NOVOS', 'Encerrados':'ENCERRADOS', 'Estoque': 'ESTOQUE'}), 
    inplace=True,)

Mai20 = pd.read_excel(r'Z:\01 PLANEJ FINANCEIRO JURIDICO\137.ANALYTICS\3 Prévias\2020\Cível\05 Consolidado Maio20.xlsx',sheet_name=('Sheet1'),header=3)
Mai20['LINHA'] = "05/01/2020"
Mai20['LINHA'] = pd.to_datetime(Mai20['LINHA'])
Mai20.dropna(how='all')
Mai20.reset_index(inplace=True, drop=True)


Mai20.rename(
    columns=({'Cadastro':'DATACADASTRO', 'novos':'NOVOS', 'estoque':'ESTOQUE', 'encerrados':'ENCERRADOS'}), 
    inplace=True,)

Abr20 = pd.read_excel(r'Z:\01 PLANEJ FINANCEIRO JURIDICO\137.ANALYTICS\3 Prévias\2020\Cível\04 Base compilada Abril20.xlsx',sheet_name=('Sheet1'),header=3)
Abr20['LINHA'] = "04/01/2020"
Abr20['LINHA'] = pd.to_datetime(Abr20['LINHA'])
Abr20.dropna(how='all')
Abr20.reset_index(inplace=True, drop=True)

Abr20.rename(
    columns=({'Novos':'NOVOS', 'Encerrados':'ENCERRADOS', 'Estoque': 'ESTOQUE'}), 
    inplace=True,)

Mar20 = pd.read_excel(r'Z:\01 PLANEJ FINANCEIRO JURIDICO\137.ANALYTICS\3 Prévias\2020\Cível\03 Base compilada Março20.xlsx',sheet_name=('Fechamento'),header=4)
Mar20['LINHA'] = "03/01/2020"
Mar20['LINHA'] = pd.to_datetime(Mar20['LINHA'])
Mar20.dropna(how='all')
Mar20.reset_index(inplace=True, drop=True)

Mar20.rename(
    columns=({'Cadastro':'DATACADASTRO', 'novo':'NOVOS', 'encerrado': 'ENCERRADOS', 'estoque':'ESTOQUE'}), 
    inplace=True,)

Fev20 = pd.read_excel(r'Z:\01 PLANEJ FINANCEIRO JURIDICO\137.ANALYTICS\3 Prévias\2020\Cível\02 Base compilada Fevereiro20.xlsx',sheet_name=('Fevereiro'),header=0)
Fev20['LINHA'] = "02/01/2020"
Fev20['LINHA'] = pd.to_datetime(Fev20['LINHA'])
Fev20.dropna(how='all')
Fev20.reset_index(inplace=True, drop=True)


Fev20.rename(
    columns=({'Cadastro':'DATACADASTRO', 'Novos':'NOVOS', 'Encerrados':'ENCERRADOS', 'Estoque': 'ESTOQUE', 'ID': 'ID PROCESSO', 'EMPRESA':'Empresa (M)', 'Grupo': 'Grupo (M)', 'Status':'STATUS (M)'}), 
    inplace=True,)

Jan20 = pd.read_excel(r'Z:\01 PLANEJ FINANCEIRO JURIDICO\137.ANALYTICS\3 Prévias\2020\Cível\01 Base compilada Janeiro20.xlsx',sheet_name=('Janeiro '),header=0)
Jan20['LINHA'] = "01/01/2020"
Jan20['LINHA'] = pd.to_datetime(Jan20['LINHA'])
Jan20.dropna(how='all')
Jan20.reset_index(inplace=True, drop=True)

Jan20.rename(
    columns=({'Cadastro':'DATACADASTRO', 'novos':'NOVOS', 'Estoque':'ESTOQUE', 'Encerrados':'ENCERRADOS', 'ID': 'ID PROCESSO', 'Provisão Total':'Provisão Total (M)'}), 
    inplace=True,)

pdList = [Set21, Ago21, Jul21, Jun21, Mai21, Abr21, Mar21, Fev21, Jan21
          ,Dez20, Nov20, Out20, Set20, Ago20, Jul20, Jun20, Mai20, Abr20, Mar20, Fev20, Jan20]
#cria uma lista com todos os dataframes importados
new_df = pd.concat(pdList,ignore_index=True)
#new_df é a junção de todos os dataframes listados

new_df.rename(
    columns=({ 'LINHA': 'Data'}), 
    inplace=True,)
#Substitui a coluna 'LINHA' por uma coluna chamada Data

drop_columns = (['SOCIO: Correção (M-1)', 'EMPRESA: Correção (M-1)',
                 'PAGAMENTOS', 'TIPO DE PAGAMENTO', 'S/C Pagamento',
                 'incontroverso', 'UF', 'Área Funcional', 'PROVISÃO', 
                 'acrodo bom/ruim', '.', 'AREA FUNC', 'STATUS', 'PROV',
                 'PROV ATLZ', 'CC', 'Fase', 'Indicação Processo Estratégico',
                 'emregenciais', 'PagamentoValor', 'Pagamento', 'Penhoras',
                 'C/pagamento / S/pagamento', 'DUPLICADOS', 'pagamentos',
                 'Cadastro', 'Tipo', 'Linha Pasta_M-1', 'Centro de Custo SAP',
                 'Objeto', 	'Passivo', '% Êxito', 'Passivo.1', 'Atual. e Juros (M-1)',
                 'Atual. e Juros (Adição)', 'Provisão Total', 'Passivo.2',
                 'Atual. e Juros (M-1).1', 'Provisão Total.1', 'Passivo.3',
                 'Tipo Variação', 'Atual. e Juros', 'Tipo Variação.1',
                 'Provisão Total.2', 'DT DISTRIBUIÇÃO', 'Nª DO PROCESSO',
                 'ESCRITORIO', 'VALOR CAUSA', 'CC ANTERIOR', 'CHECK CC',
                 'EMPRESA', 'Grupo', 'Status', 'Prévia 18-08', 'Estratégia Prévia 18-08',
                 'Justificativa Reversão', 'Prov', 'Responsavilidade', 'Grupo (Fechamento)',
                 'Pgto', 'Tipo Pgto', 'Prv', 'PGTO ANTERIOR', 'PGTO ',
                 'Sub tipo.1', 'pgto m-1+m'])
new_df.drop(drop_columns ,axis='columns',inplace=True)

remove_cols = [col for col in new_df.columns if 'Unnamed' in col]
new_df.drop(remove_cols,axis='columns',inplace=True)
#Remover todas as colunas sem some nos dataframes

new_df.to_excel('Civ Fechamento Consolidado 2021_2020.xlsx', index=False)
#Exportar os arquivos para Excel