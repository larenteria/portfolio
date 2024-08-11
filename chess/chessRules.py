"""
Chess Rules

TODO: 
1. Pawn Promotion
2. Stalemate
3. Draw, 50 move rule and 3 fold repetition
4. Flip board for black


TODO: 
1. CREATE LUISFISH
"""

#############################################
### GLOBALS #################################
#############################################

# En Passant
Prev_Move = None

### Castling Globals ###

# Check if rooks have moved 
Rook_Moved = {'w': {'left': False, 'right': False}, 'b': {'left': False, 'right': False}}
# Check if Kings have moved
King_Moved = {'w': False, 'b': False}


#############################################
### END GLOBALS #############################
#############################################

# Check if a move is valid 
def is_valid_move(piece, start_pos, end_pos, board, last_move):
    global Prev_Move
    Last_move = last_move
    end_row, end_col = end_pos
    if piece[0] == 'w' and board[end_row][end_col].startswith('w'):
        return False
    if piece[0] == 'b' and board[end_row][end_col].startswith('b'):
        return False
    
    piece_type = piece[2:]
    
    if piece_type == 'pawn':
        return is_valid_pawn_move(piece, start_pos, end_pos, board, Prev_Move)
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

def is_valid_pawn_move(piece, start_pos, end_pos, board, last_move):
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
        if last_move:
            last_start_pos, last_end_pos, last_piece = last_move
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
            # Check if the squares between king and rook are empty and the rook has not moved
            if not Rook_Moved[piece[0]]['right'] and board[start_row][start_col + 1] == 'X' and board[start_row][start_col + 2] == 'X':
                # Ensure the king does not move through or land in check
                temp_board = [row[:] for row in board]
                temp_board[start_row][start_col] = 'X'
                temp_board[start_row][start_col + 1] = piece
                temp_board[start_row][start_col + 2] = board[start_row][start_col + 3]
                temp_board[start_row][start_col + 3] = 'X'
                if not is_in_check(temp_board, piece[0], 8, 8)[0]:
                    return "kingside_castling"

        elif end_col == start_col - 2:  # Queenside castling
            # Check if the squares between king and rook are empty and the rook has not moved
            if not Rook_Moved[piece[0]]['left'] and board[start_row][start_col - 1] == 'X' and board[start_row][start_col - 2] == 'X' and board[start_row][start_col - 3] == 'X':
                # Ensure the king does not move through or land in check
                temp_board = [row[:] for row in board]
                temp_board[start_row][start_col] = 'X'
                temp_board[start_row][start_col - 1] = piece
                temp_board[start_row][start_col - 2] = board[start_row][start_col - 4]
                temp_board[start_row][start_col - 4] = 'X'
                if not is_in_check(temp_board, piece[0], 8, 8)[0]:
                    return "queenside_castling"

    return False


### CHECK AND CHECKMATE ### 

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
    king_row, king_col = king_pos
    for row in range(rows):
        for col in range(cols):
            piece = board[row][col]
            if piece != 'X' and piece.startswith('b' if color == 'w' else 'w') and is_valid_move(piece, (row, col), king_pos, board, Prev_Move):
                return True, king_pos
    return False, king_pos

# Example: is_checkmate(board, 'w', 8, 8)
def is_checkmate(board, color, rows, cols): 

    # Check if the king is in checkmate
    in_check, king_pos = is_in_check(board, color, rows, cols)
    if not in_check:
        return False, False 

    # Check all possible moves for the current player
    for row in range(rows):
        for col in range(cols):
            piece = board[row][col]
            if piece != 'X' and piece.startswith(color):
                for r in range(rows):
                    for c in range(cols):
                        if is_valid_move(piece, (row, col), (r, c), board, Prev_Move):
                            temp_king_pos = king_pos
                            if piece[2:] == 'king':
                                king_pos = (r, c)
                            temp_board = [r[:] for r in board]
                            temp_board[r][c] = piece
                            temp_board[row][col] = 'X'

                            # check if the king is still in check after some move
                            if not is_in_check(temp_board, color, 8, 8)[0]:
                                return False, True
                            
                            king_pos = temp_king_pos
    
    # Find all squares where the losing king is and the winning king
    losing_king_pos = king_pos
    winning_king_color = 'w' if color == 'b' else 'b'
    winning_king_pos = None
    for row in range(rows):
        for col in range(cols):
            if board[row][col] == f'{winning_king_color}_king':
                winning_king_pos = (row, col)
                break
        if winning_king_pos:
            break

    checkmate_info = {losing_king_pos: 'losing', winning_king_pos: 'winning'}
    return True, checkmate_info

def make_move(selected_piece, end_pos, board, white_turn, Prev_Move):
    start_row, start_col = selected_piece[0], selected_piece[1]
    end_row, end_col = end_pos
    piece = selected_piece[2]

    valid_move = is_valid_move(piece, (start_row, start_col), (end_row, end_col), board, Prev_Move)

    if valid_move:
        temp_board = [r[:] for r in board]

        if valid_move == "kingside_castling":
            # Move the king two squares to the right
            temp_board[end_row][end_col] = piece
            temp_board[start_row][start_col] = 'X'

            # Move rook to the square next to the king on the left
            temp_board[start_row][start_col + 1] = board[start_row][start_col + 3]
            temp_board[start_row][start_col + 3] = 'X'

        elif valid_move == "queenside_castling":
            # Move the king two squares to the left
            temp_board[end_row][end_col] = piece
            temp_board[start_row][start_col] = 'X'

            # Move the rook to the square next to the king on the right
            temp_board[start_row][start_col - 1] = board[start_row][start_col - 4]
            temp_board[start_row][start_col - 4] = 'X'

        else:
            # Normal move
            temp_board[start_row][start_col] = 'X'
            temp_board[end_row][end_col] = piece

        # Check if the move puts the player in check
        if is_in_check(temp_board, 'w' if white_turn else 'b', 8, 8)[0]:
            return None, False, False, None

        clr = 'w' if not white_turn else 'b'
        is_checkmate_game, in_check = is_checkmate(temp_board, clr, 8, 8)

        # Update Prev_Move for En passant
        Prev_Move = ((start_row, start_col), (end_row, end_col), piece)

        if valid_move == "kingside_castling":
            King_Moved[piece[0]] = True  # Mark the king as moved
            Rook_Moved[piece[0]]['right'] = True  # Mark the kingside rook as moved

        elif valid_move == "queenside_castling":
            King_Moved[piece[0]] = True  # Mark the king as moved
            Rook_Moved[piece[0]]['left'] = True  # Mark the queenside rook as moved

        if piece[2:] == 'king': 
            update_king_status(piece)
        elif piece[2:] == 'rook':
            update_rook_status(piece, (end_row, end_col))

        return temp_board, True, in_check, is_checkmate_game
    else:
        return None, False, False, None