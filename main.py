import requests


TOKEN = '03e50a2a051c4ba776daf0de24e91ff2a534093b0cca8c0a1c2f6bbc09a116e2'
headers = {"Authorization": TOKEN} 



r_mathes = requests.get("https://lksh-enter.ru/matches",headers = headers)

mathes = r_mathes.json()


r_teams = requests.get("https://lksh-enter.ru/teams",headers = headers)
teams = r_teams.json()


print("DEBUG:",teams)

print("DEBUG:",mathes)
