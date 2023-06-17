import pandas as pd
import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import plotly.express as px
import dash_bootstrap_components as dbc
import plotly.graph_objects as go

# Load the CSV file into a pandas DataFrame
data = pd.read_csv('GDP.csv')

# Drop the '2019' column
data = data.drop(columns=['2019'])

# Convert NaN values to 0
data = data.fillna(0)

# Get the list of unique countries
countries = data['Country '].unique()

# Define the years to include in the year slider
included_years = [1990, 1994, 1998, 2002, 2006, 2010, 2014, 2018]

# Create the marks dictionary for the year slider
marks = {i: str(year) for i, year in enumerate(included_years)}

# Create the Dash app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.MINTY])

# Define the app layout
app.layout = dbc.Container(
    style={'font-family': 'Arial, sans-serif', 'padding': '30px'},
    fluid=True,
    children=[
        dbc.Row(
            className='align-items-start',
            children=[
                dbc.Col(
                    className='col-8',
                    children=[
                        html.H2("World GDP per Capita Dashboard", style={'text-align': 'center', 'color': 'black'}),
                        html.H4("Visualizing Global Economic Growth from 1990 to 2018", style={'text-align': 'center', 'color': 'black'}),
                        html.P(
                            """Visualize the growth of world GDP per capita from 1990 to 2018 through this interactive dashboard. 
                            Explore the percentage growth in GDP per capita for each country, as represented on a choropleth map. 
                            Gain insights into global economic trends and the impact on living standards worldwide. 
                            Analyze the development of GDP per capita over time using line charts, compare countries using bar charts, 
                            and explore the growth rate and top-ranking countries for a comprehensive understanding of 
                            global economic dynamics.""",
                            style={'text-align': 'justify', 'padding': '20px', 'font-family': 'Calibri'}
                        ),
                        dbc.Container(
                            className='slider-container',
                            children=[
                                dcc.Slider(
                                    id='year-slider',
                                    min=0,
                                    max=len(included_years) - 1,
                                    value=0,
                                    marks=marks,
                                    step=1,
                                    className='slider'
                                )
                            ],
                            fluid=True,
                            style={'padding': '20px'}
                        ),
                        dbc.Row(
                            children=[
                                dbc.Col(
                                    className='col-8',
                                    children=[
                                        html.H3(
                                            id='title',
                                            style={'text-align': 'center', 'margin-top': '10px', 'color': 'black'}
                                        ),
                                        dcc.Graph(id='choropleth-graph'),
                                    ],
                                    align='top',
                                    width=8
                                ),
                                dbc.Col(
                                    className='col-4',
                                    children=[
                                        html.H5("Top Countries with Highest GDP per Capita", style={'text-align': 'left', 'color': 'black'}),
                                        html.Div(id='gdp-table'),
                                    ],
                                    align='top',
                                    width=4
                                ),
                            ],
                            style={'padding': '20px'}
                        ),
                        dbc.Row(
                            children=[
                                dbc.Col(
                                    className='col-3',
                                    children=[
                                        html.H4("Progression Analysis", style={'text-align': 'left', 'color': 'black'}),
                                        html.H6("Comparative Evolution of Selected Countries Over Time: 1990-2018", style={'text-align': 'left', 'color': 'black'}),
                                        html.P(
                                            """This line chart showcases the development of GDP per capita from 1990 to 2018. 
                                            Explore the changes in economic prosperity over time as countries progress and evolve. 
                                            By selecting specific countries, you can compare their individual growth trajectories 
                                            and gain insights into the factors influencing their GDP per capita. 
                                            Observe trends, fluctuations, and significant milestones as you analyze the dynamic 
                                            nature of economic development across nations. Discover the story behind GDP per capita 
                                            and its impact on countries' standards of living and overall economic well-being.""",
                                            style={'text-align': 'justify', 'padding': '5px', 'font-family': 'Calibri'}
                                        ),
                                    ],
                                    align='top',
                                    width=3
                                ),
                                dbc.Col(
                                    className='col-9',
                                    children=[
                                        html.H4("Line Chart", style={'text-align': 'left', 'color': 'black'}),
                                        dcc.Dropdown(
                                            id='country-dropdown-line',
                                            options=[{'label': country, 'value': country} for country in countries],
                                            value=['Germany', 'United States', 'China'],  # Default selected countries
                                            multi=True
                                        ),
                                        dcc.Graph(id='line-chart'),
                                    ],
                                    align='center',
                                    width=9
                                ),
                            ],
                            style={'padding': '20px'}
                        ),
                        dbc.Row(
                            children=[
                                dbc.Col(
                                    className='col-9',
                                    children=[
                                        html.H4("Bar Chart", style={'text-align': 'left', 'color': 'black'}),
                                        dcc.Dropdown(
                                            id='country-dropdown-bar',
                                            options=[{'label': country, 'value': country} for country in countries],
                                            value=['Germany', 'United States', 'China'],  # Default selected countries
                                            multi=True
                                        ),
                                        dcc.Dropdown(
                                            id='year-dropdown-bar',
                                            options=[{'label': year, 'value': year} for year in data.columns[2:]],
                                            value=data.columns[-1],  # Set default value to the last year 2018
                                            multi=False
                                        ),
                                        dcc.Graph(id='bar-chart'),
                                    ],
                                    align='center',
                                    width=9
                                ),
                                dbc.Col(
                                    className='col-3',
                                    children=[
                                        html.H4("Comparison Analysis", style={'text-align': 'left', 'color': 'black'}),
                                        html.H6("Comparative Analysis of Selected Countries for a Specific Year", style={'text-align': 'left', 'color': 'black'}),
                                        html.P(
                                            """In this part of the dashboard, you can select multiple countries of your choice and choose 
                                            a particular year to perform a GDP per capita analysis. The results will 
                                            be displayed in ascending order, with the country having a higher GDP per capita appearing at the top of the list. 
                                            This allows you to compare the economic performance of different countries 
                                            and gain insights into their relative prosperity.""",
                                            style={'text-align': 'justify', 'padding': '5px', 'font-family': 'Calibri'}
                                        ),
                                    ],
                                    align='top',
                                    width=3
                                ),
                            ],
                            style={'padding': '20px'}
                        ),
                        dbc.Row(
                            children=[
                                dbc.Col(
                                    className='col-3',
                                    children=[
                                        html.H4("Growth Rate Analysis", style={'text-align': 'left', 'color': 'black'}),
                                        html.H6("Analyzing the Annual Percentage Growth of GDP per Capita (%)", style={'text-align': 'left', 'color': 'black'}),
                                        html.P(
                                            """Explore the GDP growth rate percentage analysis to understand the dynamic changes in 
                                            economic performance across countries. This visualization showcases the annual growth 
                                            rates of GDP from 1990 to 2018, providing insights into the speed and direction of 
                                            economic expansion. Compare the growth rates of different countries and uncover trends, 
                                            fluctuations, and significant milestones. Gain a deeper understanding of the factors 
                                            driving economic growth and the implications for countries' development and prosperity.""",
                                            style={'text-align': 'justify', 'padding': '5px', 'font-family': 'Calibri'}
                                        ),
                                    ],
                                    align='top',
                                    width=3
                                ),
                                dbc.Col(
                                    className='col-9',
                                    #style={'background-color': 'darkgray'},  # Change 'lightgray' to 'darkgray' for dark backgroun
                                    children=[
                                        html.H4("Growth Rate %", style={'text-align': 'left', 'color': 'black'}),
                                        dcc.Dropdown(
                                            id='country-dropdown-growth',
                                            options=[{'label': country, 'value': country} for country in countries],
                                            value=['Germany', 'United States', 'China'],  # Default selected countries
                                            multi=True
                                        ),
                                        dcc.Graph(id='growth-rate'),
                                    ],
                                    align='center',
                                    width=9
                                )
                            ],
                            style={'padding': '20px'}
                        ),
                        html.P("Developed By: Suleman Butt", 
                        style={'text-align': 'left', 'font-weight': 'bold', 'color': 'black'}),
                        html.P("Data Source: Kaggle  ",
                        style={'text-align': 'left', 'font-family': 'Calibri', 'font-style': 'italic', 'display': 'inline'}),
                        html.A("https://www.kaggle.com/datasets/nitishabharathi/gdp-per-capita-all-countries",
                        href="https://www.kaggle.com/datasets/nitishabharathi/gdp-per-capita-all-countries",
                        target="_blank",
                        style={'text-align': 'left', 'font-family': 'Calibri', 'color': 'black', 'display': 'inline'})
                    ],
                    align='center',
                    width=12
                ),
            ]
        )
    ]
)

