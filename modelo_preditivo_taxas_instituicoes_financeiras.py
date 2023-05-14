# -----------------------------------------------------------------------------
# Modelo de anaalise das taxas cobradas pelas instituicoes financeiras
# -----------------------------------------------------------------------------


# quero construir um modelo capaz de prever como sera a taxa de juros praticada pelas instituicoes
# para isso usarei 3 fatos e 3 dimensoes


# Importando as Bibliotecas que serao usadas durante o Script ----------------

#importando biblioteca de manipulacao de tabelas
import pandas as pd
#importanto biblioteca para visualizacao de dados
import matplotlib.pyplot as plt 
#importanto classe para modelos de regressao linear 
from sklearn.linear_model import LinearRegression 
#importanto funcao para dividir os dados em treino e teste 
from sklearn.model_selection import train_test_split  


# Conectando com as Fontes de Dados ------------------------------------------

# sera necessario extrair os arquivos em xlsx com as informacoes

#carrega o arquivo xlsx com a tabela fato de taxas de juros
fato_juros = pd.read_excel('D:/TCC/Arquivos_xlsx/fato_juros.xlsx')

#carrega o arquivo xlsx com a tabela fato de taxas de endividamento  
fato_endividamento_familiar = pd.read_excel('D:/TCC/Arquivos_xlsx/fato_endividamento_familiar.xlsx')  

#carrega o arquivo xlsx com a tabela fato de taxas inadimplencia  
fato_inadimplencia = pd.read_excel('D:/TCC/Arquivos_xlsx/fato_inadimplencia.xlsx')  

#carrega o arquivo xlsx com a tabela dimensao de calendario
dim_calendario = pd.read_excel('D:/TCC/Arquivos_xlsx/dim_calendario.xlsx')

#carrega o arquivo xlsx com a tabela dimensao de instituicoes
dim_instituicoes = pd.read_excel('D:/TCC/Arquivos_xlsx/dim_instituicoes.xlsx')  

#carrega o arquivo xlsx com a tabela dimensao de modalidade  
dim_modalidade = pd.read_excel('D:/TCC/Arquivos_xlsx/dim_modalidade.xlsx')  


# Preparando os dados para juntar todas as tabelas ---------------------------

# sera necessario juntar as tabelas de fato com as dimensoes 
# para isso usarei o pd.merge e excluirei as colunas que sao repetidas em outras tabelas

#junta 'fato_juros' com 'dim_calendario'
df = pd.merge(fato_juros, dim_calendario, on='DataReferencia')

#exclui 'DataReferencia'
df = df.drop(columns=['DataReferencia'])

# sera necessario criar os campos 'Mes' e 'Ano' para juntar outras tabelas de fato ao dim_calendario

#adiciona as variaaveis de mes e ano ao
fato_endividamento_familiar['Mes'] = fato_endividamento_familiar['DataReferencia'].dt.month
fato_endividamento_familiar['Ano'] = fato_endividamento_familiar['DataReferencia'].dt.year
fato_inadimplencia['Mes'] = fato_inadimplencia['DataReferencia'].dt.month
fato_inadimplencia['Ano'] = fato_inadimplencia['DataReferencia'].dt.year

#junta o df com 'fato_endividamento_familiar'
df = pd.merge(df, fato_endividamento_familiar, on=['Ano', 'Mes'], how= 'left')

#exclui 'DataReferencia'
df = df.drop(columns=['DataReferencia'])

#junta o df com 'fato_inadimplencia'
df = pd.merge(df, fato_inadimplencia, on=['Ano', 'Mes', 'Modalidade'], how= 'left')

#junta o df com 'dim_instituicoes' usando os dados das intituicoes como chave
df = pd.merge(df, dim_instituicoes, on=['CNPJ', 'InstituicaoFinanceira'], how= 'left')

#junta o df com 'fato_inadimplencia' usando a modalidade como chave
df = pd.merge(df, dim_modalidade, on='Modalidade', how= 'left')

#deleta as linhas onde alguma coluna apresente dados vazios
df = df.dropna()


# Convertendo e ajustando os campos da tabela de taxas -----------------------

# para melhor aproveitamento da base sera necessario converter alguns campos

#converte as taxas para string (texto)
df['TaxaJurosAoMes'] = df['TaxaJurosAoMes'].astype(str)
df['TaxaJurosAoAno'] = df['TaxaJurosAoAno'].astype(str)
df['TaxaEndividamento'] = df['TaxaEndividamento'].astype(str)
df['TaxaInadimplencia'] = df['TaxaInadimplencia'].astype(str)

