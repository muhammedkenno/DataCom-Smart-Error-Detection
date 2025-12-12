import socket
import random

HOST = "127.0.0.1"
PORT1 = 5000
PORT2 = 6000

def bit_flip(data):
    bit_data = ''.join(format(ord(c), '08b') for c in data)
    pos = random.randint(0, len(bit_data)-1)
    flipped = list(bit_data)
    flipped[pos] = '0' if flipped[pos] == '1' else '1'
    return ''.join(chr(int(''.join(flipped[i:i+8]), 2)) for i in range(0, len(flipped), 8))

def char_substitution(data):
    i = random.randint(0, len(data)-1)
    return data[:i] + random.choice("ABCDEFGHIJKLMNOPQRSTUVWXYZ") + data[i+1:]

def deletion(data):
    i = random.randint(0, len(data)-1)
    return data[:i] + data[i+1:]

def insertion(data):
    i = random.randint(0, len(data))
    return data[:i] + random.choice("ABCDEFGHIJKLMNOPQRSTUVWXYZ") + data[i:]

def burst_error(data):
    if len(data) < 3:
        return data
    start = random.randint(0, len(data)-3)
    length = random.randint(2, 4)
    replace = ''.join(random.choice("XYZ") for _ in range(length))
    return data[:start] + replace + data[start+length:]

errors = [bit_flip, char_substitution, deletion, insertion, burst_error]

server1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server1.bind((HOST, PORT1))
server1.listen(1)
print("Waiting for Client 1...")

conn1, _ = server1.accept()
packet = conn1.recv(2048).decode()

data, method, control = packet.split("|")

# اختيار تخريب عشوائي
error_func = random.choice(errors)
corrupted = error_func(data)

new_packet = f"{corrupted}|{method}|{control}"

server2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server2.bind((HOST, PORT2))
server2.listen(1)
print("Waiting for Client 2...")

conn2, _ = server2.accept()
conn2.send(new_packet.encode())

print("Original:", data)
print("After corruption:", corrupted)

conn1.close()
conn2.close()
