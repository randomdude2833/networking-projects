import socket
import sys
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("port", type=int, nargs="?", default=28333, help="Port number. Server's default port is 28333.")

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
	print(f"Server is listening on: 0.0.0.0:{port}")

	while True:
		client_socket, client_addr = server_socket.accept()
		print("===== NEW CONNECTION =====")
		print(f"Client address: {client_addr[0]}:{client_addr[1]}")

		request_buffer = bytearray()
		while True:
			request_bytes = client_socket.recv(2)
			if len(request_bytes) == 0:
				client_socket.close()
				client_socket = None
				break
			
			request_buffer.extend(request_bytes)
			if b"\r\n\r\n" in request_buffer:
				request_header, request_body = request_buffer.split(b"\r\n\r\n", 1)
				request_headers = request_header.decode("ISO-8859-1").split("\r\n")
				request_line = request_headers.pop(0)

				method, path, version = request_line.split(" ")
				print(f"Request method: {method}")

				if method == "POST":
					content_length = None
					for header in request_headers:
						key, value = header.split(":", 1)
						if key.strip().lower() == "content-length":
							content_length = int(value.strip())

					if content_length is not None:
						while content_length - len(request_body) > 0:
							payload_bytes = client_socket.recv(content_length - len(request_body))
							request_body += payload_bytes
						print("Payload:", request_body)

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
	
