from Crypto.PublicKey import RSA

key = RSA.generate(2048)
f = open('mykey.pem','wb')
f.write(key.exportKey('PEM'))
f.close()

f = open('public_key_test.pub','r')
key = RSA.importKey(f.read())

print(key)

