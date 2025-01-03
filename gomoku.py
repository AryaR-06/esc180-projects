def is_empty(board):
    for y in range (len(board)):
        for x in range (len(board[0])):
            if board[y][x] != " ":
                return False
    return True
    
def is_bounded(board, y_end, x_end, length, d_y, d_x):
    closed = 0

    height = len(board)
    width = len(board[0])

    y_start = y_end - d_y*(length-1)
    x_start = x_end - d_x*(length-1)

    end_out_of_bound = not ((0 <= y_end + d_y < height) and (0 <= x_end + d_x < width))
    start_out_of_bound = not ((0 <= y_start - d_y < height) and (0 <= x_start - d_x < width))
    
    if end_out_of_bound or board[y_end + d_y][x_end + d_x] != " ":
        closed += 1

    if start_out_of_bound or board[y_start - d_y][x_start - d_x] != " ":
        closed += 1

    if closed == 2:
        return "CLOSED"
    
    elif closed == 1:
        return "SEMIOPEN"
    
    elif closed == 0:
        return "OPEN"
    
def detect_row(board, col, y_start, x_start, length, d_y, d_x):
    open_seq_count = 0
    semi_open_seq_count = 0

    y = y_start
    x = x_start

    height = len(board)
    width = len(board[0])

    temp_len = 0

    while (0 <= y < height) and (0 <= x < width):
        end_out_of_bound = not ((0 <= y + d_y < height) and (0 <= x + d_x < width))

        if board[y][x] == col:
            temp_len += 1
        else:
            temp_len = 0

        if temp_len == length and (end_out_of_bound or (not end_out_of_bound and board[y + d_y][x + d_x] != col)):
            opening = is_bounded(board, y, x, length, d_y, d_x)
            if opening == "SEMIOPEN":
                semi_open_seq_count += 1
            elif opening == "OPEN":
                open_seq_count += 1
            temp_len = 0
            
        y += d_y
        x += d_x

    return open_seq_count, semi_open_seq_count
    
def detect_rows(board, col, length):
    open_seq_count = 0
    semi_open_seq_count = 0

    height = len(board)
    width = len(board[0])

    for i in range (height):
        open, semi_open = detect_row (board, col, i, 0, length, 0, 1)
        open_seq_count += open
        semi_open_seq_count += semi_open

    for i in range (width):
        open, semi_open = detect_row (board, col, 0, i, length, 1, 0)
        open_seq_count += open
        semi_open_seq_count += semi_open

    for i in range (height):
        open, semi_open = detect_row (board, col, i, 0, length, 1, 1)
        open_seq_count += open
        semi_open_seq_count += semi_open
    
    for i in range (1, width):
        open, semi_open = detect_row (board, col, 0, i, length, 1, 1)
        open_seq_count += open
        semi_open_seq_count += semi_open

    for i in range (height):
        open, semi_open = detect_row (board, col, i, width - 1, length, 1, -1)
        open_seq_count += open
        semi_open_seq_count += semi_open
    
    for i in range (width-1):
        open, semi_open = detect_row (board, col, 0, i, length, 1, -1)
        open_seq_count += open
        semi_open_seq_count += semi_open

    return open_seq_count, semi_open_seq_count

def my_detect_row(board, col, y_start, x_start, length, d_y, d_x):
    open_seq_count = 0
    semi_open_seq_count = 0
    closed_seq_count = 0

    y = y_start
    x = x_start

    height = len(board)
    width = len(board[0])

    temp_len = 0

    while (0 <= y < height) and (0 <= x < width):
        end_out_of_bound = not ((0 <= y + d_y < height) and (0 <= x + d_x < width))

        if board[y][x] == col:
            temp_len += 1
        else:
            temp_len = 0

        if temp_len == length and (end_out_of_bound or (not end_out_of_bound and board[y + d_y][x + d_x] != col)):
            opening = is_bounded(board, y, x, length, d_y, d_x)
            if opening == "SEMIOPEN":
                semi_open_seq_count += 1
            elif opening == "OPEN":
                open_seq_count += 1
            elif opening == "CLOSED":
                closed_seq_count += 1
            temp_len = 0
            
        y += d_y
        x += d_x

    return open_seq_count, semi_open_seq_count, closed_seq_count
    
