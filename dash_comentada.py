import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input,Output
import graficos as gr
import pandas as pd

# cria o index dos dropdowns

df = pd.read_csv('new_3.csv', usecols= ['paises', 'ouvintes', 'estilos']) 

# cria o index do gráfico de gênero
df2 = df[['ouvintes']].groupby(df['estilos']).sum().sort_values(by = 'ouvintes', ascending = False).index # pega os estilos em ordem
df2 = df2[:500] # tira os estilos a partir do 501
df2 = df2.drop('outro') # tira o estilo "outro"
df2 = df2.drop('britpop') # tira o estilo "britpop"

for estilo in df2[80:]: # repetição for para tirar os estilos do dropdown que possuam menos que 11 países (a partir da posição 80)
    df_est = df[df['estilos'] == estilo] # cria um data frame apenas com o estilo do for
    df_i = df_est[['ouvintes']].groupby(df['paises']).sum() # cria um novo data frame com a soma de cada país separado 
    if len(df_i) < 11: # condição para ver se o df_i (dataframe do estilo determinado pelo for agrupado por países) possui menos de 11 países
        df2 = df2.drop(estilo) # se a condição for verdadeira (o estilo possuir menos de 11 países) este estilo é retirado do index do dropdown

# cria o index do gráfico de país
df3 = df[['ouvintes']].groupby(df['paises']).sum().sort_values(by = 'ouvintes', ascending = False).index # pega os países em ordem de maior ouvinte pro menor

df3 = df3.drop('outro') # tira o estilo "outro" do dropdown

for país in df3: # repetição for para tirar os países com menos de 11 gêneros diferentes
    df_pa = df[df['paises'] == país] # cria um dataframe com apenas o país em questão do for
    df_k = df_pa[['ouvintes']].groupby(df['estilos']).sum() # cria um novo data frame com a soma de cada gênero separado
    if len(df_k) < 11: # condição para verificar se o país em questão possui menos de 11 estilos diferentes
        df3 = df3.drop(país) # se a condição for verdadeira, retira o país do dropdown

#################################################################################################################################

app = dash.Dash(__name__) # cria a dash (argumento '__name__' pega e utiliza o .css na pasta assets)

