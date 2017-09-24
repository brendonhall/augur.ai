from datetime import datetime
import pandas as pd
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
from plotly import tools

from io_helpers import sensors_explanation, H5_File


h5_file = H5_File('esp_data_interp.h5')
data_description = h5_file.data_description()

fields_to_choose = sorted(data_description.keys(), key=lambda x: int(x))

app = dash.Dash()

current_selection = {'field': None,
                     'pump': None}

app.layout = html.Div([
    html.Div([
        html.Label('Field #'),
        dcc.Dropdown(
            id='field-selected',
            options=[{'label': f, 'value': f} for f in fields_to_choose],
            value=None
        )
    ], style={'width': '49%', 'display': 'inline-block'}),

    html.Div([
        html.Label('Pump #'),
        dcc.Dropdown(id='pump-selected')
    ], style={'width': '49%', 'display': 'inline-block'}),

    html.Label('Sensors'),
    dcc.Checklist(
        id='sensor-selected',
        options=[],
        values=[],
        style={'columnCount': 5}
    ),

    dcc.Graph(id='sensor-readings')
])

@app.callback(
    dash.dependencies.Output('pump-selected', 'options'),
    [dash.dependencies.Input('field-selected', 'value')]
)
def set_pump_options(field):
    if field is None:
        return []
    current_selection['field'] = field
    options = [{'label': i, 'value': i} for i in sorted(data_description[field].keys(),
                                                        key=lambda x: int(x))]
    print(options)
    return options


@app.callback(
    dash.dependencies.Output('pump-selected', 'value'),
    [dash.dependencies.Input('pump-selected', 'options')]
)
def set_pump_value(available_options):
    if not available_options:
        return None
    return available_options[0]['value']


@app.callback(
    dash.dependencies.Output('sensor-selected', 'options'),
    [dash.dependencies.Input('pump-selected', 'value')]
)
def set_sensor_options(pump):
    field = current_selection['field']
    if field is None or pump is None:
        return []
    current_selection['pump'] = pump
    options = set(data_description[field][pump]) - set(['TCPU', 'PLIN', 'TVFD1', 'EINPA', 'JOUT', 'YSD', 'KRUNRSAC', 'EVFD1OUT'])
    return [{'label': sensors_explanation[i], 'value': i} for i in options]


@app.callback(
    dash.dependencies.Output('sensor-selected', 'values'),
    [dash.dependencies.Input('sensor-selected', 'options')]
)
def set_sensor_values(available_options):
    return []


@app.callback(
    dash.dependencies.Output('sensor-readings', 'figure'),
    [dash.dependencies.Input('sensor-selected', 'values')])
def update_graphs(sensors):
    field = current_selection['field']
    pump = current_selection['pump']
    if field is None or pump is None or not sensors:
        return {}

    sensor_data = h5_file.query(field, pump, sensors[0]).value
    fig = tools.make_subplots(rows=len(sensors), cols=1,
                              subplot_titles=tuple(s for s in sensors),
                              shared_xaxes=True, shared_yaxes=False,
                              vertical_spacing=0.2)

    for i, sensor in enumerate(sensors):
        sensor_data = h5_file.query(field, pump, sensor).value
        s_data = go.Scatter(
            x=sensor_data[0,:],
            y=sensor_data[1,:],
            name=sensors_explanation[sensor],
        )
        fig.append_trace(s_data, i+1, 1)

    fig['layout'].update(height=800)
    return fig


app.css.append_css({
   "external_url": 'https://cdnjs.cloudflare.com/ajax/libs/skeleton-framework/1.1.1/skeleton.min.css'
})

if __name__ == '__main__':
    app.run_server(debug=True, host='0.0.0.0')
