"""
Chess Rules

TODO: 
1. CREATE LUISFISH
"""
import pygame

#############################################
### GLOBALS #################################
#############################################

###### DYANMIC VARIABLES ####################

# For En Passant:
Prev_Move = None

# For Castling:
    # To check if rooks have moved 
Rook_Moved = {'w': {'left': False, 'right': False}, 'b': {'left': False, 'right': False}}
    # To check if Kings have moved
King_Moved = {'w': False, 'b': False}

# For Draw by three-fold repetition and 50-move rule
move_history = []
half_moves_since_last_capture_or_pawn_move = 0

# For flipping the board
Board_Flipped = False

###### END DYANMIC VARIABLES ################

#############################################
### END GLOBALS #############################
#############################################




#############################################
### MOVE VALIDATION #########################
#############################################

def is_valid_move(piece, start_pos, end_pos, board):
    end_row, end_col = end_pos
    
    if piece[0] == 'w' and board[end_row][end_col].startswith('w'):
        return False
    if piece[0] == 'b' and board[end_row][end_col].startswith('b'):
        return False
    
    piece_type = piece[2:]
    
    if piece_type == 'pawn':
        return is_valid_pawn_move(piece, start_pos, end_pos, board)
    elif piece_type == 'rook':
        return is_valid_rook_move(start_pos, end_pos, board)        
    elif piece_type == 'knight':
        return is_valid_knight_move(start_pos, end_pos)
    elif piece_type == 'bishop':
        return is_valid_bishop_move(start_pos, end_pos, board)
    elif piece_type == 'queen':
        return is_valid_queen_move(start_pos, end_pos, board)
    elif piece_type == 'king':
        return is_valid_king_move(piece, start_pos, end_pos, board)
    
    return False

def is_valid_pawn_move(piece, start_pos, end_pos, board):
    global Prev_Move
    start_row, start_col = start_pos
    end_row, end_col = end_pos

    direction = 1 if piece.startswith('w') else -1
    start_row_initial = 6 if piece.startswith('w') else 1
    
    # Move forward
    if start_col == end_col:
        if end_row == start_row - direction and board[end_row][end_col] == 'X':
            return True
        if start_row == start_row_initial and end_row == start_row - 2*direction and board[start_row - direction][start_col] == 'X' and board[end_row][end_col] == 'X':
            return True
    
    # Capture
    if abs(start_col - end_col) == 1 and end_row == start_row - direction:
        # Regular capture
        if board[end_row][end_col] != 'X':
            return True
        
        # En passant capture
        if Prev_Move:
            last_start_pos, last_end_pos, last_piece = Prev_Move
            last_start_row, _ = last_start_pos
            last_end_row, last_end_col = last_end_pos
            
            if last_piece[2:] == 'pawn' and abs(last_start_row - last_end_row) == 2:
                if last_end_row == start_row and last_end_col == end_col:
                    if board[start_row][end_col] == last_piece:
                        # Perform en passant capture
                        board[start_row][end_col] = 'X'  # Remove the captured pawn
                        return True
    return False

def is_valid_rook_move(start_pos, end_pos, board):
    start_row, start_col = start_pos
    end_row, end_col = end_pos

    if start_row != end_row and start_col != end_col:
        return False

    if start_row == end_row:
        step = 1 if start_col < end_col else -1
        for col in range(start_col + step, end_col, step):
            if board[start_row][col] != 'X':
                return False
    
    if start_col == end_col:
        step = 1 if start_row < end_row else -1
        for row in range(start_row + step, end_row, step):
            if board[row][start_col] != 'X':
                return False

    return True

def is_valid_knight_move(start_pos, end_pos):
    start_row, start_col = start_pos
    end_row, end_col = end_pos
    row_diff = abs(start_row - end_row)
    col_diff = abs(start_col - end_col)
    
    return (row_diff == 2 and col_diff == 1) or (row_diff == 1 and col_diff == 2)

