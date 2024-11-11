import socket

# Server Setup
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(("localhost", 5555))  # Replace with your IP and port
server.listen(1)
print("Waiting for a connection...")
conn, addr = server.accept()
print(f"Connected to {addr}")

# Tic-Tac-Toe Board
board = [" " for _ in range(9)]

def display_board():
    print("\n".join([
        f"{board[0]} | {board[1]} | {board[2]}",
        "---------",
        f"{board[3]} | {board[4]} | {board[5]}",
        "---------",
        f"{board[6]} | {board[7]} | {board[8]}"
    ]))

def check_win():
    win_combinations = [(0,1,2), (3,4,5), (6,7,8), (0,3,6), (1,4,7), (2,5,8), (0,4,8), (2,4,6)]
    for combo in win_combinations:
        if board[combo[0]] == board[combo[1]] == board[combo[2]] and board[combo[0]] != " ":
            return True
    return False

def game():
    turn = "X"
    for _ in range(9):
        display_board()
        
        # Server's Turn (Player "X")
        if turn == "X":
            try:
                move = int(input("Your move (0-8): "))
                # Check if the move is within range and if the cell is empty
                while move < 0 or move > 8 or board[move] != " ":
                    print("Invalid move, try again.")
                    move = int(input("Your move (0-8): "))
                
                board[move] = "X"
                conn.send(f"{move}".encode())
                
                if check_win():
                    display_board()
                    print("You win!")
                    conn.send("win".encode())
                    break
                
                turn = "O"
            
            except ValueError:
                print("Please enter a valid integer between 0 and 8.")
                continue

        # Client's Turn (Player "O")
        else:
            print("Waiting for client to move...")
            move = int(conn.recv(1024).decode())
            if board[move] == " ":
                board[move] = "O"
                if check_win():
                    display_board()
                    print("Client wins!")
                    conn.send("win".encode())
                    break
                turn = "X"
            else:
                conn.send("retry".encode())

    display_board()
    conn.close()
    server.close()

game()
