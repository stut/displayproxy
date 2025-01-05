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

## Usage

All configuration is done using command line options. The default values are:
- `host` = `"localhost"`
- `port` = `8000`
- `buttons` = `""`
- `options` = `""`

```bash
$ python3 -m displayproxy.server [--host HOST] [--port PORT] [--buttons BUTTONS]
```

Nothing is drawn to the display until an image is received, so don't expect
anything to happen on startup.

## Buttons

DisplayProxy can be configured to listen for button presses on the display.
The format of this option is different depending on the display type.

It should be noted that the nature of this system does not lend itself to
scenarios needing a responsive UI, or a UI that provides instant feedback to
the user.

### Inky

The `buttons` option for Inky displays is a semicolon-separated list of
`label=gpio-pin`. The label can be any string so long as it does not contain a
semicolon. The GPIO pin should be the number of the pin on the Raspberry Pi
that the button is connected to.

By default the pins are pulled up. To pull them down suffix the pin number with
`d`. For consistency you can add `u` to pins that should be pulled up. When
pulled up it will detect a falling edge, when pulled down it will detect a
rising edge.

For example, to listen for button presses on GPIO pins 5 (button `A`) and 6
(button B, pulled down), the option would be `--buttons "A=5;B=6d"`.

Use the `GET /buttons` endpoint to see when the buttons were last pressed.

### Pygame

The `buttons` option for Pygame displays is a semicolon-separated list of
`label=bounding-box`. The label can be any string so long as it does not
contain a semicolon. The bounding box should be a comma-separated list of
four integers representing the top-left x, y coordinates and the bottom-right
x, y coordinates of the bounding box in which the button is located.

If the `buttons` option is set to `screen` then the entire screen will be
considered a button with the label, `screen`. No other buttons can be defined
if this option is used.

Use the `GET /buttons` endpoint to see when the buttons were last pressed.

## Options

TODO: Document the options option.

## API

### `GET /info`

This endpoint returns information about the Inky display, such as the colour
and resolution.

#### Example response

```json
{
  "capabilities": {
    "color": true
  },
  "resolution": {
    "width": 600,
    "height": 448
  }
}
```

### `GET /buttons`

This endpoint returns the unix timestamp when each of the buttons on the Inky
display was last pressed.

#### Example response

```json
{
  "a": 0,
  "b": 1736005506,
  "c": 0,
  "d": 0,
}
```

This indicates that button `b` was last pressed at the unix timestamp
`1736005506`, while the other buttons have not been pressed.

### `POST /update`

This endpoint accepts raw image data in the request body and will display it on
the Inky display.

- The image data should be in a format that the `PIL.Image` class can read.
- The image will be stretched to fit the Inky display. Use the `/info` endpoint
  to get the display's resolution.
- The request will not return until the image has been displayed.
- The response will be a `204` status code if the image was displayed
  successfully.
- If the supplied image couuld not be displayed, a `400` status code will be
  returned.
- If the image is valid but something else went wrong, a `500` status code will
  be returned.

### `POST /shutdown`

This endpoint will shut down the server. It takes no body and returns a
`202 Accepted` status code since the actual shutdown may not happen immediately.
