import requests
import json
import sys
from dotenv import load_dotenv
import os
from prettytable import PrettyTable





load_dotenv()  # Загружает переменные из .env
TOKEN = os.getenv("API_TOKEN")
headers = {"Authorization": TOKEN} 

# матчи

r_mathes = requests.get("https://lksh-enter.ru/matches",headers = headers)
if r_mathes.status_code != 200:
    print("Ошибка сервера:", r_mathes.status_code)
    sys.exit(1)
try:  
    mathes = r_mathes.json()
except:
    print("Ошибка")
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
all_camands = [
    ['stats? "Название команды" ', "Выведет статистику команды"],
    ["versus? player1 player2", "Выведет статистику игроков друг против друга"]
]  
table = PrettyTable(["Команда","Что делает"])
for i in all_camands:
    table.add_row(i)
print(table)   

    
#print(mathes)    
while True:
    command = input("Введите команду: ")
    if "stats?" in command and '"' in command: 
        team = command.split('"')[1]
        if team not in teams_info:
            print("0 0 0")
            continue
        else:
           #print("Каманда есть в teams_info")
           team_id = teams_info[team]["id"]
           wins = 0
           loses = 0
           goals_rz = 0
            
           for match in mathes:
                if match["team1"] == team_id:
                    #print(f"Каманда {team} - это team1 ")
                    if match["team1_score"] > match["team2_score"]:
                        wins += 1
                    if match["team1_score"] < match["team2_score"]:
                        loses += 1   
                    goals_rz += (match["team1_score"] - match["team2_score"])       
                if match["team2"] == team_id:
                    #print(f"Каманда {team} - это team2 ")
                    if match["team2_score"] > match["team1_score"]:
                        wins += 1
                    if match["team2_score"] < match["team1_score"]:
                        loses += 1  
                    goals_rz += (match["team2_score"] - match["team1_score"])     
           formatted_diff = f"+{goals_rz}" if goals_rz > 0 else str(goals_rz)
           print(f"{wins} {loses} {formatted_diff}")
    if "versus?" in command:
        
        
        com = command.split()
        if len(com) < 3:
            print("Ошибка ввода")
        else:    
            try:
                
                id1 = int(com[1])
                id2 = int(com[2])
                if id1 < 0 or id2 < 0:
                    raise ValueError
            except:
                print("Ошибка ввода")    
            res = []
            
           
                
            if id1 not in players or id2 not in players:
                print('0')
                continue
            # команды первого игрока
            pl1_teams = []
            for tems_name in teams_info:
                if id1 in teams_info[tems_name]["players"]:
                        pl1_teams.append(teams_info[tems_name]["id"])
                # команды второго игрока
            pl2_teams = []  
            for team_name in teams_info:
                if id2 in teams_info[team_name]["players"]:
                    pl2_teams.append(teams_info[team_name]["id"])
            #print(f"Команды первого игрока {pl1_teams}") тестовые print
            #print(f"Команды второго игрока {pl2_teams}") 
            mathc_count = 0 
            for match in mathes:
                if ((match["team1"] in pl1_teams) and (match["team2"] in pl2_teams ) and (pl2_teams != pl1_teams)) or (match["team1"] in pl1_teams and match["team1"] in pl2_teams):
                    mathc_count += 1
                elif (match["team1"] in pl2_teams) and (match["team2"] in pl1_teams) and (pl2_teams != pl1_teams) or (match["team2"] in pl1_teams and match["team2"] in pl2_teams):
                    mathc_count += 1
            print(mathc_count)        
    elif  ("versus?" not  in command) and ( "stats?" not in command and '"' not  in command):
        print("Команда не распознана")             
                  
           
               
