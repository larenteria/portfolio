""" 
Customization 

TODO: 
 - make settings menu functional
"""

# Basic Colors
BLACK = (0, 0, 0)
DARK_GREY = (80, 80, 80)
LIGHT_GREY = (200, 200, 200)
WHITE = (255, 255, 255)
HIGHLIGHT_COLOR = (186, 202, 68)

# Chessboard color themes

# Theme 1: Classic Brown
DARK_BROWN = (139, 69, 19)
LIGHT_BROWN = (245, 222, 179)

# Theme 2: Modern Grey
DARK_GREY_SQUARE = (50, 50, 50)
LIGHT_GREY_SQUARE = (220, 220, 220)

# Theme 3: Blue Serenity
DARK_BLUE = (0, 51, 102)
LIGHT_BLUE = (173, 216, 230)

# Theme 4: Pink Fantasy
DARK_PINK = (199, 21, 133)
LIGHT_PINK = (255, 182, 193)

# Theme 5: Red Passion
DARK_RED = (139, 0, 0)
LIGHT_RED = (255, 99, 71)

# Theme 6: Forest Green
DARK_GREEN = (34, 139, 34)
LIGHT_GREEN = (144, 238, 144)

# Theme 7: Royal Purple
DARK_PURPLE = (75, 0, 130)
LIGHT_PURPLE = (216, 191, 216)

# Theme 8: Orange Sunset
DARK_ORANGE = (255, 69, 0)
LIGHT_ORANGE = (255, 165, 0)

# Theme 9: Slate Blue
DARK_SLATE = (47, 79, 79)
LIGHT_SLATE = (119, 136, 153)

# Theme 10: Monochrome
DARK_MONO = (30, 30, 30)
LIGHT_MONO = (180, 180, 180)

# Chessboard configurations
CHESSBOARD_THEMES = [
    (LIGHT_BROWN, DARK_BROWN),         # 0. Classic Brown
    (LIGHT_GREY_SQUARE, DARK_GREY_SQUARE),  # 1. Modern Grey
    (LIGHT_BLUE, DARK_BLUE),           # 2. Blue Serenity
    (LIGHT_PINK, DARK_PINK),           # 3.Pink Fantasy
    (LIGHT_RED, DARK_RED),             # 4. Red Passion
    (LIGHT_GREEN, DARK_GREEN),         # 5. Forest Green
    (LIGHT_PURPLE, DARK_PURPLE),       # 6. Royal Purple
    (LIGHT_ORANGE, DARK_ORANGE),       # 7. Orange Sunset
    (LIGHT_SLATE, DARK_SLATE),         # 8. Slate Blue
    (LIGHT_MONO, DARK_MONO )           # 9. Monochrome
]




LIGHT_SQUARES, DARK_SQUARES = CHESSBOARD_THEMES[9]
SCREEN_COLOR = DARK_GREY
FONT_COLOR = BLACK
BUTTON_COLOR = LIGHT_GREY



