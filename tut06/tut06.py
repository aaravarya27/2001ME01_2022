import os
import pandas as pd
from datetime import datetime, timedelta
os.system('cls')

start_time = datetime.now()

def attendance_report():
    try:
        try:
            # read input files as csv
            input_attendance = "./input_attendance.csv"
            input_registered_students = "./input_registered_students.csv"

            att = pd.read_csv(input_attendance)
            reg = pd.read_csv(input_registered_students)

        except FileNotFoundError:
            print('Input file not found :', name)
            exit()
        except:
            print('Error in file: Could not open ', name)
            exit() 

        # converted all entries in attendance file to upper case
        att.dropna(axis="index", inplace = True)
        att.iloc[:, 1] = att.iloc[:, 1].apply(str.upper)

        # list with each object as roll no. name
        temp = []
        for i in range(len(reg)):
            temp.append(reg.iloc[i, 0] + " " + reg.iloc[i, 1])
        reg = temp

        # finding the start date 
        for i in att["Timestamp"]:
            valid = datetime.strptime(i, "%d-%m-%Y %H:%M")
            # break at 1st valid date
            if(valid.weekday() == 0 or valid.weekday() == 3): 
                start = valid.date()
                break
        # finding the end date
        for i in att["Timestamp"]:
            valid = datetime.strptime(i, "%d-%m-%Y %H:%M")
            if(valid.weekday() == 0 or valid.weekday() == 3):
                end = valid.date()     
        
        # adding all valid lecture dates to a list
        lectures = []
        x = start
        while(x <= end):
            if x.weekday() == 0 or x.weekday() == 3:
                rev = '-'.join(str(x).split('-')[::-1]) #reverse the format of the date to get DD-MM-YYY
                lectures.append(rev)
            x += timedelta(days = 1) #used to increment days

        # lectures.remove('15-08-2022') # 15th August if marked as holiday

        # create lists roll and name from registred students data
        consolidated = pd.DataFrame()
        roll = []
        name = []
        for i in reg:
            roll.append(i.split(" ", 1)[0])
            name.append(i.split(" ",1)[1])

        # create columns for roll and name in consolidated report
        consolidated["Roll"] = pd.Series(roll)
        consolidated["Name"] = pd.Series(name)
        consolidated.index = pd.Index(consolidated["Roll"].values) #change index to read through roll no

        #fill all rows with A initially for each lecture date
        for i in lectures:
            consolidated[i] = 'A' 

        #create other required columns 
        actuallectures = len(lectures) 
        consolidated["Actual Lecture Taken"] = actuallectures
        consolidated["Total Real"] = pd.NA
        consolidated["% Attendance"] = pd.NA

        #start and endtime of the class
        starttime = datetime(2022, 1, 1, 14, 0).time()
        endtime = datetime(2022, 1, 1, 15, 0).time()

        #creating individual reports by iterating over the list of registered students
        for i in reg:
            df = pd.DataFrame() #new dataframe
            # get roll and name
            roll = i.split(" ", 1)[0] 
            name = i.split(" ", 1)[1]
            
            #fill lecture dates, roll and name
            df["Date"] = pd.Series([pd.NA] + lectures)
            df["Roll"] = pd.Series([roll])
            df["Name"] = pd.Series([name])

            #create other required columns and initialize to zero
            df["Total Attendance Count"] = 0
            df["Real"] = 0
            df["Duplicate"] = 0
            df["Invalid"] = 0
            df["Absent"] = 0

            #one empty cell in each
            df.at[0, "Total Attendance Count"] = pd.NA
            df.at[0, "Real"] = pd.NA
            df.at[0, "Duplicate"] = pd.NA
            df.at[0, "Invalid"] = pd.NA
            df.at[0, "Absent"] = pd.NA
            
            #total lectures in total attendance column
            for j in range (len(lectures)):
                df.iloc[j+1, 3] = len(lectures)
            
            #separate dataframe for entry by each student
            student_att = att[att["Attendance"] == i]
            
            #filling the columns of real, duplicate and invalid attendance
            for k in student_att.iloc[:,0]:
                #take timestamp column and split to get date and time separately 
                date = k.split(" ")[0]
                time = k.split(" ")[1]

                #iteraating over valid dates
                if(date in lectures):
                    #invalid if lies outside the lecture hour
                    if(str(starttime)[:-3] > time or str(endtime)[:-3] < time):
                        df.iloc[lectures.index(date) + 1, 6] += 1
                    else:
                        #else real for 1st occurance and duplicate for successive occurances
                        if(df.iloc[lectures.index(date) + 1, 4] == 0):
                            df.iloc[lectures.index(date) + 1, 4] += 1
                        else:
                            df.iloc[lectures.index(date) + 1, 5] += 1

            #absent if real attendance is zero
            for date in lectures:        
                if(df.iloc[lectures.index(date) + 1, 4] == 0):
                    df.iloc[lectures.index(date) + 1, 7] += 1

            try:
                #writing each csv in excel file
                df.to_excel("./output/" + roll + ".xlsx", index = False)
            except PermissionError:
                print('Permission Error: Cannot overwrite an opened file')
                exit()
            except:
                print('Error in file: Could not overwrite')
                exit()

            #marking P if real attendance exists
            sum = 0
            for date in lectures:
                if(df.iloc[lectures.index(date) + 1, 4] == 1):
                    consolidated.at[roll, date] = "P"
                    sum += 1

            consolidated.at[roll, "Total Real"] = sum #total real is sum of real
            consolidated.at[roll, "% Attendance"] = round(sum*100/len(lectures), 2)

        try:
            #writing consolidated report to excel        
            consolidated.to_excel("./output/attendance_report_consolidated.xlsx", index = False)
        except PermissionError:
            print('Permission Error: Cannot overwrite an opened file')
            exit()
        except:
            print('Error in file: Could not overwrite')
            exit()

    except:
        print('Error in function : attendance_report')

#check python version
from platform import python_version
ver = python_version()

if ver == "3.8.10":
    print("Correct Version Installed")
else:
    print("Please install 3.8.10. Instruction are present in the GitHub Repo/Webmail. Url: https://pastebin.com/nvibxmjw")

attendance_report() #function call

#This shall be the last lines of the code.
end_time = datetime.now()
print('Duration of Program Execution: {}'.format(end_time - start_time))