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

    # read input CSV file
    csv1 = pd.read_csv('octant_input.csv')

    #store length of dataframe 
    len_csv1 = csv1.shape[0]

    # insert U Avg, V Avg & W Avg columns with blank values using .insert()
    csv1.insert(4, 'U Avg', "", True)
    csv1.insert(5, 'V Avg', "", True)
    csv1.insert(6, 'W Avg', "", True)

    # calculate mean values of U,V,W and assigned to index 0 row of U Avg, V Avg, W Avg using .at()
    csv1.at[0,'U Avg'] = csv1['U'].mean()
    csv1.at[0,'V Avg'] = csv1['V'].mean()
    csv1.at[0,'W Avg'] = csv1['W'].mean()

    # insert U', V' & W' columns 
    csv1.insert(7, 'U\'=U-U Avg', "", True)
    csv1.insert(8, 'V\'=V-V Avg', "", True)
    csv1.insert(9, 'W\'=W-W Avg', "", True)

    # calculate U', V', W' for each row using .subtract()
    csv1['U\'=U-U Avg'] = csv1['U'].subtract(csv1['U Avg'][0])
    csv1['V\'=V-V Avg'] = csv1['V'].subtract(csv1['V Avg'][0])
    csv1['W\'=W-W Avg'] = csv1['W'].subtract(csv1['W Avg'][0])
    
    # lambda function
    # .apply() to pass a function and apply it to all rows
    csv1['Octant'] = csv1.apply(lambda row: octant_assign(row["U'=U-U Avg"], row["V'=V-V Avg"], row["W'=W-W Avg"]), axis = 1)

    # insert column 11
    csv1.insert(11, '', "", True)
    csv1.at[1,''] = 'User Input'

    #insert column 12
    csv1.insert(12, 'Octant ID', "", True)
    csv1.at[0, 'Octant ID'] = 'Overall Count'
    csv1.at[1, 'Octant ID'] = 'Mod ' + str(mod) # display mod as string using str()
    csv1.at[2, 'Octant ID'] = '0 - ' + str(mod - 1) # range goes from 0 to mod - 1

    num = len_csv1/mod
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
        if(range_right >= len_csv1): # right value for cases where num != 0
            range_right = len_csv1 - 1
        csv1.at[i+2, 'Octant ID'] = str(range_left) + '-' + str(range_right)

        # create a list with octant values
    octant = [1, -1, 2, -2, 3, -3, 4, -4]
    
    # iterating over objects of list octant
    for octant_number in octant:
        csv1.insert(csv1.shape[1], octant_number, "", True) #new columns with names as objects of octant
        csv1.at[0, octant_number] = csv1['Octant'].value_counts()[octant_number] # use .value_counts() to count the number of occurances of each object of octant

    #for loop to get individual counts
    for i in range(1, range_total+2):
        # variable to store individual count of each range for a mod value
        count = csv1['Octant'][temp:temp+mod].value_counts() #range goes from temp to temp+mod - 1
        for j in octant: #iterate for objects in octant
            if(j in count):
                csv1.at[i+1 ,j] = count[j] # assign count of particular octant to designated cell
            else: # to accomodate the case of no occurance of an octant in a particular range
                csv1.at[i+1 ,j] = 0
        temp = temp + mod

    # write over the octant_output.csv file
    csv1.to_csv('octant_output.csv', index = False)

# check python version
from platform import python_version
ver = python_version()

if ver == "3.8.10":
    print("Correct Version Installed")
else:
    print("Please install 3.8.10. Instruction are present in the GitHub Repo/Webmail. Url: https://pastebin.com/nvibxmjw")

mod = 700 # hardcoded mod value
octact_identification(mod) # call the function