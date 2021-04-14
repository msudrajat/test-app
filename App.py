import plotly.graph_objs as go
import plotly.express as px
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
Server = app.server

app.layout = html.Div([
    dbc.Row(dbc.Col(html.H3("Billable Hours"),
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
    ),
    dbc.Row(
        [
            dbc.Col(dcc.Graph(id='Sunburst 2', figure={}),
                    width=8, lg={'size': 6, "offset": 0, 'order': 'first'}
                    ),
            dbc.Col(dcc.Graph(id='Sunburst', figure={}),
                    width=4, lg={'size': 6, "offset": 0, 'order': 'last'}
                    ),
        ]
    )

])


@app.callback(
    [Output(component_id='Utilization Graph', component_property='figure'),
     Output(component_id='Utilization Graph 2', component_property='figure'),
     Output(component_id='Sunburst', component_property='figure'),
     Output(component_id='Sunburst 2', component_property='figure')],
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
    Figl.update_layout(title='Trending Billable By Group (TTW)', paper_bgcolor='lightsteelblue')
    Figl['layout']['xaxis']['autorange'] = "reversed"

    S1 = df1[df1['last name'] == employee_name_value].groupby(['Week End']).sum().tail(12)
    DFS = df1[df1['last name'] == employee_name_value]

    Figs = go.Figure()
    Figs.add_trace(go.Scatter(x=S1.index, y=S1['tc unit'], mode='lines', name=employee_name_value, connectgaps=True))

    Figs.update_layout(hovermode='x unified')
    Figs.update_layout(title='Trending Billable By Employee (TTW)', paper_bgcolor='lightsteelblue')
    Figs['layout']['xaxis']['autorange'] = "reversed"

    Figb = px.sunburst(df1, path=['Day', 'Employee Group'], values='tc unit',
                       color='Day')
    Figb.update_layout(title='Group Billable Hours Breakdown by Day', paper_bgcolor='lightsteelblue')

    Figa = px.sunburst(DFS, path=['Day'], values='tc unit',
                       color='Day')
    Figa.update_layout(title='Employee Billable Hours Breakdown by Day', paper_bgcolor='lightsteelblue')

    return Figl, Figs, Figb, Figa


if __name__ == '__main__':
    app.run_server(debug=True)
