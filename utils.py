from PyQt5.QtGui import QColor

def is_color_dark(qcolor: QColor) -> bool:
    r, g, b, _ = qcolor.getRgb()
    luminance = 0.299*r + 0.587*g + 0.114*b
    return luminance < 128
