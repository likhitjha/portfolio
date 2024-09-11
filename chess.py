import streamlit as st

class ChessPiece:
    def __init__(self, color, symbol):
        self.color = color
        self.symbol = symbol

class ChessBoard:
    def __init__(self):
        self.board = [[None for _ in range(8)] for _ in range(8)]
        self.current_turn = 'white'
        self.setup_board()

    def setup_board(self):
        # Set up pawns
        for col in range(8):
            self.board[1][col] = ChessPiece('black', '♟')
            self.board[6][col] = ChessPiece('white', '♙')
        
        # Set up other pieces
        back_row = ['♜', '♞', '♝', '♛', '♚', '♝', '♞', '♜']
        for col in range(8):
            self.board[0][col] = ChessPiece('black', back_row[col])
            self.board[7][col] = ChessPiece('white', back_row[col].translate(str.maketrans('♜♞♝♛♚', '♖♘♗♕♔')))

    def move_piece(self, from_pos, to_pos):
        from_row, from_col = 8 - int(from_pos[1]), ord(from_pos[0]) - ord('a')
        to_row, to_col = 8 - int(to_pos[1]), ord(to_pos[0]) - ord('a')
        
        piece = self.board[from_row][from_col]
        if piece and piece.color == self.current_turn:
            self.board[to_row][to_col] = piece
            self.board[from_row][from_col] = None
            self.current_turn = 'black' if self.current_turn == 'white' else 'white'
            return True
        return False

    def __str__(self):
        board_str = ""
        for row in self.board:
            for piece in row:
                board_str += piece.symbol if piece else '·'
            board_str += '\n'
        return board_str

def main():
    st.set_page_config(page_title="Simple Chess Game", layout="wide")
    st.title("Simple Chess Game")

    if 'board' not in st.session_state:
        st.session_state.board = ChessBoard()

    # Display the chess board
    board_display = st.session_state.board.__str__().replace('\n', '<br>')
    st.markdown(f"<pre style='font-size:24px; line-height:1;'>{board_display}</pre>", unsafe_allow_html=True)

    # Input for moves
    col1, col2 = st.columns(2)
    with col1:
        from_pos = st.text_input("From position (e.g., e2):", key="from_input")
    with col2:
        to_pos = st.text_input("To position (e.g., e4):", key="to_input")

    if st.button("Make Move"):
        if len(from_pos) == 2 and len(to_pos) == 2:
            if st.session_state.board.move_piece(from_pos, to_pos):
                st.success(f"Moved piece from {from_pos} to {to_pos}")
            else:
                st.error("Invalid move. Please try again.")
        else:
            st.error("Invalid input. Please use format like 'e2' for positions.")

    st.write(f"Current turn: {st.session_state.board.current_turn.capitalize()}")

    if st.button("Reset Game"):
        st.session_state.board = ChessBoard()
        st.experimental_rerun()

if __name__ == "__main__":
    main()