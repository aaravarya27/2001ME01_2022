import os
import pandas as pd
os.system('cls')

def octact_identification(mod=5000):
    # read input CSV file
    csv1 = pd.read_csv('octant_input.csv')
    
    # insert U Avg, V Avg & W Avg columns with blank values
    csv1.insert(4, 'U Avg', "", True)
    csv1.insert(5, 'V Avg', "", True)
    csv1.insert(6, 'W Avg', "", True)

    # calculate mean values of U,V,W and assigned to index 0 row of U Avg, V Avg, W Avg
    csv1['U Avg'][0] = csv1['U'].mean()
    csv1['V Avg'][0] = csv1['V'].mean()
    csv1['W Avg'][0] = csv1['W'].mean()

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