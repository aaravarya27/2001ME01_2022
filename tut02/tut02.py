import os
import pandas as pd
import math
os.system('cls')

# function to assign octant
try:
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

#except block in case an error occurs anywhere in the above function
except:
        print('Error in function: octant_assign')
        exit()

def table_transition(data_xlsx, range_left, range_right, index, octant):

    try:
        #empty heading
        table_name = ""
        #Assign Table name
        if (range_left < 0): #initialized to -1 later
            table_name += "Overall Transition Count"
        else:
            table_name += "Mod Transition Count"
            data_xlsx.iloc[index+1,12] = str(range_left) + '-' + str(range_right) 

        data_xlsx.iloc[index,12] = table_name
        data_xlsx.iloc[index+1,13] = "To"
        index += 2
        data_xlsx.iloc[index,12] = "Count"
        data_xlsx.iloc[index+1,11] = "From" 

        #assign octant value as row and col headings
        tempVar = 0 #temporary variable initialized to 0
        for i in octant: #iterating in list octant
            data_xlsx.iloc[index+1+tempVar,12] = i #row headings
            data_xlsx.iloc[index,13+tempVar] = i #column headings
            tempVar += 1

        index += 1

        #initialize zero in all cells of the table since str + int concatenation is not allowed while increasing count value
        for row1 in range(0,8):
            for col1 in range(0,8):
                data_xlsx.iloc[index+row1,13+col1] = 0

    #except block in case an error occurs anywhere in the above function
    except:
        print('Error in function: table_transition')
        exit()

def value_transition(data_xlsx, range_left, range_right, len_data_xlsx, index):

    try:
        if(range_right != len_data_xlsx):
            range_right += 1

        #assign octant value of two successive data points to var1 and var2 respectively
        for i in range(range_left,range_right):
            var1 = data_xlsx.iloc[i,10]
            var2 = data_xlsx.iloc[i+1,10]

            #if negative octant, we consider modulus of the value
            if (var1 < 0):
                row1 = 2*(abs(var1)-1)+1 #row number = 1,3,5,7 for -1,-2,-3,-4 respectively
            else:
                row1 = 2*(var1-1) #row number = 0,2,4,6 for 1,2,3,4 respectively

            #same in case of columns
            if(var2<0):
                col = 2*(abs(var2)-1)+14
            else:
                col = 2*(var2-1)+13      
            
            data_xlsx.iloc[row1+index+3,col] += 1 #increase count of octant by 1 for each transition and assign in dedicated cell using .iloc[]

    #except block in case an error occurs anywhere in the above code
    except:
        print('Error in function: value_transition')
        exit()

        
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

        # create a list with octant values
    octant = [1, -1, 2, -2, 3, -3, 4, -4]
    
    # iterating over objects of list octant
    for octant_number in octant:
        data_xlsx.insert(data_xlsx.shape[1], octant_number, "", True) #new columns with names as objects of octant
        data_xlsx.at[0, octant_number] = data_xlsx['Octant'].value_counts()[octant_number] # use .value_counts() to count the number of occurances of each object of octant

    #for loop to get individual counts
    for i in range(1, range_total+2):
        # variable to store individual count of each range for a mod value
        count = data_xlsx['Octant'][temp:temp+mod].value_counts() #range goes from temp to temp+mod - 1
        for j in octant: #iterate for objects in octant
            if(j in count):
                data_xlsx.at[i+1 ,j] = count[j] # assign count of particular octant to designated cell
            else: # to accomodate the case of no occurance of an octant in a particular range
                data_xlsx.at[i+1 ,j] = 0
        temp = temp + mod
    
    table_transition(data_xlsx,-1,-1,(range_total+5),octant)
    value_transition(data_xlsx, 0, len_data_xlsx-1, len_data_xlsx-1, (range_total+5))

    index = range_total + 18
    for i in range (range_total+1):
        #defining the extreme bounds of a range
        range_left = i*mod
        range_right = min(len_data_xlsx-1, ((i+1)*mod)-1)
    
        table_transition(data_xlsx,range_left,range_right,index,octant)
        value_transition(data_xlsx, range_left,range_right, len_data_xlsx-1, index)
        index += 13

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
