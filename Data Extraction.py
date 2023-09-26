import serial
import time

print("Python script started")

try:
    ser = serial.Serial('COM3', 9600)
    print("Serial port opened successfully")

    # Clear the serial buffer
    while ser.in_waiting:
        ser.readline()
    print("Serial buffer cleared")

except serial.serialutil.SerialException as e:
    print(f"Failed to open serial port: {e}")
    exit(1)

filename = input("Enter the filename to save the data (e.g., object1.txt): ")

try:
    with open(filename, 'w') as file:
        print("File opened successfully")
        while True:
            if ser.in_waiting:
                try:
                    line = ser.readline().decode('utf-8').strip()
                    timestamp = time.time()  # Get current timestamp
                    print(f"Received line: {line}, Timestamp: {timestamp}")  # Print to the console
                    file.write(f"{timestamp},{line}\n")  # Save to the file with timestamp
                    file.flush()  # Flush the file buffer to ensure data is actually saved
                except (serial.serialutil.SerialException, UnicodeDecodeError) as e:
                    print(f"Error reading line: {e}")
                    ser.close()
                    print("Serial port closed due to error")
                    break
except KeyboardInterrupt:
    print("Data collection complete!")
    ser.close()
    print("Serial port closed")
