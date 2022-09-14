import os
import pandas as pd
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
        oct = oct*-1

    return oct # return integer value

def octact_identification(mod=5000):

    # read input CSV file
    csv1 = pd.read_csv('octant_input.csv')
    
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
    csv1["Octant"] = csv1.apply(lambda row: octant_assign(row["U'=U-U Avg"], row["V'=V-V Avg"], row["W'=W-W Avg"]), axis = 1)

    # display contents of CSV file upto index 4
    print(csv1.head())

from platform import python_version
ver = python_version()

if ver == "3.8.10":
    print("Correct Version Installed")
else:
    print("Please install 3.8.10. Instruction are present in the GitHub Repo/Webmail. Url: https://pastebin.com/nvibxmjw")

mod=5000
octact_identification(mod)