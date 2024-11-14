# tabs/sensor_tab/sensor_cards/accelerometersensor_card.py
from .base_sensor_card import BaseSensorCard
from ..data_handlers.base_data_handler import BaseSensorDataHandler
from dash import html, dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State, MATCH
import plotly.graph_objects as go
import pandas as pd
from datetime import datetime, timedelta
import importlib

class AccelerometerSensorCard(BaseSensorCard):
    def __init__(self, app, sensor_name, sensor):
        super().__init__(app, sensor_name, sensor)