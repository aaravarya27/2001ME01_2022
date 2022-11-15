import os
import pandas as pd
import math
import openpyxl
from openpyxl.styles.borders import Border, Side
from openpyxl.styles import PatternFill
from datetime import datetime
os.system('cls')

start_time = datetime.now()

# function to assign octant
def octant_assign(x,y,z):
    try:
        oct = 0 # initialization
        if(x>=0 and y>=0):
            oct = 1
        elif(x<0 and y>=0):
            oct = 2
        elif(x<0 and y<0):
            oct = 3
        elif(x>=0 and y<0):
            oct = 4

        if(z<0): # reduce number of if conditions
            oct *= -1

        return oct # return integer value

    #except block in case an error occurs anywhere in the above function
    except:
        print('Error in function: octant_assign')
        exit()

def octant_count(df, range_total, octant, len_df):
    try:
        r=0
        while(r < range_total):
            df.at[r+1,'Octant ID']= str(mod*(r) ) + "-" + str( mod*(r+1)-1) 
            r += 1

        df.at[r+1, 'Octant ID']= str(mod*(r)) + "-" + str(len_df)

        for i in octant:
            df[str(i)] = ''
            df.at[0, str(i)] = df["Octant"].value_counts()[i]
            r = 0
            p = 0
            while(r < range_total):
                df.at[r+1, str(i)] = df["Octant"][p:p + mod].value_counts()[i]
                p += mod
                r += 1

            df.at[r+1, str(i)] = df["Octant"][p:len_df].value_counts()[i]

    #except block in case an error occurs anywhere in the above function
    except:
        print('Error in function: octant_count')
        exit()
    

def octact_identification(mod=5000):
    try:
        # read input excel file
        df = pd.read_excel('1.0.xlsx')
    except FileNotFoundError:
        print('Input file not found')
        exit()
    except:
        print('Error in file: Could not open')
        exit()

    try:
        #store length of dataframe 
        len_df = df.shape[0]

        # insert U Avg, V Avg & W Avg columns with blank values using .insert()
        df.insert(4, 'U Avg', "", True)
        df.insert(5, 'V Avg', "", True)
        df.insert(6, 'W Avg', "", True)

        # calculate mean values of U,V,W and assigned to index 0 row of U Avg, V Avg, W Avg using .at()
        df.at[0,'U Avg'] = df['U'].mean()
        df.at[0,'V Avg'] = df['V'].mean()
        df.at[0,'W Avg'] = df['W'].mean()

        # insert U', V' & W' columns 
        df.insert(7, 'U\'=U-U Avg', "", True)
        df.insert(8, 'V\'=V-V Avg', "", True)
        df.insert(9, 'W\'=W-W Avg', "", True)

        # calculate U', V', W' for each row using .subtract()
        df['U\'=U-U Avg'] = df['U'].subtract(df['U Avg'][0])
        df['V\'=V-V Avg'] = df['V'].subtract(df['V Avg'][0])
        df['W\'=W-W Avg'] = df['W'].subtract(df['W Avg'][0])
        
        # lambda function
        # .apply() to pass a function and apply it to all rows
        df['Octant'] = df.apply(lambda row: octant_assign(row["U'=U-U Avg"], row["V'=V-V Avg"], row["W'=W-W Avg"]), axis = 1)

        # insert column empty 11
        df.insert(11, '', "", True)

        #insert column 12
        df.insert(12, ' ', "", True)
        df.at[0, ' '] = 'Mod ' + str(mod) # display mod as string using str()
        
		# insert column 13
        df.insert(13, 'Octant ID', "", True)
        df.at[0, 'Octant ID'] = "Overall Count"

        num = len_df/mod
        range_total = math.floor(num) # total number of ranges
                                    # .floor() works as greatest integer function

        octant = [1, -1, 2, -2, 3, -3, 4, -4]

        octant_count(df, range_total, octant, len_df)
        
        # i = 0
        # for j in octant:
        #     df.insert(22+i, 'Rank Octant '+ str(j), '', True)
        #     i += 1

    except:
        print('Error in function: octant_identification')
        exit()

    try:
        # Write over corresponding output file
        df.to_excel('test.xlsx', index = False)
    except PermissionError:
        print('Permission Error: Cannot overwrite an opened file')
        exit()
    except:
        print('Error in file: Could not overwrite')
        exit()


# check python version
from platform import python_version
ver = python_version()

if ver == "3.8.10":
    print("Correct Version Installed")
else:
    print("Please install 3.8.10. Instruction are present in the GitHub Repo/Webmail. Url: https://pastebin.com/nvibxmjw")

mod = 5000 # hardcoded mod value
octact_identification(mod) # call the function

#This shall be the last lines of the code.
end_time = datetime.now()
print('Duration of Program Execution: {}'.format(end_time - start_time))
