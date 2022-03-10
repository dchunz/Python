
import pandas as pd
#importar a biblioteca pandas para manipulação das bases

Set21 = pd.read_excel(r'Z:\01 PLANEJ FINANCEIRO JURIDICO\137.ANALYTICS\3 Prévias\2021\09. Setembro\19.09.2021 Fechamento Trabalhista - Bartira.xlsx',sheet_name=('Base Fechamento'),header=2)
#importar as bases de fechamento com seus respectivos períodos
Set21['LINHA'] = "09/01/2021"
#fazer da primeira coluna uma coluna referencial da data da base de dados
Set21['LINHA'] = pd.to_datetime(Set21['LINHA'])
#converter o valor das datas armazenadas como texto para formato data
Set21.dropna(how='all')
#excluir colunas vazias

Dez20 = pd.read_excel(r'Z:\01 PLANEJ FINANCEIRO JURIDICO\137.ANALYTICS\3 Prévias\2020\Trabalhista\12 Compilado dezembro20 trabalhista.xlsx',sheet_name=('Fechamento'),header=3)
Dez20['LINHA'] = "12/01/2020"
Dez20['LINHA'] = pd.to_datetime(Dez20['LINHA'])
Dez20.dropna(how='all')

Dez20.rename(
    columns=({'Cadastro':'DATACADASTRO', 'Novos':'NOVOS','Encerrados':'ENCERRADOS', 'Estoque':'ESTOQUE'}), 
    inplace=True,)

Nov20 = pd.read_excel(r'Z:\01 PLANEJ FINANCEIRO JURIDICO\137.ANALYTICS\3 Prévias\2020\Trabalhista\11 Compilado novembro20 trabalhista.xlsx',sheet_name=('Fechamento'),header=3)
Nov20['LINHA'] = "11/01/2020"
Nov20['LINHA'] = pd.to_datetime(Nov20['LINHA'])
Nov20.dropna(how='all')

Nov20.rename(
    columns=({'Cadastro':'DATACADASTRO', 'Novos':'NOVOS','Encerrados':'ENCERRADOS', 'Estqoue':'ESTOQUE'}), 
    inplace=True,)

Out20 = pd.read_excel(r'Z:\01 PLANEJ FINANCEIRO JURIDICO\137.ANALYTICS\3 Prévias\2020\Trabalhista\10 Compilado outubro20 trabalhista.xlsx',sheet_name=('Fechamento'),header=3)
Out20['LINHA'] = "10/01/2020"
Out20['LINHA'] = pd.to_datetime(Out20['LINHA'])
Out20.dropna(how='all')

Out20.rename(
    columns=({'Cadastro':'DATACADASTRO', 'NOVO':'NOVOS', 'ENCERRADO':'ENCERRADOS'}), 
    inplace=True,)

Set20 = pd.read_excel(r'Z:\01 PLANEJ FINANCEIRO JURIDICO\137.ANALYTICS\3 Prévias\2020\Trabalhista\09 Compilado setembro20 trabalhista.xlsx',sheet_name=('Fechamento'),header=3)
Set20['LINHA'] = "09/01/2020"
Set20['LINHA'] = pd.to_datetime(Set20['LINHA'])
Set20.dropna(how='all')

Ago20 = pd.read_excel(r'Z:\01 PLANEJ FINANCEIRO JURIDICO\137.ANALYTICS\3 Prévias\2020\Trabalhista\08 Compilado agosto20 trabalhista.xlsx',sheet_name=('Fechamento'),header=3)
Ago20['LINHA'] = "08/01/2020"
Ago20['LINHA'] = pd.to_datetime(Ago20['LINHA'])
Ago20.dropna(how='all')

Ago20.rename(
    columns=({'Cadastro':'DATACADASTRO', 'SÓCIO: Provisão Mov. (M)':'SOCIO: Provisão Mov. (M)', 'SÓCIO: Correção Mov. (M)':'SOCIO: Correção Mov. (M)', 'SÓCIO: Provisão Mov. Total (M)':'SOCIO: Provisão Mov. Total (M)', 'Novo':'NOVOS', 'Encerrado ':'ENCERRADOS', 'estoque':'ESTOQUE'}), 
    inplace=True,)

