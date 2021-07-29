
import json 
import pdb 

# file with predictions 
PATH_TO_DEV_FILE_PRED = "../coreference/filtered_dev_preds_final.json"
PATH_TO_TRAIN_FILE_PRED = "../coreference/filtered_train_preds_final.json"
FILE_WITH_LINE_NRS = "/Users/talita/Documents/PhD/corpora/rulebook_diffs/2019-09-23/boardgame_scripts/wikihow/data/wikihow-with-line-numbers.json"

with open(FILE_WITH_LINE_NRS, "r") as json_in: 
     bigger_file = json.load(json_in)


with open("../../tacl/data/references_for_lm.json", "r") as json_in: 
     all_data = json.load(json_in)


with open(PATH_TO_DEV_FILE_PRED, "r") as json_in: 
     predictions = json.load(json_in)

with open(PATH_TO_TRAIN_FILE_PRED, "r") as json_in: 
    predictions_data =  json.load(json_in)

predictions_data.update(predictions)
# dict_keys(['predictions', 'key', 'revised_sentence', 
# 'insertion', 'coref', 'sents', 'filename', 'base_tokenized', 
# 'id', 'revised_tokenized', 'insertion_phrases', 
# 'Base_Sentence', 'Base_Nr', 'Revised_Nr', 'parsed_revised_sentence',
# 'Base_Article', 'Base_Article_Clean', 'par', 'index_of_insertion', 
# 'index_of_reference', 'bigram', 'stats', 'reference', 'reference-type', 
# 'position-of-ref-in-insertion', 'Split', 'insertion-type', 'language_model_text', 'revised_afer_insertion', 'revised_untill_insertion', 'filtered_fillers'])


# of 
# dict_keys(['predictions', 'key', 'revised_sentence', 'insertion', 'base_tokenized', 'insertion_type', 'index_of_insertion', 'index_of_reference', 'context_plus_revised', 'language_model_text', 'revised_untill_insertion', 'revised_after_insertion', 'reference', 'reference-type', 'position-of-ref-in-insertion', 'filename', 'par', 'Split', 'insertion-type', 'filtered_fillers'])

simplified_dict = {}
counter = 0 
for key, _ in predictions_data.items(): 
    counter +=1 
    print(counter)

    if "GPT+Finetuning+P-perplexityPred" not in predictions_data[key].keys(): 
        predictions = [prediction.lstrip() for prediction in predictions_data[key]["predictions"]["generated_texts"]] 
    else: 
        predictions = [prediction.lstrip() for prediction in predictions_data[key]["GPT+Finetuning+P-perplexityPred"]]
    
    if "revised_sentence" not in predictions_data[key].keys(): 
        revised_sentence = predictions_data[key]["RevisedSentence"]  
    else:
        revised_sentence = predictions_data[key]["revised_sentence"] 
    

    if "reference" not in predictions_data[key].keys(): 
        reference = predictions_data[key]["CorrectReference"]
    else: 
        reference = predictions_data[key]["reference"]
    

    if "revised_after_insertion" in predictions_data[key].keys(): 
        revised_after_insertion = predictions_data[key]["revised_after_insertion"]
    else: 
        revised_after_insertion = predictions_data[key]["revised_afer_insertion"]

    if "revised_untill_insertion" not in predictions_data[key].keys(): 
        pdb.set_trace()

    simplified_dict[key] = {"predictions": [prediction.lstrip() for prediction in predictions]}
    other_info = {"RevisedSentence": revised_sentence, 
    "Reference": reference, 
    "Par": all_data[key]["par"], 
    "Split": all_data[key]["Split"], 
    "Filename": bigger_file[key]["Filename"], 
    "BaseNr": bigger_file[key]["Source_Line_Nr"][0], 
    "RevisedNr": bigger_file[key]["Target_Line_Nr"][-1], 
    "RevisedBeforeInsertion": predictions_data[key]["revised_untill_insertion"], 
    "RevisedAfterInsertion": revised_after_insertion, 
    "LanguageModelText": predictions_data[key]["language_model_text"]}


    simplified_dict.update(other_info)
    

    with open("all_references.json", "w") as json_out: 
         json.dump(simplified_dict, json_out)