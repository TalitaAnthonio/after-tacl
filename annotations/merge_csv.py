# Use script to merge csvs from Michael, me and Anna. 

import pandas as pd 
import pdb 



def read_dfs(csv_michael, csv_anna, csv_talita): 
    """ 
        Returns: 
        - concatenation of the dataframe (by columns)
    """
    

    df_michael = pd.read_csv(csv_michael)
    df_anna = pd.read_csv(csv_anna)
    df_talita = pd.read_csv(csv_talita)
    merged_df = pd.concat([df_michael, df_anna, df_talita])
    return merged_df 



def main(): 
    # read files from michael 
    batch3_michael_path = "./files/batch3_michael.csv"
    batch4_michael_path = "./files/batch4_michael.csv"
    batch5_michael_path = "./files/batch5_michael.csv"

    # read files from anna 
    batch3_anna_path = "./files/batch3_anna.csv"
    batch4_anna_path = "./files/batch4_anna.csv"
    batch5_anna_path = "./files/batch5_anna.csv"

    # read my files 
    batch3_talita_path = "./files/batch3_talita.csv"
    batch4_talita_path = "./files/batch4_talita.csv"
    batch5_talita_path = "./files/batch5_talita.csv"


    # merge the files 
    batch3 = read_dfs(batch3_michael_path, batch3_anna_path, batch3_talita_path)
    batch4 = read_dfs(batch4_michael_path, batch4_anna_path, batch4_talita_path)
    batch5 = read_dfs(batch5_michael_path, batch5_anna_path, batch5_talita_path)

    
    # save to csv 
    batch3.to_csv("trial_batch3.csv", index=False)
    batch4.to_csv("trial_batch4.csv", index=False)
    batch5.to_csv("trial_batch5.csv", index=False)
    



main()