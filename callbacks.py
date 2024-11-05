# callbacks.py
from dash.dependencies import Input, Output, State, MATCH, ALL
from dash import html, dcc
import plotly.graph_objects as go
from tabs import get_tab_modules

def register_callbacks(app, sensors, sensor_dict):
    # Get the list of tab modules
    tab_modules = get_tab_modules()
    tab_module_dict = {module.tab_id: module for module in tab_modules}

    # Callback to render tab content
    @app.callback(
        Output('tabs-content', 'children'),
        [Input('tabs', 'value')]
    )
    def render_content(tab_id):
        if tab_id in tab_module_dict:
            return tab_module_dict[tab_id].get_layout(sensors)
        else:
            return html.Div([
                html.H3('Tab content not found')
            ])

    # Sensor tab callbacks
    if 'sensor-tab' in tab_module_dict:
        sensor_tab_module = tab_module_dict['sensor-tab']

        # Callback to update the sensor content when the interval fires
        @app.callback(
            Output({'type': 'sensor-content', 'sensor_name': MATCH}, 'children'),
            [Input({'type': 'sensor-interval', 'sensor_name': MATCH}, 'n_intervals')],
            [State({'type': 'sensor-content', 'sensor_name': MATCH}, 'id')]
        )
        def update_sensor_content(n_intervals, content_id):
            sensor_name = content_id['sensor_name']
            sensor = sensor_dict[sensor_name]
            df = sensor.get_data()
            current_values = {}
            graphs = []
            # Create graphs regardless of whether df is empty
            for field in sensor.data_fields:
                fig = go.Figure()
                if not df.empty:
                    fig.add_trace(go.Scatter(
                        x=df['Time'],
                        y=df[field],
                        mode='lines',
                        name=field
                    ))
                else:
                    # Create an empty figure with layout
                    fig.add_trace(go.Scatter(
                        x=[],
                        y=[],
                        mode='lines',
                        name=field
                    ))
                # Capitalize the first letter of the field name in titles and labels
                field_capitalized = field.capitalize()
                # Replace "Over" with "/" in the graph titles
                fig.update_layout(
                    title=f'{field_capitalized}/Time',
                    xaxis_title='Time',
                    yaxis_title=field_capitalized,
                    margin=dict(l=20, r=20, t=40, b=20)
                )
                graphs.append(dcc.Graph(figure=fig, id=f'{sensor_name}-{field}-graph'))

            # Get the latest values if available
            if not df.empty:
                latest_data = df.iloc[-1]
                for field in sensor.data_fields:
                    current_values[field] = latest_data[field]
            else:
                for field in sensor.data_fields:
                    current_values[field] = 'N/A'

            # Create current values display with capitalized field names
            current_values_display = html.Div([
                html.H6('Current Values:'),
                html.Ul([html.Li(f'{field.capitalize()}: {value}') for field, value in current_values.items()])
            ])

            # Return the updated content
            return [current_values_display, html.Div(graphs)]

        # Callback to update the interval when the user adjusts the interval control
        @app.callback(
            Output({'type': 'sensor-interval', 'sensor_name': MATCH}, 'interval'),
            [Input({'type': 'interval-control', 'sensor_name': MATCH}, 'value')]
        )
        def update_interval(value):
            try:
                interval_ms = max(1, int(value)) * 1000  # Convert to milliseconds
            except (ValueError, TypeError):
                interval_ms = 5000  # Default to 5 seconds if invalid input
            return interval_ms

    # Optional: Callback for the Emergency button
    @app.callback(
        Output('emergency-button', 'children'),
        [Input('emergency-button', 'n_clicks')]
    )
    def handle_emergency(n_clicks):
        if n_clicks:
            # Placeholder for emergency action
            print("Emergency button clicked!")
            # You can implement any emergency procedures here
            return "Emergency Activated"
        else:
            return "Emergency"
