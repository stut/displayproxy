from displayproxy.display_base import BaseDisplay
from displayproxy.config import Config


try:
    from copy import deepcopy
    from sys import exit

    from inky.auto import auto
    import RPi.GPIO as GPIO
    from PIL import Image

    class InkyDisplay(BaseDisplay):
        """Displays images on an Inky display."""
        _default_options = {
            "saturation": 0.5,
            "border_colour": "black",
            "diff_percent_threshold": 1.0,
        }

        def __init__(self, config: Config):
            """
            Initialise the display.

            :param buttons: A dictionary of button definitions.
            :param options: A dictionary of options specific to the display type.
            """
            super().__init__(config)

            self._saturation = self._config.option_float('saturation', self._default_options['saturation'])
            self._border_colour = self._config.option_str('border_colour', self._default_options['border_colour'])
            self._diff_percent_threshold = self._config.option_float('diff_percent_threshold', self._default_options['diff_percent_threshold'])

            try:
                self._display = auto(ask_user=True, verbose=True)
            except TypeError:
                exit('You need to update the Inky library to >= v1.1.0')

            self._current_image = None
            self._setup_buttons()

        @property
        def width(self) -> int:
            """Return the width of the display."""
            return self._display.width

        @property
        def height(self) -> int:
            """Return the height of the display."""
            return self._display.height

        def _setup_buttons(self) -> None:
            """
            Setup the buttons.
            """
            GPIO.setmode(GPIO.BCM)
            for label in self._button_defs.keys():
                try:
                    # The pin will default to pull-up and falling edge unless
                    # the pin ends in 'd' (for down)
                    pin_def = self._button_defs[label].lower()
                    pull_up_down = GPIO.PUD_UP
                    if pin_def.endswith('d'):
                        pin_def = int(pin_def[:-1])
                        pull_up_down = GPIO.PUD_DOWN
                    elif pin_def.endswith('u'):
                        pin_def = int(pin_def[:-1])
                        pull_up_down = GPIO.PUD_UP
                    else:
                        pin_def = int(pin_def)

                    GPIO.setup([pin_def], GPIO.IN, pull_up_down=pull_up_down)
                    GPIO.add_event_detect(pin_def, GPIO.FALLING if pull_up_down == GPIO.PUD_UP else GPIO.RISING,
                                          self._handle_button_pressed, bouncetime=500)

                    # Update the button definition to just be the pin number so
                    # the callback can look up the label.
                    self._button_defs[label] = pin_def
                except Exception as e:
                    exit(f"Error setting up button '{label}': {e}")

        def _compare_pixels(self, currentImage: Image, newImage: Image) -> float:
            """
            Compare two PIL Image objects pixel by pixel, returning the percentage
            of pixels that differ. Returns 100 if the images are different sizes.

            :param img1: The first image to compare.
            :param img2: The second image to compare.
            :return: The percentage of pixels that differ between the two images.
            """
            pixels1 = list(currentImage.getdata())
            pixels2 = list(newImage.getdata())
            if len(pixels1) != len(pixels2):
                return 100
            mismatch = 0
            for i in range(0, len(pixels1)):
                if pixels1[i] != pixels2[i]:
                    mismatch += 1
            return mismatch/len(pixels1)*100

        def update(self, img: Image) -> None:
            """
            Update the image on the display. The image will be stretched to fit the
            display resolution. The display will only be updated if the new image
            differs from the last image displayed by more than the diff_percent_threshold.

            :param img: The image to draw.
            :param saturation: The saturation of the display.
            :param border_colour: The colour of the border.
            """
            rgb_img = img.convert('RGB')

            diff_percent = 100
            if self._current_image is not None:
                diff_percent = self._compare_pixels(self._current_image, rgb_img)

            if diff_percent == -1 or diff_percent > self._diff_percent_threshold:
                self._current_image = deepcopy(rgb_img)
                self._display.set_image(img.resize(self._display.resolution), saturation=self._saturation)
                self._display.set_border(self._border_colour)
                self._display.show()

except ImportError:
    class InkyDisplay(BaseDisplay):
        """Dummy class for when the Inky library is not installed."""

        def __init__(self, diff_percent_threshold: float = 1.0, buttons: dict = {}):
            exit('The Inky library is not installed; cannot use an Inky display without it.')
