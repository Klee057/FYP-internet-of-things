import socket
import subprocess
import threading
import time
from gpiozero import DistanceSensor, LED
## server is send_message.py
SERVER_IP = '192.168.23.228'
ultrasonic = DistanceSensor(echo=17, trigger=4, threshold_distance=0.5)
led = LED(22)
led.on()
# Event to control LED flashing
onFlash = threading.Event()

def flash_led():
    """Toggle LED based on onFlash event status."""
    while True:
        onFlash.wait()  # Wait for the event to be set
        led.on()
        time.sleep(0.4)
        led.off()
        time.sleep(0.4)

def call_recognition():
    """Function to execute when an object is within the threshold distance."""
    print(f"Object detected within threshold distance! {ultrasonic.distance * 100:.2f} cm")
    print("Sending message to server...")
    onFlash.set()  # Start flashing LED
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((SERVER_IP, 5005))  # Connect to the server
        s.sendall(b"Object detected!")  # Send a message to the server
    print("Running server....")
    subprocess.run(["python", "web.py"])  # Run the web.py script
    print("Execution of web.py completed.")
    print("ultrasonic started")
    onFlash.clear()  # Stop flashing LED
    led.on()
    ultrasonic.when_in_range = call_recognition  # Reassign event handler

try:
    print("Ultrasonic sensor started...")
    # Start LED flashing thread
    threading.Thread(target=flash_led, daemon=True).start()

    # Assign event handler for object detection
    ultrasonic.when_in_range = call_recognition

    # Main loop to keep the script running
    while True:
        time.sleep(0.1)

except KeyboardInterrupt:
    print("Program terminated by user.")
