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
print(key)
iv = target_android.recv(16)
print(iv)

cipher_type = AES.new(key, AES.MODE_CFB, iv)
enc = cipher_type.encrypt(memories)

for x in enc:
    tmpstr = 'EncryptedMemories: ' + buf(hex(x)[2:])
    print(tmpstr)
    target_android.send(tmpstr.encode())

target_android.send("Co__mplet_ed".encode())
target_android.close()
s.close()
