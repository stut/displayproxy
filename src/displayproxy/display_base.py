from copy import copy
from datetime import datetime
from threading import Event, Lock
from time import sleep

from PIL import Image

from displayproxy.config import Config


class BaseDisplay:
    """Base class for displays."""

    def __init__(self, config: Config):
        """
        Initialise common display properties.

        :param buttons: A string of button configuration in the format
            'label=spec,label=spec,...'.
        :param options: A dictionary of options specific to the display type,
            in the format 'key=value,key=value,...'.
        """
        self._config = config
        self._shutdown_event = Event()
        self._button_defs = self._config.buttons
        self._button_status = {label: 0 for label in self._button_defs} if self._button_defs else {}
        self._button_lock = Lock()

        # Base level default options.
        self._max_upload_size = self._config.option_int('max_upload_size', 1024 * 1024 * 5)  # 5MB

    @property
    def width(self) -> int:
        """Return the width of the display."""
        self._config.option_int('width', 0)

    @property
    def height(self) -> int:
        """Return the height of the display."""
        self._config.option_int('width', 0)

    @property
    def max_upload_size(self) -> int:
        """Return the maximum upload size."""
        return self._max_upload_size

    def get_button_status(self) -> dict:
        """Return the current state of the buttons."""
        with self._button_lock:
            return copy(self._button_status)

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

    def _handle_button_pressed(self, pin: int) -> None:
        """
        Update the status of a button to say it was pressed now.

        :param pin: The pin of the button that was pressed.
        """
        with self._button_lock:
            for label, spec in self._button_defs.items():
                if spec == pin:
                    self._button_status[label] = datetime.now().timestamp()
                    break
