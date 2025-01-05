import RPi.GPIO as GPIO


def detect_button_presses(buttons: dict, callback: callable) -> None:
    """
    Detect button presses and call a callback function when a button is pressed.

    :param buttons: A dictionary of GPIO pin number to button label.
    :param callback: A function to call when a button is pressed, passing
        the button label.
    """
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(buttons.keys(), GPIO.IN, pull_up_down=GPIO.PUD_UP)
    for pin in buttons.keys():
        GPIO.add_event_detect(pin, GPIO.FALLING,
                              lambda: callback(buttons[pin]),
                              bouncetime=500)
