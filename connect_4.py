import streamlit as st
import numpy as np
from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage

# Game constants
ROWS = 6
COLS = 7
EMPTY = "⚪"
PLAYER_1 = "🔴"
PLAYER_2 = "🟡"

# Default prompts
DEFAULT_PROMPT1 = [
    "You are an AI playing Connect Four. The board is represented as a 6x7 grid. Empty spots are '⚪', your pieces are '🟡', and the opponent's pieces are '🔴'. Respond with only the column number (0-6) for your move.",
    "Here's the current board state:\n{board_string}\nWhat's your move?"
]

def create_board():
    return np.full((ROWS, COLS), EMPTY)

def drop_piece(board, row, col, piece):
    board[row][col] = piece

def is_valid_location(board, col):
    return board[ROWS-1][col] == EMPTY

def get_next_open_row(board, col):
    for r in range(ROWS):
        if board[r][col] == EMPTY:
            return r

def winning_move(board, piece):
    # Check horizontal locations
    for c in range(COLS-3):
        for r in range(ROWS):
            if board[r][c] == piece and board[r][c+1] == piece and board[r][c+2] == piece and board[r][c+3] == piece:
                return True

    # Check vertical locations
    for c in range(COLS):
        for r in range(ROWS-3):
            if board[r][c] == piece and board[r+1][c] == piece and board[r+2][c] == piece and board[r+3][c] == piece:
                return True

    # Check positively sloped diagonals
    for c in range(COLS-3):
        for r in range(ROWS-3):
            if board[r][c] == piece and board[r+1][c+1] == piece and board[r+2][c+2] == piece and board[r+3][c+3] == piece:
                return True

    # Check negatively sloped diagonals
    for c in range(COLS-3):
        for r in range(3, ROWS):
            if board[r][c] == piece and board[r-1][c+1] == piece and board[r-2][c+2] == piece and board[r-3][c+3] == piece:
                return True

    return False

def draw_board(board):
    for row in range(ROWS-1, -1, -1):
        st.write(" ".join(board[row]))

def get_ai_move(board, ai_piece, sys_msg, human_msg):
    chat = ChatOpenAI(temperature=0, openai_api_key='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')
    
    board_string = "\n".join([" ".join(row) for row in reversed(board)])
    print(board_string)
    messages = [
        SystemMessage(content=sys_msg),
        HumanMessage(content=human_msg.format(board_string=board_string))
    ]
    
    # Print the system and human messages in the Streamlit app
    st.write("System Message:")
    st.write(sys_msg)
    st.write("Human Message:")
    st.write(human_msg.format(board_string=board_string))
    
    response = chat(messages)
    return int(response.content)

# Streamlit app
st.title("Connect Four Game")

# Initialize session state
if 'board' not in st.session_state:
    st.session_state.board = create_board()
if 'game_over' not in st.session_state:
    st.session_state.game_over = False
if 'turn' not in st.session_state:
    st.session_state.turn = 0
if 'mode' not in st.session_state:
    st.session_state.mode = 'Human vs AI'  # Default mode

# Game mode selection
st.session_state.mode = st.selectbox("Select Game Mode:", ["Human vs AI", "Human vs Human"])

# Display and edit prompts for AI mode
if st.session_state.mode == "Human vs AI":
    with st.expander("Prompt for the Agent-1"):
        board_string = "\n".join([" ".join(row) for row in st.session_state.board])
        sys_msg = st.text_area("System Message (opt.)", value=DEFAULT_PROMPT1[0], height=120, key="prompt1_sys_msg")
        human_msg = st.text_area("Human Message", value=DEFAULT_PROMPT1[1], height=120, key="prompt1_human_msg")
        st.text_area("Current Board State", value=board_string, height=200, key="board_string_display", disabled=True)

# Main game loop
if not st.session_state.game_over:
    # Display current player
    current_player = PLAYER_1 if st.session_state.turn % 2 == 0 else PLAYER_2
    st.write(f"Current player: {'Human' if current_player == PLAYER_1 else 'AI' if st.session_state.mode == 'Human vs AI' and current_player == PLAYER_2 else 'Human 2'}")

    # Display the board
    draw_board(st.session_state.board)

    if current_player == PLAYER_1 or (st.session_state.mode == "Human vs Human" and current_player == PLAYER_2):
        # Human player's turn
        col = st.number_input("Select column (0-6):", min_value=0, max_value=6, step=1)
        if st.button("Drop piece"):
            if is_valid_location(st.session_state.board, col):
                row = get_next_open_row(st.session_state.board, col)
                drop_piece(st.session_state.board, row, col, current_player)

                if winning_move(st.session_state.board, current_player):
                    st.session_state.game_over = True
                    st.write(f"{'Human' if current_player == PLAYER_1 else 'Human 2'} wins!")
                elif np.all(st.session_state.board != EMPTY):
                    st.session_state.game_over = True
                    st.write("It's a tie!")
                else:
                    st.session_state.turn += 1
            else:
                st.write("Invalid move. Try again.")

            # Rerun the app to update the board
            st.rerun()
    else:
        # AI player's turn in Human vs AI mode
        if st.session_state.mode == "Human vs AI":
            col = get_ai_move(st.session_state.board, current_player, sys_msg, human_msg)
            if is_valid_location(st.session_state.board, col):
                row = get_next_open_row(st.session_state.board, col)
                drop_piece(st.session_state.board, row, col, current_player)

                if winning_move(st.session_state.board, current_player):
                    st.session_state.game_over = True
                    st.write("AI wins!")
                elif np.all(st.session_state.board != EMPTY):
                    st.session_state.game_over = True
                    st.write("It's a tie!")
                else:
                    st.session_state.turn += 1

            # Rerun the app to update the board
            st.rerun()

# Game over state
if st.session_state.game_over:
    draw_board(st.session_state.board)
    if st.button("Play Again"):
        st.session_state.board = create_board()
        st.session_state.game_over = False
        st.session_state.turn = 0
        st.rerun()
