import streamlit as st
import numpy as np

# Define constants
GRID_SIZE = 5
EMPTY = "⬛"
PLAYER1 = "🟢"
PLAYER2 = "🔵"

# Initialize game state
def initialize_game():
    return np.full((GRID_SIZE, GRID_SIZE), EMPTY)

def render_grid(grid, player):
    st.write("### Chain Reaction Game")
    st.write(f"Current Player: {player}")
    
    cols = st.columns(GRID_SIZE)
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            with cols[col]:
                if st.button(grid[row, col], key=f"cell_{row}_{col}"):
                    return row, col
    return None, None

def update_grid(grid, row, col, player):
    # Simple mechanism to increment energy and trigger chain reaction
    if grid[row, col] == EMPTY:
        grid[row, col] = player
    return grid

def main():
    st.title("Chain Reaction Game")
    
    # Initialize session state
    if 'grid' not in st.session_state:
        st.session_state.grid = initialize_game()
    if 'current_player' not in st.session_state:
        st.session_state.current_player = PLAYER1
    
    # Render grid and get player move
    row, col = render_grid(st.session_state.grid, st.session_state.current_player)
    
    if row is not None and col is not None:
        st.session_state.grid = update_grid(st.session_state.grid, row, col, st.session_state.current_player)
        # Switch player
        st.session_state.current_player = PLAYER2 if st.session_state.current_player == PLAYER1 else PLAYER1
        st.experimental_rerun()

if __name__ == "__main__":
    main()