import socket
import sys
import argparse
import os

supported_mime_types = {
	".txt": "text/plain",
	".css": "text/css",
	".html": "text/html",
	".jpg": "image/jpeg",
	".jpeg": "image/jpeg",
	".png": "image/png",
}

parser = argparse.ArgumentParser()
parser.add_argument("host", help="Domain name or IP address.")
parser.add_argument("port", type=int, nargs="?", default=80, help="Port number. Client uses port 80 as default.")
parser.add_argument("--method", type=str.upper, choices=["GET", "POST"], default="GET", help="Request method. Supports GET and POST methods only.")
parser.add_argument("--file", help="File to include as POST payload.")

args = parser.parse_args()
port = args.port 
host = args.host
method = args.method
file = args.file
payload = bool(file)

if port < 1 or port > 65535:
	sys.exit("Port number has to be between 1 and 65535")

if method == "GET" and payload:
	sys.exit("GET doesn't support sending payload")

if method == "POST" and not payload:
	sys.exit("POST requires payload (--file FILE)")

request = (
	f"{method} / HTTP/1.1\r\n"
	f"Host: {host}\r\n"
	"Connection: close\r\n"
)

if method == "POST":
	if not os.path.exists(file):
		sys.exit(f"File not found: {file}")
	
	file_extension = os.path.splitext(file)[1]
	mime_type = supported_mime_types.get(file_extension, "application/octet-stream")
	
	with open(file, "rb") as f:
		payload = f.read()
	
	payload_length = len(payload)
	request += f"Content-Type: {mime_type}\r\n"
	request += f"Content-Length: {payload_length}\r\n"
	request += "\r\n"
	request = request.encode("ISO-8859-1")
	request += payload
else:
	request += "\r\n"	
	request = request.encode("ISO-8859-1")
	
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((host, port))
client_socket.sendall(request)

response_buffer = bytearray()
while True:
	response_bytes = client_socket.recv(1024)
	if len(response_bytes) == 0:
		break
	response_buffer.extend(response_bytes)
	
response_parts = response_buffer.split(b"\r\n\r\n", 1)
response_header = response_parts[0].decode("ISO-8859-1")
response_body = response_parts[1]

print("===== RESPONSE HEADER =====")
print(response_header)
print("===== RESPONSE BODY =====")
print(response_body)

