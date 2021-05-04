# Information

Encrypted client server program.
Client sends encrypted symmetric key to server, and server decrypts using PKI.
Then further communication is done via the symmetric key.

The images contain the inital message which is encrypted using PKI.
Then one image shows encryption, while the other shows a message "WIRESHARK" that was sent to the server with no encryption.

The server will print the username and password provided by the client decrypted and encrypted. The client then sends an unencrypted message. The client then encrypts that message and sends to server again. The server prints the encrypted and unencrypted versions. 

User authentication works. This portion was done to show that I can store passwords correctly. The passwords are all in the passfile.txt. The add_user.py is what will add users to the database.

# Install  
- pip install pycryptodome

# Running

- in root dir of project

- "python add_user.py" to add a user to the server

- Once a user is added, the user can be verified on the server. 

- Open two terminals. 

- In both: cd to root dir of project

- Client: 

- cd to client dir

- "python client.py"

- Server:

- cd to server dir

- "python server.py"

- If a user is in the server's "database", user will authenticate.

# Additional information

- Username is stored as plain text.

- Passwords are salted, and salt is stored as plaintext.

- Passwords are hashed using SHA256

- Networking was written by professor, but all the encryption was written by me. I modified some of the networking as well. This was a project assignment for a intro to security course