def is_valid_bishop_move(start_pos, end_pos, board):
    start_row, start_col = start_pos
    end_row, end_col = end_pos
    
    if abs(start_row - end_row) != abs(start_col - end_col):
        return False
    
    step_row = 1 if start_row < end_row else -1
    step_col = 1 if start_col < end_col else -1
    for i in range(1, abs(start_row - end_row)):
        if board[start_row + i*step_row][start_col + i*step_col] != 'X':
            return False

    return True

def is_valid_queen_move(start_pos, end_pos, board):
    return is_valid_rook_move(start_pos, end_pos, board) or is_valid_bishop_move(start_pos, end_pos, board)

def is_valid_king_move(piece, start_pos, end_pos, board):
    global King_Moved, Rook_Moved
    start_row, start_col = start_pos
    end_row, end_col = end_pos
    row_diff = abs(start_row - end_row)
    col_diff = abs(start_col - end_col)
    
    if row_diff <= 1 and col_diff <= 1:
        # Normal king move
        return True

    # Castling logic
    if start_row == end_row and not King_Moved[piece[0]]:
        if end_col == start_col + 2:  # Kingside castling
            # Check if squares between king and rook are empty and the rook has not moved
            if not Rook_Moved[piece[0]]['right'] and board[start_row][start_col + 1] == 'X' and board[start_row][start_col + 2] == 'X':
                # Make sure king doesn't move through/land in check
                temp_board = [row[:] for row in board]
                temp_board[start_row][start_col] = 'X'
                temp_board[start_row][start_col + 1] = piece
                temp_board[start_row][start_col + 2] = board[start_row][start_col + 3]
                temp_board[start_row][start_col + 3] = 'X'
                if not is_in_check(temp_board, piece[0], 8, 8)[0]:
                    return "kingside_castling"

        elif end_col == start_col - 2:  # Queenside castling
            # Check if squares between king and rook are empty and the rook has not moved
            if not Rook_Moved[piece[0]]['left'] and board[start_row][start_col - 1] == 'X' and board[start_row][start_col - 2] == 'X' and board[start_row][start_col - 3] == 'X':
                # Make sure king doesn't move through/land in check
                temp_board = [row[:] for row in board]
                temp_board[start_row][start_col] = 'X'
                temp_board[start_row][start_col - 1] = piece
                temp_board[start_row][start_col - 2] = board[start_row][start_col - 4]
                temp_board[start_row][start_col - 4] = 'X'
                if not is_in_check(temp_board, piece[0], 8, 8)[0]:
                    return "queenside_castling"

    return False


### END MOVE VALIDATION #####################




#############################################
### SPECIAL PIECE CIRCUMSTANCES #############
#############################################


############## Pawn Promotion ###############
def promote_pawn(board, row, col, white_turn):
    piece_type = None
    print("Promote pawn to [Q]ueen, [R]ook, [B]ishop, or k[N]ight?") # TODO: Add GUI
    while piece_type not in ['queen', 'rook', 'bishop', 'knight']:
        try:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        piece_type = 'queen'
                    elif event.key == pygame.K_r:
                        piece_type = 'rook'
                    elif event.key == pygame.K_b:
                        piece_type = 'bishop'
                    elif event.key == pygame.K_k:
                        piece_type = 'knight'
                    if piece_type:
                        break
        except KeyError:
            print("Invalid key pressed. Please choose Q, R, B, or K.")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

    new_piece = 'w_' + piece_type if white_turn else 'b_' + piece_type
    board[row][col] = new_piece


######## Castling Update Variables  #########

def update_rook_status(piece, start_pos):
    global Rook_Moved
    row, col = start_pos
    if piece[0] == 'w':
        if row == 7 and col == 0:
            Rook_Moved['w']['left'] = True
        elif row == 7 and col == 7:
            Rook_Moved['w']['right'] = True
    elif piece[0] == 'b':
        if row == 0 and col == 0:
            Rook_Moved['b']['left'] = True
        elif row == 0 and col == 7:
            Rook_Moved['b']['right'] = True

def update_king_status(piece):
    global King_Moved
    King_Moved[piece[0]] = True

### END SPECIAL PIECE CIRCUMSTANCES ########

#############################################
#### EXTRA FUNCTIONS ########################
#############################################


###### Flipping board/coordinates ###########
def flip_board(board):
    return [row[::-1] for row in board[::-1]]