# Define the callback function to update the title based on the selected year
@app.callback(
    dash.dependencies.Output('title', 'children'),
    [dash.dependencies.Input('year-slider', 'value')]
)
def update_title(year_index):
    year = included_years[year_index]
    title = html.H5(
        f'GDP per Capita {year}',
        style={'text-align': 'center', 'margin-bottom': '0px', 'color': 'black'}
    )
    return title

# Define the callback function to update the choropleth graph based on the selected year
@app.callback(
    dash.dependencies.Output('choropleth-graph', 'figure'),
    [dash.dependencies.Input('year-slider', 'value')]
)
def update_choropleth(year_index):
    year = included_years[year_index]

    fig = px.choropleth(
        data_frame=data,
        locations='Country Code',
        locationmode='ISO-3',
        color=str(year),
        hover_data={'Country ': True, str(year): ':$,.0f'},
        color_continuous_scale='viridis',
        range_color=(data[str(year)].min(), data[str(year)].max()),
        labels={str(year): 'GDP per Capita '},
    )

    fig.update_geos(showframe=False, showcoastlines=False, projection_type="equirectangular")
    fig.update_layout(
        margin=dict(l=0, r=80, t=80, b=0),
        coloraxis_colorbar=dict(title='GDP per Capita $'),
    )

    return fig

