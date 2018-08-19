from socket import *

serverName = "127.0.0.1"
serverPort = 12001
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((serverName, serverPort))
message = input('input lowercase sentence:')
clientSocket.send(str.encode(message))
modifiedMessage = clientSocket.recv(1024)
print('From server:', modifiedMessage.decode())
clientSocket.close()
