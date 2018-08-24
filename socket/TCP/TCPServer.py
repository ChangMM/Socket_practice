from socket import *
serverPort = 12001
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(('', serverPort))
serverSocket.listen(1)
print("The server is ready to receive")
while True:
	connectionSocket, _ = serverSocket.accept()
	message = connectionSocket.recv(1024)
	upper = message.upper()
	connectionSocket.send(upper)
	connectionSocket.close()
