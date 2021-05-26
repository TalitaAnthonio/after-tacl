import spacy 

MODEL = spacy.load('en_core_web_sm')

def pos_tag(text_to_tag): 
    tagged = MODEL(text_to_tag)
    return [[token.text, token.tag_] for token in tagged]

