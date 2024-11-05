# tabs/another_tab.py
from dash import html
from .base_tab import BaseTab

tab_id = 'another-tab'
tab_label = 'Another Tab'

def get_layout(sensors):
    layout = html.Div([
        html.H3('Content for Another Tab'),
        # Additional content can go here
    ])
    return layout
