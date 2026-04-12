import socket
import sys
import argparse

parser = argparse.ArgumentParser(add_help=False)
parser.add_argument("host")
parser.add_argument("port", type=int, nargs="?", default=80)

args = parser.parse_args()
port = args.port 
host = args.host

if port < 1 or port > 65535:
	sys.exit("Port number has to be between 1 and 65535")

request = (
	"GET / HTTP/1.1\r\n"
	f"Host: {host}\r\n"
	"Connection: close\r\n"
	"\r\n"
).encode("ISO-8859-1")

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((host, port))
client_socket.sendall(request)

response_buffer = bytearray()
while True:
	response_bytes = client_socket.recv(1024)
	if len(response_bytes) == 0:
		break
	response_buffer.extend(response_bytes)
	
response_parts = response_buffer.split(b"\r\n\r\n")
response_header = response_parts[0].decode("ISO-8859-1")
response_body = response_parts[1].decode("UTF-8")

print(response_header)
