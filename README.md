# Install  
pip install pycryptodome

# Running

in root dir of project

"python add_user.py" to add a user to the server

Once a user is added, the user can be verified on the server. 

Open two terminals. 

In both: cd to root dir of project

Client: 

cd to client dir

"python client.py"

Server:

cd to server dir

"python server.py"

If a user is in the server's "database", user will authenticate.

# Additional information

Username is stored as plain text.

Passwords are salted, and salt is stored as plaintext.

Passwords are hashed using SHA256