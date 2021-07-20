import requests
import json


class User:
    # Variables for the api
    url = 'https://authserver.mojang.com'
    client_token = "default"
    post_headers = {'Content-Type': 'application/json'}
    get_headers = {}
    # Variables to hold user info.
    username = None
    profileName = None
    password = None
    access_token = None
    userId = None
    profileId = None  # Same as User UUID
    # Initialise the user with the username and password.

    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.AuthenticateUser(username, password)

    def AuthenticateUser(self, username, password):
        # Create the body payload to pass in the http request.
        payload = {
            "agent": {
                "name": "Minecraft",
                "version": 1
            },
            "username": username,
            "password": password,
            "clientToken": "default",
            "requestUser": True
        }
        # Capture the response from the http request.
        response = requests.post(
            self.url+"/authenticate", data=json.dumps(payload), headers=self.post_headers)
        # If the response is an error throw the error.
        if 'error' in response.text:
            raise Exception(json.loads(response.text)['errorMessage'])
        else:
            return True

    def Signout(self):
        payload = {
            "username": self.username,
            "password": self.password
        }
        response = requests.post(
            self.url + "/signout", data=json.dumps(payload), headers=self.post_headers)
        if "error" in response.text:
            raise Exception('\n\n'+json.loads(response.text)
                            ['error']+'\n'+json.loads(response.text)['errorMessage']+'\n\n')
        print("Sucessfully Signed Out")

    def ShowUserObject(self):
        payload = {
            "agent": {
                "name": "Minecraft",
                "version": 1
            },
            "username": self.username,
            "password": self.password,
            "clientToken": "default",
            "requestUser": True
        }
        response = requests.post(
            self.url+"/authenticate", data=json.dumps(payload), headers=self.post_headers)
        print(json.dumps(json.loads(response.text), indent=4))

    def ShowAccessToken(self):
        print(self.access_token)

    # Doesn't work. Gives an error saying acecss token already has user attached.

    def RefressAccessToken(self):
        payload = {
            "accessToken": self.access_token,
            "clientToken": self.client_token,
            "selectedProfile": {
                "id": self.profileId,
                "name": self.profileName
            },
            "requestUser": True
        }
        response = requests.post(
            self.url + "/refresh", data=json.dumps(payload), headers=self.post_headers)
        if "error" in response.text:
            raise Exception('\n\n'+json.loads(response.text)
                            ['error']+'\n'+json.loads(response.text)['errorMessage']+'\n\n')
        self.access_token = json.loads(response.text)['accessToken']
        self.userId = json.loads(response.text)['user']['id']
        self.profileId = json.loads(response.text)['selectedProfile']['id']
        self.profileName = json.loads(response.text)[
            'availableProfiles'][0]['name']

    def GetUserNameHistory(self):
        response = requests.get(
            'https://api.mojang.com/user/profiles/'+self.profileId+'/names')
        if 'error' in response.text:
            raise Exception('\n\n'+json.loads(response.text)
                            ['errorMessage']+'\n\n')
        print("\nYour name history:")
        jsonObject = json.loads(response.text)
        for i in json.loads(response.text):
            if 'name' in i:
                print(i['name'])

        print('\n')

    def ChangeUsername(self):
        response = None
        while(True):
            newName = input(
                "What would you like to change your username to?: ")
            response = requests.get('https://api.minecraftservices.com/minecraft/profile/name/'+str(
                newName)+'/available', headers={"Authorization": "Bearer " + self.access_token})
            if not response.ok:
                print("Error\n\n")
                return
            if json.loads(response.text)['status'] == 'DUPLICATE':
                print("This is taken, try another.")
            else:
                break
            confirmation = input(
                'Are you sure you want to change your name to "'+newName+'"? y/n')
            if confirmation == 'n':
                print("Canceling Operation...\n\n")
                return
            elif confirmation != 'y':
                print("Invalid input, canceling operation...\n\n")
                return
            response = requests.put('https://api.minecraftservices.com/minecraft/profile/name/'+str(newName), headers={"Authorization": "Bearer " + self.access_token})
            if response.ok:
                print("Name has been changed.\n\n")
            else:
                print(json.loads(response.text)['error']+": "+json.loads(response.text)['details']['status']+'\n\n')