"""
	client.py - Connect to an SSL server

	CSCI 3403
	Authors: Matt Niemiec and Abigail Fernandes
	Number of lines of code in solution: 117
		(Feel free to use more or less, this
		is provided as a sanity check)

	Put your team members' names: 
	
	Jordan Smart: josm7269@colorado.edu 
Jonathan Bluhm: jobl6075@colorado.edu 
Laura Kaiser: laka4851@colorado.edu 



"""

import socket
import os
import sys
import base64
import Crypto 
from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.PublicKey import RSA

host = "127.0.0.1"
port = 10001

def pad_message(message):
	return message + " "*((16-len(message))%16)

def generate_key():
	#AES has 128 bits or 16 bytes
	return os.urandom(16) 

# Takes an AES session key and encrypts it using the appropriate
# key and return the value
def encrypt_handshake(session_key):

	with open(os.path.join(sys.path[0], "public_key.pub"), "r") as f:
		public_key = f.read()        
	
	public_key = RSA.importKey(public_key)
	cipher = PKCS1_OAEP.new(public_key)
	encrypted_key = cipher.encrypt(session_key)
	
	return encrypted_key

# Encrypts the message using AES. Same as server function
def encrypt_message(message, session_key):

	message = pad_message(message).encode("utf8")
	cipher= AES.new(session_key, AES.MODE_ECB)
	return cipher.encrypt(message)

# Decrypts the message using AES. Same as server function
def decrypt_message(message, session_key):

	cipher= AES.new(session_key, AES.MODE_ECB)

	return cipher.decrypt(message)


# Sends a message over TCP
def send_message(sock, message):
	sock.sendall(message)


# Receive a message from TCP
def receive_message(sock):
	data = sock.recv(1024)
	return data


def main():
		
	user = input("What's your username? ")
	password = input("What's your password? ")

	# Create a TCP/IP socket
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

	# Connect the socket to the port where the server is listening
	server_address = (host, port)
	print('connecting to {} port {}'.format(*server_address))
	sock.connect(server_address)
	try:
		# Message that we need to send
		message = user + ' ' + password

		# Generate random AES key
		key = generate_key()

		# Encrypt the session key using server's public key
		encrypted_key = encrypt_handshake(key)

		# Initiate handshake
		send_message(sock, encrypted_key)

		# Listen for okay from server
		if receive_message(sock).decode() != "okay":
			print("Couldn't connect to server")
			exit(0)
		
		# We now use symmetric key to encrypt

		#send user name and password to server
		encrypted_msg = encrypt_message(message,key)
		send_message(sock, encrypted_msg)

		auth_result = decrypt_message(receive_message(sock), key)
		print(auth_result.decode("utf-8"))

		last_message = "sent from client no encryption"
		send_message(sock, last_message.encode())

		last_message_encrypted = encrypt_message(last_message, key)

		send_message(sock, last_message_encrypted)

	finally:
		print('closing socket')
		sock.close()


if __name__ in "__main__":
	main()
