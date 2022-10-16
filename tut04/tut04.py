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

def subsequence_octant(data_xlsx, len_data_xlsx, octant):
    try:
       
        count = 1 #initial value of count is 1 since atleast 1 occurance of an octant will be present  i.e. ith element
        for i in range(len_data_xlsx): #iterating over entire data set
            if(data_xlsx.iloc[i,10] == data_xlsx.iloc[i+1,10]): #if two successive octant values are same
                count += 1 #increase count by 1 for (i+1)th element
            
            else:
                num = data_xlsx.iloc[i,10]
                index = octant.index(num) #index of corrensponding octant number in the list octant [1,-1,2,-2,3,-3,4,-4]
               

                if(count == data_xlsx.iloc[index,13] ): #if longest subsequent count remains same
                    data_xlsx.iloc[index,14] += 1 #increment count of the longest subsequent count i.e. column 14 of corresponding octant number
                  
                elif (count > data_xlsx.iloc[index,13]): #if longest subsequent count is greater than the previous one
                    data_xlsx.iloc[index,13] = count #new value of longest subsequent count in column 13 of corresponding octant number
                    data_xlsx.iloc[index,14] = 1 #reset count to 1 in coloum 14 of corresponding octant number
                   

                count = 1
    

    #except block in case an error occurs anywhere in the above function
    except:
        print('Error in function: subsequence_octant')
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

def octant_longest_subsequence_count():
    try:
        octact_identification()
        
        #store length of dataframe 
        len_data_xlsx = data_xlsx.shape[0]

        # insert column empty 11
        data_xlsx.insert(11, '', "", True)
        # insert column 12 with heading Octant Number
        data_xlsx.insert(12, 'Octant Number', "", True)
        # insert column 13 with heading Longest Subsequent Length
        data_xlsx.insert(13, 'Longest Subsequent Length', "", True)
        # insert column 14 with Count
        data_xlsx.insert(14, 'Count', "", True)
        data_xlsx.insert(15, '', "", True)
        data_xlsx.insert(16, 'Octant Number', "", True)
        data_xlsx.insert(17, 'Longest Subsequent Length', "", True)
        data_xlsx.insert(18, 'Count', "", True)
            
        #list containing octant numbers
        octant = [1, -1, 2, -2, 3, -3, 4, -4]

        #insert values 1,-1,2,-2,3,-3,4,-4 in column 12
        temp = 0 #temporary variable
        for i in octant:
            data_xlsx.iloc[temp,12] = i
            temp += 1

        #initialize the table with 0 values since str + int concatenation is not allowed in python
        for i in range(0,8):
            data_xlsx.iloc[i,13] = 0
            data_xlsx.iloc[i,14] = 0

        #function call    
        subsequence_octant(data_xlsx, len_data_xlsx-1, octant)

    #except block in case an error occurs anywhere in the above function
    except:
        print('Error in function: octant_longest_subsequence_count')
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
    data_xlsx = pd.read_excel('input_octant_longest_subsequence_with_range.xlsx')

except FileNotFoundError:
        print('Input file not found')
        exit()
except:
        print('Error in file: Could not open')
        exit()

#list containing octant numbers
octant = [1, -1, 2, -2, 3, -3, 4, -4]


# Write over corresponding output file
try:
    data_xlsx.to_excel('output_octant_longest_subsequence_with_range.xlsx', index = False)

except PermissionError:
    print('Permission Error: Cannot overwrite an opened file')
    exit()
except:
    print('Error in file: Could not overwrite')
    exit()

#This shall be the last lines of the code.
end_time = datetime.now()
print('Duration of Program Execution: {}'.format(end_time - start_time))