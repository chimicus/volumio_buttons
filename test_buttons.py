import RPi.GPIO as GPIO
import sys

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: test_button.py <button to test>")
        sys.exit(1)
    try:
        button = int(sys.argv[1])
    except ValueError:
        print("The button parameter needs to be a number")
        sys.exit(1)
    GPIO.setmode(GPIO.BCM)
    default_bouncetime=1000
    GPIO.setup(button, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    while True:
        print(GPIO.input(button), end='\r')

