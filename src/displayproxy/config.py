

class Config:
    _type_defaults = {
        'inky-impression-5.7': {
            'display_type': 'inky',
            'display_variant': '5.7',
            'buttons': {
                'A': '5u',
                'B': '6u',
                'C': '16u',
                'D': '24u',
            },
            'options': {
                'width': '600',
                'height': '448',
            },
        },
        'pygame-inky-impression-5.7': {
            'display_type': 'pygame',
            'buttons': {
                'A': '0,37,37,74',
                'B': '0,148,37,185',
                'C': '0,259,37,296',
                'D': '0,370,37,407',
            },
            'options': {
                'width': '600',
                'height': '448',
                'button_color': '#777777',
            },
        },
        'inky-impression-7.3': {
            'display_type': 'inky',
            'display_variant': '7.3',
            'buttons': {
                'A': '5u',
                'B': '6u',
                'C': '16u',
                'D': '24u',
            },
            'options': {
                'width': '800',
                'height': '480',
            },
        },
        'pygame-inky-impression-7.3': {
            'display_type': 'pygame',
            'buttons': {
                'A': '0,37,37,74',
                'B': '0,148,37,185',
                'C': '0,259,37,296',
                'D': '0,370,37,407',
            },
            'options': {
                'width': '800',
                'height': '480',
                'button_color': '#777777',
            },
        },
    }

    def __init__(self, display_type: str, buttons: str, options: str):
        """
        Create a Config object.

        :param display_type: The display type.
        :param buttons: A string of button configuration in the format
            'label=spec,label=spec,...'.
        :param options: A dictionary of options specific to the display type,
            in the format 'key=value,key=value,...'.
        """
        type_defaults = self._type_defaults.get(display_type, {})
        self._display_type = type_defaults.get("display_type", display_type)
        self._display_variant = type_defaults.get("display_variant", 'auto')
        self._buttons = {**type_defaults.get("buttons", {}), **self._parse_buttons(buttons)}
        self._options = {**type_defaults.get("options", {}), **self._parse_options(options)}

    @property
    def display_type(self) -> str:
        """Return the display type."""
        return self._display_type

    @property
    def display_variant(self) -> str:
        """Return the display variant."""
        return self._display_variant

    @property
    def buttons(self) -> dict:
        """Return the button configuration."""
        return self._buttons

    @property
    def options(self) -> dict:
        """Return the display options."""
        return self._options

    def option_str(self, key: str, default: str = '') -> str:
        """Return the option value as a string."""
        return self._options.get(key, default)

    def option_int(self, key: str, default: int = 0) -> int:
        """Return the option value as an integer."""
        return int(self._options.get(key, default))

    def option_float(self, key: str, default: float = 0.0) -> float:
        """Return the option value as a float."""
        return float(self._options.get(key, default))

    def option_bool(self, key: str, default: bool = False) -> bool:
        """Return the option value as a boolean."""
        return self._is_truthy_str(self._options.get(key, str(default)))

    def set_option(self, key: str, value: str) -> None:
        """Set an option value."""
        self._options[key] = value

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

    def _is_truthy_str(self, value: str) -> bool:
        """Return True if the value is a truthy string."""
        # This is used when parsing options to convert strings to booleans.
        return value.lower() in ['true', 'yes', 'y', '1']
