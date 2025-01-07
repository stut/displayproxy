# API

## `GET /info`

This endpoint returns information about the Inky display, such as the colour
and resolution.

### Example response

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

## `GET /buttons`

This endpoint returns the unix timestamp when each of the buttons on the Inky
display was last pressed.

### Example response

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

## `POST /update`

This endpoint accepts raw image data in the request body and will display it on
the Inky display.

- The image data should be in a format that the pillow `Image.open` function
  can read, or raw bytes in the pillow RGBA (3x8-bit pixels, true color) or
  RGBA (4x8-bit pixels, true color with transparency mask) modes of the same
  resolution as the display.
- The image will be resized to fit the display's resolution. Dynamic clients
  can use the `/info` endpoint to get the display's resolution.
- The request will not return until the image has been displayed.
- The response will be a `204` status code if the image was displayed
  successfully.
- If the supplied image could not be displayed, a `400` status code will be
  returned.
- If the image is valid but something else went wrong, a `500` status code will
  be returned.

## `POST /shutdown`

This endpoint will shut the server down. It takes no body and returns a
`202 Accepted` status code. The actual shutdown may not happen immediately.
