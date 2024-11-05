# tabs/sensor_tab.py
import dash_bootstrap_components as dbc
from dash import html
from components import create_sensor_card
from .base_tab import BaseTab

tab_id = 'sensor-tab'
tab_label = 'Sensors'

def get_layout(sensors):
    sensor_cards = []
    for sensor in sensors:
        card = create_sensor_card(sensor.name, sensor)
        sensor_cards.append(
            dbc.Col(card, width=12, lg=6)
        )
    layout = dbc.Row(
        id='sensor-cards',
        children=sensor_cards
    )
    return layout
