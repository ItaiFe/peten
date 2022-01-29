import socket

IP = "192.168.1.1"
PORT = 8000

def connect():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((IP, PORT))
    return sock

def go_up(sock, soldier_id):
    sock.send("up")
    