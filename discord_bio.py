import requests
from dotenv import load_dotenv
import unicodedata
import os

load_dotenv()


def strip_accents(s):
   return ''.join(c for c in unicodedata.normalize('NFD', s)
                  if unicodedata.category(c) != 'Mn')
                  
def set(bio):
    headers = {
        'Content-Type': 'application/json',
        'Authorization': os.environ["TOKEN"],
    }
    data = '{"bio":"' + strip_accents(str(bio[:190])) + '"\n}'
    try:
        response = requests.patch('https://discord.com/api/v9/users/@me/profile', headers=headers, data=data, timeout=3)
        return response.status_code
    except:
        print("Cannot change Discord Bio")
        return 401
