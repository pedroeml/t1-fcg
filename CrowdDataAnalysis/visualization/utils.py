from collections import deque


def generate_colors():
    colors = deque()

    for r in [0, 127, 255]:
        for g in [0, 255, 127]:
            for b in [255, 127, 0]:
                color = (b, g, r)
                colors.append(color)

    return colors
