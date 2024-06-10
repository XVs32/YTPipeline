
import json

class userCore():
    email = ""

    def __init__(self, email):
        self.email = email 

    def getAuthorizedEmail(self, email):
        
        # Open the JSON file
        with open('./user/authorizeList.json', 'r') as file:
            # Load the JSON data from the file
            authorized_emails = json.load(file)

        # check if the email is in the list
        if email in authorized_emails:
            return authorized_emails[email] 
        else:
            return email

    def getPassword(self):
        return self.password

    def setUsername(self, username):
        self.username = username

    def setPassword(self, password):
        self.password = password

    def __str__(self):
        return "Username: " + self.username + " Password: " + self.password