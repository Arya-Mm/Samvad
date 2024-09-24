from flask import Flask, request
import serial
import time

app = Flask(__name__)

# Establish serial connection with Arduino
ser = serial.Serial('COM4', 9600)  # Adjust 'COM4' to match your Arduino's serial port
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

@app.route('/send-letter', methods=['POST'])
def send_letter():
    data = request.json
    text_input = data['letter']
    sign_language_gestures = convert_text_to_sign_language(text_input)
    send_gestures_to_arduino(sign_language_gestures)
    return 'Letter received and gesture sent to Arduino'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
