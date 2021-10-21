import re 

def format_title(title): 
    return "How to {0}".format(title.replace("_", " ").strip(".txt"))

def remove_hashes(paragraph_before): 
    cleaned = []
    for index, sent in enumerate(paragraph_before,0): 
        if index == 0: 
           sent = sent.replace("#", "")
    
        cleaned.append(sent)
    return cleaned 

def format_revised_before_insertion(original_sentence, original_sentence_in_raw, revised_before_insertion): 
    """ 

        Original sentence: the sentence as given in the tsv file 
        original_sentence_in_raw : the sentence in the article 
        revised_before_insertion {str}: the part before the insertion
    """

    starts_with_bullet_point = re.findall(r"^[0-9]+\.", original_sentence_in_raw[0])

   
    if starts_with_bullet_point: 
       original_sentence = " ".join(starts_with_bullet_point) + " " + original_sentence
       revised_before_insertion = " ".join(starts_with_bullet_point) + " " + revised_before_insertion
    elif original_sentence_in_raw[0].startswith("* "): 
        original_sentence = "* " + original_sentence
        revised_before_insertion = "* " + revised_before_insertion
    
    else: 
        original_sentence = original_sentence
        revised_before_insertion = revised_before_insertion
    

    print(revised_before_insertion)
    print("==================================")
    
    return revised_before_insertion