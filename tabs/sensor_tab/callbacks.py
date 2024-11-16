# tabs/sensor_tab/callbacks.py
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
from .components import create_sensor_card
import dash_bootstrap_components as dbc

def register_callbacks(app, sensors):
    """
    Register sensor-specific callbacks.

    Parameters:
    - app: The Dash app instance.
    - sensors: List of sensor objects.
    """
    sensor_dict = {sensor.name: sensor for sensor in sensors}

    # Callback to generate sensor cards based on selected sensors
    @app.callback(
        Output('sensor-cards', 'children'),
        [Input('sensor-dropdown', 'value')]
    )
    def update_sensor_cards(selected_sensor_names):
        """
        Update the displayed sensor cards based on user selection.

        Parameters:
        - selected_sensor_names: List of sensor names selected by the user.

        Returns:
        - A list of dbc.Col components containing sensor cards.
        """
        cards = []
        if not selected_sensor_names:
            return cards  # Return empty if no sensors are selected
        for sensor_name in selected_sensor_names:
            sensor = sensor_dict[sensor_name]
            card = create_sensor_card(app, sensor_name, sensor)
            cards.append(
                dbc.Col(card, width=12, lg=6)
            )
        return cards

    @app.callback(
        Output('callback-store', 'data'),
        Input('data', 'modified_timestamp'),
        State('sensor-cards', 'children'),
        State('callback-store', 'data')
    )
    def register_sensor_cards_callbacks(mod, sensor_cards, data):
        """
        Register sensor-specific callbacks for all sensor cards.
        """
        if not data['sensor-tab']:
            data['sensor-tab'] = {}
            data['sensor-tab']['sensor-cards'] = False
        
        if data['sensor-tab']['sensor-cards']:
            raise PreventUpdate
        else:
            data['sensor-tab']['sensor-cards'] = True
            for card in sensor_cards:
                card.register_callbacks()
        
        return data