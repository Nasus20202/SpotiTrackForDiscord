import requests
from dotenv import load_dotenv
import os

load_dotenv()


def set(bio):
    headers = {
        'Content-Type': 'application/json',
        'Authorization': os.environ["TOKEN"],
    }
    data = '{"bio":"' + str(bio[:190]) + '"\n}'
    try:
        response = requests.patch('https://discord.com/api/v9/users/@me', headers=headers, data=data)
        return response.status_code
    except:
        print("Cannot change Discord Bio")
        return 401