"""
	server.py - host an SSL server that checks passwords

	CSCI 3403
	Authors: Matt Niemiec and Abigail Fernandes
	Number of lines of code in solution: 140
		(Feel free to use more or less, this
		is provided as a sanity check)

	Put your team members' names:
	
Jordan Smart: josm7269@colorado.edu 
Jonathan Bluhm: jobl6075@colorado.edu 
Laura Kaiser: laka4851@colorado.edu 


"""

import socket
import Crypto 
import sys
import os
import signal
from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.PublicKey import RSA
from Crypto.Hash import SHA256
from pathlib import PureWindowsPath
from sys import exit
from signal import signal, SIGINT
host = "127.0.0.1"
port = 10001

#https://stackoverflow.com/questions/27360218/how-to-close-socket-connection-on-ctrl-c-in-a-python-programme
def signal_handler(signal, frame):
		# close the socket here
		exit(0)

# A helper function. It may come in handy when performing symmetric encryption
def pad_message(message):
	return message + " " * ((16 - len(message)) % 16)


# Write a function that decrypts a message using the server's private key
def decrypt_key(session_key):

	with open(os.path.join(sys.path[0], "private_key"), "r") as f:
		private_key = f.read()

	private_key = RSA.importKey(private_key)
	cipher = PKCS1_OAEP.new(private_key)
	decrypted_key = cipher.decrypt(session_key)	
	return decrypted_key


# Write a function that decrypts a message using the session key
def decrypt_message(client_message, session_key):

	cipher= AES.new(session_key, AES.MODE_ECB)
	return cipher.decrypt(client_message)

# Encrypt a message using the session key
def encrypt_message(message, session_key):

	message = pad_message(message).encode("utf8")
	cipher= AES.new(session_key, AES.MODE_ECB)
	return cipher.encrypt(message)


# Receive 1024 bytes from the client
def receive_message(connection):
	return connection.recv(1024)

# Sends message to client
def send_message(connection, data):
	if not data:
		print("Can't send empty string")
		return
	if type(data) != bytes:
		data = data.encode()
	connection.sendall(data)

# A function that reads in the password file, salts and hashes the password, and
# checks the stored hash of the password to see if they are equal. It returns
# True if they are and False if they aren't. The delimiters are newlines and tabs
def verify_hash(user, password):
	try:
		
		reader = open(os.path.join(sys.path[0], "passfile.txt"), 'r')
		for line in reader.read().split('\n'):
			line = line.split("\t")
			
			if line[0] == user:
				# TODO: Generate the hashed password
				password_and_salt = password+line[1]
				
				hashed_password =SHA256.new(str.encode(password_and_salt)).hexdigest()
				return hashed_password == line[2]
		reader.close()
	except FileNotFoundError:
		print("NO FILE")
		return False
	return False


def main():
	# Set up network connection listener
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	server_address = (host, port)
	print('starting up on {} port {}'.format(*server_address))
	sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	sock.bind(server_address)
	sock.listen(1)

	try:
		
		# Wait for a connection
		print('waiting for a connection')
		connection, client_address = sock.accept()
		try:
			print('connection from', client_address)

			# Receive encrypted key from client
			encrypted_key = receive_message(connection)

			# Send okay back to client
			send_message(connection, "okay")

			# Decrypt key from client
			plaintext_key = decrypt_key(encrypted_key)

			# Receive encrypted message from client
			ciphertext_message = receive_message(connection)

			#decrypt message from client
			decrypted_message = decrypt_message(ciphertext_message,plaintext_key)
			
			print("Encrypted message is:\n"+str(ciphertext_message)+"\n")
			print("Decrypted message is:\n"+decrypted_message.decode("utf-8")+"\n")

			# TODO: Split response from user into the username and password
			split_msg = decrypted_message.split()

			user_name = split_msg[0].decode("utf-8") 
			user_pswd = split_msg[1].decode("utf-8") 

			if verify_hash(user_name,user_pswd) == True:
				success_msg = encrypt_message(pad_message("User Aunthenticated"), plaintext_key)
				send_message(connection, success_msg)
			else:
				fail_msg = encrypt_message(pad_message("User not found"), plaintext_key)   
				send_message(connection,fail_msg)
			
			unencrypted_message = receive_message(connection)
			encrypted_message = receive_message(connection)
			print("Unencrypted message from client: \n"+unencrypted_message.decode("utf-8"))

			print("Encrypted message from client: \n"+str(encrypted_message))

		except KeyboardInterrupt:
			print("Finished with ctrl-c")
			exit(0)
		finally:
			# Clean up the connection
			connection.close()
	except KeyboardInterrupt:
				print("Finished with ctrl-c")
				exit(0)
	finally:
		sock.close()
	print("Server exited successfully!")

if __name__ in "__main__":
	signal(SIGINT, signal_handler)
	main()
