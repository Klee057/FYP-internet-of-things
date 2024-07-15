from gpiozero import AngularServo
from gpiozero import Servo
from time import sleep

# servo = AngularServo(18, min_pulse_width=0.0007, max_pulse_width=0.0023)

# while (True):
#     servo.angle = 90
#     sleep(2)
#     servo.angle = 00
#     sleep(2)
#     # servo.angle = -90
#     # sleep(2)

# servo = Servo(18)

# try:
#     while True:
#         servo.min()
#         sleep(0.5)
#         servo.max()
#         sleep(0.5)
# except KeyboardInterrupt:
#     pass

from gpiozero import Servo
from time import sleep

servo = Servo(18)
val = -1
try:
    while True:
        servo.value = 0.3
        sleep(3)
        break
	# servo.min()
	# sleep(2)
        print("servo.value", servo.value)
    # sleep(2)
	# servo.max()
except KeyboardInterrupt:
	print("Program stopped")
     

    