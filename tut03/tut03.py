import os
import pandas as pd
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


def octact_identification():
    try:
        # insert U Avg, V Avg & W Avg columns with blank values using .insert()
        data_xlsx.insert(4, 'U Avg', "", True)
        data_xlsx.insert(5, 'V Avg', "", True)
        data_xlsx.insert(6, 'W Avg', "", True)

        # calculate mean values of U,V,W and assigned to index 0 row of U Avg, V Avg, W Avg using .at()
        data_xlsx.at[0,'U Avg'] = data_xlsx['U'].mean()
        data_xlsx.at[0,'V Avg'] = data_xlsx['V'].mean()
        data_xlsx.at[0,'W Avg'] = data_xlsx['W'].mean()

        # insert U', V' & W' columns 
        data_xlsx.insert(7, 'U\'=U-U Avg', "", True)
        data_xlsx.insert(8, 'V\'=V-V Avg', "", True)
        data_xlsx.insert(9, 'W\'=W-W Avg', "", True)

        # calculate U', V', W' for each row using .subtract()
        data_xlsx['U\'=U-U Avg'] = data_xlsx['U'].subtract(data_xlsx['U Avg'][0])
        data_xlsx['V\'=V-V Avg'] = data_xlsx['V'].subtract(data_xlsx['V Avg'][0])
        data_xlsx['W\'=W-W Avg'] = data_xlsx['W'].subtract(data_xlsx['W Avg'][0])
            
        # lambda function
        # .apply() to pass a function and apply it to all rows
        data_xlsx['Octant'] = data_xlsx.apply(lambda row: octant_assign(row["U'=U-U Avg"], row["V'=V-V Avg"], row["W'=W-W Avg"]), axis = 1)

    #except block in case an error occurs anywhere in the above function
    except:
        print('Error in function: octact_identification')
        exit()


# check python version
from platform import python_version
ver = python_version()

if ver == "3.8.10":
    print("Correct Version Installed")
else:
    print("Please install 3.8.10. Instruction are present in the GitHub Repo/Webmail. Url: https://pastebin.com/nvibxmjw")

# read input excel file
try:
    data_xlsx = pd.read_excel('input_octant_longest_subsequence.xlsx')

except FileNotFoundError:
        print('Input file not found')
        exit()
except:
        print('Error in file: Could not open')
        exit()




#This shall be the last lines of the code.
end_time = datetime.now()
print('Duration of Program Execution: {}'.format(end_time - start_time))