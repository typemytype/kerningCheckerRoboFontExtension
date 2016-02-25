# kerning Checker

Checks kerning in the UFO file and compares it with the generated binary file (otf, ttf only).

The extension subscribes to the `fontDidGenerate` notification and compares the `font.kerning` with the kerning in the compiled font. If this is not the same a warning pops up and the result is printed to the output window.
