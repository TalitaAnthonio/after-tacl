import pandas as pd 
import pdb 

path_to_batch1 = "implicit_references_batch1.csv"
path_to_batch2 = "implicit_references_batch2.csv"
path_to_batch3 = "implicit_references_batch3.csv"
path_to_batch4 = "batch4.csv"
path_to_batch5 = "batch5.csv"
path_to_batch6 = "batch6.csv"

batch1 = pd.read_csv(path_to_batch1)
batch2 = pd.read_csv(path_to_batch2)
batch3 = pd.read_csv(path_to_batch3)
batch4 = pd.read_csv(path_to_batch4)
batch5 = pd.read_csv(path_to_batch5)
batch6 = pd.read_csv(path_to_batch6)

keys_to_check = [row["Id"] for index, row in batch5.iterrows()]



def get_sentences_from_keys(df): 
    """ 
        Param: dataframe 

    """
    
    d = {}
    for index, row in df.iterrows(): 
        if row["Id"] in keys_to_check: 

            # some ids will occur twice in batch 6 
            if row["Id"] in d.keys(): 
               d[row["Id"]].append(row["Sent"]) 
            else: 
               d[row["Id"]] = []
               d[row["Id"]].append(row["Sent"]) 

    return d 

def main(): 
    
    sents_in_batch1 = get_sentences_from_keys(batch1)
    sents_in_batch2 = get_sentences_from_keys(batch2)
    sents_in_batch3 = get_sentences_from_keys(batch3)
    sents_in_batch4 = get_sentences_from_keys(batch4)
    sents_in_batch5 = get_sentences_from_keys(batch5)
    sents_in_batch6 = get_sentences_from_keys(batch6)


    d = {}
    counter = 0 
    for key in keys_to_check: 
        if key in sents_in_batch6.keys(): 
            all_sents = sents_in_batch1[key] + sents_in_batch2[key] + sents_in_batch3[key] + sents_in_batch4[key] + sents_in_batch5[key] + sents_in_batch6[key]
        else: 
            all_sents = sents_in_batch1[key] + sents_in_batch2[key] + sents_in_batch3[key] + sents_in_batch4[key] + sents_in_batch5[key]

        #print(all_sents, len(all_sents), len(set(all_sents))) 
        assert len(set(all_sents)) == 5 
    
main()