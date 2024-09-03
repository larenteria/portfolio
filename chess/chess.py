import pygame
import chessRules as cr
import chessCustomization as cc
import sys

# Initialize Pygame
pygame.init()

##########################
### GLOBALS ##############
##########################

# Constants
WIDTH, HEIGHT = 800, 900  # Increased height for buffer
ROWS, COLS = 8, 8
SQ_SIZE = WIDTH // COLS
TOP_BUFFER = 60  # Buffer height for buttons

IN_CHECK = False # Flag to indicate if a player is in check
SHOW_SETTINGS = False  # Flag to show/hide the settings menu


# Pieces
PIECES = ['b_pawn', 'b_rook', 'b_knight', 'b_bishop', 'b_queen', 'b_king', 'w_pawn', 'w_rook', 'w_knight', 'w_bishop', 'w_queen', 'w_king']

##########################
### END GLOBALS ##########
##########################

##########################
### SETUP ###############
##########################

# Load images
def load_images(sq_size):
    images = {}
    for piece in PIECES:
        images[piece] = pygame.transform.scale(pygame.image.load(f'chessPieces/{piece}.png'), (sq_size, sq_size))
    return images

# Draw buttons
def draw_buttons(screen):
    font = pygame.font.SysFont(None, 35)
    settings_button = pygame.Rect(40, 20, 150, 35)  # Button dimensions and position
    quit_button = pygame.Rect(650, 20, 100, 35)
    
    pygame.draw.rect(screen, (200, 200, 200), settings_button)  # Settings button
    pygame.draw.rect(screen, (200, 200, 200), quit_button)  # Quit button
    
    settings_text = font.render('Settings', True, cc.FONT_COLOR)
    quit_text = font.render('Quit', True, cc.FONT_COLOR)
    
    screen.blit(settings_text, (60, 25))
    screen.blit(quit_text, (670, 25))
    
    return settings_button, quit_button

# Draw settings menu
def draw_settings_menu(screen):
    font = pygame.font.SysFont(None, 36)
    menu_width, menu_height = 300, 200
    menu_rect = pygame.Rect((WIDTH - menu_width) // 2, (HEIGHT - menu_height) // 2, menu_width, menu_height)
    
    # Draw menu background
    pygame.draw.rect(screen, cc.SCREEN_COLOR, menu_rect)
    
    # Draw buttons for menu options
    reset_button = pygame.Rect(menu_rect.x + 50, menu_rect.y + 50, 200, 40)
    color_button = pygame.Rect(menu_rect.x + 50, menu_rect.y + 120, 200, 40)
    
    pygame.draw.rect(screen, (150, 150, 150), reset_button)
    pygame.draw.rect(screen, (150, 150, 150), color_button)
    
    reset_text = font.render('Reset Board', True, cc.FONT_COLOR)
    color_text = font.render('Change Color', True, cc.FONT_COLOR)
    
    screen.blit(reset_text, (reset_button.x + 20, reset_button.y + 10))
    screen.blit(color_text, (color_button.x + 20, color_button.y + 10))
    
    return reset_button, color_button

# Draw chessboard
def draw_board(screen, sq_size, selected_square=None, colors=[cc.LIGHT_SQUARES, cc.DARK_SQUARES]):
    for row in range(ROWS):
        for col in range(COLS):
            color = colors[(row + col) % 2]
            rect = pygame.Rect(col * sq_size, row * sq_size + TOP_BUFFER, sq_size, sq_size)  # Account for buffer
            pygame.draw.rect(screen, color, rect)

            if selected_square and (row, col) == (selected_square[0], selected_square[1]):
                color = cc.HIGHLIGHT_COLOR
                pygame.draw.rect(screen, color, rect, 3)  # Highlight selected square
            else:
                pygame.draw.rect(screen, cc.BLACK, rect, 1)  # Draw grid lines

# Draw pieces
def draw_pieces(screen, board, images, sq_size):
    for row in range(ROWS):
        for col in range(COLS):
            piece = board[row][col]
            if piece != 'X':
                screen.blit(images[piece], pygame.Rect(col * sq_size, row * sq_size + TOP_BUFFER, sq_size, sq_size))  # Account for buffer

##########################
### END SETUP ###############
##########################

# Main
def main():
    global IN_CHECK, WIDTH, HEIGHT, SQ_SIZE, SHOW_SETTINGS
    screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
    pygame.display.set_caption('Chess')

    images = load_images(SQ_SIZE)

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
    white_turn = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.VIDEORESIZE:
                WIDTH, HEIGHT = event.w, event.h
                SQ_SIZE = min(WIDTH // COLS, (HEIGHT - TOP_BUFFER) // ROWS)  # Update square size based on new dimensions
                screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
                images = load_images(SQ_SIZE)  # Reload images with the new square size
                        # Handle key press to flip the board
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_f:
                    board = cr.flip_board(board)
                    cr.Board_Flipped = not cr.Board_Flipped

            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()

                # Check if a button was clicked
                settings_button, quit_button = draw_buttons(screen)
                if settings_button.collidepoint(pos):
                    SHOW_SETTINGS = not SHOW_SETTINGS  # Toggle settings menu
                elif quit_button.collidepoint(pos):
                    pygame.quit()
                    sys.exit()

                # If settings menu is displayed, check for clicks in it
                if SHOW_SETTINGS:
                    reset_button, color_button = draw_settings_menu(screen)
                    if reset_button.collidepoint(pos):
                        print("Reset board clicked")
                        # TODO: Reset board logic here
                    elif color_button.collidepoint(pos):
                        print("Change color clicked")
                        # TODO: Change piece color logic here
                else:
                    # Check if a chessboard square was clicked (ignore clicks in settings menu)
                    if pos[1] > TOP_BUFFER:  # Ignore clicks in the button area
                        col = pos[0] // SQ_SIZE
                        row = (pos[1] - TOP_BUFFER) // SQ_SIZE  # Adjust for the buffer

                        if selected_piece:
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

                            else:
                                selected_piece = None
                        else:
                            piece = board[row][col]
                            if piece != 'X' and ((white_turn and piece.startswith('w')) or (not white_turn and piece.startswith('b'))):
                                selected_piece = (row, col, piece)
        # Draw everything
        screen.fill(cc.SCREEN_COLOR)
        settings_button, quit_button = draw_buttons(screen)  # Draw buttons
        draw_board(screen, SQ_SIZE, selected_piece)  # Draw board
        draw_pieces(screen, board, images, SQ_SIZE)  # Draw pieces

        if SHOW_SETTINGS:
            draw_settings_menu(screen)  # Draw settings menu if active

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
