from copy import deepcopy
from datetime import datetime
from threading import Event, Lock
from time import sleep

from PIL import Image


class BaseDisplay:
    """Base class for displays."""
    _default_options = {}

    def __init__(self, buttons: str, options: str):
        """
        Initialise common display properties.

        :param buttons: A string of button configuration in the format
            'label=spec,label=spec,...'.
        :param options: A dictionary of options specific to the display type,
            in the format 'key=value,key=value,...'.
        """
        self._shutdown_event = Event()
        self._button_defs = self._parse_buttons(buttons)
        self._button_status = {label: 0 for label in self._button_defs} if self._button_defs else {}
        self._button_lock = Lock()
        self._options = {**self._default_options, **self._parse_options(options)}

    @property
    def width(self) -> int:
        """Return the width of the display."""
        raise Exception("Width property must be implemented in Display classes")

    @property
    def height(self) -> int:
        """Return the height of the display."""
        raise Exception("Height property must be implemented in Display classes")

    def get_button_status(self) -> dict:
        """Return the current state of the buttons."""
        with self._button_lock:
            return deepcopy(self._button_status)

    def run(self) -> None:
        """Handle input events."""
        while True:
            if self._shutdown_event.is_set():
                return
            sleep(1)

    def update(self, img: Image) -> None:
        """
        Update the image on the display.

        :param img: The image to draw.
        """
        raise Exception("Update method must be implemented in Display classes")

    def shutdown(self) -> None:
        """Shutdown the display."""
        self._shutdown_event.set()

    def cleanup(self) -> None:
        """Cleanup the display object."""
        pass

    def _parse_buttons(self, buttons: str) -> dict:
        """
        Parse the button configuration string into a dictionary.
        Semicolon-separated list of label=spec.

        :param buttons: The button configuration string.
        :return: A dict of button labels to type-specific specs.
        """
        try:
            buttons_defs = {}
            buttons = buttons.strip()
            if buttons == '':
                return buttons_defs

            for button in buttons.split(';'):
                # Allow for '=' in the button label since it's not supported
                # in the spec.
                bits = button.split('=')
                spec = bits.pop()
                buttons_defs['='.join(bits).strip()] = spec.strip()
            return buttons_defs
        except Exception as e:
            exit(f'Error parsing button configuration: {e}')

    def _parse_options(self, options: str) -> dict:
        """
        Parse the option configuration string into a dictionary.
        Semicolon-separated list of key=value pairs.

        :param buttons: The option configuration string.
        :return: A dict of option keys to values.
        """
        try:
            options_dict = {}
            options = options.strip()
            if options == '':
                return options_dict

            for option in options.split(';'):
                # Allow for '=' in the option value since it's not supported in
                # the key.
                key, value = option.split('=', 2)
                options_dict[key.strip()] = value.strip()
            return options_dict
        except Exception as e:
            exit(f'Error parsing button configuration: {e}')

    def _button_pressed_callback(self, pin: int) -> None:
        """
        Update the status of a button to say it was pressed now.

        :param pin: The pin of the button that was pressed.
        """
        print(f"Button pressed: {pin}")
        with self._button_lock:
            for label, spec in self._button_defs.items():
                if spec == pin:
                    self._button_status[label] = datetime.now().timestamp()
                    break

    def _is_truthy_str(self, value: str) -> bool:
        """Return True if the value is a truthy string."""
        # This is used when parsing options to convert strings to booleans.
        return value.lower() in ['true', 'yes', 'y', '1']
