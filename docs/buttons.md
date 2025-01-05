# Buttons

DisplayProxy can be configured to listen for button presses on the display.
The format of this option is different depending on the display type.

It should be noted that the nature of this system does not lend itself to
scenarios needing a responsive UI, or a UI that provides instant feedback to
the user.

## Inky

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

## Pygame

The `buttons` option for Pygame displays is a semicolon-separated list of
`label=bounding-box`. The label can be any string so long as it does not
contain a semicolon. The bounding box should be a comma-separated list of
four integers representing the top-left x, y coordinates and the bottom-right
x, y coordinates of the bounding box in which the button is located.

If the `buttons` option is set to `screen` then the entire screen will be
considered a button with the label, `screen`. No other buttons can be defined
if this option is used.

Use the `GET /buttons` endpoint to see when the buttons were last pressed.