Jul20 = pd.read_excel(r'Z:\01 PLANEJ FINANCEIRO JURIDICO\137.ANALYTICS\3 Prévias\2020\Trabalhista\07 Compilado julho20 trabalhista.xlsx',sheet_name=('BASE'),header=6)
Jul20['LINHA'] = "07/01/2020"
Jul20['LINHA'] = pd.to_datetime(Jul20['LINHA'])
Jul20.dropna(how='all')

Jul20.rename(
    columns=({'Cadastro':'DATACADASTRO', 'Novos':'NOVOS','Encerrados':'ENCERRADOS', 'Estoque':'ESTOQUE'}), 
    inplace=True,)


Jun20 = pd.read_excel(r'Z:\01 PLANEJ FINANCEIRO JURIDICO\137.ANALYTICS\3 Prévias\2020\Trabalhista\06 Compilado junho20 trabalhista.xlsx',sheet_name=('Fechamento'),header=3)
Jun20['LINHA'] = "06/01/2020"
Jun20['LINHA'] = pd.to_datetime(Jun20['LINHA'])
Jun20.dropna(how='all')

Jun20.rename(
    columns=({'Novos':'NOVOS','Encerrados':'ENCERRADOS', 'Estoque':'ESTOQUE', 'EMPRESA: Correção':'EMPRESA: Correção (M)'}), 
    inplace=True,)


Mai20 = pd.read_excel(r'Z:\01 PLANEJ FINANCEIRO JURIDICO\137.ANALYTICS\3 Prévias\2020\Trabalhista\05 Compilado maio20 trabalhista.xlsx',sheet_name=('Fechamento'),header=4)
Mai20['LINHA'] = "05/01/2020"
Mai20['LINHA'] = pd.to_datetime(Mai20['LINHA'])
Mai20.dropna(how='all')

Mai20.rename(
    columns=({'Novos':'NOVOS','Encerrados':'ENCERRADOS', 'Estoque':'ESTOQUE'}), 
    inplace=True,)

Abr20 = pd.read_excel(r'Z:\01 PLANEJ FINANCEIRO JURIDICO\137.ANALYTICS\3 Prévias\2020\Trabalhista\04 Compilado abril20 trabalhista.xlsx',sheet_name=('Fechamento'),header=3)
Abr20['LINHA'] = "04/01/2020"
Abr20['LINHA'] = pd.to_datetime(Abr20['LINHA'])
Abr20.dropna(how='all')

Abr20.rename(
    columns=({'Cadastro':'DATACADASTRO', 'novo':'NOVOS', 'encerrado':'ENCERRADOS', 'Estoque':'ESTOQUE'}), 
    inplace=True,)

Mar20 = pd.read_excel(r'Z:\01 PLANEJ FINANCEIRO JURIDICO\137.ANALYTICS\3 Prévias\2020\Trabalhista\03 Compilado março20 trabalhista.xlsx',sheet_name=('Sheet1'),header=3)
Mar20['LINHA'] = "03/01/2020"
Mar20['LINHA'] = pd.to_datetime(Mar20['LINHA'])
Mar20.dropna(how='all')

Mar20.rename(
    columns=({'Cadastro':'DATACADASTRO', 'novos':'NOVOS', 'encerrados':'ENCERRADOS', 'estoque':'ESTOQUE'}), 
    inplace=True,)

Fev20 = pd.read_excel(r'Z:\01 PLANEJ FINANCEIRO JURIDICO\137.ANALYTICS\3 Prévias\2020\Trabalhista\02 Compilado fevereiro20 trabalhista.xlsx',sheet_name=('Prov'),header=2)
Fev20['LINHA'] = "02/01/2020"
Fev20['LINHA'] = pd.to_datetime(Fev20['LINHA'])
Fev20.dropna(how='all')

Fev20.rename(
    columns=({'Cadastro':'DATACADASTRO', 'novos':'NOVOS', 'Encerrados':'ENCERRADOS', 'ID': 'ID PROCESSO','Centro de Custo':'Centro de Custo (M)', 'estoques':'ESTOQUE'
}), 
    inplace=True,)

Jan20 = pd.read_excel(r'Z:\01 PLANEJ FINANCEIRO JURIDICO\137.ANALYTICS\3 Prévias\2020\Trabalhista\01 Compilado janeiro20 trabalhista.xlsx',sheet_name=('Prov'),header=2)
Jan20['LINHA'] = "01/01/2020"
Jan20['LINHA'] = pd.to_datetime(Jan20['LINHA'])
Jan20.dropna(how='all')