def flip_coordinates(row, col):
    return 7 - row, 7 - col

#### END EXTRA FUNCTIONS ####################




#############################################
### CHECK/CHECKMATE/STALEMATE/DRAW ##########
#############################################

def is_in_check(board, color, rows, cols):
    # Find the king's position
    king_pos = None 
    for row in range(rows):
        for col in range(cols):
            if board[row][col] == f'{color}_king':
                king_pos = (row, col) # Example: of 'w' king
                break
        if king_pos:
            break

    # Check if the king is in check
    for row in range(rows):
        for col in range(cols):
            piece = board[row][col]
            if piece != 'X' and piece.startswith('b' if color == 'w' else 'w') and is_valid_move(piece, (row, col), king_pos, board):
                return True, king_pos
    return False, king_pos

# Example: is_checkmate(board, 'w', 8, 8)
def is_checkmate(board, color, rows, cols):
    # Check if the king is in checkmate
    in_check, king_pos = is_in_check(board, color, rows, cols)
    if not in_check:
        # If not in check, check for stalemate
        is_stalemate_game = is_stalemate(board, color, rows, cols)
        return False, is_stalemate_game

    # Check all possible moves for the current player
    for row in range(rows):
        for col in range(cols):
            piece = board[row][col]
            if piece != 'X' and piece.startswith(color):
                for r in range(rows):
                    for c in range(cols):
                        if is_valid_move(piece, (row, col), (r, c), board):
                            temp_king_pos = king_pos
                            if piece[2:] == 'king':
                                king_pos = (r, c)
                            temp_board = [r[:] for r in board]
                            temp_board[r][c] = piece
                            temp_board[row][col] = 'X'

                            # check if the king is still in check after some move
                            if not is_in_check(temp_board, color, 8, 8)[0]:
                                return False, False
                            
                            king_pos = temp_king_pos

    # If no legal moves left and the king is in check, it's checkmate
    """ CURRENTLY DOES NOTHING """
    # checkmate_info = {"losing_king_pos": king_pos, "winning_king_pos": None}
    # winning_king_color = 'w' if color == 'b' else 'b'
    # for row in range(rows):
    #     for col in range(cols):
    #         if board[row][col] == f'{winning_king_color}_king':
    #             checkmate_info["winning_king_pos"] = (row, col)
    #             break

    return True, False  # It's checkmate, not stalemate

def is_stalemate(board, color, rows, cols):
    for row in range(rows):
        for col in range(cols):
            piece = board[row][col]
            if piece.startswith(color): 
                # Check for legal moves of the current player and return False if there is any
                for r in range(rows):
                    for c in range(cols):
                        if is_valid_move(piece, (row, col), (r, c), board):
                            temp_board = [r[:] for r in board]
                            temp_board[row][col] = 'X'
                            temp_board[r][c] = piece
                            if not is_in_check(temp_board, color, rows, cols)[0]:  
                                return False  
    return True  

def is_draw(board, color):
    global move_history, half_moves_since_last_capture_or_pawn_move
    
    # Check for three-fold repetition
    board_tuple = tuple(tuple(row) for row in board)
    if move_history.count(board_tuple) >= 3:
        return True, "Three-fold repetition"

    # Check for 50-move rule
    if half_moves_since_last_capture_or_pawn_move >= 50:
        return True, "50-move rule"

    # Check for insufficient material
    insufficient_material, reason = is_draw_by_insufficient_material(board)
    if insufficient_material:
        return True, reason

    return False, None # No draw

def is_draw_by_insufficient_material(board):
    pieces = [piece for row in board for piece in row if piece != 'X']

    # Count pieces by type
    kings = sum(piece.startswith('w_king') or piece.startswith('b_king') for piece in pieces)
    bishops = sum(piece.endswith('bishop') for piece in pieces)
    knights = sum(piece.endswith('knight') for piece in pieces)

    # Only two kings
    if len(pieces) == 2 and kings == 2:
        return True, "King vs. King"

    # King vs. King + Bishop
    if len(pieces) == 3 and kings == 2 and bishops == 1:
        return True, "King vs. King + Bishop"

    # King vs. King + Knight
    if len(pieces) == 3 and kings == 2 and knights == 1:
        return True, "King vs. King + Knight"

    # King + Bishop vs. King + Bishop with same color bishops
    if len(pieces) == 4 and kings == 2 and bishops == 2:
        bishop_squares = [row.index(piece) % 2 for row in board for piece in row if piece.endswith('bishop')]
        if len(set(bishop_squares)) == 1:  # Same color bishops
            return True, "King + Bishop vs. King + Bishop with same color bishops"

    return False, None

