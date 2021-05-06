TRANSPARENT = "rgba(255, 255, 255, 0)"

WHITE = "rgb(255, 255, 255)"

ORANGE = "rgb(255, 128, 59)"

LIGHT_ORANGE = "rgb(255, 200, 170)"

LIGHT_GRAY = "rgb(230, 231, 233)"

GRAY = "rgb(190, 190, 190)"

DARK_GRAY = "rgb(96, 96, 98)"

GREEN = "rgb(0, 255, 0)"

YELLOW = "rgb(255, 255, 0)"

RED = "rgb(255, 0, 0)"

BLACK = "rgb(0, 0, 0)"


#######################################################################################
def foregroundStyle(color):
    return " color: " + color + "; "


#######################################################################################
def backgroundStyle(color):
    return " background-color: " + color + "; "


#######################################################################################
def whiteForeground():
    return foregroundStyle(WHITE)


#######################################################################################
def orangeForeground():
    return foregroundStyle(ORANGE)


#######################################################################################
def grayForeground():
    return foregroundStyle(GRAY)


#######################################################################################
def darkGrayForeground():
    return foregroundStyle(DARK_GRAY)


#######################################################################################
def blackForeground():
    return foregroundStyle(BLACK)


#######################################################################################
def redForeground():
    return foregroundStyle(RED)


#######################################################################################
def transparentBackground():
    return backgroundStyle(TRANSPARENT)


#######################################################################################
def whiteBackground():
    return backgroundStyle(WHITE)


#######################################################################################
def orangeBackground():
    return backgroundStyle(ORANGE)


#######################################################################################
def lightGrayBackground():
    return backgroundStyle(LIGHT_GRAY)


#######################################################################################
def grayBackground():
    return backgroundStyle(GRAY)


#######################################################################################
def darkGrayBackground():
    return backgroundStyle(DARK_GRAY)


#######################################################################################
def border(width, color, radius=0):
    return "" + \
           "border-radius: " + str(radius) + "px; " + \
           "border-style: solid; " + \
           "border-width: " + str(width) + "px; " + \
           "border-color: " + color + ";"


#######################################################################################
def noBorder(radius=0):
    return border(0, TRANSPARENT, radius)


#######################################################################################
def mainComponentBorder():
    return border(3, GRAY, 12)


#######################################################################################
def littleComponentBorder():
    return border(3, GRAY, 8)


def padding(p):
    return "padding: " + str(p) + "px;"


#######################################################################################
def universalStyle():
    style = ''
    return style
