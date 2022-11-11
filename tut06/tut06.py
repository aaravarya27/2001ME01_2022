import os
import pandas as pd
from datetime import datetime
os.system('cls')

start_time = datetime.now()

def attendance_report():

    try:
        regStd = pd.read_csv("input_registered_students.csv")
    except:
        print('Error in reading csv file : input_registered_students')
        exit()

    try:
        att = pd.read_csv("input_attendance.csv")
    except:
        print('Error in reading csv file : input_attendance')
        exit()

    

# check python version
from platform import python_version
ver = python_version()

if ver == "3.8.10":
    print("Correct Version Installed")
else:
    print("Please install 3.8.10. Instruction are present in the GitHub Repo/Webmail. Url: https://pastebin.com/nvibxmjw")

attendance_report()

#This shall be the last lines of the code.
end_time = datetime.now()
print('Duration of Program Execution: {}'.format(end_time - start_time))
