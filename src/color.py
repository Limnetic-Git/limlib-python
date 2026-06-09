from typing import Union

class Color:
    def __init__(self, rgba_or_hex: Union[tuple, list, str]):
        self.color = None
        if isinstance(rgba_or_hex, str):
            self.color = self.hex_to_rgba(rgba_or_hex)
        else:
            self.color = [i / 255 for i in rgba_or_hex]
            if len(self.color) == 3:
                self.color.append(1.0)

    def __call__(self):
        return self.color

    def __repr__(self):
        return str(self.color)

    @staticmethod
    def hex_to_rgba(hex_color, alpha=255):
        """Converting HEX color to RGBA"""
        hex_color = hex_color.lstrip('#')
        rgb = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
        return [i / 255 for i in rgb + (alpha,)]

WHITE = Color('#ffffff')
BLACK = Color('#000000')
RED = Color('#ff0000')
GREEN = Color('#00ff00')
BLUE = Color('#0000ff')
YELLOW = Color('#ffff00')

