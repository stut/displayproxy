from copy import deepcopy
from threading import Event
from time import sleep

from PIL import Image
import contextlib
with contextlib.redirect_stdout(None):
    import pygame

from displayproxy.display_base import BaseDisplay
from displayproxy.config import Config


class PygameDisplay(BaseDisplay):
    """Displays images fullscreen using pygame."""
    _default_options = {
        # Fullscreen mode; if width and height are specified they will be
        # stretched/compressed to fill the screen.
        "fullscreen": 'false',
        # Hide the cursor; useful for touchscreens or where you have no buttons.
        "hidecursor": 'false',
        # If width and height are 0 the display will match the screen resolution.
        "width": 600,
        "height": 448,
        # Button color as a hex value. If not specified, buttons will not be drawn.
        "buttoncolor": '',
    }

    def __init__(self, config: Config):
        """
        Initialise the display.

        :param buttons: A dictionary of button definitions.
        :param options: A dictionary of options specific to the display type.
        """
        super().__init__(config)

        self._fullscreen = self._config.option_bool('fullscreen', self._default_options['fullscreen'])
        self._hide_cursor = self._config.option_bool('hidecursor', self._default_options['hidecursor'])
        self._width = self._config.option_int('width', self._default_options['width'])
        self._height = self._config.option_int('height', self._default_options['height'])
        self._button_color = pygame.Color(self._config.option_str('button_color'))
        self._show_buttons = self._button_color != ''
        if self._show_buttons:
            self._button_surfaces = {}
            self._button_hover_surfaces = {}

        pygame.init()
        pygame.display.set_caption("displayproxy")
        pygame.font.init()

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

        self._setup_buttons()

        # Draw the initial screen.
        self._current_surface = pygame.Surface((self._width, self._height))
        waiting = pygame.font.SysFont('arial', 36).render("Waiting for data...", True, (224, 224, 224))
        r = waiting.get_rect(center=(self._width // 2, self._height // 2 - 30))
        self._current_surface.blit(waiting, r)
        press_esc = pygame.font.SysFont('arial', 24).render("Press ESC to quit", True, (224, 224, 224))
        r = press_esc.get_rect(center=(self._width // 2, self._height // 2 + 20))
        self._current_surface.blit(press_esc, r)

        self._updated = Event()

    def run(self):
        """Run the display."""
        # Aim for roughly 60fps
        loop_sleep_time = 1 / 60
        while True:
            if self._shutdown_event.is_set():
                return

            try:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        return
                    elif event.type == pygame.KEYDOWN and event.key in [pygame.K_ESCAPE, pygame.K_q]:
                        return
                    elif event.type == pygame.MOUSEBUTTONUP:
                        pos = pygame.mouse.get_pos()
                        for label, rect in self._button_defs.items():
                            if rect.collidepoint(pos):
                                self._handle_button_pressed(rect)

                self._display.blit(pygame.transform.scale(self._current_surface, (self.width, self.height)), (0, 0))
                self._draw_buttons()
                pygame.display.flip()

            except Exception as e:
                print(f"Exception in pygame loop: {e}")

            sleep(loop_sleep_time)

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
        self._current_surface = pygame.image.fromstring(img.tobytes(), img.size, img.mode).convert()
        self._updated.set()

    def cleanup(self) -> None:
        """Cleanup the display object."""
        pygame.quit()

    def _setup_buttons(self) -> None:
        """
        Setup the buttons.
        """
        for label in self._button_defs.keys():
            try:
                x1, y1, x2, y2 = self._button_defs[label].split(',')
                self._button_defs[label] = pygame.Rect(int(x1), int(y1), int(x2) - int(x1), int(y2) - int(y1))

                if self._show_buttons:
                    s = pygame.Surface((self._button_defs[label].width, self._button_defs[label].height), pygame.SRCALPHA)
                    pygame.draw.rect(s, self._button_color, (0, 0, self._button_defs[label].width, self._button_defs[label].height), 3)
                    size = 10
                    while True:
                        f = pygame.font.SysFont('Arial', size)
                        st = f.render(label, True, self._button_color)
                        r = st.get_rect()
                        if r.width > self._button_defs[label].width - 20 or r.height > self._button_defs[label].height - 20:
                            s.blit(st, ((self._button_defs[label].width - r.width) // 2, (self._button_defs[label].height - r.height) // 2))
                            self._button_surfaces[label] = s

                            hover_color = deepcopy(self._button_color)
                            hover_color.a = 128
                            self._button_hover_surfaces[label] = pygame.Surface((self._button_defs[label].width, self._button_defs[label].height), pygame.SRCALPHA)
                            self._button_hover_surfaces[label].fill(hover_color)
                            self._button_hover_surfaces[label].blit(s, (0, 0))

                            self._button_surfaces[label].set_alpha(128)
                            break
                        size += 2
            except Exception as e:
                exit(f"Error setting up button '{label}': {e}")

    def _draw_buttons(self) -> None:
        """
        Draw the buttons.
        """
        if self._show_buttons:
            for label, rect in self._button_defs.items():
                mouse_pos = pygame.mouse.get_pos()
                hover = rect.collidepoint(mouse_pos)
                self._display.blit(self._button_hover_surfaces[label] if hover else self._button_surfaces[label],
                                   (rect.x, rect.y))
