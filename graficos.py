#%%
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import layout_m as lm
import math

df_inicial = pd.read_csv('new_3.csv')

#||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||#
# MAPA ARTISTAS

def mapa():
    
    df = df_inicial[['paises', 'artistas', 'ouvintes']]       
    df = df.sort_values(by = 'ouvintes', ascending = False)

    # LÊ O CSV, DETERMINA AS COLUNAS A SEREM UTILIZADAS E ORDENA POR OUVINTES

    pais = df['paises']
    artista = df['artistas']
    paises = []
    artistas = []
    for i in range(len(df)):   
        if pais[i] not in paises and artista[i] not in artistas and type(pais[i]) == str:
            paises.append(pais[i])
            artistas.append(artista[i])

    # EVITA O APARECIMENTO DE NaN E FAZ COM QUE PAISES APAREÇAM APENAS UMA VEZ 
           
    su = paises.index('Soviet Union')
    del(paises[su]) 
    del(artistas[su])

    # APAGA A UNIÃO SOVIÉTICA DAS LISTAS PARA EVITAR QUE ELA SOBRESCREVA A RUSSIA

    trace = go.Scattergeo(
                        fill = 'toself',
                        fillcolor = '#252e3f', # DETERMINA A COR DA CAIXA DE TEXTO
                        locationmode = 'country names', # DETERMINA O MODO EM QUE VÃO SER ENCONTRADOS 
                                                        # AS LOCALIZAÇÕES QUE APARECEM NA VARIÁVEL "LOCATIONS"
                        locations = paises, # DETERMINA AS LOCALIZAÇÕES QUE APARECEM NO MAPA, NO CASO OS PAÍSES
                        text = artistas, # DETERMINA O TEXTO QUE APARECE NA CAIXA DE TEXTO,
                                        # NESTE CASO, OS ARTISTAS MAIS INFLUENTES NO PAÍS
                        mode = 'none', # DETERMINA O MODO DE COMO VÃO APARECER AS LOCALIZAÇÕES NO MAPA
                        )

    # CRIA O GRÁFICO

    layout = lm.layout_mc('Most Relevant Artist by Country')

    # EDITA O LAYOUT 

    data = [trace]
    fig = go.Figure(data=data, layout=layout)
    return fig

#||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||#
# MAPA DE CALOR

def calor(): 
    
    df = df_inicial[['scrobbles', 'paises']]
    df = df.groupby(by = 'paises').sum()

    # LÊ O CSV, DETERMINA AS COLUNAS A SEREM UTILIZADAS E 
    # SOMA OS SCROBBLES SEPARANDO-OS POR PAISES

    scrobbles = [math.log2(i) for i in df['scrobbles']]
    # CALCULA O LOG DOS SCROBBLES DE CADA PAÍS

    trace = go.Choropleth(
                        locationmode = 'country names', # DETERMINA O MODO QUE MOSTRARÁ OS PONTOS NO MAPA
                        locations = df.index, # DETERMINA AS LOCALIZAÇÕES QUE APARECEM NO MAPA, NO CASO OS PAÍSES
                        z = scrobbles, # BASE PARA AS CORES DO MAPA
                        text = df['scrobbles'],
                        colorscale = [
                                    'rgb(255, 255, 255)',
                                    'rgb(67, 183, 152)'
                                    ], # ESCALA DE CORES DETERMINADA PARA O GRÁFICO
                        colorbar = {'thickness' : 25,
                                    'tickfont' : {'color' : '#c8d4d3',
                                                'family' : 'Courier New'}} # DETERMINA A COR E FONTE DO TEXTO E A LARGURA DA BARRA DE CORES
                        )

    # CRIA O GRÁFICO

    layout = lm.layout_mc('Heat Map of Scrobbles per Country')

    # EDITA O LAYOUT

    data = [trace]
    fig = go.Figure(data=data, layout=layout)
    return fig

#||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||#
# GRÁFICO PAÍS

