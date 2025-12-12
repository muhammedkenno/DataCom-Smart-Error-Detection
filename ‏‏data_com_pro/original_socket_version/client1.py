import socket
from utils import generate_parity, generate_crc, generate_hamming


HOST = "127.0.0.1"
PORT = 5000

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))

data = input("Enter data: ")
method = input("Choose method (PARITY / CRC / HAMMING): ").upper()

if method == "PARITY":
    control = generate_parity(data)
elif method == "CRC":
    control = generate_crc(data)
elif method == "HAMMING":
    control = generate_hamming(data)
else:
    print("Invalid method!")
    client.close()
    exit()



packet = f"{data}|{method}|{control}"
client.send(packet.encode())

print("Sent:", packet)
client.close()