### END CHECK/CHECKMATE/STALEMATE/DRAW ######



#############################################
### MAKE MOVE ###############################
#############################################

def make_move(selected_piece, end_pos, board, white_turn):
    # Returns: new board state, whether the move was made, whether the player is in check, whether the game is checkmate, and whether the game is a draw
    global Prev_Move, move_history, half_moves_since_last_capture_or_pawn_move, Board_Flipped

    # Flip board if necessary to make calculations easier
    if Board_Flipped:
        board = flip_board(board)
        start_row, start_col = flip_coordinates(selected_piece[0], selected_piece[1])
        end_row, end_col = flip_coordinates(end_pos[0], end_pos[1])
    else: 
        start_row, start_col = selected_piece[0], selected_piece[1]
        end_row, end_col = end_pos

    piece = selected_piece[2]

    # Check if the move is valid
    valid_move = is_valid_move(piece, (start_row, start_col), (end_row, end_col), board)

    # If the move is valid, valid_move == True/False unless it's castling
    if valid_move:
        temp_board = [r[:] for r in board]

        if valid_move == "kingside_castling":
            temp_board[end_row][end_col] = piece
            temp_board[start_row][start_col] = 'X'
            temp_board[start_row][start_col + 1] = board[start_row][start_col + 3]
            temp_board[start_row][start_col + 3] = 'X'

        elif valid_move == "queenside_castling":
            temp_board[end_row][end_col] = piece
            temp_board[start_row][start_col] = 'X'
            temp_board[start_row][start_col - 1] = board[start_row][start_col - 4]
            temp_board[start_row][start_col - 4] = 'X'

        else:
            temp_board[start_row][start_col] = 'X'
            temp_board[end_row][end_col] = piece

        # Pawn promotion check
        if piece[2:] == 'pawn' and (end_row == 0 or end_row == 7):
            promote_pawn(temp_board, end_row, end_col, white_turn)

        # Update half-move count
        if piece[2:] == 'pawn' or board[end_row][end_col] != 'X':
            half_moves_since_last_capture_or_pawn_move = 0
        else:
            half_moves_since_last_capture_or_pawn_move += 1

        # Update move history
        move_history.append(tuple(tuple(row) for row in temp_board))

        # Check if player tries to make a move that does not take them out of check
        if is_in_check(temp_board, 'w' if white_turn else 'b', 8, 8)[0]:
            return None, False, True, None, False

        clr = 'w' if not white_turn else 'b'
        is_checkmate_game, is_stalemate_game = is_checkmate(temp_board, clr, 8, 8)
        in_check = not is_stalemate_game and is_in_check(temp_board, clr, 8, 8)[0]
        draw, draw_reason = is_draw(temp_board, clr)

        # Update Prev_Move for En passant
        Prev_Move = ((start_row, start_col), (end_row, end_col), piece)

        # Update castling status
        if valid_move == "kingside_castling":
            King_Moved[piece[0]] = True
            Rook_Moved[piece[0]]['right'] = True

        elif valid_move == "queenside_castling":
            King_Moved[piece[0]] = True
            Rook_Moved[piece[0]]['left'] = True

        # Update king/rook status for castling
        if piece[2:] == 'king': 
            update_king_status(piece)
        elif piece[2:] == 'rook':
            update_rook_status(piece, (end_row, end_col))

        if Board_Flipped:
            temp_board = flip_board(temp_board)
        return temp_board, True, in_check, is_checkmate_game, is_stalemate_game or draw

    else:
        return None, False, False, None, False
    
### END MAKE MOVE ###########################