import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import serial

# Set up the Arduino serial connection
arduino_port = '/dev/cu.usbmodem101'
baud_rate = 9600
ser = None

# Try to initialize the serial connection only once
try:
    ser = serial.Serial(arduino_port, baud_rate)
    print("Connection to Arduino successful")
except serial.SerialException as e:
    print(f"Failed to connect: {e}")
    ser = None  # If connection fails, ser remains None and won't be used in the callback

# Initialize Dash app
app = dash.Dash(__name__)

# Initialize acceleration data dictionary
acceleration_data = {
    'x': [],
    'y': [],
    'z': []
}

# App layout
app.layout = html.Div([
    dcc.Graph(id='live-graph', style={'width': '70%', 'display': 'inline-block'}),
    dcc.Interval(id='graph-update', interval=500, n_intervals=100),  # Update every second
])

# Define the callback to update the graph live
@app.callback(
    Output('live-graph', 'figure'),
    [Input('graph-update', 'n_intervals')]
)
def update_graph(n):
    # Only proceed if the serial connection was established successfully
    if ser and ser.in_waiting > 0:
        try:
            # Read data from Arduino
            arduino_data = ser.readline().decode('utf-8').strip()
            # Parse the incoming serial data (assuming comma-separated X, Y, Z values)
            
            arduino_data = arduino_data.replace('Distance: ', '')

            x = arduino_data
            acceleration_data['x'].append(x)
        except (ValueError, serial.SerialException) as e:
            print(f"Data parsing error: {e}")  # Print an error if parsing fails

    # Create a line plot for acceleration X, Y, Z axes
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=list(range(len(acceleration_data['x']))),
        y=acceleration_data['x'],
        mode='lines+markers',
        name='Acceleration X'
    ))

    # Update figure layout
    fig.update_layout(
        title='Live Accelerometer Data from Arduino',
        xaxis_title='Time',
        yaxis_title='Acceleration (m/s²)',
        showlegend=True
    )
    return fig

# Run the app and ensure serial connection is closed on exit
if __name__ == '__main__':
    try:
        app.run_server(debug=True)
    finally:
        if ser and ser.is_open:
            ser.close()
            print("Serial connection closed")