#substitui pontos por virgulas para serem adaptados
df['TaxaJurosAoMes'] = df['TaxaJurosAoMes'].str.replace(',','.')
df['TaxaJurosAoAno'] = df['TaxaJurosAoAno'].str.replace(',','.')
df['TaxaEndividamento'] = df['TaxaEndividamento'].str.replace(',','.')
df['TaxaInadimplencia'] = df['TaxaInadimplencia'].str.replace(',','.')

#converte as taxas para float (numero)
df['TaxaJurosAoMes'] = df['TaxaJurosAoMes'].astype(float)
df['TaxaJurosAoAno'] = df['TaxaJurosAoAno'].astype(float)
df['TaxaEndividamento'] = df['TaxaEndividamento'].astype(float)
df['TaxaInadimplencia'] = df['TaxaInadimplencia'].astype(float)


# Mapeando as categorias de Modalidade de texto para valores numericos -------

# para que a modalidade entre nas premissas de previsao sera necessario codifica-las
# sera considerado a ordem alfabetica e numerado de ordem crescente do 1 ao 11

#mapeia cada Modalidade com um codigo
modalidade_codigo = {
    'AQUISIÇÃO DE OUTROS BENS': 1,
    'AQUISIÇÃO DE VEÍCULOS': 2,
    'ARRENDAMENTO MERCANTIL DE VEÍCULOS': 3,
    'CARTÃO DE CRÉDITO - PARCELADO': 4,
    'CARTÃO DE CRÉDITO - ROTATIVO TOTAL': 5,
    'CHEQUE ESPECIAL': 6,
    'CRÉDITO PESSOAL CONSIGNADO INSS': 7,
    'CRÉDITO PESSOAL CONSIGNADO PRIVADO': 8,
    'CRÉDITO PESSOAL CONSIGNADO PÚBLICO': 9,
    'CRÉDITO PESSOAL NÃO-CONSIGNADO': 10,
    'DESCONTO DE CHEQUES': 11
}

#substitui as categorias de texto pelos valores numericos correspondentes
df['CodigoModalidade'] = df['Modalidade'].map(modalidade_codigo)


# Criando o df para receber os dados resumidos e descobrir as maiores taxas --

# sera considerado o ano atual sempre para pegar os ultimos 3 anos

#pondera o ano atual
ano_atual = pd.Timestamp.now().year

#filtra os ultimos 3 anos
anos_filtrados = range(ano_atual-2, ano_atual+1)

#calcula a media das taxas de juros para cada instituicao financeira e cria um df separado
taxas_medias = df.groupby(['Modalidade', 'CodigoModalidade', 'Ano'])['TaxaJurosAoMes'].mean().reset_index()

#filtra no df criado os dados dos ultimos 3 anos
taxas_medias = taxas_medias[taxas_medias['Ano'].isin(anos_filtrados)]

#realiza um agrupamento em modalidade retirando o campo 'Ano'
taxas_medias = taxas_medias.groupby(['Modalidade', 'CodigoModalidade'])['TaxaJurosAoMes'].mean().reset_index()

#ordena o df por taxa de juros media em ordem decrescente
taxas_medias = taxas_medias.sort_values(by='TaxaJurosAoMes', ascending=False)

#calcula a porcentagem acumulada das taxas de juros adicionando uma coluna com as porcentagens acumuladas
taxas_medias['PorcentagemAcumulada'] = (taxas_medias['TaxaJurosAoMes'].cumsum() 
                                        / taxas_medias['TaxaJurosAoMes'].sum()) * 100



# Usando o df 'taxas_medias' para plotar um pareto ---------------------------

#cria a figura e os eixos
fig, ax1 = plt.subplots()

# Plotando as barras das taxas de juros medias --------

#prepara os dados do grafico de barras definindo o eixo x e y, alem de definir a cor
ax1.bar(taxas_medias['Modalidade'], taxas_medias['TaxaJurosAoMes'], color='tab:blue')
#define o titulo do eixo x
ax1.set_xlabel('Modalidade')
#define o titulo do eixo y e a cor
ax1.set_ylabel('Taxa de Juros média de 3 anos', color='tab:blue')
#define  a cor (parametros) do eixo y do primeiro grafico (ax1)
ax1.tick_params(axis='y', labelcolor='tab:blue')


# Plotando a linha da porcentagem acumulada --------

#cria um segundo conjunto de eixos (ax2) que compartilha o mesmo eixo x (Modalidade) com o primeiro grafico
ax2 = ax1.twinx()
#prepara os dados do grafico de linhas definindo o eixo x e y, alem de definir a cor e o marcador
ax2.plot(taxas_medias['Modalidade'], taxas_medias['PorcentagemAcumulada'], color='tab:red', marker='o')
#define o minimo e o maximo do eixo y do segundo grafico
ax2.set_ylim([0, 105])
#define o titulo do eixo y e a cor
ax2.set_ylabel('Porcentagem acumulada', color='tab:red')
#define a cor (parametros) do eixo y do segundo grafico (ax2)
ax2.tick_params(axis='y', labelcolor='tab:red')

