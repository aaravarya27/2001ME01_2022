import os
import pandas as pd
from datetime import datetime, timedelta
os.system('cls')

start_time = datetime.now()

def attendance_report():

    # read input files as csv
    input_attendance = "./input_attendance.csv"
    input_registered_students = "./input_registered_students.csv"

    att = pd.read_csv(input_attendance)
    reg = pd.read_csv(input_registered_students)

    # converted all entries in attendance file to upper case
    att.dropna(axis="index", inplace = True)
    att.iloc[:, 1] = att.iloc[:, 1].apply(str.upper)

    # list with each object as roll no. name
    
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