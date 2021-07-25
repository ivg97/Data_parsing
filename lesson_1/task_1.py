import requests
from github import Github

import json
username = 'ivg97'
url = f'https://api.github.com/users/{username}'

response = requests.get(url).json()

print(f'\tGithub user: {response["name"]}\n{("-") * 30} \n Url ty repository: {response["repos_url"]}\n')


git = Github()
user = git.get_user(username)
repo_lst = []
response_for_json = {'name': response["name"], 'repository': {}}
for repository in user.get_repos():
    repo_lst.append({repository.name: {'full_name': repository.full_name, 'url': repository.url}})
    print(f'*\t{repository.name} | {repository.full_name} | {repository.url}')

response_for_json['repository'] = repo_lst




with open('data_git.json', 'w') as write_data_git_json:
    json.dump(dict(response_for_json), write_data_git_json, indent=4)