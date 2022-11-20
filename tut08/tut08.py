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
