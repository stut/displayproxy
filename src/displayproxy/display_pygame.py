from displayproxy.display_base import BaseDisplay
from copy import deepcopy
from threading import Event
from time import sleep

from PIL import Image
import contextlib
with contextlib.redirect_stdout(None):
    import pygame


class PygameDisplay(BaseDisplay):
    """Displays images fullscreen using pygame."""
    _default_options = {
        # Fullscreen mode; if width and height are specified they will be
        # stretched/compressed to fill the screen.
        "fullscreen": 'true',
        # Hide the cursor; useful for touchscreens or where you have no buttons.
        "hide_cursor": 'false',
        # If width and height are 0 the display will match the screen resolution.
        "width": 0,
        "height": 0,
        # Sleep for this number of seconds after each loop. This is the max timw
        # it may take to update the display when a new image is received. It also
        # affects how frequently inputs are checked.
        "sleep": 1,
        # Forcefully refresh the display every n seconds. This should not be too
        # frequent, and is here to prevent the display from getting stuck.
        "refresh": 10,
    }

    def __init__(self, buttons: str, options: str):
        """
        Initialise the display.

        :param buttons: A dictionary of button definitions.
        :param options: A dictionary of options specific to the display type.
        """
        super().__init__(buttons, options)

        self._fullscreen = self._is_truthy_str(self._options['fullscreen'])
        self._hide_cursor = self._is_truthy_str(self._options['hide_cursor'])
        self._width = int(self._options['width'])
        self._height = int(self._options['height'])
        self._sleep = float(self._options['sleep'])
        self._refresh = float(self._options['refresh'])

        pygame.init()
        pygame.display.set_caption("displayproxy")

        display_info = pygame.display.Info()
        if self._width == 0:
            self._width = display_info.current_w
        if self._height == 0:
            self._height = display_info.current_h

        self._display = pygame.display.set_mode(
            (self._width, self._height),
            pygame.FULLSCREEN if self._fullscreen else 0)
        if self._hide_cursor:
            pygame.mouse.set_visible(0)

        self._display.fill((32, 32, 32))
        self._display.blit(pygame.font.SysFont("Arial", 24).render(
            "Waiting for data...", 1, (192, 192, 192)), (30, 30))
        self._display.blit(pygame.font.SysFont("Verdana", 16).render(
            "Press ESC to quit", 1, (192, 192, 192)), (30, 90))
        pygame.display.flip()

        self._updated = Event()

    def run(self):
        """Run the display."""
        refresh_counter = 1 / self._sleep * self._refresh
        while True:
            if self._shutdown_event.is_set():
                return

            try:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        return
                    elif event.type == pygame.KEYDOWN and event.key in [pygame.K_ESCAPE, pygame.K_q]:
                        return

                if refresh_counter <= 0 or self._updated.is_set():
                    self._updated.clear()
                    refresh_counter = 1 / self._sleep * self._refresh
                    pygame.display.flip()
                else:
                    refresh_counter -= 1

            except Exception as e:
                print(f"Exception in pygame loop: {e}")

            sleep(self._sleep)

    @property
    def width(self) -> int:
        """Return the width of the display."""
        return self._width

    @property
    def height(self) -> int:
        """Return the height of the display."""
        return self._height

    def update(self, img: Image) -> None:
        """
        Update the image on the display.

        :param img: The image to draw.
        """
        self._current_image = deepcopy(img)
        surface = pygame.image.fromstring(img.tobytes(), img.size, img.mode).convert()
        self._display.blit(pygame.transform.scale(surface, (self.width, self.height)), (0, 0))
        self._updated.set()

    def cleanup(self) -> None:
        """Cleanup the display object."""
        pygame.quit()
