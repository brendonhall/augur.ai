from datetime import datetime
import pandas as pd

import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go

from io_helpers import sensors_explanation


esp_data_filename = 'esp.pkl'
data = pd.read_pickle(esp_data_filename)

levels = data.columns.levels
fields_to_choose = levels[0].values
pumps_to_choose = levels[1].values
sensors_to_choose = levels[2].values

app = dash.Dash()

app.layout = html.Div([
    html.Div([
        html.Label('Field #'),
        dcc.Dropdown(
            id='field-selected',
            options=[{'label': str(f), 'value': str(f)} for f in fields_to_choose],
            value=str(fields_to_choose[0]))
    ], style={'width': '49%', 'display': 'inline-block'}),

    html.Div([
        html.Label('Pump #'),
        dcc.Dropdown(
            id='pump-selected',
            options=[{'label': str(p), 'value': str(p)} for p in pumps_to_choose],
            value=str(pumps_to_choose[0]))
    ], style={'width': '49%', 'display': 'inline-block'}),

    html.Label('Sensor'),
    dcc.RadioItems(
        id='sensor-selected',
        options=[{'label': sensors_explanation[s], 'value': s} for s in sensors_to_choose],
        value=str(sensors_to_choose[0]),
        style={'columnCount': 5}
    ),

    dcc.Graph(id='sensor-readings')
])


@app.callback(
    dash.dependencies.Output('sensor-readings', 'figure'),
    [dash.dependencies.Input('field-selected', 'value'),
     dash.dependencies.Input('pump-selected', 'value'),
     dash.dependencies.Input('sensor-selected', 'value')])
def update_graph(field, pump, sensor):
    sensor_data = data[int(field), int(pump), sensor]
    times = sensor_data.index.values
    time_to_plot = [datetime.fromtimestamp(t) for t in times] #[(t - times[0])/60 for t in times]
    readings = sensor_data.values

    return {
        'data': [go.Scatter(
            x=time_to_plot,
            y=readings,
        )],
        'layout': go.Layout(
            xaxis={
                'title': 'Time since start [mins]',
                'type': 'time'
            },
            yaxis={
                'title': sensors_explanation[sensor],
                'type': 'linear' #if yaxis_type == 'Linear' else 'log'
            },
            margin={'l': 80, 'b': 40, 't': 10, 'r': 0},
            hovermode='closest'
        )
    }


app.css.append_css({
    "external_url": 'https://cdnjs.cloudflare.com/ajax/libs/skeleton-framework/1.1.1/skeleton.min.css'
})

if __name__ == '__main__':
    app.run_server(debug=True)
