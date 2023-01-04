# -----------------------------------------------------------------------------
# Tabela de endividamento familiar
# -----------------------------------------------------------------------------


# relacao entre a soma dividas das familias e a renda acumulada nos ultimos doze meses.
# para isso usarei 10 instituicoes como exemplo

# Importando as Bibliotecas que serao usadas durante o Script ----------------

#importando biblioteca de manipulacao de tabelas
import pandas as pd



# Conectando com as Fontes de Dados ------------------------------------------

# sera necessario extrair a API do Banco Central do Brasil

#conecta com a API do Banco Central do Brasil extraindo o arquivo em json e lendo com Pandas
df_endividamento = pd.read_json("https://api.bcb.gov.br/dados/serie/bcdata.sgs.29037/dados?formato=json")

# preparando as variasveis de data
mes = df_endividamento['data'].str[3:5]
dia = df_endividamento['data'].str[0:2]
ano = df_endividamento['data'].str[-4:]

#ajustando as datas
df_endividamento['data'] = mes+'/'+dia+'/'+ano

#transforma a data em formato de data padrao
df_endividamento['data'] = pd.to_datetime(df_endividamento['data'])

#filtra datas acima de 31/12/2011 para que todas as dimensoes e fatos tenham o mesmo periodo
df_endividamento = df_endividamento[df_endividamento.data > pd.to_datetime('31/12/2011')]

#converte as taxas de juros anuais e mensais para string
df_endividamento['valor'] = df_endividamento['valor'].astype(str)

#substitui pontos por virgulas para serem adaptados
df_endividamento['valor'] = df_endividamento['valor'].str.replace('.', ',')

# Criar as tabelas Fato relacionadas aos dados extraídos

# Prepara a fato endividamento familiar --------------------------------------

#separa a tabela fato com o historico de endividamento familiar
fato_endividamento_familiar = df_endividamento

#renomeia a coluna de data 
fato_endividamento_familiar = fato_endividamento_familiar.rename(columns={'data': 'DataReferencia'})

#renomeia a coluna de valor 
fato_endividamento_familiar = fato_endividamento_familiar.rename(columns={'valor': 'TaxaEndividamento'})

#deleta as dfs e lst que nao sera mais usada
del df_endividamento, mes, dia, ano

# salva na unidade

with pd.ExcelWriter('D:/TCC/Arquivos_xlsx/fato_endividamento_familiar.xlsx', engine='xlsxwriter') as writer:
    fato_endividamento_familiar.to_excel(writer, sheet_name='fato_endividamento_familiar', index = False)
    
# Fecha o pip e gera o arquivo .xlsx
writer.save()

del writer