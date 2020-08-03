import os
from Crypto.Cipher import AES
def decryptFile(decrypter, origin):
    with open(origin, "rb") as handle:
        content = handle.read()
    if not os.path.exists('decrypted'):
        os.makedirs('decrypted')
    with open(os.path.join('decrypted', origin), "wb+") as handle:
        handle.write(decrypter.decrypt(content))


for file in os.listdir():
    if file.endswith('.ts'):
        key_file = os.path.join(file.split('.')[0]+'.key')
        with open(key_file, 'rb') as handle:
            key_content = handle.read()
        decrypter = AES.new(key_content, AES.MODE_CBC, IV=key_content)
        if file.endswith('.ts'):
            decryptFile(decrypter, file)