def pais(pais):
    
    df = df_inicial[['paises', 'ouvintes', 'estilos']]
    df = df.sort_values(by = 'ouvintes', ascending = False)

    # LÊ O CSV, DETERMINA AS COLUNAS A SEREM UTILIZADAS E ORDENA POR OUVINTES

    x = pais
    uk = df[df['paises'] == x].dropna()
    # CRIA UM DATA FRAME COM APENAS OS DADOS DO PAÍS DESEJADO E RETIRA OS NaN

    group = uk[['ouvintes']].groupby(uk['estilos']).sum().sort_values(by = 'ouvintes', ascending = False)
    group['estilos'] = group.index

    # SOMA TODOS OS OUVINTES, SEPARANDO-OS POR ESTILOS

    if 'outro' in group['estilos'][:10]:
            y = group.loc['outro']
            group = group.drop('outro')
            group = group.append(y)

    # MOVE O ESTILO "OUTRO" PARA O FINAL DO DATAFRAME

    total = group['ouvintes'].sum()
    group['porcentagem'] = (group['ouvintes'] / total)
    # CALCULA A PORCENTAGEM DE CADA ESTILO E CRIA UMA COLUNA COM ESTAS PORCENTAGENS

    others = group['porcentagem'][11:].sum()
    group['porcentagem'][10] = others

    # SOMA A PORCENTAGEM DE TODOS ESTILOS A PARTIR DO 11° RELEVANTE E ADICIONA UMA LINHA COM ESTA PORCENTAGEM

    group_top = group.head(n = 11)
    group_top['estilos'][10] = 'others'

    # PEGA OS PRIMEIROS 10 ESTILOS MAIS RELEVANTES E A SOMA DAS OUTRAS PORCENTAGENS

    trace = go.Bar(x = group_top['estilos'],
                y = group_top['porcentagem'],
                marker = {'color' : '#c8d4d3'})

    # CRIA O GRÁFICO COM OS ESTILOS E A PORCENTAGEM DE CADA UM E DEFINE SUA COR
                    
    layout = lm.layout_gps('Percentage of Listeners by Genres: ' + x.title(),
                        'listeners percentage',
                        )
    # MUDA O LAYOUT DO GRÁFICO

    data = [trace]
    fig = go.Figure(data = data, layout = layout)
    return fig

#||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||#
# GRÁFICO GêNERO

def genero(estilo):
    
    df = df_inicial[['paises', 'ouvintes', 'estilos']]
    df = df.sort_values(by = 'ouvintes', ascending = False)

    # LÊ O CSV, DETERMINA AS COLUNAS A SEREM UTILIZADAS E ORDENA POR OUVINTES

    x = estilo
    uk = df[df['estilos'] == x].dropna()
    # CRIA UM DATA FRAME COM APENAS OS DADOS DO ESTILO DESEJADO E RETIRA OS NaN

    group = uk[['ouvintes']].groupby(uk['paises']).sum().sort_values(by = 'ouvintes', ascending = False)
    group['paises'] = group.index

    # SOMA TODOS OS OUVINTES, SEPARANDO-OS POR PAÍSES

    if 'outro' in group['paises'][:10]:
            y = group.loc['outro']
            group = group.drop('outro')
            group = group.append(y)

    # MOVE O PAÍS "OUTRO" PARA O FINAL DO DATAFRAME

    total = group['ouvintes'].sum()
    group['porcentagem'] = (group['ouvintes'] / total)
    # CALCULA A PORCENTAGEM DE CADA PAÍS E CRIA UMA COLUNA COM ESTAS PORCENTAGENS

    others = group['porcentagem'][11:].sum()
    group['porcentagem'][10] = others

    # SOMA A PORCENTAGEM DE TODOS PAÍSES A PARTIR DO 11° RELEVANTE E ADICIONA UMA LINHA COM ESTA PORCENTAGEM

    group_top = group.head(n = 11)
    group_top['paises'][10] = 'others'

    # PEGA OS PRIMEIROS 10 PAÍSES MAIS RELEVANTES E A SOMA DAS OUTRAS PORCENTAGENS

    trace = go.Bar(x = group_top['paises'],
                y = group_top['porcentagem'],
                marker = {'color' : '#c8d4d3'})

    # CRIA O GRÁFICO COM OS PAÍSES E A PORCENTAGEM DE CADA UM E DEFINE SUA COR
                    
    layout = lm.layout_gps('Percentage of Listeners by Countries: ' + x.title(),
                        'listeners percentage',
                        )
    # MUDA O LAYOUT DO GRÁFICO

    data = [trace]
    fig = go.Figure(data = data, layout = layout)
    return fig