Jan20.rename(
    columns=({'Cadastro':'DATACADASTRO', 'Novos':'NOVOS','Encerrados':'ENCERRADOS', 'Estoque':'ESTOQUE', 'ID': 'ID PROCESSO','Centro de Custo':'Centro de Custo (M)', 'Estoques':'ESTOQUE'}), 
    inplace=True,)

Ago21 = pd.read_excel(r'Z:\01 PLANEJ FINANCEIRO JURIDICO\137.ANALYTICS\3 Prévias\2021\08. Agosto\19.08.2021 Fechamento Trabalhista - Bartira.xlsx',sheet_name=('Base Fechamento'),header=2)
Ago21['LINHA'] = "08/01/2021"
Ago21['LINHA'] = pd.to_datetime(Ago21['LINHA'])
Ago21.dropna(how='all')

Jul21 = pd.read_excel(r'Z:\01 PLANEJ FINANCEIRO JURIDICO\137.ANALYTICS\3 Prévias\2021\07. Julho\19.07.2021 Fechamento Trabalhista - Bartira.xlsx',sheet_name=('Base Fechamento'),header=2)
Jul21['LINHA'] = "07/01/2021"
Jul21['LINHA'] = pd.to_datetime(Jul21['LINHA'])
Jul21.dropna(how='all')

Jun21 = pd.read_excel(r'Z:\01 PLANEJ FINANCEIRO JURIDICO\137.ANALYTICS\3 Prévias\2021\06. Junho\18.06.2021 Fechamento Trabalhista Bartira.xlsx',sheet_name=('Base Fechamento'),header=1)
Jun21['LINHA'] = "06/01/2021"
Jun21['LINHA'] = pd.to_datetime(Jun21['LINHA'])
Jun21.dropna(how='all')

Mai21 = pd.read_excel(r'Z:\01 PLANEJ FINANCEIRO JURIDICO\137.ANALYTICS\3 Prévias\2021\05. Maio\19.05.2021 Fechamento Trabalhista - Bartira.xlsx',sheet_name=('Base Prévia'),header=1)
Mai21['LINHA'] = "05/01/2021"
Mai21['LINHA'] = pd.to_datetime(Mai21['LINHA'])
Mai21.dropna(how='all')

Abr21 = pd.read_excel(r'Z:\01 PLANEJ FINANCEIRO JURIDICO\137.ANALYTICS\3 Prévias\2021\04. Abril\19.04.2021 Fechamento Trabalhista - Bartira.xlsx',sheet_name=('Base Prévia'),header=1)
Abr21['LINHA'] = "04/01/2021"
Abr21['LINHA'] = pd.to_datetime(Abr21['LINHA'])
Abr21.dropna(how='all')

Mar21 = pd.read_excel(r'Z:\01 PLANEJ FINANCEIRO JURIDICO\137.ANALYTICS\3 Prévias\2021\03. Março\19.03.2021 Fechamento Trabalhista - Bartira.xlsx',sheet_name=('Base Prévia'),header=1)
Mar21['LINHA'] = "03/01/2021"
Mar21['LINHA'] = pd.to_datetime(Mar21['LINHA'])
Mar21.dropna(how='all')

Mar21.rename(
    columns=({'Cadastro':'DATACADASTRO'}), 
    inplace=True,)


Fev21 = pd.read_excel(r'Z:\01 PLANEJ FINANCEIRO JURIDICO\137.ANALYTICS\3 Prévias\2021\02. Fevereiro\18.02.2021 Fechamento Trabalhista fevereiro.xlsx',sheet_name=('Fechamento Trabalhista'),header=3)
Fev21['LINHA'] = "02/01/2021"
Fev21['LINHA'] = pd.to_datetime(Fev21['LINHA'])
Fev21.dropna(how='all')

Fev21.rename(
    columns=({'Cadastro':'DATACADASTRO', 'Novos':'NOVOS', 'Encerrados':'ENCERRADOS', 'Estoque': 'ESTOQUE'}), 
    inplace=True,)


