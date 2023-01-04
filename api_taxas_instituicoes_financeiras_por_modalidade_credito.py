# -----------------------------------------------------------------------------
# Tabelas das taxas cobradas pelas instituicoes financeiras
# -----------------------------------------------------------------------------


# quero saber qual as taxas praticadas pelas instituicoes historicamente
# para isso usarei 10 instituicoes como exemplo

# Importando as Bibliotecas que serao usadas durante o Script ----------------

#importando biblioteca para manipulacao de arquivos em json
import json, requests
#importando biblioteca de manipulacao de tabelas
import pandas as pd
#importando biblioteca para calculos e funcoes
import numpy as np


# Conectando com as Fontes de Dados ------------------------------------------


# sera necessario extrair a API do Banco Central do Brasil

#conecta com a API do Banco Central do Brasil filtrando
recurso_api_bcb = requests.get(
    "https://olinda.bcb.gov.br/olinda/servico/taxaJuros/versao/v2/odata/"
    #filtra as instituicoes que serao usadas nas bases
    "TaxasJurosDiariaPorInicioPeriodo?$filter="
    "InstituicaoFinanceira%20eq%20'CAIXA%20ECONOMICA%20FEDERAL'"               # 'CAIXA ECONOMICA FEDERAL'
    "%20or%20InstituicaoFinanceira%20eq%20'BCO%20ITAUCARD%20S.A.'"             # 'BCO ITAUCARD S.A.'
    "%20or%20InstituicaoFinanceira%20eq%20'BCO%20BRADESCO%20S.A.'"             # 'BCO BRADESCO S.A.'
    "%20or%20InstituicaoFinanceira%20eq%20'BCO%20DO%20BRASIL%20S.A.'"          # 'BCO DO BRASIL S.A.'
    "%20or%20InstituicaoFinanceira%20eq%20'BCO%20CREFISA%20S.A.'"              # 'BCO CREFISA S.A.'
    "%20or%20InstituicaoFinanceira%20eq%20'NU%20FINANCEIRA%20S.A.%20CFI'"      # 'NU FINANCEIRA S.A. CFI'
    "%20or%20InstituicaoFinanceira%20eq%20'BCO%20C6%20S.A.'"                   # 'BCO C6 S.A.'
    "%20or%20InstituicaoFinanceira%20eq%20'BCO%20SAFRA%20S.A.'"                # 'BCO SAFRA S.A.'
    "%20or%20InstituicaoFinanceira%20eq%20'BANCO%20ORIGINAL'"                  # 'BANCO ORIGINAL'
    "%20or%20InstituicaoFinanceira%20eq%20'BANCO%20PAN'"                       # 'BANCO PAN'
    #determina que o arquivo será em json
    "&$format=json"
    #seleciona os intens relacionados ao nome da instituicao e a URL da API
    "&$select=InicioPeriodo,Segmento,Modalidade,cnpj8,InstituicaoFinanceira,TaxaJurosAoMes,TaxaJurosAoAno")


#carrega os dados em json
json_bcb = json.loads(recurso_api_bcb.text)

#faz um drill down para a lista value (onde os dados encontram-se)
json_bcb_drill = json_bcb['value']

#transforma em DataFrame a lista extraída da API do Banco Central do Brasil
df_bcb = pd.DataFrame(json_bcb_drill)

#cria os filtros que serao usados para extrair as bases
filtro  = df_bcb['Segmento'] == 'PESSOA FÍSICA'


#gera os DataFrames com base nos filtros criados
df_bcb  = df_bcb.where(     filtro       ).dropna(how='all')


#deleta as df e lst que nao serao usadas novamente
del recurso_api_bcb, json_bcb, json_bcb_drill, filtro

# Converter e ajustar os campos da tabela de taxas ---------------------------

# para melhor aproveitamento da base sera necessario converter alguns campos

#converte o campo 'InicioPeriodo' para datetime
df_bcb['InicioPeriodo'] = pd.to_datetime(df_bcb['InicioPeriodo'])

