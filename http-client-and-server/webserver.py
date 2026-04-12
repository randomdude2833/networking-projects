import socket
import sys
import argparse

parser = argparse.ArgumentParser(add_help=False)
parser.add_argument("port", type=int, nargs="?", default=28333)

args = parser.parse_args()
port = args.port 

response = (
	"HTTP/1.1 200 OK\r\n"
	"Content-Type: text/plain\r\n"
    f"Content-Length: 6\r\n"
	"Connection: close\r\n"
	"\r\n"
	"Hello!"
).encode("ISO-8859-1")

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind(("", port))
server_socket.listen()

try:
	client_socket = None

	while True:
		client_socket, client_addr = server_socket.accept()

		request_buffer = bytearray()
		while True:
			request_bytes = client_socket.recv(1024)
			if len(request_bytes) == 0:
				client_socket.close()
				client_socket = None
				break
			
			request_buffer.extend(request_bytes)
			if b"\r\n\r\n" in request_buffer:
				client_socket.sendall(response)	
				client_socket.close()
				client_socket = None
				break

except KeyboardInterrupt:
	print() # fixes the terminal prompt after CTRL-C
finally:
	if client_socket:
		client_socket.close()
	server_socket.close()
	
