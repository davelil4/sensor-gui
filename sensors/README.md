# **Sensors Module README**

Welcome to the **Sensors Module** of the **Sensor Dashboard Application**! This module is responsible for managing sensor interactions, including communication, data retrieval, and sensor initialization. It provides a structured way to integrate various sensors into the application, ensuring scalability and maintainability.

---

## **Table of Contents**

- [Overview](#overview)
- [Module Structure](#module-structure)
- [Communication Classes](#communication-classes)
  - [PySerial Communication](#pyserial-communication)
    - [Installation](#installation)
    - [Usage](#usage)
    - [Configuring Serial Communication](#configuring-serial-communication)
    - [Example: Reading Data from Arduino](#example-reading-data-from-arduino)
  - [Arduino Data Format](#arduino-data-format)
    - [Expected Data Format](#expected-data-format)
    - [Sample Arduino Code](#sample-arduino-code)
- [Creating a New Sensor](#creating-a-new-sensor)
  - [1. Create Sensor Class](#1-create-sensor-class)
  - [2. Update `load_sensors` Function](#2-update-load_sensors-function)
- [Sensor Class Guidelines](#sensor-class-guidelines)
- [Example: Multiple Sensors with Multiple Values](#example-multiple-sensors-with-multiple-values)
- [Best Practices](#best-practices)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [License](#license)

---

## **Overview**

The **Sensors Module** is designed to:

- **Facilitate Sensor Integration**: Provide a standardized way to add new sensors.
- **Manage Communication**: Handle communication protocols (e.g., serial communication with Arduino).
- **Support Data Retrieval**: Define methods for fetching sensor data.
- **Promote Modularity**: Allow sensors to be added or removed without affecting other parts of the application.

---

## **Module Structure**

```
sensor_dashboard/
├── sensors/
    ├── __init__.py
    ├── communication.py
    ├── load_sensors.py
    ├── base_sensor.py
    ├── temperature_sensor.py
    ├── accelerometer_sensor.py
    └── ... (other sensor classes)
```

- **`communication.py`**: Defines communication classes used by sensors.
- **`load_sensors.py`**: Contains the `load_sensors` function to initialize all sensors.
- **`base_sensor.py`**: Provides a base class for sensors to inherit common functionality.
- **`<sensor_name>_sensor.py`**: Individual sensor classes implementing specific sensor logic.

---

## **Communication Classes**

The module includes communication classes to abstract the details of how sensors communicate with the application.

### **PySerial Communication**

**PySerial** is a Python library that encapsulates the access for the serial port. It provides backends for Python running on Windows, Linux, and other platforms.

#### **Installation**

To use PySerial, you need to install it using pip:

```bash
pip install pyserial
```

#### **Usage**

**File**: `sensors/communication.py`

```python
import serial

class PySerialCommunication:
    def __init__(self, port, baudrate=9600, timeout=1):
        """
        Initialize serial communication.

        Parameters:
        - port (str): Serial port name (e.g., '/dev/ttyUSB0' on Linux or 'COM3' on Windows).
        - baudrate (int): Communication speed.
        - timeout (float): Read timeout in seconds.
        """
        self.port = port
        self.baudrate = baudrate
        self.timeout = timeout
        try:
            self.serial_connection = serial.Serial(port=self.port, baudrate=self.baudrate, timeout=self.timeout)
            print(f"Connected to serial port {self.port}")
        except serial.SerialException as e:
            print(f"Error connecting to serial port {self.port}: {e}")
            self.serial_connection = None

    def read_line(self):
        """
        Read a line from the serial port.

        Returns:
        - str: Decoded line from the serial port.
        """
        if self.serial_connection and self.serial_connection.in_waiting:
            line = self.serial_connection.readline()
            return line.decode('utf-8').strip()
        return None

    def write(self, data):
        """
        Write data to the serial port.

        Parameters:
        - data (str): Data to send.
        """
        if self.serial_connection:
            self.serial_connection.write(data.encode('utf-8'))
```

#### **Configuring Serial Communication**

When initializing `PySerialCommunication`, you need to provide the correct serial port and parameters.

**Example Initialization in `app.py`:**

```python
# app.py
from sensors.communication import PySerialCommunication

# Initialize shared communication using dependency injection
communication = PySerialCommunication(
    port='/dev/ttyUSB0',  # Replace with your serial port (e.g., 'COM3' on Windows)
    baudrate=9600,        # Ensure this matches the Arduino's baud rate
    timeout=1
)
```

**Determining the Serial Port:**

- **Linux/Mac**: Serial ports are usually named `/dev/ttyUSB0`, `/dev/ttyACM0`, etc.
- **Windows**: Serial ports are named `COM1`, `COM2`, etc.

#### **Example: Reading Data from Arduino**

In your sensor class, you can use the `read_line` method to get data from the Arduino.

```python
# sensors/your_sensor.py

from .base_sensor import BaseSensor
from datetime import datetime

class YourSensor(BaseSensor):
    def __init__(self, communication):
        super().__init__(communication)
        self.name = "Your Sensor Name"
        self.data_fields = ['Field1', 'Field2']

    def get_data(self):
        line = self.communication.read_line()
        if line:
            data = self.parse_data(line)
            if data:
                data['Time'] = datetime.now()
                return data
        return None

    def parse_data(self, line):
        # Implement parsing logic based on the expected data format
        pass
```

---

## **Arduino Data Format**

To ensure proper communication between the Arduino and the application, the data sent from the Arduino must be in a format that the Python application can parse. When dealing with **multiple sensors**, each potentially providing **multiple values**, it's essential to design a data format that is both comprehensive and parsable.

### **Expected Data Format**

The data format should be:

- **Structured**: Clearly indicate which data belongs to which sensor and field.
- **Parsable**: Use a format that's easy to parse in Python (e.g., JSON, custom delimiter-separated values).
- **Consistent**: Each data message follows the same structure.

**Recommended Format**: **JSON Lines** (each line is a JSON object)

**Example Data Line:**

```json
{"SensorName": "TemperatureSensor", "Fields": {"Temperature": 25.0}}
{"SensorName": "AccelerometerSensor", "Fields": {"X": 0.02, "Y": -0.01, "Z": 9.81}}
```

This format allows you to:

- Easily parse each line as a JSON object.
- Include multiple sensors and multiple fields per sensor.
- Extend the data format without breaking existing parsers.

### **Sample Arduino Code**

Below is an example Arduino sketch that sends data in JSON format over serial for multiple sensors with multiple values.

**Arduino Sketch:**

```cpp
// Arduino Sketch

#include <ArduinoJson.h> // Install ArduinoJson library

void setup() {
  Serial.begin(9600); // Set the baud rate to match PySerialCommunication
}

void loop() {
  // Create a JSON document
  StaticJsonDocument<200> doc;

  // Temperature Sensor Data
  float temperature = readTemperatureSensor();
  doc["SensorName"] = "TemperatureSensor";
  JsonObject fields = doc.createNestedObject("Fields");
  fields["Temperature"] = temperature;

  // Serialize JSON to string
  String output;
  serializeJson(doc, output);

  // Send data over serial
  Serial.println(output);

  delay(1000); // Send data every second

  // Clear the JSON document for the next sensor
  doc.clear();

  // Accelerometer Sensor Data
  float accX = readAccelerometerX();
  float accY = readAccelerometerY();
  float accZ = readAccelerometerZ();
  doc["SensorName"] = "AccelerometerSensor";
  fields = doc.createNestedObject("Fields");
  fields["X"] = accX;
  fields["Y"] = accY;
  fields["Z"] = accZ;

  // Serialize and send
  serializeJson(doc, output);
  Serial.println(output);

  delay(1000); // Adjust delay as needed
}

float readTemperatureSensor() {
  // Replace with actual sensor reading code
  return 25.0; // Placeholder value
}

float readAccelerometerX() {
  // Replace with actual sensor reading code
  return 0.02; // Placeholder value
}

float readAccelerometerY() {
  // Replace with actual sensor reading code
  return -0.01; // Placeholder value
}

float readAccelerometerZ() {
  // Replace with actual sensor reading code
  return 9.81; // Placeholder value
}
```

**Notes:**

- The Arduino sends data as JSON strings, one line per sensor data reading.
- The JSON object contains:
  - `"SensorName"`: Name of the sensor.
  - `"Fields"`: An object containing key-value pairs for each field.

**ArduinoJson Library:**

- Install the ArduinoJson library via the Library Manager in the Arduino IDE.
- It's efficient and suitable for embedded devices.

---

## **Creating a New Sensor**

To add a new sensor to the application, follow these steps:

### **1. Create Sensor Class**

Create a new sensor class in the `sensors/` directory, following the naming convention `<sensor_name>_sensor.py`.

**Example**: `sensors/your_sensor.py`

```python
# sensors/your_sensor.py

from .base_sensor import BaseSensor
from datetime import datetime
import json

class YourSensor(BaseSensor):
    def __init__(self, communication):
        super().__init__(communication)
        self.name = "YourSensor"
        self.data_fields = ['Field1', 'Field2']

    def get_data(self):
        while True:
            line = self.communication.read_line()
            if line:
                data = self.parse_data(line)
                if data and data.get('SensorName') == self.name:
                    fields = data.get('Fields', {})
                    fields['Time'] = datetime.now()
                    return fields
        return None

    def parse_data(self, line):
        try:
            data = json.loads(line)
            return data
        except json.JSONDecodeError as e:
            print(f"Error parsing JSON '{line}': {e}")
            return None
```

### **2. Update `load_sensors` Function**

Add your new sensor class to the list of sensors in `load_sensors.py`.

```python
# sensors/load_sensors.py

from .your_sensor import YourSensor
from .temperature_sensor import TemperatureSensor
from .accelerometer_sensor import AccelerometerSensor

def load_sensors(communication):
    sensors = [
        TemperatureSensor(communication),
        AccelerometerSensor(communication),
        YourSensor(communication),
        # ... other sensors
    ]
    return sensors
```

---

## **Sensor Class Guidelines**

When creating a sensor class, adhere to the following guidelines:

- **Inherit from `BaseSensor`**: This ensures consistency and allows you to leverage common functionality.
- **Define `self.name`**: A unique name for the sensor, matching the `"SensorName"` in the Arduino data.
- **Define `self.data_fields`**: A list of data fields the sensor provides (excluding 'Time').
- **Implement `get_data` Method**:

  - Continuously read lines until the line corresponding to the sensor is found.
  - Return a dictionary containing the sensor data, including a 'Time' field with a timestamp.
  - Keys should match `self.data_fields`.

- **Implement `parse_data` Method**:

  - Parse the JSON string received from the serial port into a dictionary.

- **Handle Exceptions**: Ensure that any communication errors are handled gracefully.

**Example**:

```python
# sensors/base_sensor.py

class BaseSensor:
    def __init__(self, communication):
        self.communication = communication

    def get_data(self):
        raise NotImplementedError("get_data method must be implemented by subclasses.")
```

---

## **Example: Multiple Sensors with Multiple Values**

**Arduino Sketch (Sending Data for Multiple Sensors):**

```cpp
// Arduino Sketch for Multiple Sensors

#include <ArduinoJson.h>

void setup() {
  Serial.begin(9600);
}

void loop() {
  StaticJsonDocument<200> doc;

  // Temperature Sensor Data
  float temperature = readTemperatureSensor();
  doc["SensorName"] = "TemperatureSensor";
  JsonObject fields = doc.createNestedObject("Fields");
  fields["Temperature"] = temperature;
  String output;
  serializeJson(doc, output);
  Serial.println(output);
  doc.clear();

  // Accelerometer Sensor Data
  float accX = readAccelerometerX();
  float accY = readAccelerometerY();
  float accZ = readAccelerometerZ();
  doc["SensorName"] = "AccelerometerSensor";
  fields = doc.createNestedObject("Fields");
  fields["X"] = accX;
  fields["Y"] = accY;
  fields["Z"] = accZ;
  serializeJson(doc, output);
  Serial.println(output);
  doc.clear();

  delay(1000);
}

// Sensor reading functions...
```

**Python Sensor Classes:**

- **Temperature Sensor**

  ```python
  # sensors/temperature_sensor.py

  from .base_sensor import BaseSensor
  from datetime import datetime
  import json

  class TemperatureSensor(BaseSensor):
      def __init__(self, communication):
          super().__init__(communication)
          self.name = "TemperatureSensor"
          self.data_fields = ['Temperature']

      def get_data(self):
          while True:
              line = self.communication.read_line()
              if line:
                  data = self.parse_data(line)
                  if data and data.get('SensorName') == self.name:
                      fields = data.get('Fields', {})
                      fields['Time'] = datetime.now()
                      return fields
          return None

      def parse_data(self, line):
          try:
              data = json.loads(line)
              return data
          except json.JSONDecodeError as e:
              print(f"Error parsing JSON '{line}': {e}")
              return None
  ```

- **Accelerometer Sensor**

  ```python
  # sensors/accelerometer_sensor.py

  from .base_sensor import BaseSensor
  from datetime import datetime
  import json

  class AccelerometerSensor(BaseSensor):
      def __init__(self, communication):
          super().__init__(communication)
          self.name = "AccelerometerSensor"
          self.data_fields = ['X', 'Y', 'Z']

      def get_data(self):
          while True:
              line = self.communication.read_line()
              if line:
                  data = self.parse_data(line)
                  if data and data.get('SensorName') == self.name:
                      fields = data.get('Fields', {})
                      fields['Time'] = datetime.now()
                      return fields
          return None

      def parse_data(self, line):
          try:
              data = json.loads(line)
              return data
          except json.JSONDecodeError as e:
              print(f"Error parsing JSON '{line}': {e}")
              return None
  ```

**Explanation:**

- **Continuous Reading**: The `get_data` method loops continuously, reading lines from the serial port until it finds data corresponding to the sensor's `name`.
- **Data Parsing**: The `parse_data` method uses `json.loads` to parse each line into a Python dictionary.
- **Matching Sensor Data**: Only the data where `'SensorName'` matches the sensor's `self.name` is processed.

---

## **Best Practices**

- **Consistent Data Format**: Use a structured data format like JSON to encapsulate sensor data.
- **Unique Sensor Names**: Ensure each sensor has a unique `SensorName` in the data and matches `self.name` in the sensor class.
- **Efficient Parsing**: Use efficient parsing methods (`json.loads`) and avoid blocking the serial port.
- **Error Handling**: Implement robust error handling for data parsing and communication errors.
- **Resource Management**: Close serial connections properly when the application exits.

---

## **Troubleshooting**

### **No Data Received from Arduino**

- **Check Serial Port**: Verify the correct serial port is used.
- **Baud Rate Mismatch**: Ensure baud rates match between Arduino and PySerial.
- **Arduino Not Sending Data**: Confirm that the Arduino is powered and running the correct sketch.
- **Permissions**: On Unix systems, you may need to add your user to the `dialout` group or run the application with elevated permissions.

### **Data Parsing Errors**

- **Incorrect Data Format**: Ensure the data sent from the Arduino matches the expected JSON format.
- **Error Messages**: Review any error messages printed during parsing to identify issues.
- **Incomplete Data**: Check if data lines are incomplete or truncated due to serial communication issues.

### **Serial Connection Errors**

- **Port Already in Use**: Close other programs that might be using the serial port (e.g., Arduino IDE Serial Monitor).
- **SerialException**: Check for exceptions when initializing `PySerialCommunication`.

---

## **Contributing**

Contributions to the Sensors Module are welcome! Please ensure that any additions adhere to the project's modular design principles.

### **Steps to Contribute**

1. **Fork the Repository**

   ```bash
   git clone https://github.com/yourusername/sensor_dashboard.git
   ```

2. **Create a Feature Branch**

   ```bash
   git checkout -b feature/your-feature
   ```

3. **Make Changes and Commit**

   ```bash
   git add .
   git commit -m "Add your feature"
   ```

4. **Push to Your Fork and Submit a Pull Request**

   ```bash
   git push origin feature/your-feature
   ```

---

## **License**

This project is licensed under the MIT License.

---

Thank you for using and contributing to the **Sensor Dashboard Application**! If you have any questions or need further assistance with the Sensors Module, please feel free to reach out.

---

**Note**: When adding new sensors, consider whether you also need to create a corresponding **Data Handler** in `tabs/sensor_tab/data_handlers/` to process and format the sensor data for display. This ensures consistency in how data is presented in the dashboard.

---