# Plotando a parte visual do grafico --------

#adiciona uma linha vertical para 80% de porcentagem acumulada, alem de definir o estilo da linha
ax2.axhline(y=80, color='tab:green', linestyle='--')

#define o titulo do grafico
plt.title('Gráfico de Pareto - Taxas de juros por Modalidade')

#ajusta automaticamente o espaçamento entre os elementos do grafico e o espaçamento entre as barras
plt.tight_layout()

#rotaciona os rotulos do eixo x para melhor visualizacao no ax1
ax1.set_xticklabels(taxas_medias['Modalidade'], rotation=90)

#rotaciona os rotulos do eixo x para melhor visualizacao no ax2
ax2.set_xticklabels(taxas_medias['Modalidade'], rotation=90)

#exibe o grafico
plt.show()


# Preparando os dados para o modelo de aprendizado de maquina ----------------

# para isso vou usar alguns campos como variaveis importantes na analise dos dados

#prepara o eixo x com alguns campos
X = df[['TaxaEndividamento'
        , 'TaxaInadimplencia'
        , 'CodigoModalidade'
        , 'Ano'
        , 'Mes']]

#prepara o eixo y com 'TaxaJurosAoMes'
y = df[['TaxaJurosAoMes']]

#divide os dados em treino e teste (80% para treino, 20% para teste)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

#cria o modelo de regressao linear
model = LinearRegression()

#treina o modelo com os dados de treino
model.fit(X_train, y_train)

# para garantir que o modelo esta confiavel avalia-se o score onde, quanto mais proximo de 1 melhor

#avalia o modelo com os dados de teste
score = model.score(X_test, y_test)

#exibe o score do modelo
print('Score do modelo:', score)


# Preparando as premissas para predicao das taxas de juros -------------------

# para isso vou usar as taxas de endividamento e inadimplencia mais recentes
# alem disso vou declarar o ano e mes que quero predizer

#calcula a media das taxas de juros para cada instituicao financeira
df_endividamento = df[['DataReferencia','CodigoModalidade', 'TaxaEndividamento']]
df_inadimplencia = df[['DataReferencia','CodigoModalidade', 'TaxaInadimplencia']]

#ordena o dfs criados pela coluna de data em ordem decrescente
df_endividamento = df_endividamento.sort_values("DataReferencia", ascending=False)
df_inadimplencia = df_inadimplencia.sort_values("DataReferencia", ascending=False)

#agrupa os dados por CodigoModalidade e obtem o valor mais recente de cada grupo
df_endividamento_recente = df_endividamento.groupby('CodigoModalidade').first().reset_index()
df_inadimplencia_recente = df_inadimplencia.groupby('CodigoModalidade').first().reset_index()

#seleciona apenas as colunas necessárias
df_endividamento_recente = df_endividamento_recente[['CodigoModalidade', 'TaxaEndividamento']]
df_inadimplencia_recente = df_inadimplencia_recente[['CodigoModalidade', 'TaxaInadimplencia']]

# Criando um novo conjunto de dados -------------------------------------------

#prepara o eixo x 
X_pred = pd.DataFrame({
#usa as taxas predefinidas
    'TaxaEndividamento': df_endividamento_recente['TaxaEndividamento'],
    'TaxaInadimplencia': df_inadimplencia_recente['TaxaInadimplencia'],
#declara todas as modalidades de credito
    'CodigoModalidade': [1,2,3,4,5,6,7,8,9,10,11],
#define o ano e o mes e repete para todas as modalidades
    'Ano': [2023] * len(df_inadimplencia_recente),
    'Mes': [12] * len(df_inadimplencia_recente)
})


# Fazendo uma predicao com o novo conjunto de dados
y_pred = model.predict(X_pred)

X_pred['predicao'] = y_pred



# Plotando grafico de linha com base na taxa de inadimplencia e na previsao --

#prepara os dados do grafico de linha definindo o eixo x e y, alem de definir a cor
plt.plot(X_pred['TaxaInadimplencia'], X_pred['predicao'], label='Predição', color='black')

#define o rotulo para os eixo x
plt.xlabel('Taxa de Inadimplência')
#define o rotulo para os eixo y
plt.ylabel('Predição')

#define o titulo do grafico
plt.title('Evolução da Predição x Inadimplência')

#adiciona uma legenda ao grafico
plt.legend()

#exibe o grafico
plt.show()


