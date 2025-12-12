import socket
from utils import check_parity, check_crc, check_hamming


HOST = "127.0.0.1"
PORT = 6000

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))

packet = client.recv(1024).decode()
data, method, received_control = packet.split("|")

print("Received Data:", data)
print("Method:", method)
print("Received Control:", received_control)

if method == "PARITY":
    ok = check_parity(data, received_control)
elif method == "CRC":
    ok = check_crc(data, received_control)
elif method == "HAMMING":
    corrected = check_hamming(data, received_control)
    print("Corrected Data:", corrected)
    ok = corrected == data
else:
    print("Unknown method")
    exit()


print("Status: DATA CORRECT ✅" if ok else "Status: DATA CORRUPTED ❌")

client.close()
