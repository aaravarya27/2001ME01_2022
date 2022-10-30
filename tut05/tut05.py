import os
import pandas as pd
import math
from datetime import datetime
os.system('cls')

start_time = datetime.now()

# function to assign octant
def octant_assign(x,k,z):
    try:
        octant = 0 # initialization
        if(x>=0 and k>=0):
            octant = 1
        elif(x<0 and k>=0):
            octant = 2
        elif(x<0 and k<0):
            octant = 3
        elif(x>=0 and k<0):
            octant = 4

        if(z<0): # reduce number of if conditions
            octant *= -1

        return octant # return integer value

    #except block in case an error occurs anywhere in the above function
    except:
        print('Error in function: octant_assign')
        exit()

# function to count each rank and rank1 octant ID and Name
def octant_frequency(data_xlsx, range_total, octant_name_id_mapping, octant):
    try:
        c = -1 #counter variable
        #while loop only for overall count row
        while(c < 0):
            oct = {} # empty dictionary to store octant with corresponding count value
            t = 0
            for i in octant:
                oct[i] = data_xlsx.iloc[0, 13+t]
                t += 1 # increment for next octant number

            oct = dict(sorted(oct.items(), key=lambda item: item[1], reverse=True)) # decreasingly sorted using lambda function

            t = 1
            for i in oct:
                data_xlsx.at[0,'Rank ' + str(i)] = t #since oct is sorted, rank will be assigned in corresponding order
                if(t == 1): # if rank is 1 then fill column 29 and 30
                    data_xlsx.at[0,'Rank1 Octant ID'] = i 
                    data_xlsx.at[0,'Rank1 Octant Name'] = octant_name_id_mapping[str(i)] #Name for corresponding key
                t += 1
            c +=1 #new counter value => 0 hence shifts to else condition

        #else condition for mod count rows
        else:
            for i in range(range_total+1): # number of rows for mod count
                octMod = {} # empty dictionary to store octant with corresponding count value
                t = 0
                for j in octant: 
                    octMod[j] = data_xlsx.iloc[i+2, 13+t] #store key value pair for each iteration of mod count
                    t += 1 # increment for next octant number

                octMod = dict(sorted(octMod.items(), key=lambda item: item[1], reverse=True)) # decreasingly sorted using lambda function

                t = 1
                for k in octMod: #since octMod is sorted, rank will be assigned in corresponding order
                    data_xlsx.at[i+2,'Rank ' + str(k)] = t
                    if(t == 1): # if rank is 1 then fill column 29 and 30
                        data_xlsx.at[i+2,'Rank1 Octant ID'] = k
                        data_xlsx.at[i+2,'Rank1 Octant Name'] = octant_name_id_mapping[str(k)] #Name for corresponding key 
                    t += 1

    #except block in case an error occurs anywhere in the above function
    except:
            print('Error while executing octant_frequency function')
            exit()

def octant_identification(mod=5000):
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

        # insert column 11
        data_xlsx.insert(11, '', "", True)
        data_xlsx.at[1,''] = 'User Input'

        #insert column 12
        data_xlsx.insert(12, 'Octant ID', "", True)
        data_xlsx.at[0, 'Octant ID'] = 'Overall Count'
        data_xlsx.at[1, 'Octant ID'] = 'Mod ' + str(mod) # display mod as string using str()
        data_xlsx.at[2, 'Octant ID'] = '0 - ' + str(mod - 1) # range goes from 0 to mod - 1

        temp = 0 # create and initialize a temporary variable

        # for loop to get ranges
        for i in range (1, range_total+1):
            range_left = i*mod # left value 
            range_right = (i+1)*mod - 1 # right value
            if(range_right >= len_data_xlsx): # right value for cases where num != 0
                range_right = len_data_xlsx - 1
            data_xlsx.at[i+2, 'Octant ID'] = str(range_left) + '-' + str(range_right)
        
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
    #except block in case an error occurs anywhere in the above function
    except:
        print('Error in function: octant_identification')
        exit()

def octant_range_names(range_total,octant):
    try:
        octant_identification(mod) # function call

        #insert columns 21 to 28 with name Rank i where i is elements of [1,-1,2,-2,3,-3,4,-4]
        col = 21
        for i in octant:
            data_xlsx.insert(col, 'Rank ' + str(i), "", True)
            col += 1

        # insert column 29 and 30
        data_xlsx.insert(29, 'Rank1 Octant ID', "", True) 
        data_xlsx.insert(30, 'Rank1 Octant Name', "", True) 

        # given dictionary with names corresponding to each octant
        octant_name_id_mapping = {'1' : "Internal outward interaction",'-1': "External outward interaction",'2' : "External Ejection",'-2': "Internal Ejection",'3' : "External inward interaction",'-3': "Internal inward interaction",'4' : "Internal sweep",'-4': "External sweep"}

        # Function call for assigning ranks & rank1 Octant ID and Octant Name
        octant_frequency(data_xlsx, range_total, octant_name_id_mapping, octant)
        
        # Headings in corresponding cells for count of Rank 1 for mod Values
        index = range_total + 6 # To ensure 3 row spacing after mod table
        data_xlsx.iloc[index, 13] = 'Octant ID'
        data_xlsx.iloc[index, 14] = 'Octant Name'
        data_xlsx.iloc[index, 15] = 'Count of Rank 1 mod values'
        
        # Create a list and store rank1 count for each octant ID
        countRank1 = [0,0,0,0,0,0,0,0] #list of size 8 initialized to 0
        for i in range (0, range_total+1): # iterating over number of ranges for corresponding mod value
            #evaluates index of Rank1 octant ID from octant
            #and increases count of that index in the list countRank1
            countRank1[octant.index(data_xlsx.at[i+2,'Rank1 Octant ID'])] += 1 
            
        

    #except block in case an error occurs anywhere in the above function
    except:
        print('Error in function: octant_range_names')
        exit()

# check python version
from platform import python_version
ver = python_version()

if ver == "3.8.10":
    print("Correct Version Installed")
else:
    print("Please install 3.8.10. Instruction are present in the GitHub Repo/Webmail. Url: https://pastebin.com/nvibxmjw")

try:
    # read input excel file
    data_xlsx = pd.read_excel('octant_input.xlsx')
except FileNotFoundError:
    print('Input file not found')
    exit()
except:
    print('Error in file: Could not open')
    exit()

mod = 5000 # hardcoded mod value
#store length of dataframe 
len_data_xlsx = data_xlsx.shape[0]

num = len_data_xlsx/mod
range_total = math.floor(num) # total number of ranges
                              # .floor() works as greatest integer function
# special case
if(mod == 29745 or mod == 1):
    range_total -= 1

# create a list with octant values
octant = [1, -1, 2, -2, 3, -3, 4, -4]

octant_range_names(range_total, octant)

try:
    # Write over corresponding output file
    data_xlsx.to_excel('test.xlsx', index = False)
except PermissionError:
    print('Permission Error: Cannot overwrite an opened file')
    exit()
except:
    print('Error in file: Could not overwrite')
    exit()

#This shall be the last lines of the code.
end_time = datetime.now()
print('Duration of Program Execution: {}'.format(end_time - start_time))
