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

                #case of other runs scored including zero
                if ('run' in case and 'out' not in case):
                    if (case.split()[0] == 'no'): 
                        bat[batsman]['R'] += 0
                        bowl[bowler]['R'] += 0
                    else:
                        bat[batsman]['R'] += int(case.split()[0])
                        bowl[bowler]['R'] += int(case.split()[0])  

                #case of 4
                elif (case == 'four'):
                    bat[batsman]['R'] += 4
                    bat[batsman]['4s'] += 1
                    bowl[bowler]['R'] += 4  
                
                #case of 6
                elif (case == 'six'):
                    bat[batsman]['R'] += 6 #scored by batsman
                    bat[batsman]['6s'] += 1 #6 tally increased by 1
                    bowl[bowler]['R'] += 6 #added to bowlers account
                
                #case of wide and wide+runs
                elif ('wide' in case):
                    if ('wides' in case):
                        wdr += int(case[0])
                        bowl[bowler]['R'] += int(case[0]) #added to bowlers runs tally
                        bowl[bowler]['WD'] += int(case[0]) #added to bowlers wides tally
                    else:
                        wdr += 1
                        bowl[bowler]['R'] += 1
                        bowl[bowler]['WD'] += 1

                #case of wickets   
                elif ('out' in case):
                    bowl[bowler]['W'] += 1 #added to bowlers wkt tally
                    if ('bowled' in case): #bowled case
                        bat[batsman]['out'] = 'b ' + bowler

                    elif ('caught' in case):
                        c = case.lower().split('by')[-1].strip()
                        for player in players2:
                            if c in player:
                                c = player.strip() #getting full name of bowler from players list
                        bat[batsman]['out'] = 'c ' + c + ' b ' + bowler #caught and bowled by different people

                    elif ('caught' in case and 'bowled' in case): #caught and bowled case
                        bat[batsman]['out'] = 'c and b ' + bowler

                    elif ('lbw' in case):
                        bat[batsman]['out'] = 'lbw b ' + bowler #lbw case

                    elif ('run' in case):
                        bowl[bowler]['W'] -= 1 #runout does not go in bowlers wkt tally
                        current = re.search('[^!]+!!\s+(\d).+', ball).group(1).strip()
                        bat[batsman]['R'] += int(current) #adding runs to batsman before getting runout
                        dismissed = case.lower().split()[1].strip()
                        for player in players1:
                            if dismissed in player:
                                dismissed = player.strip() #geting full name of thrower from players list
                        throw = re.search('\(([^\(\)]+)\)\s+[\d\s\(\)]+\[.+\]$', ball).group(1).strip()
                        bat[dismissed]['out'] = 'run out (' + throw + ')' #run out case

                eve = re.search('[^,]+,?([^,]+),?([\w\s]+)[,|!!]', ball)
                #case of byes and leg byes
                if ('bye' in eve.group(1).lower().strip()):
                    current = eve.group(2).lower().strip()

                    if ('four' == current):
                        current = 4

                    elif ('six' == current):
                        current = 6

                    elif ('run' in current):
                        current = int(current[0])

                    if ('leg' in eve.group(1).lower().strip()):
                        lbr += current

                    else:
                        br += current

                #case of no ball
                if ('no ball' in eve.group(1).lower().strip()):
                    current = eve.group(2).lower().strip()
                    
                    if ('four' == current):
                        current = 4
                        bat[batsman]['4s'] += 1

                    elif ('six' == current):
                        current = 6
                        bat[batsman]['6s'] += 1

                    elif ('run' in current):
                        current = int(nbr[0])
                        
                    nbr += 1
                    bat[batsman]['R'] += current
                    bowl[bowler]['R'] += current + 1

                if ('wide' not in case and 'no ball' not in case):
                    bat[batsman]['B'] += 1
                    bowl[bowler]['O'] += 1

                    #balls in powerplay
                    if (float(ball.split(' ')[0].strip()) < 6.1):
                        ppb += 1

                if ('out' in case):
                    wickets += 1
                    extras = br + lbr + wdr + nbr #extras is sum of nb, wd, byes and legbyes
                    temp = pd.DataFrame.from_dict(bat, orient='index').sum(axis='index')['R']
                    num = ball.split(' ')[0].strip()
                    fallwkts.append(f'{temp + extras}-{wickets} ({batsman}, {num})') #fall of wickets

                if (float(ball.split(' ')[0].strip()) < 6.1):
                    var1 = int(pd.DataFrame.from_dict(bat, orient='index').sum(axis='index')['R']) #runs in powerplay excluding extras
                    var2 = br + lbr + wdr + nbr #extras in powerplay
                    ppr = var1 + var2 #total runs in powerplay
            
            #switching for next inning
            players1, players2 = players2, players1
            
            #calculating bowler economy and overs bowled
            for key in bowl.keys():
                bowl[key]['ECO'] = round(6.00*bowl[key]['R'] / bowl[key]['O'], 1)
                bowl[key]['O'] = bowl[key]['O'] // 6.00 + (bowl[key]['O']%6.00) / 10
            
            #calculating batsman strike rate
            for key in bat.keys():
                bat[key]['SR'] = round(100* bat[key]['R'] / bat[key]['B'], 2)
            
            #separate dataframes from batting and bowling
            df1 = pd.DataFrame.from_dict(bat, orient='index')
            df2 = pd.DataFrame.from_dict(bowl, orient='index')
            
            df1_total = df1.sum(axis='index')
            df2_total = df2.sum(axis='index')

            #total runs, wkts and balls in the inning
            total = int(df1_total['R'])
            wkts = int(df2_total['W'])
            balls = df2_total['O']
            
            #row for extras and total score
            extras = br + lbr + wdr + nbr
            e = f'{extras} (b:{br}, lb:{lbr}, w:{wdr}, nb:{nbr})'
            t = f'{extras+total} ({wkts} wkts, {balls} Ov)'
            
            df1.loc['Extras'] = ['', e, '', '', '', '']
            df1.loc['Total'] = ['', t, '', '', '', '']

            df1.reset_index(inplace=True)
            df1.rename(columns={'index':'Batsman'}, inplace=True)

            df2.reset_index(inplace=True)
            df2.rename(columns={'index':'Bowler'}, inplace=True)

            outputfile = 'Scorecard.txt'

            #appending in outputfile
            with open(outputfile, "a+") as text_file:

                #batting stats
                sr = df1.to_markdown(tablefmt='plain', index=False).split('\n')
                l = int(len(sr[0]))
                pak += ' Innings' #innings heading
                score = f'{extras+total}-{wkts} ({balls} Ov)'

                print(f'{pak:<{l//2}}' + f'{score:>{l//2}}', file = text_file)
                print('', file = text_file)
                
                for i in sr:
                    print(i, file = text_file)

                print('', file = text_file)
                
                #batsman who did not bat
                if (wkts != 10):
                    print('Did not Bat', file = text_file)
                    temp = []

                    for player in players2:
                        if player not in df1['Batsman'].to_list():
                            temp.append(player) # getting full name from players list

                    print(', '.join(temp), file = text_file)
                    print('', file = text_file)
                
                #fall of wkts
                print('Fall of Wickets', file = text_file)
                print(', '.join(fallwkts), file = text_file)
                print('', file = text_file)

                #bowling stats
                bowlerstats = df2.to_markdown(tablefmt='plain', index=False).split('\n')
                
                for i in bowlerstats:
                    print(i, file = text_file)
                print('', file = text_file)

                #pp stats
                ppo = ppb // 6.00 + (ppb % 6.00) / 10
                print(format('Powerplays', f'<{l//3}') + format('Overs', f'^{l//3}') + format('Run', f'>{l//3}'), file = text_file)
                print(format('Mandatory', f'<{l//3}') + format(f'0.1-{ppo}', f'^{l//3}') + format(f'{ppr}', f'>{l//3}'), file = text_file)
                print('', file = text_file)
                
            pak, ind = ind, pak #switching for heading

    except:
        print('Error in function: scorecard')
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
