# Importando as Bibliotecas que serao usadas durante o Script ----------------

#importando biblioteca de manipulacao de tabelas
import pandas as pd


# -----------------------------------------------------------------------------
# Tabela de credito pessoal nao consignado para Pessoas Físicas
# -----------------------------------------------------------------------------


# inandimplencia das pessoas fisicas com relacao ao credito pessoal nao consignado


# Conectando com as Fontes de Dados ------------------------------------------

# sera necessario extrair a API do Banco Central do Brasil

#conecta com a API do Banco Central do Brasil extraindo o arquivo em json e lendo com Pandas
df_pessoal_nao_consignado = pd.read_json("https://api.bcb.gov.br/dados/serie/bcdata.sgs.21114/dados?formato=json")

df_pessoal_nao_consignado['Modalidade'] = 'CRÉDITO PESSOAL NÃO-CONSIGNADO'


# -----------------------------------------------------------------------------
# Tabela de credito pessoal consignado INSS para Pessoas Físicas
# -----------------------------------------------------------------------------


# inandimplencia das pessoas fisicas com relacao ao credito pessoal consignado INSS


# Conectando com as Fontes de Dados ------------------------------------------

# sera necessario extrair a API do Banco Central do Brasil

#conecta com a API do Banco Central do Brasil extraindo o arquivo em json e lendo com Pandas
df_pessoal_inss = pd.read_json("https://api.bcb.gov.br/dados/serie/bcdata.sgs.21118/dados?formato=json")

df_pessoal_inss['Modalidade'] = 'CRÉDITO PESSOAL CONSIGNADO INSS'

# -----------------------------------------------------------------------------
# Tabela de credito pessoal consignado para trabalhadores do setor privado
# -----------------------------------------------------------------------------


# inandimplencia dos trabalhadores do setor privado com relacao ao credito pessoal consignado


# Conectando com as Fontes de Dados ------------------------------------------

# sera necessario extrair a API do Banco Central do Brasil

#conecta com a API do Banco Central do Brasil extraindo o arquivo em json e lendo com Pandas
df_pessoal_privado = pd.read_json("https://api.bcb.gov.br/dados/serie/bcdata.sgs.21116/dados?formato=json")

df_pessoal_privado['Modalidade'] = 'CRÉDITO PESSOAL CONSIGNADO PRIVADO'


# -----------------------------------------------------------------------------
# Tabela de credito pessoal consignado para trabalhadores do setor publico
# -----------------------------------------------------------------------------


# inandimplencia dos trabalhadores do setor publico com relacao ao credito pessoal consignado


# Conectando com as Fontes de Dados ------------------------------------------

# sera necessario extrair a API do Banco Central do Brasil

#conecta com a API do Banco Central do Brasil extraindo o arquivo em json e lendo com Pandas
df_pessoal_publico = pd.read_json("https://api.bcb.gov.br/dados/serie/bcdata.sgs.21117/dados?formato=json")

df_pessoal_publico['Modalidade'] = 'CRÉDITO PESSOAL CONSIGNADO PÚBLICO'


# -----------------------------------------------------------------------------
# Tabela de cartao de credito total incluindo parcelado
# -----------------------------------------------------------------------------


# inandimplencia das Pessoas Fisicas com cartao de credito total incluindo parcelado


# Conectando com as Fontes de Dados ------------------------------------------

# sera necessario extrair a API do Banco Central do Brasil

#conecta com a API do Banco Central do Brasil extraindo o arquivo em json e lendo com Pandas
df_cartao_total = pd.read_json("https://api.bcb.gov.br/dados/serie/bcdata.sgs.21129/dados?formato=json")

df_cartao_total['Modalidade'] = 'CARTÃO DE CRÉDITO - PARCELADO'



# -----------------------------------------------------------------------------
# Tabela de cartao de credito rotativo
# -----------------------------------------------------------------------------


# inandimplencia das Pessoas Fisicas com cartao de credito rotativo


# Conectando com as Fontes de Dados ------------------------------------------

# sera necessario extrair a API do Banco Central do Brasil

#conecta com a API do Banco Central do Brasil extraindo o arquivo em json e lendo com Pandas
df_cartao_rotativo = pd.read_json("https://api.bcb.gov.br/dados/serie/bcdata.sgs.21127/dados?formato=json")

df_cartao_rotativo['Modalidade'] = 'CARTÃO DE CRÉDITO - ROTATIVO TOTAL'


# -----------------------------------------------------------------------------
# Tabela de cheque especial
# -----------------------------------------------------------------------------


# inandimplencia das Pessoas Fisicas com cheque especial


# Conectando com as Fontes de Dados ------------------------------------------

# sera necessario extrair a API do Banco Central do Brasil

#conecta com a API do Banco Central do Brasil extraindo o arquivo em json e lendo com Pandas
df_cheque_especial = pd.read_json("https://api.bcb.gov.br/dados/serie/bcdata.sgs.21113/dados?formato=json")

df_cheque_especial['Modalidade'] = 'CHEQUE ESPECIAL'



# -----------------------------------------------------------------------------
# Tabela de desconto de cheques
# -----------------------------------------------------------------------------


# inandimplencia das Pessoas Fisicas com desconto de cheques