#converte as taxas de juros anuais e mensais para string
df_bcb['TaxaJurosAoMes'] = df_bcb['TaxaJurosAoMes'].astype(str)
df_bcb['TaxaJurosAoAno'] = df_bcb['TaxaJurosAoAno'].astype(str)

#substitui pontos por virgulas para serem adaptados
df_bcb['TaxaJurosAoMes'] = df_bcb['TaxaJurosAoMes'].str.replace('.', ',')
df_bcb['TaxaJurosAoAno'] = df_bcb['TaxaJurosAoAno'].str.replace('.', ',')



# ----------------------------------------------------------------------------


# Criar as tabelas Dimensao relacionadas aos dados extraídos



# Prepara a dimensao de calendario ------------------------------------------------

#agrupa a 'df_bcb' pela data e armazena num intervalo 'lst_time'
lst_time = pd.date_range(start = str(min(df_bcb['InicioPeriodo'].astype(str).str[0:10].str[0:4]))+'-01-01', 
       end = str(pd.Timestamp.today(tz=None))[0:10])

#cria a dimensao 'dim_time' com base no intervalo criado
stg_time = pd.DataFrame(lst_time, columns=['DataReferencia'])

#cria a coluna Mes na dimensao
stg_time['Mes'] = stg_time['DataReferencia'].astype(str).str[0:10].str[-5:].str[0:2]

#cria a coluna Ano na dimensao
stg_time['Ano'] = stg_time['DataReferencia'].astype(str).str[0:10].str[0:4]

#cria a coluna Dia na dimensao
stg_time['Dia'] = stg_time['DataReferencia'].astype(str).str[0:10].str[-5:].str[-2:]

#transforma a data como index
stg_time.set_index(stg_time ['DataReferencia'], inplace= True)

dim_calendario = stg_time

#deleta a lst e stg que nao sera usada novamente
del lst_time, stg_time

# Prepara a dimensao de modalidade -------------------------------------------

#agrupa a 'df_bcb' pela modalidade e armazena na variavel 'dim_modalidade'
dim_modalidade = df_bcb.groupby(['Modalidade'])

#transforma o agrupamento em uma df nova
dim_modalidade = pd.DataFrame(dim_modalidade, columns=['Modalidade','Others'])

#remove outros campos que nao serao usados na dimensao
dim_modalidade = dim_modalidade.drop(['Others'],axis=1)

# para criar um agrupamento de classificacao sera criado condicoes e resultados esperados

#cria as condicoes para a classificacao das modalidades
condicoes_modalidade = [
     dim_modalidade['Modalidade'] == 'AQUISIÇÃO DE OUTROS BENS - PRÉ-FIXADO'
    ,dim_modalidade['Modalidade'] == 'AQUISIÇÃO DE VEÍCULOS - PRÉ-FIXADO'
    ,dim_modalidade['Modalidade'] == 'ARRENDAMENTO MERCANTIL DE VEÍCULOS - PRÉ-FIXADO'
    ,dim_modalidade['Modalidade'] == 'CARTÃO DE CRÉDITO - PARCELADO - PRÉ-FIXADO'
    ,dim_modalidade['Modalidade'] == 'CARTÃO DE CRÉDITO - ROTATIVO TOTAL - PRÉ-FIXADO'
    ,dim_modalidade['Modalidade'] == 'CHEQUE ESPECIAL - PRÉ-FIXADO'
    ,dim_modalidade['Modalidade'] == 'CRÉDITO PESSOAL CONSIGNADO INSS - PRÉ-FIXADO'
    ,dim_modalidade['Modalidade'] == 'CRÉDITO PESSOAL CONSIGNADO PRIVADO - PRÉ-FIXADO'
    ,dim_modalidade['Modalidade'] == 'CRÉDITO PESSOAL CONSIGNADO PÚBLICO - PRÉ-FIXADO'
    ,dim_modalidade['Modalidade'] == 'CRÉDITO PESSOAL NÃO-CONSIGNADO - PRÉ-FIXADO'
    ,dim_modalidade['Modalidade'] == 'DESCONTO DE CHEQUES - PRÉ-FIXADO'
    ]

