import requests
from private import keys

payload = {
    'context': "hello"
}

header = {
    'authorization': keys.TOKEN
}
channel = "https://discord.com/api/v9/channels/846778354157355109/messages"

r = requests.post(channel, data=payload, headers=header)
