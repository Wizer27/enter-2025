import requests
import json
import sys
from dotenv import load_dotenv
import os
load_dotenv()  # Загружает переменные из .env
TOKEN = os.getenv("API_TOKEN")
headers = {"Authorization": TOKEN} 


# матчи
r_mathes = requests.get("https://lksh-enter.ru/matches",headers = headers)
try:  
    mathes = r_mathes.json()
except:
    print("Ошибка")
print(mathes)
# команды
r_teams = requests.get("https://lksh-enter.ru/teams",headers = headers)
teams = r_teams.json()


#print("DEBUG:",teams)
#print(teams)


# вытаскиваю данные с http сервера
teams_info = {}
players = {}

for i in teams:
    r2_t = requests.get(f"https://lksh-enter.ru/teams/{i['id']}",headers = headers)
    try:
        # информация про команды
        team_det = r2_t.json()
    except:
        print("Сервер вернул не JSON. Ответ:", r2_t.text[:100])    
    #print("Статус команды:",r2_t.status_code)
    #print("Текст:",r2_t.text)
    teams_info[team_det["name"]] = {
        "id":team_det["id"],
        "players":team_det["players"]
    }
    for pl_id in team_det["players"]:
        response_player = requests.get(f"https://lksh-enter.ru/players/{pl_id}", headers=headers)
        try: 
            # игроки
            players[pl_id] = response_player.json()
        except:
            print("Что то пошло не так")
# беру только имена и фамилии            
pl = []
for i in players:
    name = players[i].get("name", "").strip()
    surname = players[i].get("surname", "").strip()
    full_name = f"{name} {surname}".strip()
    # если имя сформированно нормально
    if full_name:
        pl.append(full_name)

pl = sorted(set(pl), key=lambda x: x.lower())

# вывод отсортированный
for i in pl:
    print(i)