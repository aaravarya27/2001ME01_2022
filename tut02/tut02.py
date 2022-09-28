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
