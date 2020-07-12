"""Code to validate members from a group.
If members didn't follow instructions,
those can be found and then removed from group"""

import csv
from Model import CheckUserInGroup
from ScrapGroupMembers import CreateClient

client = CreateClient()

with open("members.csv", encoding='UTF-8') as f:
    csv_reader = csv.reader(f)
    #writer.writerow(['username','user id', 'access hash','name','group', 'group id'])
    for user in csv_reader:
        userID = user[1]
        groupID = user[5]
        status, isBot = CheckUserInGroup(userID, groupID)
        if status:
            # user present
            if isBot:
                print(f'User ID : {userID} | Name : {user[3]} in Group {user[4]} is bot')
        else:
            # user not present
            print(f'User ID : {userID} | Name : {user[3]} in Group {user[4]} did not checkin')
            # client.send_message(userID, f'Please checkin in group {user[4]} else you will be kicked out in few days.')
