# DisplayProxy

DisplayProxy runs an HTTP server to which you can send images and it will
display them on an attached Inky display, or in a pygame window. This
enables you to separate the generation of the images from the display of the
image. It also allows images to be pushed to the display from a remote
location.

This module was created to run on a Raspberry Pi connected to an Inky
display, and the Pygame option was added for development purposes. With the
same API you can point the same client code at a real Inky display or a Pygame
window of equivalent dimensions.

## Requirements

- Python 3.6+
- (for Inky displays) Inky requirements (see 
  [Pimoroni's Inky documentation](https://learn.pimoroni.com/tutorial/sandyj/getting-started-with-inky-phat)
  for more information)

## Installation

Install with pip or pipx. Note that it's not yet in pypi. Both methods will
install the `displayproxy` command, or it can be run directly with
`python3 -m displayproxy.server`.

```bash
$ pip install git+ssh://github.com/stut/displayproxy.git
```

```bash
$ pipx install git+ssh://github.com/stut/displayproxy.git
```

## Usage

All configuration is done using command line options. The default values are:
- `host` = `"localhost"`
- `port` = `8000`
- `buttons` = `""`
- `options` = `""`

```bash
$ python3 -m displayproxy.server [<display-type>] [--host <HOST>] [--port <PORT>] [--buttons <BUTTONS>] [--options <OPTIONS>]
```

### Inky displays

The display will not be updated until an image is received, so don't expect
anything to happen on startup.

The process can be run as a daemon as it does not need access to a desktop
environment. It can be run on a headless Raspberry Pi.

### Pygame

Pygame requires a desktop environment to run. The easiest way to achieve this
at startup on a Raspberry Pi is to use an autostart script.

See [the docs](docs/index.md) for more information.

## Display type aliases

The `display-type` option can be set to one of the following aliases to set
default buttons and options. These can be overridden with the `buttons` and
`options` CLI arguments.

- `inky-impression-5.7`: Inky Impression 5.7" display.
- `pygame-inky-impression-5.7`: Pygame window with the same dimensions and
  buttons as the Inky Impression 5.7" display.

PRs to add more aliases are welcome.

## TODO

- [ ] Add documentation on setting it up as a systemd service with an Inky
      display, and using an autostart script for Pygame. 
- [ ] Add a webhook option for button presses.
- [ ] Switch to using a configuration file for the complex options. Retain
      command line options for `display-type`, `host`, `port`.
- [X] Implement buttons for the pygame display mode.
- [X] Add `display-type` aliases for specific devices. For example, specifying
      `inky-impression-5.7` would set `width=600`, `height=448`, and the buttons
      config to `A=5u;B=6u;C=16u;D=24u`.
