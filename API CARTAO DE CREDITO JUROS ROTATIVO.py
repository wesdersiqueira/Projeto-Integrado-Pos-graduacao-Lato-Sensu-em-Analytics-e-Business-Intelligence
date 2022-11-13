# --------------------------------------------------------------------------------
# Tabelas das taxas de cartao de credito das instituicoes financeiras  
# --------------------------------------------------------------------------------


# quero saber qual as taxas praticadas pelas instituicoes historicamente
# para isso usarei 10 instituicoes como exemplo

# Importando as Bibliotecas que serao usadas durante o Script ----------------

#importando biblioteca para manipulacao de arquivos em json
import json, requests
#importando biblioteca de manipulacao de tabelas
import pandas as pd



# Conectando com as Fontes de Dados ------------------------------------------


# Etapa 1: extrair a lista de APIs do Banco Central do Brasil -----------------

#conecta com a API do Banco Central do Brasil filtrando
recurso_api_bcb = requests.get(
    # "https://olinda.bcb.gov.br/olinda/servico/DASFN/versao/v1/odata/"
    # #filtra Api relacionada a taxas de cartao de credito e recursos relacionados a todos os itens da lista
    # "Recursos?$filter=Api%20eq%20'taxas_cartoes'%20and%20Recurso%20eq%20'%2Fitens'"
    # #determina que o arquivo será em json
    # "&$format=json"
    # #seleciona os intens relacionados ao nome da instituicao e a URL da API
    # "&$select=NomeInstituicao,URLDados")

"https://olinda.bcb.gov.br/olinda/servico/taxaJuros/versao/v2/odata/"
"TaxasJurosDiariaPorInicioPeriodo?$filter=Segmento%20eq%20%27PESSOA%20F%C3%8DSICA%27%20and%20Modalidade%20eq%20%27CART%C3%83O%20DE%20CR%C3%89DITO%20-%20ROTATIVO%20TOTAL%20-%20PR%C3%89-FIXADO%27"
"&$format=json")


#carrega os dados em json
json_bcb = json.loads(recurso_api_bcb.text)

#faz um drill down para a lista value (onde os dados encontram-se)
json_bcb_drill = json_bcb['value']

#transforma em DataFrame a lista extraída da API do Banco Central do Brasil
df_bcb = pd.DataFrame(json_bcb_drill)

#cria os filtros que serao usados para extrair as bases
fil_1  = df_bcb['InstituicaoFinanceira'] == 'CAIXA ECONOMICA FEDERAL'
fil_2  = df_bcb['InstituicaoFinanceira'] == 'BCO ITAUCARD S.A.'
fil_3  = df_bcb['InstituicaoFinanceira'] == 'BCO BRADESCO S.A.'
fil_4  = df_bcb['InstituicaoFinanceira'] == 'BCO DO BRASIL S.A.'
fil_5  = df_bcb['InstituicaoFinanceira'] == 'BCO CREFISA S.A.'
fil_6  = df_bcb['InstituicaoFinanceira'] == 'NU FINANCEIRA S.A. CFI'
fil_7  = df_bcb['InstituicaoFinanceira'] == 'BCO C6 S.A.'
fil_8  = df_bcb['InstituicaoFinanceira'] == 'BCO SAFRA S.A.'
fil_9  = df_bcb['InstituicaoFinanceira'] == 'BANCO ORIGINAL'
fil_10 = df_bcb['InstituicaoFinanceira'] == 'BANCO PAN'

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


#une tudo em um unico DataFrame
df_taxas_cartao = pd.concat([
     df_1
    ,df_2
    ,df_3
    ,df_4
    ,df_5
    ,df_6
    ,df_7
    ,df_8
    ,df_9
    ,df_10
    ])