Jan21 = pd.read_excel(r'Z:\01 PLANEJ FINANCEIRO JURIDICO\137.ANALYTICS\3 Prévias\2021\01. Janeiro\15.01 TRABALHISTA - Fechamento 15.01.xlsx',sheet_name=('Fechamento Trabalhista'),header=4)
Jan21['LINHA'] = "01/01/2021"
Jan21['LINHA'] = pd.to_datetime(Jan21['LINHA'])
Jan21.dropna(how='all')

Jan21.rename(
    columns=({'Cadastro':'DATACADASTRO', 'SOCIO: Correção (M-1)':'SOCIO: Correção (M-1)_0001', 'Novos':'NOVOS', 'Encerrados':'ENCERRADOS', 'Estoque': 'ESTOQUE', 'Sub Tipo': 'SUB TIPO', 'EMPRESA: Correção (M-1)':'EMPRESA: Correção (M-1)_0001'}), 
    inplace=True,)



pdList = [Set21, Ago21, Jul21, Jun21, Mai21, Abr21, Mar21, Fev21, Jan21, Dez20, Nov20, Out20, Ago20, Jul20, Jun20, Mai20, Abr20, Mar20, Fev20, Jan20]
new_df = pd.concat(pdList,ignore_index=True)
#new_df é a junção de todos os dataframes listados


new_df.rename(
    columns=({ 'LINHA': 'Data'}), 
    inplace=True,)
#Substitui a coluna 'LINHA' por uma coluna chamada Data

drop_columns = (['SOCIO: Correção (M-1)', 'EMPRESA: Correção (M-1)',
                 '<>2020 NOVO RNO ATUALIZAÇÂO', 'Demitido por Reestruturação RH',
                 'PAGAMENTOS', 'C/ S/ PGTO', 'TIPO', 'UF', 'Área Funcional',
                 'fase', 'Provisão', 'Atualização', 'VALOR', 'PARCELADO',
                 'INCONTROVERSO', 'PENHORA', 'VALOR PAGO', 'x', 'OUTROS INCONTROVERSOS',
                 'm-1', 'Media de Pagamento', 'sovente', 'solvente 2', 'CLASSIFICAÇÃO',
                 'SOCIO: Correção +correção', 'Pasta Benner', 'Linha Pasta_M-1',
                 'Baixa SÓ Contábil (Não=1,Sim=0)', 'Tipo', 'Réu', 'Cargo Elaw',
                 '# Cargo Provisão', 'Cargo Provisão', '# Passivo', 'Passivo',
                 '% Êxito', '% Sócio', '% VVAR', 'Passivo.1', 'Atual. e Juros M-1',
                 'Atual. e Juros (Adição)', 'Provisão Total', 'Passivo.2', 'Atual. e Juros',
                 'Provisão Total.1', 'Passivo.3', 'Tipo variação', 'Atual. e Juros.1',
                 'Tipo variação.1', 'Provisão Total.2', 'Passivo.4', 'Atual. e Juros M-1.1',
                 'Atual. e Juros (Adição).1', 'Provisão Total.3', 'Passivo.5', 'Atual. e Juros.2',
                 'Provisão Total.4', 'Passivo.6', 'Tipo variação.2', 'Tipo variação.3',
                 'Provisão Total.5', 'Passivo.7', 'Atual. e Juros M-1.2', 'Atual. e Juros (Adição).2',
                 'Provisão Total.6', 'Passivo.8', 'Atual. e Juros.3', 'Provisão Total.7', 'Passivo1',
                 'Tipo variação.4', 'Atualização.1', 'Tipo variação.5', 'Provisão Total.8', 'Filial (M)',
                 'reclassificação socio', 'Grupo (Fechamento)','Ano Cadastro','Prov?','Valor Pagamento',
                 'Tipo Pagamento', 'Parcelado','Prov', 'Valor Pagamento Hist.',	'Pagamento Hist.',
                 'PGTO MÊS ANTERIOR', 'PGTO', '% Com custo', '% CNOVA'])
new_df.drop(drop_columns ,axis='columns',inplace=True)

remove_cols = [col for col in new_df.columns if 'Unnamed' in col]
new_df.drop(remove_cols,axis='columns',inplace=True)
#Remover todas as colunas sem some nos dataframes


new_df.to_excel('Trab Fechamento Consolidado 21_20.xlsx', index=False)
#Exportar os arquivos para Excel