# Callback for updating the GDP per capita table
@app.callback(
    Output('gdp-table', 'children'),
    [Input('year-slider', 'value')]
)
def update_gdp_table(selected_year):
    global data
    year = included_years[selected_year]
    data_year = data[['Country ', str(year)]]
    data_year['GDP per capita'] = data_year[str(year)]
    data_year = data_year[['Country ', 'GDP per capita']]
    data_year = data_year.sort_values('GDP per capita', ascending=False)
    
    # Add rank column to the DataFrame
    data_year['Rank'] = range(1, len(data_year) + 1)
    
    # Create the table using dbc.Table
    table = dbc.Table(
        [
            html.Thead(html.Tr([html.Th('Rank'), html.Th('Country'), html.Th('GDP per Capita')])),
            html.Tbody([
                html.Tr([
                    html.Td(data_year['Rank'].iloc[i]),
                    html.Td(data_year['Country '].iloc[i]),
                    html.Td('$ {:,.0f}'.format(data_year['GDP per capita'].iloc[i]))
                ]) for i in range(min(len(data_year), 10))
            ])
        ],
        striped=True,
        bordered=True,
        hover=True,
        responsive=True,
        className='table'
    )
    
    return table

# Define the callback function to update the line chart based on the selected countries
@app.callback(
    Output('line-chart', 'figure'),
    [Input('country-dropdown-line', 'value')]
)
def update_line_chart(countries):
    colors = px.colors.qualitative.Set3  # Use the qualitative Set3 color palette

    filtered_data = data[data['Country '].isin(countries)]
    filtered_data = filtered_data.melt(id_vars=['Country '], var_name='Year', value_name='GDP per Capita')

    fig = px.line(
        filtered_data,
        x='Year',
        y='GDP per Capita',
        color='Country ',
        labels={'GDP per Capita': 'GDP per Capita $'},
        color_discrete_sequence=colors
    )

    fig.update_traces(mode='lines+markers')
    fig.update_layout(
        margin=dict(l=0, r=20, t=20, b=0),
        yaxis=dict(title='GDP per Capita $'),
        legend_title='Country',
        showlegend=True
    )

    return fig


# Define the callback function to update the bar chart based on the selected countries and year
@app.callback(
    dash.dependencies.Output('bar-chart', 'figure'),
    [dash.dependencies.Input('country-dropdown-bar', 'value'),
     dash.dependencies.Input('year-dropdown-bar', 'value')]
)
def update_bar_chart(countries, year):
    colors = px.colors.qualitative.Set3  # Use the qualitative Set3 color palette

    filtered_data = data[data['Country '].isin(countries)]
    filtered_data = filtered_data.sort_values(year, ascending=False)

    fig = px.bar(
        filtered_data,
        x=year,
        y='Country ',
        orientation='h',
        color='Country ',
        color_discrete_sequence=colors[:len(countries)],
        text=filtered_data[year].apply(lambda x: f'${int(x):,d}'),  # Format the value with $ sign and no decimals,
        labels={year: 'GDP per Capita '},
        hover_name='Country ',
        hover_data={'Country ': True, year: False},  # Show only country name in hover data
    )
    fig.update_traces(hovertemplate='<b>%{hovertext}</b><br><br>GDP per Capita: $%{x:,d}')  # Update hover template
    fig.update_layout(
        title={
            'text': f'Selected {len(countries)} Countries in year {year}',
            'x': 0.5,  # Set x to 0.5 for center alignment
            'y': 0.95,  # Adjust y value for vertical alignment if needed
            'xanchor': 'center',
            'yanchor': 'top'
        },
        xaxis=dict(title='GDP per Capita'),
        yaxis=dict(title='Country'),
        margin=dict(l=50, r=50, t=70, b=50),
        showlegend=True
        
    )

    return fig

# Define the callback function to update the growth rate graph based on the selected countries
@app.callback(
    dash.dependencies.Output('growth-rate', 'figure'),
    [dash.dependencies.Input('country-dropdown-growth', 'value')]
)
def update_growth_rate(countries):
    colors = px.colors.qualitative.Set3  # Use the qualitative Set3 color palette

    filtered_data = data[data['Country '].isin(countries)].copy()
    filtered_data = filtered_data.melt(id_vars=['Country ', 'Country Code'], var_name='Year', value_name='GDP per Capita')
    filtered_data['Growth Rate'] = filtered_data.groupby('Country Code')['GDP per Capita'].pct_change() * 100

    fig = go.Figure()

    for country in countries:
        country_data = filtered_data[filtered_data['Country '] == country]
        fig.add_trace(go.Scatter(
            x=country_data['Year'],
            y=country_data['Growth Rate'],
            mode='lines+markers',
            line=dict(color=colors[countries.index(country)]),
            marker=dict(color=colors[countries.index(country)]),
            hovertemplate='Year: %{x}<br>Country: %{text}<br>Growth Rate: %{y:.2f}%',
            text=[country] * len(country_data),
            name=country
        ))

    fig.update_layout(
        
        xaxis=dict(title='Year'),
        yaxis=dict(title='Growth Rate (%)'),
        margin=dict(l=50, r=50, t=70, b=50),
        showlegend=True
    )

    return fig


if __name__ == '__main__':
    app.run_server(debug=True)