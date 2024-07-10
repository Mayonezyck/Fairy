import requests
import yaml

def load_secret():
    with open("secret.yaml", "r") as f:
        secret = yaml.safe_load(f)
        return [secret.get('APP_ID'),secret.get('DISCORD')]

APP_ID,DISCORD = load_secret()

url = f"https://discord.com/api/v10/applications/{APP_ID}/commands"
header = {f"Authorization": "Bot {DISCORD}"}
# This is an example CHAT_INPUT or Slash Command, with a type of 1
json = {
    "name": "blep",
    "type": 1,
    "description": "Send a random adorable animal photo",
    "options": [
        {
            "name": "animal",
            "description": "The type of animal",
            "type": 3,
            "required": True,
            "choices": [
                {
                    "name": "Dog",
                    "value": "animal_dog"
                },
                {
                    "name": "Cat",
                    "value": "animal_cat"
                },
                {
                    "name": "Penguin",
                    "value": "animal_penguin"
                }
            ]
        },
        {
            "name": "only_smol",
            "description": "Whether to show only baby animals",
            "type": 5,
            "required": False
        }
    ]
}


r = requests.post(url, headers=header, json=json)
