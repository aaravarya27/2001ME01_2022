import os
import pandas as pd
import math
os.system('cls')

# function to assign octant
def octant_assign(x,y,z):
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

def octact_identification(mod=5000):

    # read input excel file
    data_xlsx = pd.read_excel('input_octant_transition_identify.xlsx')

    #store length of dataframe 
    len_data_xlsx = data_xlsx.shape[0]

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

    # insert column 11
    data_xlsx.insert(11, '', "", True)
    data_xlsx.at[1,''] = 'User Input'

    #insert column 12
    data_xlsx.insert(12, 'Octant ID', "", True)
    data_xlsx.at[0, 'Octant ID'] = 'Overall Count'
    data_xlsx.at[1, 'Octant ID'] = 'Mod ' + str(mod) # display mod as string using str()
    data_xlsx.at[2, 'Octant ID'] = '0 - ' + str(mod - 1) # range goes from 0 to mod - 1

    num = len_data_xlsx/mod
    range_total = math.floor(num) # total number of ranges
                                  # .floor() works as greatest integer function
    # special case
    if(mod == 29745 or mod == 1):
        range_total -= 1

    temp = 0 # create and initialize a temporary variable

    # for loop to get ranges
    for i in range (1, range_total+1):
        range_left = i*mod # left value 
        range_right = (i+1)*mod - 1 # right value
        if(range_right >= len_data_xlsx): # right value for cases where num != 0
            range_right = len_data_xlsx - 1
        data_xlsx.at[i+2, 'Octant ID'] = str(range_left) + '-' + str(range_right)

    
    # write over the octant_output.excel file
    data_xlsx.to_excel('testfile.xlsx', index = False)

# check python version
from platform import python_version
ver = python_version()

if ver == "3.8.10":
    print("Correct Version Installed")
else:
    print("Please install 3.8.10. Instruction are present in the GitHub Repo/Webmail. Url: https://pastebin.com/nvibxmjw")

mod = 5000 # hardcoded mod value
octact_identification(mod) # call the function