def my_detect_rows(board, col, length):
    open_seq_count = 0
    semi_open_seq_count = 0
    closed_seq_count = 0

    height = len(board)
    width = len(board[0])

    for i in range (height):
        open, semi_open, closed = my_detect_row (board, col, i, 0, length, 0, 1)
        open_seq_count += open
        semi_open_seq_count += semi_open
        closed_seq_count += closed

    for i in range (width):
        open, semi_open, closed = my_detect_row (board, col, 0, i, length, 1, 0)
        open_seq_count += open
        semi_open_seq_count += semi_open
        closed_seq_count += closed

    for i in range (height):
        open, semi_open, closed = my_detect_row (board, col, i, 0, length, 1, 1)
        open_seq_count += open
        semi_open_seq_count += semi_open
        closed_seq_count += closed
    
    for i in range (1, width):
        open, semi_open, closed = my_detect_row (board, col, 0, i, length, 1, 1)
        open_seq_count += open
        semi_open_seq_count += semi_open
        closed_seq_count += closed

    for i in range (height):
        open, semi_open, closed = my_detect_row (board, col, i, width - 1, length, 1, -1)
        open_seq_count += open
        semi_open_seq_count += semi_open
        closed_seq_count += closed
    
    for i in range (width-1):
        open, semi_open, closed = my_detect_row (board, col, 0, i, length, 1, -1)
        open_seq_count += open
        semi_open_seq_count += semi_open
        closed_seq_count += closed

    return open_seq_count, semi_open_seq_count, closed_seq_count

def search_max(board):
    moves = {}
    height = len(board)
    width = len(board[0])

    for y in range (height):
        for x in range (width):
            coords = (y,x)
            if board[y][x] == " ":
                board[y][x] = "b"
                cur_score = score(board)
                board[y][x] = " "
                moves[cur_score] = coords

    move_y = moves[max(moves.keys())][0]
    move_x = moves[max(moves.keys())][1]

    return move_y, move_x
    
def score(board):
    MAX_SCORE = 100000
    
    open_b = {}
    semi_open_b = {}
    open_w = {}
    semi_open_w = {}
    
    for i in range(2, 6):
        open_b[i], semi_open_b[i] = detect_rows(board, "b", i)
        open_w[i], semi_open_w[i] = detect_rows(board, "w", i)
        
    
    if open_b[5] >= 1 or semi_open_b[5] >= 1:
        return MAX_SCORE
    
    elif open_w[5] >= 1 or semi_open_w[5] >= 1:
        return -MAX_SCORE
        
    return (-10000 * (open_w[4] + semi_open_w[4])+ 
            500  * open_b[4]                     + 
            50   * semi_open_b[4]                + 
            -100  * open_w[3]                    + 
            -30   * semi_open_w[3]               + 
            50   * open_b[3]                     + 
            10   * semi_open_b[3]                +  
            open_b[2] + semi_open_b[2] - open_w[2] - semi_open_w[2])
   
def is_win(board):
    outcome = ["White won", "Black won", "Draw", "Continue playing"]
    height = len(board)
    width = len(board[0])

    draw = True
    for y in range (height):
        for x in range (width):
            if board[y][x] == " ":
                draw = False
                break

    if draw:
        return outcome[2]

    for seq in my_detect_rows (board, "w", 5):
        if seq > 0:
            return outcome[0]
    
    for seq in my_detect_rows (board, "b", 5):
        if seq > 0:
            return outcome[1]

    return outcome[3]
    
def print_board(board):
    
    s = "*"
    for i in range(len(board[0])-1):
        s += str(i%10) + "|"
    s += str((len(board[0])-1)%10)
    s += "*\n"
    
    for i in range(len(board)):
        s += str(i%10)
        for j in range(len(board[0])-1):
            s += str(board[i][j]) + "|"
        s += str(board[i][len(board[0])-1]) 
    
        s += "*\n"
    s += (len(board[0])*2 + 1)*"*"
    
    print(s)
    
def make_empty_board(sz):
    board = []
    for i in range(sz):
        board.append([" "]*sz)
    return board
                
def analysis(board):
    for c, full_name in [["b", "Black"], ["w", "White"]]:
        print("%s stones" % (full_name))
        for i in range(2, 6):
            open, semi_open = detect_rows(board, c, i);
            print("Open rows of length %d: %d" % (i, open))
            print("Semi-open rows of length %d: %d" % (i, semi_open))
         
def play_gomoku(board_size):
    board = make_empty_board(board_size)
    board_height = len(board)
    board_width = len(board[0])
    
    while True:
        print_board(board)
        if is_empty(board):
            move_y = board_height // 2
            move_x = board_width // 2
        else:
            move_y, move_x = search_max(board)
            
        print("Computer move: (%d, %d)" % (move_y, move_x))
        board[move_y][move_x] = "b"
        print_board(board)
        analysis(board)
        
        game_res = is_win(board)
        if game_res in ["White won", "Black won", "Draw"]:
            return game_res
            
            
        
        
        
        print("Your move:")
        move_y = int(input("y coord: "))
        move_x = int(input("x coord: "))
        board[move_y][move_x] = "w"
        print_board(board)
        analysis(board)
        
        game_res = is_win(board)
        if game_res in ["White won", "Black won", "Draw"]:
            return game_res
                 
def put_seq_on_board(board, y, x, d_y, d_x, length, col):
    for i in range(length):
        board[y][x] = col        
        y += d_y
        x += d_x