app.layout = html.Div( # divisão geral
                      children = [ # lista do que tem dentro da div
    
    html.Br(),
    
    html.Div([ # divisão do título e logo
    
        html.Img(src = app.get_asset_url("logo.jpeg"), 
                className = "imagem"), # coloca a logo

        html.Br(), # pula linha (espaço "em branco")

        html.H1( 
                children = 'Music Analytics Around the World' # título
        ),

    ], className = "título"), # classe correspondente no css sobre o título

    html.Br(), # pula outra linha
    
    html.Div(style = {'backgroundColor' : '#252e3f'}, # divisão do Mapa
            children = [ # lista do que tem dentro da div
                html.Label( 
                    children = '''
                    Maps: Most Relevant Artist by Country & Numbers of Scrobbles Heat Map
                    ''',
                ), # título da divisão dos mapas

                dcc.Graph(
                    id = 'grafico' # cria o local dos mapas e determina como id 'gráfico'
                ),
                html.P(
                    'Select Map:' # "parágrafo" em cima do dropdown
                ),

                dcc.Dropdown( # botão para selecionar os mapas
                    id= 'filtro', # identificação
                    options = [{'label' : 'Relevant Artists', 'value' : 1}, # options: determina as opções e seus respectivos valores que irão aparecer no dropdown
                                {'label' : 'Scrobbles Heat Map', 'value' : 2}],
                    searchable = False, # determina que não será possível pesquisar no dropdown
                    clearable = False, # determina que não será possível limpar o dropdown
                    placeholder = 'Select a map', # texto que vai no dropdown quando não for selecionado nenhum valor
                    className = 'dropdown' # classe correspondente no css
                )

            ], className = 'mapa'), # classe correspondente no css sobre a divisão dos mapas


    html.Div( # divisão dos gráficos de país e gênero
            children = [ # lista com o conteúdo da div

        html.Div(   # divisão do gráfico de genero
            children = [ # lista com o conteúdo da div

                dcc.Graph(
                    id = 'genero' # cria o local do gráfico de gênero com a id 'genero'
                ),

                dcc.Dropdown( # botão de seleção dos gêneros
                    id = 'estilos-drop', # identificação
                    options = [{'label' : i.title(), 'value' : i} for i in df2], # opções e respectivos valores que irão aparecer no dropdown
                    clearable = False, # determina que não será possível limpar o dropdown
                    className = 'dropdown', # classe correspondente no css sobre o dropdown
                    placeholder = 'Select a Genre' # texto que vai no dropdown quando não for selecionado nenhum valor
                    
                )
            ], className = 'box1'), # classe correspondente no css sobre a divisão do gráfico de gênero


        html.Div(   # divisão do gráfico de pais
            children = [ # lista com o conteúdo da div

                dcc.Graph(
                    id = 'pais' # cria o local do gráfico de país com a id 'pais'
                ),

                dcc.Dropdown( # botão de seleção dos países
                    id = 'pais-drop', # identificação
                    options = [{'label' : i.title(), 'value' : i} for i in df3], # opções e respectivos valores que irão aparecer no dropdown
                    clearable = False, # determina que não será possível limpar o dropdown
                    className = 'dropdown', # classe correspondente no css sobre o dropdown
                    placeholder = 'Select a Country' # texto que vai no dropdown quando não for selecionado nenhum valor
                )
            ], className = 'box2') # classe correspondente no css sobre a divisão do gráfico de país

        ], className = 'divs'), # classe correspondente no css sobre a divisão dos gráficos de gênero e páis
    

    html.Br(), # pula uma "linha"

    html.Div( # divisão dos gráficos de scrobbles e histograma
            children = [ # lista com o conteúdo da div
    

        html.Div(      # Divisão do gráfico de scrobbles
                children = [ # lista com o conteúdo da div

                    dcc.Graph( # cria o local do gráfico de scrobbles
                        id = 'scrobbles', # determina a id do mesmo como 'scrobbles'
                        figure = gr.scrobbles() # chama a função scrobbles do módulo gráficos(.py) e determina como figure
                    )
                ],className = 'box1'), # classe correspondente no css sobre a divisão do gráfico de scrobbles
    

        html.Div(   # Divisão do gráfico histograma
                children = [ # lista com o conteúdo da div

                dcc.Graph(
                    id = 'histograma', # cria o local do gráfico histograma
                    figure = gr.histograma(), # chama a função histograma do módulo gráficos(.py) e determina como figure
                )
                ],className = 'box2'), # classe correspondente no css sobre a divisão do gráfico histograma
    
            ], className = 'divs'), # classe correspondente no css sobre a divisão dos gráficos de scrobbles e histograma

    html.Br() # pula outra linha

], className = 'box3') # classe correspondente no css sobre a divisão geral

@app.callback( # callback dos mapas
    Output('grafico', 'figure'), # determina que o elemento a ser mudado é a "figure" onde o id for "grafico"
    [Input(component_id = 'filtro', component_property = 'value')] # determina que para mudar a figure é necessário mudar o "value" onde o id for "filtro"
)

def update_output(value): # função chamada pelo callback com argumento o value
    if value is None or value == 1: # se o value for "nenhum" (nada selecionado) ou 1, irá chamar o gráfico de artistas
        return gr.mapa()
    else:
        if value == 2:  # se o value for 2, irá chamar o mapa de calor
            return gr.calor()

@app.callback( # callback do gráfico de gênero
    Output('genero', 'figure'), # determina que o elemento a ser mudado é a "figure" onde o id for "genero"
    [Input(component_id = 'estilos-drop', component_property = 'value')] # determina que para mudar a figure é necessário mudar o "value" onde o id for "estilos_drop"
)

def update_genero(value): # função chamada pelo callback com argumento o value
    if value == None: # se o value for nenhum, irá chamar o gráfico de gênero com argumento 'pop'
        return gr.genero('pop')
    else: # se o value não for nenhum, irá chamar o gráfico de gênero com argumento o value
        return gr.genero(value)

@app.callback( # callback do gráfico de país
    Output('pais', 'figure'), # determina que o elemento a ser mudado é a "figure" onde o id for "pais"
    [Input(component_id = 'pais-drop', component_property = 'value')] # determina que para mudar a figure é necessário mudar o "value" onde o id for "pais-drop"
)

def update_pais(value): # função chamada pelo callback com argumento o value
    if value == None: # se o value for nenhum, irá chamar o gráfico de país com argumento 'Brazil'
        return gr.pais('Brazil')
    else: # se o value não for nenhum, irá chamar o gráfico de país com argumento o value
        return gr.pais(value)

if __name__ == '__main__': # se o arquivo estiver sendo executado diretamente, irá rodar o server da dash
    app.run_server(debug = True) 