from display_base import BaseDisplay


try:
    from copy import deepcopy
    from datetime import datetime
    from sys import exit

    from inky.auto import auto
    from PIL import Image

    class InkyDisplay(BaseDisplay):
        """Displays images on an Inky display."""
        _default_options = {
            "saturation": 0.5,
            "border_colour": "black",
        }

        def __init__(self, buttons: str, options: str):
            """
            :param diff_percent_threshold: The percentage of pixels that must
                differ between the new image and the last image displayed for an
                update to occur.
            """
            super().__init__(buttons, options)

            try:
                self._display = auto(ask_user=False, verbose=False)
            except TypeError:
                exit('You need to update the Inky library to >= v1.1.0')

            self._current_image = None

        @property
        def width(self) -> int:
            """Return the width of the display."""
            return self._display.width

        @property
        def height(self) -> int:
            """Return the height of the display."""
            return self._display.height

        def _button_callback(self, button: str) -> None:
            """
            Update the status of a button to say it was pressed now.

            :param button: The label of the button that was pressed.
            """
            self._button_status[button] = datetime.now().timestamp()

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
                self._display.set_image(img.resize(self._display.resolution), saturation=self._options['saturation'])
                self._display.set_border(self._options['border_colour'])
                self._display.show()

except ImportError:
    class InkyDisplay(BaseDisplay):
        """Dummy class for when the Inky library is not installed."""

        def __init__(self, diff_percent_threshold: float = 1.0, buttons: dict = {}):
            exit('The Inky library is not installed. Please install it to use the display.')
