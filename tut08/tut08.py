import os
import pandas as pd
import re
from datetime import datetime
os.system('cls')

start_time = datetime.now()

def scorecard():
    try:
        try:
            #create blank output file
            outputfile = 'Scorecard.txt'
            f = open(outputfile, "w")
            f.write("")
            f.close()
        except FileNotFoundError:
            print('Input file not found :', outputfile)
            exit()
        except:
            print('Error in file: Could not open ', outputfile)
            exit()

        try:
            # open and read teams file to extract player list
            teams = open('teams.txt', 'r')
            players = []
            for i in teams.readlines():
                    i = i.strip()
                    if len(i) > 0:
                        players.append(i)

            teams.close()
        except FileNotFoundError:
            print('Input file not found :', teams)
            exit()
        except:
            print('Error in file: Could not open ', teams)
            exit()

        team1, team2 = players[0], players[1]
        
        #player list of team 1 and team 2
        players1 = []
        for i in team1.split(":")[1].split(','):
            players1.append(i.strip())

        players2 = []
        for i in team2.split(":")[1].split(','):
            players2.append(i.strip())

        try:
            #open and read pak_inns1 file and remove all empty lines
            pak_inns = open('pak_inns1.txt', 'r')
            inns1comm = []
            for i in pak_inns.readlines():
                    i = i.strip()
                    if len(i) > 0:
                        inns1comm.append(i) 
            pak_inns.close()

        except FileNotFoundError:
            print('Input file not found :', pak_inns)
            exit()
        except:
            print('Error in file: Could not open ', pak_inns)
            exit()

        try:
            #open and read india_inns2 file and remove all empty lines
            ind_inns = open('india_inns2.txt', 'r')
            inns2comm = []
            for i in ind_inns.readlines():
                    i = i.strip()
                    if len(i) > 0:
                        inns2comm.append(i) 
            ind_inns.close()
        
        except FileNotFoundError:
            print('Input file not found :', ind_inns)
            exit()
        except:
            print('Error in file: Could not open ', ind_inns)
            exit()

        #empty dictionary for batting and bowling data
        bat = {}
        bowl = {}
        
        #dictionary for batsman
        dict1 = {
                    'out': 'not out', 
                    'R': 0, 
                    'B': 0, 
                    '4s': 0, 
                    '6s': 0, 
                    'SR': 0
                    }

        #dictionary for bowler
        dict2 = {
                    'O': 0, 
                    'M': 0, 
                    'R': 0, 
                    'W': 0, 
                    'NB': 0, 
                    'WD': 0, 
                    'ECO': ''
                    }

        #defining other variables for extras, wickets, total, balls and powerplay
        extras, total, wkts, balls = 0, 0, 0, 0
        nbr, lbr, br, wdr = 0, 0, 0, 0
        fallwkts, wickets = [], 0
        ppo, ppr, ppb = 0, 0, 0

        #name of teams Pakistan and India
        pak = team1.split(" ")[0]
        ind = team2.split(" ")[0]
        
        #iterating for each inning
        for inning in [inns1comm, inns2comm]:
            #clearing for next inning
            bat.clear()
            bowl.clear()

            extras = 0
            total = 0 
            wkts = 0
            balls = 0

            nbr = 0
            lbr = 0 
            br = 0 
            wdr = 0
            fallwkts = [] 
            wickets = 0

            ppo = 0
            ppr = 0
            ppb = 0 

            #iterating for each ball in an inning
            for ball in inning:
                if len(ball) == 0:
                    continue
                
                #separating batsman and bowler from commentary 
                ball = ball.strip()
                bowler = ball.split('to', 1)[0].split(' ', 1)[1].strip()
                batsman = ball.split('to', 1)[1].split(',', 1)[0].strip()
                case = re.search('[^,]+,([\w\s]+)[,|!!]', ball).group(1).lower().strip()

                #matching the name from player list
                for player in players1:
                    if batsman in player:
                        batsman = player.strip()
                for player in players2:
                    if bowler in player:
                        bowler = player.strip()
                
                #addition of names in scorecard
                if (batsman not in bat.keys()):
                    bat[batsman] = dict1.copy()
                if (bowler not in bowl.keys()):
                    bowl[bowler] = dict2.copy()
                
                

from platform import python_version
ver = python_version()

if ver == "3.8.10":
	print("Correct Version Installed")
else:
	print("Please install 3.8.10. Instruction are present in the GitHub Repo/Webmail. Url: https://pastebin.com/nvibxmjw")

scorecard()

#This shall be the last lines of the code.
end_time = datetime.now()
print('Duration of Program Execution: {}'.format(end_time - start_time))
