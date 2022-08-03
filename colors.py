class Color:
    red = 0
    green = 0
    blue = 0
    alpha = 255

    def __init__(self, color):
        if type(color) == Color:
            return

        if type(color) == dict:
            print("Not implemented yet")
        elif type(color) == str:  # Assuming hex
            color = color.lstrip("#")
            if len(color) == 6:  # Assuming #343434 something
                colors = [color[i:i+2] for i in range(0, len(color), 2)]
                self.red = int("0x" + colors[0], 16)
                self.green = int("0x" + colors[1], 16)
                self.blue = int("0x" + colors[2], 16)

            elif len(color) == 8:  # Assuming #343434FF something (hex alpha)
                colors = [color[i:i + 2] for i in range(0, len(color), 2)]
                self.red = int("0x" + colors[0], 16)
                self.green = int("0x" + colors[1], 16)
                self.blue = int("0x" + colors[2], 16)
                self.alpha = int("0x" + colors[3], 16)


def colorsBetween(from_color, to_color, percentage):
    color1 = Color(from_color)
    color2 = Color(to_color)

    percentage = min(max(0.00, percentage), 1.00)

    # Calculations for each color
    red = color1.red - round((color1.red - color2.red) * percentage)
    green = color1.green - round((color1.green - color2.green) * percentage)
    blue = color1.blue - round((color1.blue - color2.blue) * percentage)

    return f'#{red:02x}{green:02x}{blue:02x}'
