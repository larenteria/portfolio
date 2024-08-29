"""

CHESS!

Summary: After completely implementing all chess rules I plan to create a chess engine 'LuisFish" to play
against the user. All of the current deficiences in the code are addressed in the first lines of 'chessRules.py'. 
I also plan to implement custimization options for the user (e.g. change the board color, piece images, etc.). 
However, that is third fiddle, to finishing the rules and building an engine. 

This code was inspired by the following tutorial: https://www.youtube.com/watch?v=EnYui0e73Rs
Though I have made significant changes to the code, the tutorial was a great starting point.

"""

import pygame
import chessRules as cr
import sys

# Initialize Pygame
pygame.init()

##########################
### GLOBALS ##############
##########################

# Constants
WIDTH, HEIGHT = 800, 800
ROWS, COLS = 8, 8
SQ_SIZE = WIDTH // COLS

IN_CHECK = False
# Colors - TO BE SHIFTED INTO A CUSTUMIZATION FILE VERY SOON
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
DARK_BROWN = (139, 69, 19)
LIGHT_BROWN = (245, 222, 179)
HIGHLIGHT_COLOR = (186, 202, 68)
LOSE_COLOR = (255, 0, 0)  # Red for losing king
WIN_COLOR = (0, 255, 0)  # Green for winning king

# Additional Colors (Optional)
BLUE = (0, 0, 255)
STEEL_BLUE = (70, 130, 180)
RED = (255, 0, 0)
GREEN = (0, 128, 0)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)
PURPLE = (128, 0, 128)
CYAN = (0, 255, 255)
MAGENTA = (255, 0, 255)
GRAY = (128, 128, 128)
LIGHT_GRAY = (211, 211, 211)
DARK_GRAY = (169, 169, 169)
PINK = (255, 192, 203)
BROWN = (165, 42, 42)
TURQUOISE = (64, 224, 208)

PIECES = ['b_pawn', 'b_rook', 'b_knight', 'b_bishop', 'b_queen', 'b_king', 'w_pawn', 'w_rook', 'w_knight', 'w_bishop', 'w_queen', 'w_king']

##########################
### END GLOBALS ##########
##########################

#---------------------------------#

##########################
### SETUP ###############
##########################

# Load images
def load_images():
    images = {}
    for piece in PIECES:
        images[piece] = pygame.transform.scale(pygame.image.load(f'chessPieces/{piece}.png'), (SQ_SIZE, SQ_SIZE))
    return images

# Draw chessboard
def draw_board(screen, selected_square=None, checkmate_info=None, colors = [LIGHT_GRAY, STEEL_BLUE]):
    for row in range(ROWS):
        for col in range(COLS):
            color = colors[((row + col) % 2)]
            rect = pygame.Rect(col * SQ_SIZE, row * SQ_SIZE, SQ_SIZE, SQ_SIZE)
            pygame.draw.rect(screen, color, rect) 

            if selected_square and (row, col) == (selected_square[0], selected_square[1]):
                color = HIGHLIGHT_COLOR
                pygame.draw.rect(screen, color, rect, 3)  # Draw black grid lines
            else:  
                pygame.draw.rect(screen, BLACK, rect, 1)  # Draw black grid lines

# Draw pieces
def draw_pieces(screen, board, images):
    for row in range(ROWS):
        for col in range(COLS):
            piece = board[row][col]
            if piece != 'X':
                screen.blit(images[piece], pygame.Rect(col * SQ_SIZE, row * SQ_SIZE, SQ_SIZE, SQ_SIZE))



##########################
### END SETUP ###############
##########################

# Main
def main():
    global IN_CHECK
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption('Chess')

    images = load_images()

    board = [
        ['b_rook', 'b_knight', 'b_bishop', 'b_queen', 'b_king', 'b_bishop', 'b_knight', 'b_rook'],
        ['b_pawn', 'b_pawn', 'b_pawn', 'b_pawn', 'b_pawn', 'b_pawn', 'b_pawn', 'b_pawn'],
        ['X', 'X', 'X', 'X', 'X', 'X', 'X', 'X'],
        ['X', 'X', 'X', 'X', 'X', 'X', 'X', 'X'],
        ['X', 'X', 'X', 'X', 'X', 'X', 'X', 'X'],
        ['X', 'X', 'X', 'X', 'X', 'X', 'X', 'X'],
        ['w_pawn', 'w_pawn', 'w_pawn', 'w_pawn', 'w_pawn', 'w_pawn', 'w_pawn', 'w_pawn'],
        ['w_rook', 'w_knight', 'w_bishop', 'w_queen', 'w_king', 'w_bishop', 'w_knight', 'w_rook']]

    clock = pygame.time.Clock()
    running = True
    selected_piece = None
    move_made = False
    white_turn = True  # White starts the game

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                col = pos[0] // SQ_SIZE
                row = pos[1] // SQ_SIZE

                if selected_piece:
                    # Call make_move from chessRules.py instead of manually checking the move
                    temp_board, move_made, in_check, is_checkmate_game, draw = cr.make_move(
                        selected_piece, (row, col), board, white_turn
                    )

                    if move_made:
                        board = temp_board
                        selected_piece = None
                        white_turn = not white_turn
                        IN_CHECK = in_check

                        if is_checkmate_game:
                            print(f"Checkmate! {'White' if not white_turn else 'Black'} wins!")
                        if draw:
                            print("Draw!")

                        move_made = True
                    else:
                        # Invalid move or player is still in check
                        selected_piece = None
                else:
                    piece = board[row][col]
                    # Select the piece if it's the current player's turn
                    if piece != 'X' and ((white_turn and piece.startswith('w')) or (not white_turn and piece.startswith('b'))):
                        selected_piece = (row, col, piece)

            # Handle key press to flip the board
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_f:
                    board = cr.flip_board(board)
                    cr.Board_Flipped = not cr.Board_Flipped

        # Redraw board and pieces after every frame
        draw_board(screen, selected_piece, None)
        draw_pieces(screen, board, images)
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