#||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||#
# GRÁFICO HISTOGRAMA

def histograma():
    
    # 1º - Definindo a variável "df" (dataframe) que receberá as informações que está no csv
    # 2º - Utilizando a biblioteca pandas (pd) lerá o csv "new_3.csv" e armazenará apenas a coluna "ouvintes" no dataframe
    df = df_inicial[['ouvintes']]
    # Calcula número de ouvintes no dataframe
    somaouvintes = df['ouvintes'].sum()
    # Cria uma lista com a porcentagem do numero de ouvintes de cada artista
    porc = (df['ouvintes'])/somaouvintes

    # Plotando o gráfico
    # 1º - Definindo a variável "fig" onde será armazenado o gráfico
    # 2º - Utiliza a função histograma no módulo "px" da biblioteca plotly
    fig = px.histogram(df, # Informa que a origem dos dados, não especificados, vêm do dataframe "df"
                    x = 'ouvintes', # O eixo x se refere ao número de ouvintes
                    y = porc, # O eixo y se refere à porcentagem de artistas com certo número de ouvintes
                    nbins = 30, # Divide o total de ouvintes em 30 intervalos
                    color_discrete_sequence = ['#c8d4d3']) # Muda a cor das barras do gráfico

    # Modificando o layout do gráfico "fig"
    fig.update_layout (lm.layout_gps('Histogram: Number of Listeners per Artist', 'percentage of artists', 'number of listeners')) # Altera a cor do papel ao redor do gráfico
    fig.update_layout(yaxis_tickformat= '.2%',
                      margin = dict(t = 100))
    # Mostra o gráfico construído
    return fig

#||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||#
# GRÁFICO SCROBBLES

def scrobbles():
    
    df = df_inicial[['paises', 'scrobbles']]
    df = df.groupby(by='paises').sum()
    df = df.sort_values(by='scrobbles', ascending=False)

    # LÊ O CSV, DETERMINA AS COLUNAS A SEREM UTILIZADAS E  
    # SOMA OS VALORES DE SCROBBLES E OUVINTES E ORDENA O DATAFRAME POR SCROBBLES

    soma = df['scrobbles'].sum()
    df['porcentagem'] = (df['scrobbles']/soma)
    df['paises'] = df.index

    # CALCULA A PORCENTAFEM DE SCROBBLES POR PAÍS

    if 'outro' in df['paises'][:10]:
            y = df.loc['outro']
            df = df.drop('outro')
            df = df.append(y)

    # MOVE O PAÍS "OUTRO" PARA O FINAL DO DATAFRAME

    others = df['porcentagem'][11:].sum()
    df['porcentagem'] = df['porcentagem'][0:11]
    df['porcentagem'][10] = others
    df['paises'][10] = 'others'
    df_top = df.head(n = 11)

    # SOMA A PORCENTAGENS DE SCROBBLES A PARTIR DO 11° E ARMAZENA NA POSIÇÃO 11 DA COLUNA "PORCENTAGEM"
    # E PEGA APENAS OS 10 PRIMEIROS PAÍSES E A SOMA

    trace = go.Bar(
                x =  df_top['paises'],
                y =  df_top['porcentagem'],
                marker = {'color': '#c8d4d3'})

    # CRIA O GRÁFICO E DETERMINA SUA COR

    layout = lm.layout_gps('Proportion of all Scrobbles by Country',
                        'listeners percentage',
                        'countries')

    # EDITA O LAYOUT DO GRÁFICO

    data = [trace]
    fig = go.Figure(data=data, layout=layout)
    return fig

# %%
