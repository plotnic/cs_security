import os, binascii
import qrcode, time
import hmac, hashlib

def generate_key():
	return binascii.hexlify(os.urandom(128))

def make_qr(data):
	img = qrcode.make(data)
	fn = "img/" + binascii.hexlify(os.urandom(32))
	img.save(fn, "png")
	return fn

def generate_code(key):
	unix = int(time.time()) / 60
	code = hmac.HMAC(key, str(unix), hashlib.sha512).hexdigest()
	offset = int(code[-1], 16)
	return code[offset:offset + 6]