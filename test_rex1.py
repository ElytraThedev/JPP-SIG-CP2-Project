import socket

# Connect to Server
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(("localhost", 5555))  # Use the same IP and port as server

def game():
    while True:
        data = client.recv(1024).decode()
        if data == "win":
            print("You lost!")
            break
        elif data == "retry":
            print("Invalid move by server.")
        else:
            move = int(input("Your move (0-8): "))
            client.send(str(move).encode())

    client.close()

game()
