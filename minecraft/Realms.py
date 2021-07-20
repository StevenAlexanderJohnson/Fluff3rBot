import json

from requests.api import head
from Authenticate import User
import requests

class Realms:
    def __init__(self, user):
        self.user = user
        self.cookie = {
            "sid": "token:"+user.access_token+":"+user.profileId,
            "user": user.profileName,
            "version": '1.17.1'
        }
        self.header = {
            "Cache-Control": "no-cache",
            "Pragma": "no-cache",
            "User-Agent": "Java/1.16.0_27",
            "Host": "pc.realms.minecraft.net",
            "Accept": "text/html, image/gif, image/jpeg, *; q=.2, */*; q=.2",
            "Connection": "keep-alive",
            "Content-Type": "application/json"
        }

    def RealmsInterface(self):
        actionOptions = {
            '2': lambda: self.GetUserOwnedWorlds(),
            '3': lambda: self.GetSubscriptionDaysLeft(),
            '4': lambda: self.GetIP(),
            '5': lambda: self.GetOPs(),
            '6': lambda: self.InvitePlayer(),
            '7': lambda: self.KickPlayer()
        }
        while(True):
            print("\n\t\tRealms Portal")
            print('1. Back\t\t\t2. Current Activity')
            print('3. Get Days Left\t4. Get Server IP')
            print('5. Get OPs\t\t6. Invite Player')
            print('7. Kick Player')
            selected = input()
            if(selected == '1'):
                print('Going back\n\n')
                break
            func = actionOptions.get(selected, lambda: print("Invalid Option\n\n"))
            func()

    def GetUserOwnedWorlds(self):
        response = requests.get('https://pc.realms.minecraft.net/worlds', cookies=self.cookie, headers=self.header)
        # print(json.dumps(json.loads(response.text), indent=4))
        # worldId = json.loads(response.text)["servers"][0]["id"]
        for world in json.loads(response.text)['servers']:
            if(world['owner'] == self.user.profileName):
                print('\n' + world['name'] + ": " + str(world['players'] if world['players'] != None else 0) + ' out of ' + str(world['maxPlayers']) + ' connected\n\n')

    
    def GetSubscriptionDaysLeft(self):
        # Holds the world name and ID for later
        worldDictionary = {}
        # Get list of worlds user owns
        response = requests.get('https://pc.realms.minecraft.net/worlds', cookies=self.cookie, headers=self.header)
        if response.ok:
            index = 1
            print("Which Realm do you want to check.")
            for world in json.loads(response.text)['servers']:
                worldDictionary.update({world['name'].lower(): world['daysLeft']})
                worldDictionary.update({str(index): world['daysLeft']})
                print(str(index) + '. ' + world['name'])
        else:
            print(response['errorMessage'] + '\n\n')
            return
        selected = input().lower()
        print('\nYou have '+ str(worldDictionary.get(selected, lambda: print("Invalid Input"))) + ' day(s) left on your subscription.\n\n')

    def GetIP(self):
        # Holds the world name and ID for later
        worldDictionary = {}
        # Get list of worlds user owns
        response = requests.get('https://pc.realms.minecraft.net/worlds', cookies=self.cookie, headers=self.header)
        if response.ok:
            index = 1
            print("Which Realm do you want to check.")
            for world in json.loads(response.text)['servers']:
                worldDictionary.update({world['name'].lower(): world['id']})
                worldDictionary.update({str(index): world['id']})
                print(str(index) + '. ' + world['name'])
                index += 1
        else:
            print(response['errorMessage'] + '\n\n')
            return
        selected = input().lower()
        if selected not in worldDictionary:
            print('\nInvalid input\n\n')
            return
        response = requests.get('https://pc.realms.minecraft.net/worlds/v1/'+str(worldDictionary.get(selected))+'/join/pc', cookies=self.cookie, headers=self.header)
        if response.ok:
            jsonResponse = json.loads(response.text)
            print('\n' + jsonResponse['address'] + '\n\n')
        else:
            print('\n\n' + response.reason + '\n\n')
            return
    
    def GetOPs(self):
        # Holds the world name and ID for later
        worldDictionary = {}
        # Get list of worlds user owns
        response = requests.get('https://pc.realms.minecraft.net/worlds', cookies=self.cookie, headers=self.header)
        if response.ok:
            index = 1
            print("Which Realm do you want to check.")
            for world in json.loads(response.text)['servers']:
                worldDictionary.update({world['name'].lower(): world['id']})
                worldDictionary.update({str(index): world['id']})
                print(str(index) + '. ' + world['name'])
        else:
            print(response['errorMessage'] + '\n\n')
            return
        selected = input().lower()
        if selected not in worldDictionary:
            print('\nInvalid input\n\n')
            return
        response = requests.get('https://pc.realms.minecraft.net/ops/'+str(worldDictionary.get(selected)), cookies=self.cookie, headers=self.header)
        if response.ok:
            print("\nOperators")
            jsonResponse = json.loads(response.text)
            for op in jsonResponse['ops']:
                response = requests.get('https://api.mojang.com/user/profiles/'+ op + '/names')
                print(json.loads(response.text)[-1]['name'])
            print('\n\n')
        else:
            print('\n\n' + response.reason + '\n\n')
            return
    
    def InvitePlayer(self):
        username = input("\nWho are you wanting to invite?: ")
        validate = input('\nMake sure that \'' + username + '\' is the correct username. y/n')
        if validate == 'n':
            print("Canceling Operation...\n\n")
            return
        elif validate != 'y':
            print("Invalid Reponse. Canceling Operation...\n\n")
            return
        response = requests.get('https://pc.realms.minecraft.net/worlds', cookies=self.cookie, headers=self.header)
        # Holds the world name and ID for later
        worldDictionary = {}
        if response.ok:
            index = 1
            print("Which Realm do you want to invite '" + username + " to?.")
            for world in json.loads(response.text)['servers']:
                worldDictionary.update({world['name'].lower(): world['id']})
                worldDictionary.update({str(index): world['id']})
                print(str(index) + '. ' + world['name'])
        else:
            print(response['errorMessage'] + '\n\n')
            return
        worldName = input().lower()
        if worldName not in worldDictionary:
            print('\nInvalid input\n\n')
            return
        response = requests.get('https://api.mojang.com/users/profiles/minecraft/' + username)
        userId = json.loads(response.text)['id']
        payload = {
            "name": str(username),
            "uuid": str(userId),
            "operator": False,
            "accepted": False,
            "online": False
        }
        response = requests.post('https://pc.realms.minecraft.net/invites/' + str(worldDictionary[worldName]), cookies=self.cookie, data=json.dumps(payload), headers=self.header)
        if response.ok:
            print("Invite Sent \n\n")
        else:
            print(response.reason + '\n\n')
    
    def KickPlayer(self):
        response = requests.get('https://pc.realms.minecraft.net/worlds', cookies=self.cookie, headers=self.header)
        # Holds the world name and ID for later
        worldDictionary = {}
        if response.ok:
            index = 1
            print("Which Realm do you want to kick a player from?: ")
            for world in json.loads(response.text)['servers']:
                worldDictionary.update({world['name'].lower(): world['id']})
                worldDictionary.update({str(index): world['id']})
                print(str(index) + '. ' + world['name'])
                index += 1
        else:
            print(response['errorMessage'] + '\n\n')
            return
        worldName = input().lower()
        if worldName not in worldDictionary:
            print('\nInvalid input\n\n')
            return
        response = requests.get('https://pc.realms.minecraft.net/worlds/' + str(worldDictionary[worldName]), cookies=self.cookie, headers=self.header)
        if not response.ok:
            print(response.reason + '\n\n')
            return
        print("Which player do you want to kick?")
        userDictionary = {}
        index = 1
        for user in json.loads(response.text)['players']:
            userDictionary.update({str(user['name']).lower(): user['uuid']})
            userDictionary.update({str(index) : user['uuid']})
            print(str(index) + '. ' + user['name'])
            index += 1
        selectedUser = input().lower()
        if selectedUser not in userDictionary:
            print("Invalid Input. Canceling opration...\n\n")
            return
        confirm = input(userDictionary[selectedUser] + ' is the user you want to kick? y/n: ')
        if confirm == 'n':
            print("Canceling opration...\n\n")
            return
        if confirm != 'y':
            print("Invalid Input. Canceling opration...\n\n")
            return
        response = requests.delete('https://pc.realms.minecraft.net/invites/' + str(worldDictionary[worldName]) + '/invite/' + str(userDictionary[selectedUser]), cookies=self.cookie, headers=self.header)
        if response.ok:
            print("User has been kicked.\n\n")
            return
        else:
            print(response.reason)
            return