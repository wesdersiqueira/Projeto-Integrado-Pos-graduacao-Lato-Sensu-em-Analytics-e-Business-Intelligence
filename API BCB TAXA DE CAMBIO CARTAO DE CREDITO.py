# --------------------------------------------------------------------------------
# Tabelas das taxas de cartao de credito das instituicoes financeiras  
# --------------------------------------------------------------------------------


# quero saber qual as taxas praticadas pelas instituicoes historicamente
# para isso usarei 10 instituicoes como exemplo

# Importando as Bibliotecas que serao usadas durante o Script ----------------

#importando biblioteca para manipulacao de arquivos em json
import json, requests
#importando biblioteca para leitura de url
import urllib
#importando biblioteca de manipulacao de tabelas
import pandas as pd
#importando biblioteca para calculos e funcoes
import numpy as np



# Conectando com as Fontes de Dados ------------------------------------------


# Etapa 1: extrair a lista de APIs do Banco Central do Brasil -----------------

#conecta com a API do Banco Central do Brasil filtrando
recurso_api_bcb = requests.get(
    "https://olinda.bcb.gov.br/olinda/servico/DASFN/versao/v1/odata/"
    #filtra Api relacionada a taxas de cartao de credito e recursos relacionados a todos os itens da lista
    "Recursos?$filter=Api%20eq%20'taxas_cartoes'%20and%20Recurso%20eq%20'%2Fitens'"
    #determina que o arquivo será em json
    "&$format=json"
    #seleciona os intens relacionados ao nome da instituicao e a URL da API
    "&$select=NomeInstituicao,URLDados")

#carrega os dados em json
json_bcb = json.loads(recurso_api_bcb.text)

#faz um drill down para a lista value (onde os dados encontram-se)
json_bcb_drill = json_bcb['value']

#transforma em DataFrame a lista extraída da API do Banco Central do Brasil
df_bcb = pd.DataFrame(json_bcb_drill, columns=['NomeInstituicao', 'URLDados'])


# Etapa 2: extrair as APIs de 10 Intituicoes Financeiras ----------------------

#cria os filtros que serao usados para extrair as bases
fil_1  = df_bcb['NomeInstituicao'] == 'CAIXA ECON. FEDERAL'
fil_2  = df_bcb['NomeInstituicao'] == 'ITAU UNIBANCO S.A.'
fil_3  = df_bcb['NomeInstituicao'] == 'BCO BRADESCO S.A.'
fil_4  = df_bcb['NomeInstituicao'] == 'BCO DO BRASIL S.A.'
fil_5  = df_bcb['NomeInstituicao'] == 'BCO CREFISA S.A.'
fil_6  = df_bcb['NomeInstituicao'] == 'NU FINANCEIRA S.A. CFI'
fil_7  = df_bcb['NomeInstituicao'] == 'BANCO C6 S.A.'
fil_8  = df_bcb['NomeInstituicao'] == 'BCO SAFRA S.A.'
fil_9  = df_bcb['NomeInstituicao'] == 'BANCO ORIGINAL'
fil_10 = df_bcb['NomeInstituicao'] == 'BANCO PAN S.A'

#gera os DataFrames com base nos filtros criados
df_1  = df_bcb.where(     fil_1       ).dropna(how='all')
df_2  = df_bcb.where(     fil_2       ).dropna(how='all')
df_3  = df_bcb.where(     fil_3       ).dropna(how='all')
df_4  = df_bcb.where(     fil_4       ).dropna(how='all')
df_5  = df_bcb.where(     fil_5       ).dropna(how='all')
df_6  = df_bcb.where(     fil_6       ).dropna(how='all')
df_7  = df_bcb.where(     fil_7       ).dropna(how='all')
df_8  = df_bcb.where(     fil_8       ).dropna(how='all')
df_9  = df_bcb.where(     fil_9       ).dropna(how='all')
df_10 = df_bcb.where(     fil_10      ).dropna(how='all')

#transforma o campo 'NomeInstituicao' como index dos DataFrames
df_1.set_index(df_1 ['NomeInstituicao'], inplace= True)
df_2.set_index(df_2 ['NomeInstituicao'], inplace= True)
df_3.set_index(df_3 ['NomeInstituicao'], inplace= True)
df_4.set_index(df_4 ['NomeInstituicao'], inplace= True)
df_5.set_index(df_5 ['NomeInstituicao'], inplace= True)
df_6.set_index(df_6 ['NomeInstituicao'], inplace= True)
df_7.set_index(df_7 ['NomeInstituicao'], inplace= True)
df_8.set_index(df_8 ['NomeInstituicao'], inplace= True)
df_9.set_index(df_9 ['NomeInstituicao'], inplace= True)
df_10.set_index(df_10['NomeInstituicao'], inplace= True)

