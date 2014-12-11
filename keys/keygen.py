import os, binascii
import qrcode, time
import hmac, hashlib
from Crypto.Cipher import AES

# Generates a random secret key (128 bytes), and returns it
# in hexadecimal.
def generate_key():
	return binascii.hexlify(os.urandom(128))

# Generates a QR code using the data passed in. Then saves it in
# a file with a randomly generated filename, returning the file name.
def make_qr(data):
	img = qrcode.make(data)
	fn = "img/" + binascii.hexlify(os.urandom(32))
	img.save(fn, "png")
	return fn

# Generates a QR code using a given secret key
def generate_code(code, key):
	code = hashlib.sha256(code).digest()
	decryptor = AES.new(code, AES.MODE_ECB)
	key = decryptor.decrypt(binascii.unhexlify(key))
	unix = int(time.time()) / 60
	code = hmac.HMAC(key, str(unix), hashlib.sha512).hexdigest()
	offset = int(code[-1], 16)
	return code[offset:offset + 6]

def encrypt_code(code, key):
	code = hashlib.sha256(code).digest()
	encryptor = AES.new(code, AES.MODE_ECB)
	key = binascii.hexlify(encryptor.encrypt(key))
	return key