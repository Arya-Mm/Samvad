import serial
import time

# Establish serial connection with Arduino
ser = serial.Serial('COM9', 9600)  # Adjust 'COM8' to match your Arduino's serial port
time.sleep(2)  # Wait for Arduino to initialize

# Mapping of text characters to sign language gestures
sign_language_mapping = {
    'A': [1, 0, 0, 0, 0],
    'B': [1, 1, 0, 0, 0],
    'C': [1, 1, 1, 0, 0],
    'D': [1, 1, 1, 1, 0],
    'E': [1, 1, 1, 1, 1],
    '1': [0, 0, 0, 0, 1],
    '2': [0, 0, 0, 1, 1],
    '3': [0, 0, 1, 1, 1],
    '4': [0, 1, 1, 1, 1],
    '5': [1, 1, 1, 1, 1]
}

def convert_text_to_sign_language(text):
    gestures = []
    for char in text.upper():
        if char in sign_language_mapping:
            gestures.append(sign_language_mapping[char])
    return gestures

def send_gestures_to_arduino(gestures):
    for gesture in gestures:
        # Send gesture signal to Arduino
        ser.write(','.join(map(str, gesture)).encode())
        time.sleep(0.1)  # Adjust delay if needed
        # Wait for acknowledgment from Arduino
        print("Sent gesture:", gesture)
        while True:
            if ser.readline().strip().decode() == "Gesture received":
                print("Gesture received by Arduino")
                break

if __name__ == "__main__":
    text_input = input("Enter the text to convert to sign language: ")
    sign_language_gestures = convert_text_to_sign_language(text_input)
    send_gestures_to_arduino(sign_language_gestures)

# Close serial connection
ser.close()
