'''
Possible improvements:
-Remove duplicates
-move day count to config.txt
'''

import facebook
import schedule
import random
import time
import os
from urllib.parse import urlparse

graph_api_version = "v5.0"

with open('config.txt', 'r') as f:
    lines = f.readlines()
f.close()

params = []
for line in lines:
    l2 = line.strip('\n')
    params.append(l2.split(': '))
values = list(zip(*params))[1]

facebook_page_id = values[0]
app_id = values[1]
app_secret = values[2]
user_short_token = values[3]
path = values[4]
text = values[5]
day = values[6]
canvas_url = values[7]

#Get facebook authentication:
import requests
access_token_url = "https://graph.facebook.com/{}/oauth/access_token?grant_type=fb_exchange_token&client_id={}&client_secret={}&fb_exchange_token={}".format(graph_api_version, app_id, app_secret, user_short_token)

r = requests.get(access_token_url)
print(access_token_url)

access_token_info = r.json()
user_long_token = access_token_info['access_token']
print(user_long_token)

#user_access_token = ""
graph = facebook.GraphAPI(user_long_token)
#Replace this id when ready to publish

perms = ["manage_pages","publish_pages"]
fb_login_url = graph.get_auth_url(app_id, canvas_url, perms)
print(fb_login_url)

token_url = urlparse("https://graph.facebook.com/oauth/client_code?access_token="+user_long_token+"&client_secret="+app_secret+"&redirect_uri="+canvas_url+"&client_id="+app_id)
#print(token_url)
#code = graph.get_object(id = token_url, fields = "code")
#print(code)

# Select a random picture to post:

def chooserandompic():

    files = os.listdir(path)
    index = random.randrange(0, len(files))
    image = path + r"\\" + str(files[index])
    print(image)
    return image

def PostImage(image_path):

    day = open("day.txt", "r")
    current_day = int(day.read())

    caption = text + str(current_day)
    graph.put_photo(image=open(image_path, 'rb'), message=caption, album_path= facebook_page_id + "/photos")

    day.close()

    next_day = current_day + 1

    #overwrite the day for tomorrow:
    with open("day.txt", "w") as overwrite:
        overwrite.write(str(next_day))
        overwrite.close()

#schedule module doesn't like to schedule a job with a different parameter every time:
def Final():
    return PostImage(chooserandompic())

PostImage(chooserandompic())
#Schedule the post
try:
    schedule.every(1).minutes.do(chooserandompic)
    schedule.every(1).minutes.do(Final)
except KeyError:
    print("Replace long-term key: https://developers.facebook.com/tools/accesstoken/")

while True:
    schedule.run_pending()
    time.sleep(5)