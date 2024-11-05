# app.py
import dash
from sensors import load_sensors
from sensors.communication import PySerialCommunication  # or ZCMCommunication
from layout import create_layout
import callbacks  # Import callbacks to register them

# Initialize the Dash app
import dash_bootstrap_components as dbc
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server

# Initialize shared communication using dependency injection
communication = PySerialCommunication(
    port='/dev/ttyUSB0',  # Replace with your serial port
    baudrate=9600,
    timeout=1
)

# Load sensors with shared communication
sensors = load_sensors(communication)
sensor_dict = {sensor.name: sensor for sensor in sensors}

# Set up the layout
app.layout = create_layout(sensors)

# Register callbacks
callbacks.register_callbacks(app, sensors, sensor_dict)

if __name__ == '__main__':
    app.run_server(debug=True)
