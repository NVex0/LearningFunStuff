import socket
from Crypto.Cipher import AES
import base64

HOST = "192.168.179.129"
PORT = 9999

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen(1)

target_android, addr = s.accept()

with open("VanessaMemories", "rb") as f:
    memories = f.read()

def buf(a):
    if len(a) < 2:
        return '0' + a
    return a

target_android.recv(1024).decode()
target_android.send('Pr0ceed___!!!'.encode())
key = base64.b64decode(target_android.recv(24))
iv = target_android.recv(16)

cipher_type = AES.new(key, AES.MODE_CFB, iv)
enc = cipher_type.encrypt(memories)

[target_android.send(('EncryptedMemories: ' + buf(hex(x)[2:])).encode()) for x in enc]

target_android.send("Co__mplet_ed".encode())
target_android.close()
s.close()