# Conectando com as Fontes de Dados ------------------------------------------

# sera necessario extrair a API do Banco Central do Brasil

#conecta com a API do Banco Central do Brasil extraindo o arquivo em json e lendo com Pandas
df_desconto_cheques = pd.read_json("https://api.bcb.gov.br/dados/serie/bcdata.sgs.21130/dados?formato=json")

df_desconto_cheques['Modalidade'] = 'DESCONTO DE CHEQUES'



# -----------------------------------------------------------------------------
# Tabela de arrendamento mercantil
# -----------------------------------------------------------------------------


# inandimplencia das Pessoas Fisicas com arrendamento mercantil


# Conectando com as Fontes de Dados ------------------------------------------

# sera necessario extrair a API do Banco Central do Brasil

#conecta com a API do Banco Central do Brasil extraindo o arquivo em json e lendo com Pandas
df_arrendamento_mercantil = pd.read_json("https://api.bcb.gov.br/dados/serie/bcdata.sgs.21124/dados?formato=json")

df_arrendamento_mercantil['Modalidade'] = 'ARRENDAMENTO MERCANTIL DE VEÍCULOS'


# -----------------------------------------------------------------------------
# Tabela de aquisicoes de veiculos
# -----------------------------------------------------------------------------


# inandimplencia das Pessoas Fisicas com aquisicoes de veiculos


# Conectando com as Fontes de Dados ------------------------------------------

# sera necessario extrair a API do Banco Central do Brasil

#conecta com a API do Banco Central do Brasil extraindo o arquivo em json e lendo com Pandas
df_aquisicoes_veiculos = pd.read_json("https://api.bcb.gov.br/dados/serie/bcdata.sgs.21121/dados?formato=json")

df_aquisicoes_veiculos['Modalidade'] = 'AQUISIÇÃO DE VEÍCULOS'


# -----------------------------------------------------------------------------
# Tabela de aquisicoes de outros bens
# -----------------------------------------------------------------------------


# inandimplencia das Pessoas Fisicas com aquisicoes de outros bens


# Conectando com as Fontes de Dados ------------------------------------------

# sera necessario extrair a API do Banco Central do Brasil

#conecta com a API do Banco Central do Brasil extraindo o arquivo em json e lendo com Pandas
df_aquisicoes_outros_bens = pd.read_json("https://api.bcb.gov.br/dados/serie/bcdata.sgs.21122/dados?formato=json")

df_aquisicoes_outros_bens['Modalidade'] = 'AQUISIÇÃO DE OUTROS BENS'


# Criar as tabelas Fato relacionadas aos dados extraídos

# Prepara a fato endividamento familiar --------------------------------------

#separa a tabela fato com o historico de endividamento familiar
df_inadimplencia = pd.concat([df_pessoal_nao_consignado
                               ,df_pessoal_inss
                               ,df_pessoal_privado
                               ,df_aquisicoes_outros_bens
                               ,df_aquisicoes_veiculos
                               ,df_arrendamento_mercantil
                               ,df_cartao_rotativo
                               ,df_cartao_total
                               ,df_cheque_especial
                               ,df_desconto_cheques
                               ,df_pessoal_publico]) 


# preparando as variasveis de data
mes = df_inadimplencia['data'].str[3:5]
dia = df_inadimplencia['data'].str[0:2]
ano = df_inadimplencia['data'].str[-4:]

#ajustando as datas
df_inadimplencia['data'] = mes+'/'+dia+'/'+ano

#transforma a data em formato de data padrao
df_inadimplencia['data'] = pd.to_datetime(df_inadimplencia['data'])

#filtra datas acima de 31/12/2011 para que todas as dimensoes e fatos tenham o mesmo periodo
df_inadimplencia = df_inadimplencia[df_inadimplencia.data > pd.to_datetime('31/12/2011')]

#converte as taxas de juros anuais e mensais para string
df_inadimplencia['valor'] = df_inadimplencia['valor'].astype(str)

#substitui pontos por virgulas para serem adaptados
df_inadimplencia['valor'] = df_inadimplencia['valor'].str.replace('.', ',')

#armazena a df em uma variavel fato
fato_inadimplencia = df_inadimplencia

#renomeia a coluna de data 
fato_inadimplencia = fato_inadimplencia.rename(columns={'data': 'DataReferencia'})

#renomeia a coluna de valor 
fato_inadimplencia = fato_inadimplencia.rename(columns={'valor': 'TaxaInadimplencia'})


del df_pessoal_nao_consignado, df_pessoal_inss, df_pessoal_privado, df_aquisicoes_outros_bens, df_aquisicoes_veiculos, df_arrendamento_mercantil, df_cartao_rotativo, df_cartao_total, df_cheque_especial, df_desconto_cheques, df_pessoal_publico
del dia, ano, mes
del df_inadimplencia


# Salvando na unidade --------------------------------------------------------

#armazena a variavel fato_inadimplencia em um arquivo xlsx no local D:
with pd.ExcelWriter('D:/TCC/Arquivos_xlsx/fato_inadimplencia.xlsx', engine='xlsxwriter') as writer:
    fato_inadimplencia.to_excel(writer, sheet_name='fato_inadimplencia', index = False)
    
# Fecha o pip e gera o arquivo .xlsx
writer.save()