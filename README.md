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

## Usage

All configuration is done using command line options. The default values are:
- `host` = `"localhost"`
- `port` = `8000`
- `buttons` = `""`
- `options` = `""`

```bash
$ python3 -m displayproxy.server [<display-type>] [--host <HOST>] [--port <PORT>] [--buttons <BUTTONS>] [--options <OPTIONS>]
```

When using an Inky display, nothing is drawn to the display until an image is
received, so don't expect anything to happen on startup.

See [the docs](docs/index.md) for more information.
