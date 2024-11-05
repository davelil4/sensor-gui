# Sensor Dashboard

A Plotly Dash GUI for visualizing data from Arduino-connected sensors using `pyserial` or ZCM protocols. This dashboard supports sensors that return multiple values per reading, like accelerometers.

## Features

- **Dependency Injection for Communication Protocols**: Inject specific communication class instances (`PySerialCommunication` or `ZCMCommunication`) directly.
- **Structured Message Format**: Arduino sends messages with sensor identifiers and multiple data values.
- **Supports Multiple Data Fields**: Sensors can handle multiple values per reading.
- **Callback Mechanism**: Communication interface dispatches messages to the appropriate sensors.
- **Dynamic Sensor Loading**: Sensors are automatically detected from the `sensors/` directory.
- **Modular Design**: Add new sensors by simply adding new Python modules.
- **Offline Functionality**: Works entirely offline after installation.
- **Bootstrap Styling**: Clean and responsive UI using Dash Bootstrap Components.

## Prerequisites

- Python 3.7 or higher
- Virtual environment (optional but recommended)
- `pyserial` package (for serial communication)
- ZCM library (for ZCM communication)

## Installation

1. **Clone the Repository**

```bash
git clone https://github.com/your_username/your_project.git
cd your_project
```
2. **Create a Virtual Environment**

```bash
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```

3. **Install Dependencies**

```bash
pip install -r requirements.txt
```

## Usage

1. **Connect Your Sensors**
* Ensure your Arduino sensors are connected to your computer via serial ports or are accessible via ZCM.

2. **Configure Arduino Code**
* Format the messages sent from the Arduino to include sensor identifiers and multiple data values separated by commas.

3. **Configure Communication Protocol in** `app.py`
* Import the specific communication class you want to use (`PySerialCommunication` or `ZCMCommunication`).
* Instantiate the communication object and pass it to `load_sensors`.
Example:
```python
from sensors.communication import PySerialCommunication  # or ZCMCommunication

# For pyserial
communication = PySerialCommunication(
    port='/dev/ttyUSB0',
    baudrate=9600,
    timeout=1
)

# For ZCM
# communication = ZCMCommunication(
#     url='udpm://239.255.76.67:7667?ttl=1',
#     channels=['ACCEL_SENSOR', 'TEMP_SENSOR']
# )
```

4. **Run the Application**
```bash
python app.py
```

5. **Open in Browser**

Navigate to http://127.0.0.1:8050/ in your web browser.

6. **Select a Sensor**

Use the dropdown menu to select a sensor and view its data.

## Adding New Sensors
To add a new sensor to the dashboard:

1. **Create a New Sensor Module**
In the `sensors/` directory, create a new file named `your_sensor_name_sensor.py`.

2. **Implement the Sensor Class**
    * Import `BaseSensor` from `base_sensor.py`.
    * Define a `Sensor` class that inherits from `BaseSensor`.
    Example:
    ```python
    from .base_sensor import BaseSensor

    class Sensor(BaseSensor):
        def __init__(self, communication):
            super().__init__(
                name='Your Sensor Name',
                communication=communication,
                sensor_id='YOUR_SENSOR_ID',
                data_fields=['field1', 'field2', 'field3']  # Define your data fields
            )
    ```
3. **Update the Arduino Code**
* Ensure the Arduino code sends messages with the new sensor identifier and data values.
    ```cpp
    Serial.print("YOUR_SENSOR_ID:");
    Serial.print(value1);
    Serial.print(",");
    Serial.print(value2);
    Serial.print(",");
    Serial.println(value3);
    ```
4. **Restart the Application**
* Save your changes and restart the Dash app.
* The new sensor will automatically appear in the dropdown menu.

## Notes
* **Dependency Injection**: The specific communication protocol is selected by injecting the appropriate communication class instance.
* **Shared Communication**: If multiple sensors use the same communication channel, use a shared communication instance to prevent conflicts.
* **Message Format**: Ensure that messages from the Arduino follow the agreed-upon format to allow correct parsing.
* **Data Fields**: Define the data fields in each sensor module to match the values sent from the Arduino.
* **Error Handling**: Add error handling in your communication and sensor classes to manage exceptions and ensure robustness.
* **Naming Convention**: Sensor module files should end with _sensor.py to be automatically detected.
Customization: Modify the UI and styling in app.py to suit your preferences.