#aciona o campo com a URL da API de cada df destacada
req_1  = requests.get(df_1 ['URLDados'][0])
req_2  = requests.get(df_2 ['URLDados'][0])
# req_3  = requests.get(df_3 ['URLDados'][0])                                   # os dados sao do tipo byte e eh necessario decodificar para string a API da instituicao sera acionada diretamente como json
# req_4  = requests.get(df_4 ['URLDados'][0])                                   # os dados sao do tipo byte e eh necessario decodificar para string a API da instituicao sera acionada diretamente como json
req_5  = requests.get(df_5 ['URLDados'][0])
req_6  = requests.get(df_6 ['URLDados'][0])
req_7  = requests.get(df_7 ['URLDados'][0])
req_8  = requests.get(df_8 ['URLDados'][0])
req_9  = requests.get(df_9 ['URLDados'][0])
req_10 = requests.get(df_10['URLDados'][0])

#usa a biblioteca urllib para acionar a URL dos dados para o df_3 e df_4
url_3 = urllib.request.urlopen(str(df_3 ['URLDados'][0]))
url_4 = urllib.request.urlopen(str(df_4 ['URLDados'][0]))
#le a URL dos dados
df_url_3 = url_3.read()
df_url_4 = url_4.read()

#carrega os dados em json dos df restantes
json_1  = json.loads(req_1.text)
json_2  = json.loads(req_2.text)
json_5  = json.loads(req_5.text)
json_6  = json.loads(req_6.text)
json_7  = json.loads(req_7.text)
json_8  = json.loads(req_8.text)
json_9  = json.loads(req_9.text)
json_10 = json.loads(req_10.text)

#aciona os arquivos json referente ao df_3 e df_4 diretamente pela URL
#usa o decode para garantir a codificacao de caracteres comum
json_3  = json.loads(df_url_3.decode("utf-8"))                                 
json_4  = json.loads(df_url_4.decode("utf-8"))                                       

# Etapa 3: transformar os json em DataFrame e unir todos em um único df -------

#faz um drill down para a lista 'historicoTaxas' (onde os dados encontram-se)
json_1_drill  = json_1['historicoTaxas']
json_2_drill  = json_2[0]['itens'][0]['historicoTaxas']                         # foi necessario fazer mais de um drill down para localizar os dados
json_3_drill  = json_3['historicoTaxas']
json_4_drill  = json_4['historicoTaxas']
json_5_drill  = json_5['historicoTaxas']
json_6_drill  = json_6['historicoTaxas']
json_7_drill  = json_7['historicoTaxas']
json_8_drill  = json_8['historicoTaxas']
json_9_drill  = json_9['historicoTaxas']
json_10_drill = json_10['historicoTaxas']

#transforma em DataFrame
df_1_drill  = pd.DataFrame(json_1_drill)
df_2_drill  = pd.DataFrame(json_2_drill)
df_3_drill  = pd.DataFrame(json_3_drill)
df_4_drill  = pd.DataFrame(json_4_drill)
df_5_drill  = pd.DataFrame(json_5_drill)
df_6_drill  = pd.DataFrame(json_6_drill)
df_7_drill  = pd.DataFrame(json_7_drill)
df_8_drill  = pd.DataFrame(json_8_drill)
df_9_drill  = pd.DataFrame(json_9_drill)
df_10_drill = pd.DataFrame(json_10_drill)

#insere um campo com o nome da Intituicao Financeira de origem dos dados
df_1_drill ['Instituicao_Financeira'] = json_1 ['emissorNome']
df_2_drill ['Instituicao_Financeira'] = json_2 [0]['itens'][0]['emissor']['emissorNome'] # foi necessario fazer mais de um drill down para localizar os dados
df_3_drill ['Instituicao_Financeira'] = json_3 ['emissorNome']
df_4_drill ['Instituicao_Financeira'] = json_4 ['emissorNome']
df_5_drill ['Instituicao_Financeira'] = json_5 ['emissorNome']
df_6_drill ['Instituicao_Financeira'] = json_6 ['emissorNome']
df_7_drill ['Instituicao_Financeira'] = json_7 ['emissorNome']
df_8_drill ['Instituicao_Financeira'] = json_8 ['emissorNome']
df_9_drill ['Instituicao_Financeira'] = json_9 ['emissorNome']
df_10_drill['Instituicao_Financeira'] = json_10['emissorNome']

#une tudo em um unico DataFrame
df_taxas_cartao = pd.concat([
     df_1_drill
    ,df_2_drill
    ,df_3_drill
    ,df_4_drill
    ,df_5_drill
    ,df_6_drill
    ,df_7_drill
    ,df_8_drill
    ,df_9_drill
    ,df_10_drill
    ])

# Etapa 4: Converter e ajustar os campos --------------------------------------

df_taxas_cartao['taxaData'] = pd.to_datetime(df_taxas_cartao['taxaData'])

