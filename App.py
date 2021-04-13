import plotly.graph_objs as go
import pandas as pd
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc

# Data
df = pd.read_excel('Utilization 2021.xlsx')
df1 = df[df['Activity Description'] == 'Billable'].sort_values('Week', ascending=False)

# Dash Deployment
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.CYBORG])
server = app.server

app.layout = html.Div([
    dbc.Row(dbc.Col(html.H3("Trending Billable Hours (TTW)"),
                    width={'size': 6, 'offset': 5},
                    ),
            ),

    dbc.Row(dbc.Col(
        dcc.Dropdown(id="Select Group", options=[{'label': x, 'value': x} for x in sorted(df1['last name'].unique())],
                     multi=False,
                     value='Pratt',
                     style={'width': '40%'}))),

    dbc.Row(
        [
            dbc.Col(dcc.Graph(id='Utilization Graph 2', figure={}),
                    width=8, lg={'size': 6, "offset": 0, 'order': 'first'}
                    ),
            dbc.Col(dcc.Graph(id='Utilization Graph', figure={}),
                    width=4, lg={'size': 6, "offset": 0, 'order': 'last'}
                    ),
        ]
    )

])


@app.callback(
    [Output(component_id='Utilization Graph', component_property='figure'),
     Output(component_id='Utilization Graph 2', component_property='figure')],
    [Input(component_id='Select Group', component_property='value')])
def update_graph(employee_name_value):
    L1 = df1[df1['Employee Group'] == 'SUP'].groupby(['Week End']).sum().tail(12)
    L2 = df1[df1['Employee Group'] == 'MIX'].groupby(['Week End']).sum().tail(12)
    L3 = df1[df1['Employee Group'] == 'EDIT'].groupby(['Week End']).sum().tail(12)
    L4 = df1[df1['Employee Group'] == 'GRFX'].groupby(['Week End']).sum().tail(12)
    L5 = df1[df1['Employee Group'] == 'MCR'].groupby(['Week End']).sum().tail(12)

    Figl = go.Figure()
    Figl.add_trace(go.Scatter(x=L1.index, y=L1['tc unit'], mode='lines', name='SUP', connectgaps=True))
    Figl.add_trace(go.Scatter(x=L2.index, y=L2['tc unit'], mode='lines', name='MIX', connectgaps=True))
    Figl.add_trace(go.Scatter(x=L3.index, y=L3['tc unit'], mode='lines', name='EDIT', connectgaps=True))
    Figl.add_trace(go.Scatter(x=L4.index, y=L4['tc unit'], mode='lines', name='GRFX', connectgaps=True))
    Figl.add_trace(go.Scatter(x=L5.index, y=L5['tc unit'], mode='lines', name='MCR', connectgaps=True))

    Figl.update_layout(hovermode='x unified')
    Figl.update_layout(title='By Group', paper_bgcolor='lightsteelblue')
    Figl['layout']['xaxis']['autorange'] = "reversed"

    S1 = df1[df1['last name'] == employee_name_value].groupby(['Week End']).sum().tail(12)

    Figs = go.Figure()
    Figs.add_trace(go.Scatter(x=S1.index, y=S1['tc unit'], mode='lines', name=employee_name_value, connectgaps=True))

    Figs.update_layout(hovermode='x unified')
    Figs.update_layout(title='By Employee', paper_bgcolor='lightsteelblue')
    Figs['layout']['xaxis']['autorange'] = "reversed"

    return Figl, Figs


if __name__ == '__main__':
    app.run_server(debug=True)