#Setup
run 'pip install -r requirements.txt'

The tester assumes that the database is empty(Use db.dropDatabase() in the mongo shell to empty a database), and that there is at least one entry in the users document with a token.

#Run
'python testapi.py portno admintoken usertoken'
where portno is the port the server is listening on
admintoken is the ADMIN_TOKEN hardcoded into the api
usertoken is the token of a user in the databse