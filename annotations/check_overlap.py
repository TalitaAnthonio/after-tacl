import pandas as pd 
import pdb 

# read the csvs 
path_to_df1 = "./implicit_references_batch1.csv"
path_to_df2 = "./implicit_references_batch2.csv"
path_to_df3 = "./implicit_references_batch3.csv"

df1 = pd.read_csv(path_to_df1)
df2 = pd.read_csv(path_to_df2)
df3 = pd.read_csv(path_to_df3)


d1 = {}
for index, row in df1.iterrows(): 
    d1[row["Id"]] = row["Sent"]
d2 = {}
for index, row in df2.iterrows(): 
    d2[row["Id"]] = row["Sent"]
d3 = {}
for index, row in df3.iterrows(): 
    d3[row["Id"]] = row["Sent"]


# check those for which we have already three fillers 
completed = []
batch_3_and_1_are_the_same = []
batch_1_and_2_are_the_same = []
batch_3_and_2_are_the_same = []
all_are_the_same = []

requires_one = {}
requires_two = {}


for key, _ in d1.items(): 
    # all of them are different 

    fillers = set([d1[key], d2[key], d3[key]])

    if d1[key] != d2[key] and d1[key] != d3[key] and d2[key] != d3[key]: 
       assert len(fillers) == 3
       completed.append(key)
    
    # all are the same 
    elif d3[key] == d2[key] == d1[key]: 
        assert len(fillers) == 1
        all_are_the_same.append(key)

    # batch3 and 1 are the same 
    elif d1[key] != d2[key] and d1[key] == d3[key]: 
        assert len(fillers) == 2
        #db.set_trace()
        batch_3_and_1_are_the_same.append(key)



    # batch2 and 1 are the same 
    elif d1[key] != d2[key] and d2[key] == d3[key]: 
        assert len(fillers) == 2
        batch_3_and_2_are_the_same.append(key)
    
    elif d3[key] != d2[key] and d1[key] == d2[key]: 
        print(d1[key], d2[key], d3[key])
        assert len(fillers) == 2
        batch_1_and_2_are_the_same.append(key)
    
    else: 
        print(d1[key], d2[key], d3[key]) 
    


""""
print("completed", len(completed))
print("1 diff", len(batch_3_and_1_are_the_same))
print("1 diff", len(batch_1_and_2_are_the_same))
print("1 diff", len(batch_3_and_2_are_the_same))
print("all same", len(all_are_the_same)) 

completed1 = df1.loc[df1['Id'].isin(completed)]
completed2 = df2.loc[df2['Id'].isin(completed)]
completed3 = df3.loc[df3['Id'].isin(completed)]

#print(len(completed))

completed1.to_csv("batch1_complete.tsv", index=False, sep='\t')
completed2.to_csv("batch2_complete.tsv", index=False, sep='\t')
completed3.to_csv("batch3_complete.tsv", index=False, sep='\t')

""" 