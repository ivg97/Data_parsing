from vk_api import VkApi
from auth import password, login, token

import json
from pprint import pprint

vk_session = VkApi(token=token)
vk = vk_session.get_api()

account_info = vk.account.getInfo()
account_profile = vk.account.getProfileInfo()
friends = vk.friends.getSuggestions(count=10)

info = {}

info['account_info'] = account_info
info['account_profile'] = account_profile
info['friends'] = friends


with open('my_account_vk.json', 'w') as file_vk:
    json.dump(dict(info), file_vk, indent=4)