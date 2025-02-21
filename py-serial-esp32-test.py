import serial
import json
import time
import os

# Function to dynamically find the ESP32 serial port (scans ttyUSB* and ttyACM*)
def find_esp32_serial_port():
    # Check connected USB devices
    devices = os.popen('ls /dev/tty*').readlines()
    
    # Filter for USB devices (these will usually be in /dev/ttyUSB* or /dev/ttyACM*)
    esp32_ports = [device.strip() for device in devices if 'ttyUSB' in device or 'ttyACM' in device]
    
    if esp32_ports:
        return esp32_ports[0]  # Return the first found ESP32 serial port
    else:
        return None

# Function to initialize serial connection
def initialize_serial_connection():
    while True:
        serial_port = find_esp32_serial_port()
        if serial_port is not None:
            print(f"Found ESP32 at: {serial_port}")
            try:
                ser = serial.Serial(serial_port, baudrate=115200, timeout=1)
                if ser.is_open:
                    return ser
                else:
                    print(f"Failed to open serial port {serial_port}. Retrying...")
                    time.sleep(2)  # Retry after 2 seconds
            except serial.SerialException:
                print(f"Failed to connect to {serial_port}. Retrying...")
                time.sleep(2)  # Retry after 2 seconds
        else:
            print("ESP32 not found. Retrying in 2 seconds...")
            time.sleep(2)  # Retry after 2 seconds

# Initialize serial connection
ser = None
while ser is None:
    ser = initialize_serial_connection()

# Main loop to keep reading serial data and process the JSON object
while True:
    try:
        # Attempt to check for data to read from serial
        if ser.in_waiting > 0:
            try:
                # Read the line and strip any extra whitespace, handle potential UnicodeDecodeError
                line = ser.readline().decode('utf-8', errors='ignore').strip()
                
                # Skip empty lines
                if not line:
                    continue

                # Parse the JSON string
                data = json.loads(line)

                # Extract values from JSON object
                device = data.get('device', 'Unknown')
                status = data.get('status', 'Unknown')
                temperature = data.get('temperature', 'Unknown')

                # Print the extracted data
                print(f"Device: {device}")
                print(f"Status: {status}")
                print(f"Temperature: {temperature} C")

            except json.JSONDecodeError:
                print("Failed to decode JSON. Waiting for 5 seconds before retrying...")
                time.sleep(5)  # Delay for 5 seconds if JSON decoding fails

                # After waiting, try to find the ESP32 serial port again
                print("Rescanning for ESP32 serial port...")
                ser.close()  # Close the existing connection
                ser = None
                while ser is None:
                    ser = initialize_serial_connection()

            except UnicodeDecodeError as e:
                print(f"Unicode decoding error: {e}. Skipping invalid data...")

    except serial.SerialException as e:
        print(f"Serial connection error: {e}. Reconnecting...")
        ser.close()  # Close the existing connection
        ser = None
        # Try to reconnect
        while ser is None:
            ser = initialize_serial_connection()

    except OSError as e:
        print(f"OS error: {e}. Attempting to reconnect...")
        ser.close()  # Close the existing connection
        ser = None
        # Try to reconnect
        while ser is None:
            ser = initialize_serial_connection()

    except Exception as e:
        # Catch all other unexpected errors and log them, but continue the program
        print(f"An unexpected error occurred: {e}. Continuing...")
    
    # Delay to prevent overloading the CPU
    time.sleep(1)