#cria os resultados para a classificacao das modalidades
resultados_modalidade = [
    'AQUISIÇÕES'
    ,'AQUISIÇÕES'
    ,'ARRENDAMENTO'
    ,'CARTÃO DE CRÉDITO'
    ,'CARTÃO DE CRÉDITO'
    ,'CHEQUE ESPECIAL'
    ,'CRÉDITO PESSOAL'
    ,'CRÉDITO PESSOAL'
    ,'CRÉDITO PESSOAL'
    ,'CRÉDITO PESSOAL'
    ,'CHEQUES'
    ]

#cria a coluna de classificacao com as condicoes e resultados esperados
dim_modalidade['Classificacao'] = np.select(condicoes_modalidade, resultados_modalidade)

#cria a coluna de tipo de modalidades com as condicoes e resultados esperados
dim_modalidade['TipoModalidade'] = dim_modalidade['Modalidade'].str[-11:]

#remove o sufixo de pre-fixado
dim_modalidade['Modalidade'] = dim_modalidade['Modalidade'].str.replace(' - PRÉ-FIXADO', '')

#transforma a modalidade como index
dim_modalidade.set_index(dim_modalidade ['Modalidade'], inplace= True)

#deleta as lst que nao serao usadas novamente
del condicoes_modalidade, resultados_modalidade


# Prepara a dimensao de instituicoes -----------------------------------------

#separa as colunas relacionadas ao cnpj e nome das instituicoes
dim_instituicoes = df_bcb[['InstituicaoFinanceira','cnpj8']]

dim_instituicoes = dim_instituicoes.drop_duplicates(subset=['InstituicaoFinanceira'])

#transforma a 'InstituicaoFinanceira' como index
dim_instituicoes.set_index(dim_instituicoes ['InstituicaoFinanceira'], inplace= True)


#renomeia a coluna de CNPJ
dim_instituicoes = dim_instituicoes.rename(columns={'cnpj8': 'CNPJ'})

# ----------------------------------------------------------------------------

# Criar as tabelas Fato relacionadas aos dados extraídos

#armazena os dados da df_bcb em uma tabela fato
fato_juros = df_bcb

#renomeia a coluna de CNPJ 
fato_juros = fato_juros.rename(columns={'cnpj8': 'CNPJ'})

#renomeia a coluna de data 
fato_juros = fato_juros.rename(columns={'InicioPeriodo': 'DataReferencia'})

#remove o sufixo de pre-fixado
fato_juros['Modalidade'] = fato_juros['Modalidade'].str.replace(' - PRÉ-FIXADO', '')

#deleta a df que nao sera usada novamente
del df_bcb

# Salvando na unidade --------------------------------------------------------

#armazena a variavel fato_juros em um arquivo xlsx no local D:
with pd.ExcelWriter('D:/TCC/Arquivos_xlsx/fato_juros.xlsx', engine='xlsxwriter') as writer:
    fato_juros.to_excel(writer, sheet_name='fato_juros', index = False)
    
# Fecha o pip e gera o arquivo .xlsx
writer.save()

#armazena a variavel dim_instituicoes em um arquivo xlsx no local D:
with pd.ExcelWriter('D:/TCC/Arquivos_xlsx/dim_instituicoes.xlsx', engine='xlsxwriter') as writer:
    dim_instituicoes.to_excel(writer, sheet_name='dim_instituicoes', index = False)
    
# Fecha o pip e gera o arquivo .xlsx
writer.save()

#armazena a variavel dim_modalidade em um arquivo xlsx no local D:
with pd.ExcelWriter('D:/TCC/Arquivos_xlsx/dim_modalidade.xlsx', engine='xlsxwriter') as writer:
    dim_modalidade.to_excel(writer, sheet_name='dim_modalidade', index = False)
    
# Fecha o pip e gera o arquivo .xlsx
writer.save()

#armazena a variavel dim_calendario em um arquivo xlsx no local D:
with pd.ExcelWriter('D:/TCC/Arquivos_xlsx/dim_calendario.xlsx', engine='xlsxwriter') as writer:
    dim_calendario.to_excel(writer, sheet_name='dim_calendario', index = False)
    
# Fecha o pip e gera o arquivo .xlsx
writer.save()